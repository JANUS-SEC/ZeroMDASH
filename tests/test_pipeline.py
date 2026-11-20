"""Scheduling contracts for whole-task pipelines, exercised without agents."""

from __future__ import annotations

import json
import threading
import unittest
from contextvars import ContextVar
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import click
from click.testing import CliRunner
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph

from zeromdash import graph as graph_mod
from zeromdash.cli import _parse_agent_config_file, _pop_task_concurrency_from_agent_config, main
from zeromdash.pipeline import TASK_CONCURRENCY_KEYS, TaskPipeline, task_pipeline_node, task_slots
from zeromdash.poc_gen.service import PocGenService
from zeromdash.state import SubtaskOutputState, SubtaskState, ZeroMDASHState
from zeromdash.workspace import Workspace


class PipelineTest(unittest.TestCase):
    def test_refills_a_finished_slot_while_another_task_is_still_running(self):
        slow_started = threading.Event()
        replacement_started = threading.Event()
        lock = threading.Lock()
        active = 0
        peak = 0
        context = ContextVar("pipeline_test", default="missing")
        context.set("run-context")

        def execute(index):
            nonlocal active, peak
            self.assertEqual(context.get(), "run-context")
            with lock:
                active += 1
                peak = max(peak, active)
            try:
                if index == 0:
                    slow_started.set()
                    self.assertTrue(replacement_started.wait(5))
                elif index == 1:
                    self.assertTrue(slow_started.wait(5))
                else:
                    replacement_started.set()
                return index
            finally:
                with lock:
                    active -= 1

        with TemporaryDirectory() as tmp:
            pipeline = TaskPipeline(2, kind="subtask", log_dir=Path(tmp))
            self.assertEqual(pipeline.run(range(3), execute), [0, 1, 2])
            events = [json.loads(line) for line in pipeline.log_path.read_text().splitlines()]
        self.assertEqual(peak, 2)
        self.assertEqual(sum(item["event"] == "queued" for item in events), 3)
        self.assertEqual(sum(item["event"] == "finished" for item in events), 3)
        self.assertLess(
            next(i for i, e in enumerate(events) if e["task_id"] == "2" and e["event"] == "started"),
            next(i for i, e in enumerate(events) if e["task_id"] == "0" and e["event"] == "finished"),
        )

    def test_failure_stops_admission_and_propagates(self):
        seen = []

        def fail(task):
            seen.append(task)
            raise RuntimeError("broken task")

        with self.assertRaisesRegex(RuntimeError, "broken task"):
            TaskPipeline(1, kind="subtask").run(range(4), fail)
        self.assertEqual(seen, [0])

    def test_empty_pipeline_and_invalid_slots(self):
        self.assertEqual(TaskPipeline(2, kind="subtask").run([], lambda task: task), [])
        for invalid in (True, 0, -1, "2", None):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                TaskPipeline(invalid, kind="subtask")

    def test_each_pipeline_has_independent_slots_and_inherits_when_unset(self):
        state = {"task_concurrency": dict(zip(TASK_CONCURRENCY_KEYS, (2, 3, 4)))}
        for kind, expected in (("subtask", 2), ("chain_subtask", 3), ("poc_task", 4)):
            self.assertEqual(task_slots(state, kind, {"max_concurrency": 1}), expected)
        self.assertEqual(task_slots({}, "subtask", {"max_concurrency": 6}), 6)
        self.assertEqual(task_slots({}, "poc_task"), 8)

    def test_explicit_task_slots_override_parent_graph_concurrency(self):
        barrier = threading.Barrier(3)

        def child(state):
            barrier.wait(timeout=5)
            return {"observations": [state["subtask"]["id"]], "errors": []}

        # Use the real graph runtime, not a mocked executor.
        child_builder = StateGraph(SubtaskState, output_schema=SubtaskOutputState)
        child_builder.add_node("work", child)
        child_builder.add_edge(START, "work")
        child_builder.add_edge("work", END)
        parent = StateGraph(ZeroMDASHState)
        parent.add_node("pipeline", task_pipeline_node(
            child_builder.compile(),
            lambda state: [Send("subtask", {"subtask": {"id": str(i)}}) for i in range(3)],
            kind="subtask", next_node="finish",
        ), destinations=("finish",))
        parent.add_node("finish", lambda state: {})
        parent.add_edge(START, "pipeline")
        parent.add_edge("finish", END)
        result = parent.compile().invoke(
            {"task_concurrency": {"subtask_concurrency": 3}, "observations": ["prior"]},
            config={"max_concurrency": 1},
        )
        self.assertEqual(result["observations"], ["prior", "0", "1", "2"])
        self.assertNotIn("subtask", result)

    def test_empty_dispatch_retains_its_fallback(self):
        node = task_pipeline_node(lambda state: self.fail("no task should run"),
                                  lambda state: "summary", kind="subtask", next_node="pool")
        self.assertEqual(node({}, {}).goto, "summary")

    def test_real_subtask_and_chain_loops_hold_the_slot_across_revise(self):
        for kind in ("subtask", "chain_subtask"):
            with self.subTest(kind=kind):
                events = []
                is_chain = kind == "chain_subtask"
                task_key = "chain_candidate" if is_chain else "subtask"
                id_key = "chain_id" if is_chain else "id"
                review_key = "chain_review" if is_chain else "review"
                investigation_node = "chain_investigate_subtask" if is_chain else "investigate_subtask"
                critic_node = "chain_critic_subtask" if is_chain else "critic_subtask"
                finalize_node = "finalize_chain_subtask" if is_chain else "finalize_subtask"

                def investigate(state, **kwargs):
                    iteration = state.get("iteration", 0) + 1
                    events.append((state[task_key][id_key], "investigate", iteration))
                    return {"iteration": iteration}

                def critic(state, **kwargs):
                    events.append((state[task_key][id_key], "critic", state["iteration"]))
                    return {review_key: {"verdict": "revise" if state["iteration"] == 1 else "reject"}}

                def finalize(state, **kwargs):
                    events.append((state[task_key][id_key], "finalize", state["iteration"]))
                    return {"errors": []}

                with patch.object(graph_mod.nodes, investigation_node, investigate), patch.object(
                    graph_mod.nodes, critic_node, critic
                ), patch.object(graph_mod.nodes, finalize_node, finalize):
                    child = (graph_mod.build_chain_subtask_graph if is_chain else graph_mod.build_subtask_graph)()
                    node = task_pipeline_node(
                        child, lambda state: [Send(kind, {task_key: {id_key: task_id}}) for task_id in ("A", "B")],
                        kind=kind, next_node="finish",
                    )
                    node({"task_concurrency": {f"{kind}_concurrency": 1}}, {"max_concurrency": 8})
                self.assertEqual(events, [
                    (task_id, stage, iteration)
                    for task_id in ("A", "B")
                    for stage, iteration in (("investigate", 1), ("critic", 1), ("investigate", 2), ("critic", 2), ("finalize", 2))
                ])

    def test_poc_records_use_their_own_slots_and_keep_selection_order(self):
        barrier = threading.Barrier(2)
        records = [{"finding_id": f"VULN-{i}"} for i in range(2)]
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="test", task_id="pipeline-poc")
            state = {"workspace_root": str(ws.root), "task_id": ws.task_id,
                     "repo_path": str(ws.main / "repo"),
                     "task_concurrency": {"poc_task_concurrency": 2}}
            service = PocGenService(state)

            def run_record(record):
                barrier.wait(timeout=5)
                return record

            with patch("zeromdash.poc_gen.service.load_finding_records", return_value=records), patch.object(
                service, "run_record", side_effect=run_record
            ):
                self.assertEqual(service.run(config={"max_concurrency": 1}), records)


class PipelineConfigTest(unittest.TestCase):
    def test_yaml_roundtrip_and_missing_values_inherit(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "agents.yaml"
            path.write_text("max_concurrency: 1\nsubtask_concurrency: 2\nchain_subtask_concurrency: 3\npoc_task_concurrency: 4\n")
            config = _parse_agent_config_file(str(path))
            self.assertEqual(_pop_task_concurrency_from_agent_config(config), dict(zip(TASK_CONCURRENCY_KEYS, (2, 3, 4))))
            self.assertNotIn("__task_concurrency__", config)
            path.write_text("max_concurrency: 6\n")
            self.assertEqual(_pop_task_concurrency_from_agent_config(_parse_agent_config_file(str(path))), {})

    def test_yaml_rejects_invalid_task_slot_values(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "agents.yaml"
            for key in TASK_CONCURRENCY_KEYS:
                for value in ("true", "0", "-1", "1.5", '"2"', "null", "[]"):
                    path.write_text(f"{key}: {value}\n")
                    with self.subTest(key=key, value=value), self.assertRaisesRegex(click.ClickException, key):
                        _parse_agent_config_file(str(path))

    def test_cli_forwards_task_slots_to_scan_restore_and_poc_entry_points(self):
        slots = dict(zip(TASK_CONCURRENCY_KEYS, (2, 3, 4)))
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            config_path = Path(tmp) / "agents.yaml"
            config_path.write_text("max_concurrency: 1\nsubtask_concurrency: 2\nchain_subtask_concurrency: 3\npoc_task_concurrency: 4\n")
            final = {"task_id": "workspace", "workspace_root": tmp, "summary": "done", "errors": []}
            cases = (
                ("run", ["--target", "libfoo"]),
                ("run_from_subtask_workspace", ["--start-from-subtask", str(workspace)]),
                ("run_from_subtask_workspace", ["--start-from-subtask", str(workspace), "--select-subtask-to-run", "spec-001"]),
                ("run_from_chain_workspace", ["--start-from-chain", str(workspace)]),
                ("run_from_chain_workspace", ["--start-from-chain", str(workspace), "--select-chain-to-run", "chain-001"]),
                ("run_summary_from_workspace", ["--start-from-summary", str(workspace)]),
                ("run_pocs_from_workspace", ["--only-gen-pocs", str(workspace)]),
            )
            for entry, arguments in cases:
                with self.subTest(entry=entry, arguments=arguments), patch(
                    "zeromdash.cli._resolve_startup_backends", return_value=({}, {})
                ), patch(f"zeromdash.cli.{entry}", return_value=final) as run:
                    result = CliRunner().invoke(main, arguments + ["--agent-config", str(config_path)])
                    self.assertEqual(result.exit_code, 0, result.output)
                    self.assertEqual(run.call_args.kwargs["task_concurrency"], slots)
                    self.assertEqual(run.call_args.kwargs["max_concurrency"], 1)
                    self.assertNotIn("__task_concurrency__", run.call_args.kwargs["agent_configs"])


if __name__ == "__main__":
    unittest.main()
