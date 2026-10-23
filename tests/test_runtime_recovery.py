"""Runtime recovery at real invocation and LangGraph concurrency boundaries."""

from __future__ import annotations

import copy
import json
import subprocess
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from click.testing import CliRunner
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph

from zeromdash import nodes
from zeromdash.agents import AgentHealth, AgentResult
from zeromdash.cli import _recover_runtime_config, main
from zeromdash.graph import build_subtask_graph
from zeromdash.nodes.core.recovery import (
    RecoveryRequest, RuntimeRecovery, RuntimeRecoveryAborted, runtime_recovery_scope,
)
from zeromdash.state import ZeroMDASHState
from zeromdash.workspace import Workspace


def investigation():
    return json.dumps({
        "title": "checked input", "detail": "source verification completed",
        "evidence": {"code_locations": ["src/parser.c:10"], "call_path": ["entry -> parse"]},
    })


class RuntimeRecoveryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ws = Workspace.create(self.tmp.name, target="libfoo", task_id="recovery")
        self.calls = []
        self.requests = []
        self.manual = {"runtime": "claude_code", "config": "manual.json", "model": "working"}

    def state(self, task="spec-001"):
        return {
            "target": "libfoo", "workspace_root": str(self.ws.root), "task_id": self.ws.task_id,
            "repo_path": str(self.ws.main_path("repo")),
            "subtask": {"id": task, "bucket": "spec", "objective": "check input"},
            "iteration": 0, "max_iterations": 3, "min_critic_skills": 0,
            "agent_configs": {"investigate_subtask": {
                "runtime": "codex", "model": "primary", "focus": "preserve this focus",
                "fallbacks": [{"runtime": "claude_code", "model": "fallback"}],
            }},
        }

    def run_agent(self, agent, node, backend, prompt, sub_ws, timeout, configs, *args):
        model = configs[node].get("model")
        self.calls.append((node, sub_ws.name, model))
        return AgentResult(
            stdout=investigation() if model == "working" else "",
            stderr="", returncode=1 if model == "primary" else 0, backend=backend, cwd=str(sub_ws),
        )

    def request(self, request):
        self.requests.append(request)
        return self.manual

    def test_all_attempts_and_fallbacks_finish_before_prompt_then_reuse_override(self):
        state = self.state()
        before = copy.deepcopy(state)
        recovery = RuntimeRecovery(self.request)
        def request(req):
            self.assertEqual([m for _, _, m in self.calls], ["primary"] * 3 + ["fallback"] * 3)
            self.assertEqual(req.current["model"], "fallback")
            self.assertEqual(req.current["focus"], "preserve this focus")
            return self.request(req)
        recovery.request_config = request
        with runtime_recovery_scope(recovery), patch.object(nodes, "_run_agent_with_config", side_effect=self.run_agent):
            update = nodes.investigate_subtask(state, backends={"investigate_subtask": "codex"})
            later = nodes.investigate_subtask(self.state("spec-002"), backends={"investigate_subtask": "codex"})
        self.assertTrue(update["investigation_valid"])
        self.assertTrue(later["investigation_valid"])
        self.assertEqual(update["iteration"], 1)
        self.assertEqual(state, before)
        self.assertEqual(len(self.requests), 1)
        self.assertEqual([m for _, _, m in self.calls], ["primary"] * 3 + ["fallback"] * 3 + ["working"] * 2)
        logs = self.ws.log_path("review_log")
        self.assertTrue((logs / "spec-001.iter-1.investigate_subtask.attempt-6.log").is_file())
        self.assertTrue((logs / "spec-001.iter-1.recovery-1.investigate_subtask.attempt-1.log").is_file())
        journal = [json.loads(line) for line in (self.ws.log / "runtime_recovery.jsonl").read_text().splitlines()]
        self.assertEqual(journal[0]["config"]["model"], "working")

    def test_langgraph_concurrent_subtasks_share_one_prompt_and_all_reach_critic(self):
        count = 6
        barrier = threading.Barrier(count)
        call_lock = threading.Lock()
        first_calls = set()
        reached_critic = set()
        caller_thread = threading.get_ident()
        def request(req):
            self.assertEqual(threading.get_ident(), caller_thread)
            return self.request(req)
        def agent(*args):
            task = args[4].name
            model = args[6][args[1]].get("model")
            with call_lock:
                first = task not in first_calls
                first_calls.add(task)
            if first and model == "primary":
                barrier.wait(timeout=10)
            return self.run_agent(*args)
        def critic(state, *, backends=None):
            with call_lock:
                reached_critic.add(state["subtask"]["id"])
            return {"review": {"verdict": "reject", "reasoning": "guard holds"}}
        with patch.object(
            nodes, "_run_agent_with_config", side_effect=agent
        ), patch.object(nodes, "critic_subtask", side_effect=critic):
            graph = StateGraph(ZeroMDASHState)
            graph.add_node("subtask", build_subtask_graph())
            graph.add_conditional_edges(START, lambda state: [Send("subtask", self.state(f"spec-{i:03}")) for i in range(count)])
            graph.add_edge("subtask", END)
            compiled = graph.compile()
            result = RuntimeRecovery(request).run(
                lambda: compiled.invoke(self.state(), config={"max_concurrency": count})
            )
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(len(reached_critic), count)
        self.assertFalse(result.get("errors"))
        self.assertEqual(sum(m == "working" for _, _, m in self.calls), count)

    def test_main_thread_cancellation_wakes_all_queued_workers(self):
        for exception in (EOFError, KeyboardInterrupt):
            with self.subTest(exception=exception.__name__):
                barrier = threading.Barrier(4)
                prompts = []
                caller_thread = threading.get_ident()
                def request(req):
                    self.assertEqual(threading.get_ident(), caller_thread)
                    prompts.append(req.node)
                    raise exception()
                recovery = RuntimeRecovery(request)
                results = []
                def worker(index):
                    barrier.wait(timeout=5)
                    req = RecoveryRequest("investigate_subtask", str(index), {}, "failed", self.ws.log)
                    try:
                        recovery.recover(req, 0)
                    except RuntimeRecoveryAborted:
                        return "aborted"
                def operation():
                    with ThreadPoolExecutor(max_workers=4) as pool:
                        results.extend(pool.map(worker, range(4)))
                with self.assertRaises(RuntimeRecoveryAborted):
                    recovery.run(operation)
                self.assertEqual(results, ["aborted"] * 4)
                self.assertEqual(len(prompts), 1)

    def test_prompt_serialization_across_nodes_and_shared_abort(self):
        for abort in (False, True):
            with self.subTest(abort=abort):
                count = 4
                barrier = threading.Barrier(count)
                active = 0
                maximum = 0
                prompts = []
                def request(req):
                    nonlocal active, maximum
                    active += 1
                    maximum = max(maximum, active)
                    prompts.append(req.node)
                    try:
                        if abort:
                            raise EOFError("input closed")
                        return self.manual
                    finally:
                        active -= 1
                recovery = RuntimeRecovery(request)
                def worker(index):
                    req = RecoveryRequest(f"node-{index}", str(index), {}, "failed", self.ws.log)
                    revision, _ = recovery.snapshot(req.node)
                    barrier.wait(timeout=5)
                    try:
                        recovery.recover(req, revision)
                    except RuntimeRecoveryAborted:
                        return "aborted"
                    return "configured"
                with ThreadPoolExecutor(max_workers=count) as pool:
                    results = list(pool.map(worker, range(count)))
                self.assertEqual(maximum, 1)
                self.assertEqual(results, ["aborted" if abort else "configured"] * count)
                self.assertEqual(len(prompts), 1 if abort else count)

    def test_replacement_failure_can_prompt_again_and_run_scopes_do_not_leak(self):
        def request(req):
            self.requests.append(req)
            return {**self.manual, "model": "still-broken" if len(self.requests) == 1 else "working"}
        with runtime_recovery_scope(RuntimeRecovery(request)), patch.object(nodes, "_run_agent_with_config", side_effect=self.run_agent):
            result = nodes.investigate_subtask(self.state())
        self.assertTrue(result["investigation_valid"])
        self.assertEqual(len(self.requests), 2)
        self.assertEqual(sum(m == "still-broken" for _, _, m in self.calls), 3)
        with patch.object(nodes, "_run_agent_with_config", side_effect=self.run_agent):
            result = nodes.investigate_subtask(self.state("spec-002"))
        self.assertFalse(result["investigation_valid"])
        self.assertEqual(len(self.requests), 2)

    def test_valid_artifact_avoids_human_recovery_even_when_stdout_is_empty(self):
        def agent(*args):
            (args[4] / "finding.json").write_text(investigation())
            return AgentResult("", "", 0, args[2], cwd=str(args[4]))
        with runtime_recovery_scope(RuntimeRecovery(self.request)), patch.object(nodes, "_run_agent_with_config", side_effect=agent):
            result = nodes.investigate_subtask(self.state())
        self.assertTrue(result["investigation_valid"])
        self.assertEqual(self.requests, [])

    def test_successful_explicit_fallback_does_not_request_manual_input(self):
        state = self.state()
        state["agent_configs"]["investigate_subtask"]["fallbacks"] = [self.manual]
        with runtime_recovery_scope(RuntimeRecovery(self.request)), patch.object(nodes, "_run_agent_with_config", side_effect=self.run_agent):
            result = nodes.investigate_subtask(state)
        self.assertTrue(result["investigation_valid"])
        self.assertEqual([m for _, _, m in self.calls], ["primary"] * 3 + ["working"])
        self.assertEqual(self.requests, [])

    def test_selected_run_recovery_logs_are_isolated(self):
        selected = self.ws.base / "selected-run"
        state = {**self.state(), "selected_subtask_log_dir": str(selected)}
        with runtime_recovery_scope(RuntimeRecovery(self.request)), patch.object(nodes, "_run_agent_with_config", side_effect=self.run_agent):
            result = nodes.investigate_subtask(state)
        self.assertTrue(result["investigation_valid"])
        self.assertTrue((selected / "runtime_recovery.jsonl").is_file())
        self.assertFalse((self.ws.log / "runtime_recovery.jsonl").exists())
        self.assertTrue(list((selected / "attempts").glob("*recovery-1*")))

    def test_process_launch_and_timeout_errors_follow_the_recovery_path(self):
        for error in (OSError("executable missing"), subprocess.TimeoutExpired("claude", 10)):
            with self.subTest(error=type(error).__name__):
                self.calls.clear()
                def run(prompt, cwd=None, timeout=None, extra_args=None, env=None):
                    model = extra_args[extra_args.index("--model") + 1]
                    self.calls.append(model)
                    if model != "working":
                        raise error
                    return AgentResult(investigation(), "", 0, "claude_code", cwd=str(cwd))
                with runtime_recovery_scope(RuntimeRecovery(self.request)), patch.object(nodes, "_make_agent") as agent:
                    agent.return_value.run.side_effect = run
                    result = nodes.investigate_subtask(self.state())
                self.assertTrue(result["investigation_valid"])
                self.assertEqual(self.calls, ["primary"] * 3 + ["fallback"] * 3 + ["working"])

    def test_critic_recovers_empty_output_but_does_not_prompt_on_valid_revise(self):
        state = self.state()
        state.update(iteration=1, investigation=investigation())
        state["agent_configs"]["critic_subtask"] = {"runtime": "codex", "model": "broken"}
        def agent(*args):
            good = args[6]["critic_subtask"].get("model") == "working"
            return AgentResult(json.dumps({"verdict": "revise", "reasoning": "needs evidence"}) if good else "", "", 0, args[2])
        with runtime_recovery_scope(RuntimeRecovery(self.request)), patch.object(nodes, "_run_agent_with_config", side_effect=agent):
            result = nodes.critic_subtask(state)
        self.assertEqual(result["review"]["verdict"], "revise")
        self.assertEqual(result["review"]["reasoning"], "needs evidence")
        self.assertEqual(len(self.requests), 1)

    def test_cli_recovers_and_records_final_config_or_aborts_on_eof(self):
        for has_input in (True, False):
            with self.subTest(has_input=has_input):
                def run(**kwargs):
                    result = nodes.investigate_subtask(self.state())
                    return {**self.state(), **result}
                stdin = "claude_code\nark-proxy\nark\nworking\n" if has_input else ""
                with patch("zeromdash.cli._resolve_startup_backends", return_value=({}, {})), patch(
                    "zeromdash.cli.run", side_effect=run
                ), patch("zeromdash.cli.check_agent_health", return_value=AgentHealth(name="claude_code", ok=True, message="ok")), patch(
                    "zeromdash.cli.langfuse_is_configured", return_value=False
                ), patch.object(nodes, "_run_agent_with_config", side_effect=self.run_agent):
                    result = CliRunner().invoke(main, ["--target", "libfoo"], input=stdin)
                if has_input:
                    self.assertEqual(result.exit_code, 0, result.output)
                    final = json.loads((self.ws.base / "final_state.json").read_text())
                    self.assertEqual(final["agent_configs"]["investigate_subtask"]["model"], "working")
                    self.assertIn("Temporary configuration verified", result.output)
                else:
                    self.assertNotEqual(result.exit_code, 0)
                    self.assertIn("no temporary configuration was provided", result.output)

    def test_cli_rechecks_invalid_and_unhealthy_manual_configs(self):
        request = RecoveryRequest("investigate_subtask", "spec-001", {"runtime": "codex"}, "empty", self.ws.log)
        answers = ["kimi", "", "", "", "codex", "bad", "", "", "claude_code", "ark-proxy", "ark", "working"]
        with patch("zeromdash.cli.click.prompt", side_effect=answers), patch(
            "zeromdash.cli.check_agent_health", side_effect=[
                AgentHealth(name="codex", ok=False, message="expired login"),
                AgentHealth(name="claude_code", ok=True, message="ok"),
            ]
        ) as health:
            config = _recover_runtime_config(request)
        self.assertEqual(config["runtime"], "claude_code")
        self.assertTrue(config["config"].endswith(".claude/settings.ark-proxy.json"))
        self.assertEqual(health.call_count, 2)


if __name__ == "__main__":
    unittest.main()
