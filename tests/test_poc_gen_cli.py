"""CLI and graph integration tests for PoC generation modes."""

from __future__ import annotations

import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from click.testing import CliRunner

from zeromdash import nodes as node_facade
from zeromdash.cli import _parse_agent_config_file, _pop_poc_config_from_agent_config, main
from zeromdash.graph import build_graph, run_pocs_from_workspace
from zeromdash.poc_gen.config import POC_AGENT_NODES
from zeromdash.workspace import Workspace


class PocConfigAndGraphTest(unittest.TestCase):
    def test_agent_config_poc_section_and_runtime(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "agents.yaml"
            path.write_text(
                "poc:\n"
                "  enabled: true\n"
                "  max_findings: 2\n"
                "node:\n"
                "  plan_poc:\n"
                "    runtime: codex\n"
            )
            configs = _parse_agent_config_file(str(path))
            poc = _pop_poc_config_from_agent_config(configs)
        self.assertEqual(poc, {"enabled": True, "max_findings": 2})
        self.assertEqual(configs["plan_poc"]["runtime"], "codex")
        self.assertTrue(all(node in node_facade.DEFAULT_BACKENDS for node in POC_AGENT_NODES))
        self.assertNotIn("poc_gen", node_facade.DEFAULT_BACKENDS)

    def test_graph_poc_is_opt_in_and_summary_stops_before_polish_and_poc(self):
        default_nodes = build_graph().get_graph().nodes
        enabled_nodes = build_graph(poc_enabled=True).get_graph().nodes
        summary_nodes = build_graph(till_node="summary", poc_enabled=True).get_graph().nodes
        self.assertNotIn("poc_gen", default_nodes)
        self.assertIn("poc_gen", enabled_nodes)
        self.assertIn("summary", summary_nodes)
        self.assertNotIn("polish_report", summary_nodes)
        self.assertNotIn("poc_gen", summary_nodes)


class PocCliTest(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.tmp = TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.workspace = self.root / "workspace_for_libfoo"
        self.workspace.mkdir()
        self.final = {
            "summary": "original summary",
            "task_id": self.workspace.name,
            "workspace_root": str(self.root),
            "errors": [],
            "poc_results": [
                {"finding_id": "VULN-001", "status": "validated", "attempt_count": 1, "release_path": "release"}
            ],
        }

    def tearDown(self):
        self.tmp.cleanup()

    def test_help_exposes_only_gen_modes_and_summary(self):
        result = self.runner.invoke(main, ["--help"])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("--only-gen-pocs", result.output)
        self.assertIn("--only-gen-poc", result.output)
        self.assertIn("summary", result.output)

    def test_only_gen_pocs_uses_workspace_without_target(self):
        with patch("zeromdash.cli._resolve_startup_backends", return_value=({"plan_poc": "codex"}, {})) as resolve, patch(
            "zeromdash.cli.run_pocs_from_workspace", return_value=self.final
        ) as run:
            result = self.runner.invoke(main, ["--only-gen-pocs", str(self.workspace)])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("VULN-001: validated", result.output)
        self.assertEqual(run.call_args.kwargs["workspace_path"], str(self.workspace))
        self.assertEqual(run.call_args.kwargs["finding_id"], "")
        disabled = resolve.call_args.args[2]
        self.assertIn("summary", disabled)
        self.assertTrue(all(node not in disabled for node in POC_AGENT_NODES))
        self.assertIn("original summary", (self.workspace / "final_state.json").read_text())

    def test_only_gen_pocs_prints_legacy_note_and_selection_stats(self):
        final = {
            **self.final,
            "poc_results": [],
            "poc_selection_stats": {
                "considered": 53,
                "admitted_legacy_confirm": 36,
                "skipped_legacy_not_confirmed": 15,
                "skipped_gate_failed": 2,
            },
        }
        with patch("zeromdash.cli._resolve_startup_backends", return_value=({"plan_poc": "codex"}, {})), patch(
            "zeromdash.cli.run_pocs_from_workspace", return_value=final
        ):
            result = self.runner.invoke(main, ["--only-gen-pocs", str(self.workspace)])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("No qualified findings found", result.output)
        self.assertIn("legacy finding(s) admitted", result.output)
        self.assertIn("considered=53", result.output)

    def test_only_gen_poc_splits_on_last_colon(self):
        workspace = self.root / "workspace:with-colon"
        workspace.mkdir()
        final = {**self.final, "task_id": workspace.name}
        with patch("zeromdash.cli._resolve_startup_backends", return_value=({"plan_poc": "codex"}, {})), patch(
            "zeromdash.cli.run_pocs_from_workspace", return_value=final
        ) as run:
            result = self.runner.invoke(main, ["--only-gen-poc", f"{workspace}:VULN-001"])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(run.call_args.kwargs["workspace_path"], str(workspace))
        self.assertEqual(run.call_args.kwargs["finding_id"], "VULN-001")

    def test_till_summary_disables_polish_and_poc_health_checks(self):
        with patch("zeromdash.cli._resolve_startup_backends", return_value=({}, {})) as resolve, patch(
            "zeromdash.cli.run", return_value=self.final
        ) as run:
            result = self.runner.invoke(main, ["--target", "libfoo", "--till-node", "summary"])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(run.call_args.kwargs["till_node"], "summary")
        disabled = resolve.call_args.args[2]
        self.assertIn("polish_report", disabled)
        self.assertTrue(all(node in disabled for node in POC_AGENT_NODES))

    def test_workspace_runner_restores_relative_path_and_preserves_summary(self):
        ws = Workspace.create(self.root, target="restore-target")
        (ws.main_path("repo") / "main.c").write_text("int main(void) { return 0; }\n")
        (ws.main_path("attack_surface") / "attack_surface.md").write_text("# Attack surface\n")
        (ws.base / "final_state.json").write_text('{"summary": "keep me", "summary_en": "keep me"}')
        relative = os.path.relpath(ws.base, Path.cwd())
        def fake_node(state, backends=None):
            del backends
            return {"poc_results": [{"finding_id": "VULN-001", "status": "validated"}], "errors": []}
        with patch("zeromdash.graph.nodes.poc_gen", side_effect=fake_node):
            final = run_pocs_from_workspace(relative, poc_config={"enabled": False})
        self.assertEqual(final["summary"], "keep me")
        self.assertTrue(final["poc_config"]["enabled"])
        self.assertEqual(final["poc_results"][0]["status"], "validated")

    def test_only_gen_rejects_missing_finding_id(self):
        result = self.runner.invoke(main, ["--only-gen-poc", str(self.workspace)])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("WORKSPACE:FINDING_ID", result.output)


if __name__ == "__main__":
    unittest.main()
