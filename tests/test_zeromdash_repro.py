"""Unit tests for the standalone zeromdash_repro workflow."""

from __future__ import annotations

import json
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from click.testing import CliRunner

from zeromdash.agents import AgentHealth
from zeromdash_repro import graph as graph_mod, nodes
from zeromdash_repro.agents import AgentResult
from zeromdash_repro.cli import _resolve_startup_backends, main
from zeromdash_repro.workspace import ReproWorkspace


class ReproNodesTest(unittest.TestCase):
    def test_load_subtask_results_reads_zeromdash_subtask_res_directory(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = ReproWorkspace.create(tmp.name, target="libfoo", task_id="load")
        result_dir = ws.input / "subtask_res"
        result_dir.mkdir()
        (result_dir / "one.json").write_text(
            json.dumps({"finding": {"title": "reachable parser bug", "detail": "details"}})
        )

        update = nodes.load_subtask_results({"subtask_res": str(result_dir)})

        self.assertEqual(update["errors"], [])
        self.assertEqual(update["findings"][0]["title"], "reachable parser bug")
        self.assertEqual(
            update["subtask_result_files"],
            [str(result_dir / "one.json")],
        )

    def test_load_review_results_legacy_wrapper_preserves_review_files(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        result_dir = ReproWorkspace.create(
            tmp.name, target="libfoo", task_id="legacy-load"
        ).input / "review_res"
        result_dir.mkdir()
        result_file = result_dir / "one.json"
        result_file.write_text(json.dumps({"finding": {"title": "legacy"}}))

        update = nodes.load_review_results({"review_res": str(result_dir)})

        self.assertEqual(update["review_files"], [str(result_file)])
        self.assertEqual(update["subtask_result_files"], [str(result_file)])

    def test_repro_nodes_use_agent_workspace_without_presets(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = ReproWorkspace.create(tmp.name, target="libfoo", task_id="nodes")
        captured = {}

        def fake_invoke(ws_arg, node, prompt, backends, timeout=None):
            del timeout
            captured[node] = {"ws": ws_arg, "prompt": prompt, "backends": backends}
            if node == "plan_repro":
                return AgentResult(stdout='{"tasks": []}', stderr="", returncode=0, backend="codex", metadata={"resume_id": "codex-plan"})
            if node == "build_harmless_poc":
                return AgentResult(stdout="built local harness", stderr="", returncode=0, backend="codex")
            if node == "validate_repro":
                return AgentResult(stdout="validation ok", stderr="", returncode=0, backend="codex")
            return AgentResult(stdout="summary ok", stderr="", returncode=0, backend="claude_code")

        state = {
            "target": "libfoo",
            "workspace_root": str(ws.root),
            "task_id": ws.task_id,
            "repo_path": "/tmp/repo",
            "findings": [{"title": "bug"}],
            "subtask_result_files": ["finding.json"],
        }
        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            plan = nodes.plan_repro(state, backends={"plan_repro": "codex"})
            build = nodes.build_harmless_poc({**state, **plan}, backends={"build_harmless_poc": "codex"})
            validate = nodes.validate_repro({**state, **plan, **build}, backends={"validate_repro": "codex"})
            summary = nodes.summary({**state, **plan, **build, **validate}, backends={"summary": "claude_code"})

        self.assertEqual(plan["repro_plan"], '{"tasks": []}')
        self.assertEqual(build["build_report"], "built local harness")
        self.assertEqual(validate["validation_report"], "validation ok")
        self.assertEqual(summary["summary"], "summary ok")
        self.assertTrue((ws.reports / "repro_plan.json").is_file())
        self.assertTrue((ws.reports / "build_report.md").is_file())
        self.assertTrue((ws.reports / "validation_report.md").is_file())
        self.assertIn("local-only", captured["build_harmless_poc"]["prompt"])

    def test_repro_invoke_records_agent_resume_metadata(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = ReproWorkspace.create(tmp.name, target="libfoo", task_id="invoke-meta")

        class FakeAgent:
            def run(self, prompt, cwd=None, timeout=None):
                del prompt, timeout
                return AgentResult(
                    stdout='{"tasks": []}',
                    stderr="",
                    returncode=0,
                    backend="codex",
                    cwd=str(cwd),
                    metadata={"resume_id": "codex-plan", "command": ["codex", "exec", "-"]},
                )

        with patch.object(nodes, "_make_agent", return_value=FakeAgent()):
            nodes._invoke(ws, "plan_repro", "prompt", {"plan_repro": "codex"})

        meta = json.loads((ws.agent_workspace / "node_plan_repro" / "agent_invocation.json").read_text())
        self.assertEqual(meta["resume_id"], "codex-plan")
        self.assertEqual(meta["backend"], "codex")
        log_records = [json.loads(line) for line in (ws.log / "agent_commands.jsonl").read_text().splitlines()]
        self.assertEqual(len(log_records), 1)
        self.assertEqual(log_records[0]["node"], "plan_repro")
        self.assertEqual(log_records[0]["backend"], "codex")
        self.assertEqual(log_records[0]["command"], ["codex", "exec", "-"])
        self.assertEqual(log_records[0]["resume_id"], "codex-plan")
        self.assertTrue(log_records[0]["ok"])
        self.assertIn("node_plan_repro", log_records[0]["agent_workspace"])

    def test_agent_workspace_materializes_headless_agent_files(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = ReproWorkspace.create(tmp.name, target="libfoo", task_id="agents")

        cwd = ws.prepare_agent_workspace("build_harmless_poc", repo_path="/tmp/repo")

        self.assertIn("ZeroMDASH Repro agent", (cwd / "AGENTS.md").read_text())
        self.assertIn("ZeroMDASH Repro agent", (cwd / "CLAUDE.md").read_text())
        self.assertTrue((cwd / ".codex" / "config.toml").is_file())
        self.assertTrue((cwd / ".claude" / "settings.json").is_file())
        self.assertIn("network_access = false", (cwd / ".codex" / "config.toml").read_text())
        self.assertIn("/tmp/repo", (cwd / ".claude" / "settings.json").read_text())

    def test_backend_fallback_chain_supports_codex_claude_and_opencode(self):
        self.assertEqual(nodes.backend_fallback_chain("plan_repro"), ["codex", "claude_code", "opencode"])
        self.assertEqual(nodes.backend_fallback_chain("summary"), ["claude_code", "codex", "opencode"])
        self.assertEqual(
            nodes.backend_fallback_chain("plan_repro", {"plan_repro": "opencode"}),
            ["opencode", "codex", "claude_code"],
        )


class ReproGraphCliTest(unittest.TestCase):
    def test_graph_runs_standalone_repro_workflow(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        review_file = ReproWorkspace.create(tmp.name, target="seed", task_id="seed").input / "finding.json"
        review_file.write_text(json.dumps({"finding": {"title": "bug"}}))

        def fake_invoke(ws_arg, node, prompt, backends, timeout=None):
            del ws_arg, prompt, backends, timeout
            outputs = {
                "plan_repro": '{"tasks": []}',
                "build_harmless_poc": "build ok",
                "validate_repro": "validate ok",
                "summary": "summary ok",
            }
            return AgentResult(stdout=outputs[node], stderr="", returncode=0, backend="codex")

        with patch.object(graph_mod.nodes, "_invoke", side_effect=fake_invoke):
            final = graph_mod.run(
                subtask_res=str(review_file),
                repo_path="/tmp/repo",
                target="libfoo",
                workspace_root=tmp.name,
            )

        self.assertEqual(final["summary"], "summary ok")
        self.assertEqual(final["build_report"], "build ok")
        self.assertEqual(final["validation_report"], "validate ok")
        self.assertEqual(final["findings"][0]["title"], "bug")

    def test_cli_passes_arguments_to_repro_run(self):
        runner = CliRunner()
        final = {"summary": "done", "task_id": "task-1", "errors": []}

        selected = {
            "plan_repro": "claude_code",
            "build_harmless_poc": "codex",
            "validate_repro": "codex",
            "summary": "claude_code",
        }
        with patch("zeromdash_repro.cli._resolve_startup_backends", return_value=(selected, {})), patch(
            "zeromdash_repro.cli.run", return_value=final
        ) as run:
            result = runner.invoke(
                main,
                [
                    "--subtask-res",
                    "/tmp/subtask_res",
                    "--repo-path",
                    "/tmp/repo",
                    "--target",
                    "libfoo",
                    "--backend",
                    "plan_repro=claude_code",
                ],
            )

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("=== repro summary ===", result.output)
        self.assertEqual(run.call_args.kwargs["subtask_res"], "/tmp/subtask_res")
        self.assertEqual(run.call_args.kwargs["repo_path"], "/tmp/repo")
        self.assertEqual(run.call_args.kwargs["target"], "libfoo")
        self.assertEqual(run.call_args.kwargs["backends"], selected)

    def test_cli_accepts_legacy_review_res_alias(self):
        runner = CliRunner()
        final = {"summary": "done", "task_id": "task-1", "errors": []}
        with patch(
            "zeromdash_repro.cli._resolve_startup_backends",
            return_value=({}, {}),
        ), patch("zeromdash_repro.cli.run", return_value=final) as run:
            result = runner.invoke(main, ["--review-res", "/tmp/review_res"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(run.call_args.kwargs["subtask_res"], "/tmp/review_res")

    def test_startup_backend_resolution_can_fallback_to_opencode(self):
        health = {
            "codex": AgentHealth(name="codex", ok=False, binary="codex", message="bad codex"),
            "claude_code": AgentHealth(name="claude_code", ok=False, binary="claude", message="bad claude"),
            "opencode": AgentHealth(name="opencode", ok=True, binary="opencode", message="ok"),
        }

        def fake_health(agent, timeout=60):
            del timeout
            return health[agent.name]

        with patch("zeromdash_repro.cli.check_agent_health", side_effect=fake_health):
            selected, cache = _resolve_startup_backends({})

        self.assertEqual(selected["plan_repro"], "opencode")
        self.assertEqual(selected["build_harmless_poc"], "opencode")
        self.assertEqual(selected["validate_repro"], "opencode")
        self.assertEqual(selected["summary"], "opencode")
        self.assertFalse(cache["codex"].ok)


if __name__ == "__main__":
    unittest.main()
