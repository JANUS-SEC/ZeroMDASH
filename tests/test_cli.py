"""Unit tests for the zeromdash CLI startup flow."""

from __future__ import annotations

import os
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import click
from click.testing import CliRunner

from zeromdash.agents import AgentHealth
from zeromdash.cli import (
    _parse_agent_config_file,
    _pop_common_focus_from_agent_config,
    _pop_max_concurrency_from_agent_config,
    _pop_target_repos_from_agent_config,
    _pop_top_k_from_agent_config,
    _resolve_startup_backends,
    main,
)


class CliStartupHealthCheckTest(unittest.TestCase):
    def test_cli_help_hides_deprecated_focus_and_backend_options(self):
        result = CliRunner().invoke(main, ["--help"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("--agent-config", result.output)
        self.assertIn("--preset-attack-surface", result.output)
        self.assertIn("--scan-mode", result.output)
        self.assertIn("--diff-file", result.output)
        self.assertIn("--diff-git", result.output)
        self.assertIn("--fail-on-gate", result.output)
        self.assertIn("--disable-target-history", result.output)
        self.assertIn("--till-node", result.output)
        self.assertIn("--start-from-subtask", result.output)
        self.assertIn("--start-from-subagent", result.output)
        self.assertIn("--select-subtask-to-run", result.output)
        self.assertIn("--select-subagent-to-run", result.output)
        self.assertIn("--select-subtask-to-run-log-dir", result.output)
        self.assertIn("--select-subagent-to-run-log-dir", result.output)
        self.assertNotIn("--backend", result.output)
        self.assertNotIn("--common-focus", result.output)
        self.assertNotIn("--focus", result.output)
        self.assertNotIn("--fetch-target-repo-focus", result.output)
        self.assertNotIn("--search-fuzz-driver-focus", result.output)
        self.assertNotIn("--search-similar-software-focus", result.output)
        self.assertNotIn("--search-target-history-focus", result.output)
        self.assertNotIn("--analyze-attack-surface-focus", result.output)
        self.assertNotIn("--summary-focus", result.output)

    def test_cli_exits_before_run_when_agent_health_check_fails_without_human_override(self):
        runner = CliRunner()
        long_stderr = "not logged in: " + "x" * 700
        failed = AgentHealth(
            name="codex",
            ok=False,
            binary="codex",
            message="codex headless health check failed with rc=1",
            returncode=1,
            stderr=long_stderr,
            command=["codex", "exec", "-"],
            env_overlay={"ZEROMDASH_CODEX_MODEL": "deepseek-v4-pro"},
        )

        with patch("zeromdash.cli.check_agent_health", return_value=failed) as check, patch("zeromdash.cli.run") as run:
            result = runner.invoke(main, ["--target", "libfoo"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("ZeroMDASH startup agent health check failed", result.output)
        self.assertIn('command: ["codex", "exec", "-"]', result.output)
        self.assertIn('env_overlay: {"ZEROMDASH_CODEX_MODEL": "deepseek-v4-pro"}', result.output)
        self.assertIn(long_stderr, result.output)
        self.assertEqual(check.call_count, 1)
        run.assert_not_called()

    def test_cli_runs_workflow_after_agent_health_check_passes(self):
        runner = CliRunner()

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with TemporaryDirectory() as tmp:
            final = {"summary": "done", "task_id": "workspace_for_libfoo__task-1", "workspace_root": tmp, "errors": []}
            final_state_path = Path(tmp) / final["task_id"] / "final_state.json"
            final_state_path.parent.mkdir(parents=True)
            cfg = Path(tmp) / "agents.yaml"
            preset_attack_surface = Path(tmp) / "attack_surface.md"
            preset_attack_surface.write_text("# Existing attack surface\n")
            cfg.write_text(
                "common_focus: config global threat model\n"
                "top_K:\n"
                "  spec: 3\n"
                "  vuln: 10\n"
                "  feature: 4\n"
                "max_concurrency: 6\n"
                "node:\n"
                "  search_spec:\n"
                "    runtime: claude_code\n"
                "    config: bedrock\n"
                "    provider: bedrock\n"
                "    focus: authoritative specs only\n"
                "  plan_by_spec:\n"
                "    runtime: codex_cli\n"
                "    config: doubao\n"
                "    provider: ark\n"
            )
            with patch.dict(os.environ, {"AWS_BEARER_TOKEN_BEDROCK": "token-1"}, clear=True), patch(
                "zeromdash.cli.check_agent_health", side_effect=fake_health
            ) as check, patch("zeromdash.cli.run", return_value=final) as run:
                result = runner.invoke(
                    main,
                    [
                        "--target",
                        "libfoo",
                        "--common-focus",
                        "network reachable paths",
                        "--fetch-target-repo-focus",
                        "official upstream only",
                        "--search-fuzz-driver-focus",
                        "HTTP parser harnesses",
                        "--search-similar-software-focus",
                        "state-machine peers",
                        "--search-target-history-focus",
                        "parser CVEs",
                        "--analyze-attack-surface-focus",
                        "trust boundaries",
                        "--summary-focus",
                        "actionable triage",
                        "--backend",
                        "summary=codex",
                        "--role-lang",
                        "zh_CN",
                        "--agent-config",
                        str(cfg),
                        "--preset-attack-surface",
                        str(preset_attack_surface),
                    ],
                )
            final_state = json.loads(final_state_path.read_text())

        self.assertEqual(final_state, final)

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("final state written to", result.output)
        self.assertNotIn('"workspace_root"', result.output)
        self.assertNotIn('"task_id"', result.output)
        self.assertIn("=== summary ===", result.output)
        self.assertIn("done", result.output)
        self.assertGreaterEqual(check.call_count, 2)
        run.assert_called_once()
        self.assertEqual(run.call_args.kwargs["target"], "libfoo")
        self.assertEqual(run.call_args.kwargs["common_focus"], "network reachable paths")
        self.assertEqual(run.call_args.kwargs["fetch_target_repo_focus"], "official upstream only")
        self.assertEqual(run.call_args.kwargs["search_fuzz_driver_focus"], "HTTP parser harnesses")
        self.assertEqual(run.call_args.kwargs["search_similar_software_focus"], "state-machine peers")
        self.assertEqual(run.call_args.kwargs["search_target_history_focus"], "parser CVEs")
        self.assertEqual(run.call_args.kwargs["analyze_attack_surface_focus"], "trust boundaries")
        self.assertEqual(run.call_args.kwargs["summary_focus"], "actionable triage")
        self.assertEqual(run.call_args.kwargs["role_lang"], "zh_CN")
        self.assertEqual(run.call_args.kwargs["backends"]["summary"], "codex")
        self.assertEqual(run.call_args.kwargs["preset_attack_surface_path"], str(preset_attack_surface))
        self.assertEqual(run.call_args.kwargs["target_repos"], [])
        self.assertEqual(run.call_args.kwargs["top_K"], {"spec": 3, "vuln": 10, "feature": 4})
        self.assertEqual(run.call_args.kwargs["max_concurrency"], 6)
        self.assertEqual(
            run.call_args.kwargs["agent_configs"],
            {
                "search_spec": {
                    "runtime": "claude_code",
                    "provider": "bedrock",
                    "config": os.path.expanduser("~/.claude/settings.bedrock.json"),
                    "focus": "authoritative specs only",
                },
                "plan_by_spec": {
                    "runtime": "codex",
                    "provider": "ark",
                    "config": "doubao",
                },
            },
        )

    def test_cli_disable_spec_threads_disabled_nodes(self):
        runner = CliRunner()

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with TemporaryDirectory() as tmp:
            final = {"summary": "done", "task_id": "t1", "workspace_root": tmp, "errors": []}
            (Path(tmp) / "t1").mkdir(parents=True)
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text("top_K:\n  spec: 99\n")
            with patch("zeromdash.cli.check_agent_health", side_effect=fake_health), patch(
                "zeromdash.cli.run", return_value=final
            ) as run:
                result = runner.invoke(main, ["--target", "libfoo", "--disable-spec", "--agent-config", str(cfg)])

        self.assertEqual(result.exit_code, 0, result.output)
        run.assert_called_once()
        self.assertEqual(run.call_args.kwargs["disabled_nodes"], {"search_spec", "plan_by_spec"})
        self.assertEqual(run.call_args.kwargs["top_K"], {"spec": 99})

    def test_agent_config_target_repos_threads_to_run(self):
        runner = CliRunner()

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with TemporaryDirectory() as tmp:
            final = {"summary": "done", "task_id": "t1", "workspace_root": tmp, "errors": []}
            (Path(tmp) / "t1").mkdir(parents=True)
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text(
                "target_repos:\n"
                "  - id: core\n"
                "    target: https://example.com/core.git\n"
                "    role: main\n"
                "  - id: plugin-auth\n"
                "    path: ~/plugins/auth\n"
                "    role: plugin\n"
            )
            with patch("zeromdash.cli.check_agent_health", side_effect=fake_health), patch(
                "zeromdash.cli.run", return_value=final
            ) as run:
                result = runner.invoke(main, ["--target", "product", "--agent-config", str(cfg)])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(
            run.call_args.kwargs["target_repos"],
            [
                {"id": "core", "target": "https://example.com/core.git", "role": "main"},
                {"id": "plugin-auth", "target": os.path.expanduser("~/plugins/auth"), "role": "plugin"},
            ],
        )

    def test_target_repos_can_supply_default_target_name(self):
        runner = CliRunner()

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with TemporaryDirectory() as tmp:
            final = {"summary": "done", "task_id": "t1", "workspace_root": tmp, "errors": []}
            (Path(tmp) / "t1").mkdir(parents=True)
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text("target_repos:\n  - id: core\n    target: https://example.com/core.git\n")
            with patch("zeromdash.cli.check_agent_health", side_effect=fake_health), patch(
                "zeromdash.cli.run", return_value=final
            ) as run:
                result = runner.invoke(main, ["--agent-config", str(cfg)])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(run.call_args.kwargs["target"], "multi-repo-target")

    def test_diff_mode_rejects_target_repos(self):
        runner = CliRunner()

        with TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text("target_repos:\n  - id: core\n    target: https://example.com/core.git\n")
            for diff_args in (["--diff-git", "a..b"], ["--diff-file", str(cfg)]):
                with self.subTest(diff_args=diff_args):
                    result = runner.invoke(
                        main,
                        [
                            "--target",
                            "product",
                            "--scan-mode",
                            "diff",
                            *diff_args,
                            "--agent-config",
                            str(cfg),
                        ],
                    )
                    self.assertNotEqual(result.exit_code, 0)
                    self.assertIn("support --scan-mode full only", result.output)

    def test_cli_disable_target_history_threads_disabled_nodes(self):
        runner = CliRunner()

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with TemporaryDirectory() as tmp:
            final = {"summary": "done", "task_id": "t1", "workspace_root": tmp, "errors": []}
            (Path(tmp) / "t1").mkdir(parents=True)
            with patch("zeromdash.cli.check_agent_health", side_effect=fake_health), patch(
                "zeromdash.cli.run", return_value=final
            ) as run:
                result = runner.invoke(main, ["--target", "libfoo", "--disable-target-history"])

        self.assertEqual(result.exit_code, 0, result.output)
        run.assert_called_once()
        self.assertEqual(run.call_args.kwargs["disabled_nodes"], {"search_target_history", "plan_by_vuln_patch"})

    def test_cli_disable_new_feature_threads_disabled_nodes(self):
        runner = CliRunner()

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with TemporaryDirectory() as tmp:
            final = {"summary": "done", "task_id": "t1", "workspace_root": tmp, "errors": []}
            (Path(tmp) / "t1").mkdir(parents=True)
            with patch("zeromdash.cli.check_agent_health", side_effect=fake_health), patch(
                "zeromdash.cli.run", return_value=final
            ) as run:
                result = runner.invoke(main, ["--target", "libfoo", "--disable-new-feature"])

        self.assertEqual(result.exit_code, 0, result.output)
        run.assert_called_once()
        self.assertEqual(run.call_args.kwargs["disabled_nodes"], {"search_new_feature", "plan_by_new_feature"})

    def test_cli_disable_chain_threads_plan_and_battle_disabled_nodes(self):
        runner = CliRunner()

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with TemporaryDirectory() as tmp:
            final = {"summary": "done", "task_id": "t1", "workspace_root": tmp, "errors": []}
            (Path(tmp) / "t1").mkdir(parents=True)
            with patch("zeromdash.cli.check_agent_health", side_effect=fake_health), patch(
                "zeromdash.cli.run", return_value=final
            ) as run:
                result = runner.invoke(main, ["--target", "libfoo", "--disable-chain"])

        self.assertEqual(result.exit_code, 0, result.output)
        run.assert_called_once()
        self.assertEqual(
            run.call_args.kwargs["disabled_nodes"],
            {"plan_chains", "chain_investigate_subtask", "chain_critic_subtask"},
        )

    def test_cli_till_node_threads_to_run_and_skips_later_health_checks(self):
        runner = CliRunner()
        health_nodes = []

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            health_nodes.append(agent.name)
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with TemporaryDirectory() as tmp:
            final = {
                "summary": "",
                "stopped_at": "analyze",
                "task_id": "t1",
                "workspace_root": tmp,
                "errors": [],
            }
            (Path(tmp) / "t1").mkdir(parents=True)
            with patch("zeromdash.cli.check_agent_health", side_effect=fake_health), patch(
                "zeromdash.cli.run", return_value=final
            ) as run:
                result = runner.invoke(main, ["--target", "libfoo", "--till-node", "analyze"])

        self.assertEqual(result.exit_code, 0, result.output)
        run.assert_called_once()
        self.assertEqual(run.call_args.kwargs["till_node"], "analyze")
        # analyze mode still health-checks analyze_attack_surface (codex), but
        # skips planner/subtask/summary health checks.
        self.assertEqual(health_nodes.count("codex"), 1)

    def test_cli_start_from_subtask_uses_workspace_without_target(self):
        runner = CliRunner()
        health_nodes = []

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            health_nodes.append(agent.name)
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace_for_libfoo"
            workspace.mkdir()
            final = {
                "summary": "restored",
                "task_id": workspace.name,
                "workspace_root": tmp,
                "errors": [],
            }
            with patch("zeromdash.cli.check_agent_health", side_effect=fake_health), patch(
                "zeromdash.cli.run_from_subtask_workspace", return_value=final
            ) as restore:
                result = runner.invoke(main, ["--start-from-subagent", str(workspace)])

        self.assertEqual(result.exit_code, 0, result.output)
        restore.assert_called_once()
        self.assertEqual(restore.call_args.kwargs["workspace_path"], str(workspace))
        self.assertIn("codex", health_nodes)
        self.assertIn("claude_code", health_nodes)
        # Front-half Claude search/fetch nodes are disabled for restore; one
        # Claude health check remains for summary.
        self.assertEqual(health_nodes.count("claude_code"), 1)

    def test_cli_selected_subtasks_skip_summary_and_write_isolated_final_state(self):
        runner = CliRunner()
        health_nodes = []

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            health_nodes.append(agent.name)
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace_for_libfoo"
            workspace.mkdir()
            selected_dir = workspace / "selected-output"
            selected_dir.mkdir()
            final = {
                "task_id": workspace.name,
                "workspace_root": tmp,
                "selected_subtask_log_dir": str(selected_dir),
                "selected_subtask_statuses": [
                    {
                        "subtask_id": "vuln-013",
                        "status": "completed",
                        "verdict": "confirm",
                        "severity": "high",
                        "iterations": 2,
                    }
                ],
                "stopped_at": "selected_subtasks",
                "errors": [],
            }
            with patch(
                "zeromdash.cli.check_agent_health",
                side_effect=fake_health,
            ), patch(
                "zeromdash.cli.run_from_subtask_workspace",
                return_value=final,
            ) as restore:
                result = runner.invoke(
                    main,
                    [
                        "--start-from-subagent",
                        str(workspace),
                        "--select-subagent-to-run",
                        "vuln-013",
                        "--select-subagent-to-run-log-dir",
                        "selected-output",
                    ],
                )

            isolated_final_state = selected_dir / "final_state.json"
            isolated_final_state_exists = isolated_final_state.is_file()
            canonical_final_state_exists = (
                workspace / "final_state.json"
            ).is_file()

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertTrue(isolated_final_state_exists)
        self.assertFalse(canonical_final_state_exists)
        self.assertNotIn("=== summary ===", result.output)
        self.assertIn("=== selected subtask statuses ===", result.output)
        self.assertIn("vuln-013: completed", result.output)
        self.assertNotIn("claude_code", health_nodes)
        self.assertEqual(
            restore.call_args.kwargs["selected_subtask_ids"],
            ["vuln-013"],
        )
        self.assertEqual(
            restore.call_args.kwargs["selected_subtask_log_dir"],
            "selected-output",
        )
        self.assertFalse(restore.call_args.kwargs["run_summary"])

    def test_cli_selected_subtask_options_require_restore_selection(self):
        result = CliRunner().invoke(
            main,
            ["--target", "libfoo", "--select-subagent-to-run", "vuln-013"],
        )
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn(
            "--select-subtask-to-run requires --start-from-subtask",
            result.output,
        )

        result = CliRunner().invoke(
            main,
            [
                "--start-from-subagent",
                "/tmp/workspace",
                "--select-subagent-to-run-log-dir",
                "selected-output",
            ],
        )
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn(
            "--select-subtask-to-run-log-dir requires --select-subtask-to-run",
            result.output,
        )

    def test_cli_requires_target_without_restore_mode(self):
        result = CliRunner().invoke(main, [])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("--target is required unless a restore mode is used", result.output)

    def test_cli_diff_mode_requires_diff_file(self):
        result = CliRunner().invoke(main, ["--target", "libfoo", "--scan-mode", "diff"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("--scan-mode diff requires --diff-file or --diff-git", result.output)

    def test_cli_diff_file_requires_diff_mode(self):
        with TemporaryDirectory() as tmp:
            diff = Path(tmp) / "change.patch"
            diff.write_text("diff --git a/a.c b/a.c\n")
            result = CliRunner().invoke(main, ["--target", "libfoo", "--diff-file", str(diff)])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("--diff-file/--diff-git require --scan-mode diff", result.output)

    def test_cli_diff_file_and_diff_git_are_mutually_exclusive(self):
        with TemporaryDirectory() as tmp:
            diff = Path(tmp) / "change.patch"
            diff.write_text("diff --git a/a.c b/a.c\n")
            result = CliRunner().invoke(
                main,
                [
                    "--target",
                    "libfoo",
                    "--scan-mode",
                    "diff",
                    "--diff-file",
                    str(diff),
                    "--diff-git",
                    "before..after",
                ],
            )

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("mutually exclusive", result.output)

    def test_cli_rejects_diff_git_for_local_directory_target(self):
        with TemporaryDirectory() as tmp:
            result = CliRunner().invoke(
                main,
                [
                    "--target",
                    tmp,
                    "--scan-mode",
                    "diff",
                    "--diff-git",
                    "before..after",
                ],
            )

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("local directory targets use --diff-file", result.output)

    def test_cli_threads_diff_mode_and_diff_file_to_run(self):
        runner = CliRunner()

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with TemporaryDirectory() as tmp:
            diff = Path(tmp) / "change.patch"
            diff.write_text("diff --git a/a.c b/a.c\n--- a/a.c\n+++ b/a.c\n@@ -1 +1 @@\n-old\n+new\n")
            final = {"summary": "done", "task_id": "t1", "workspace_root": tmp, "errors": []}
            (Path(tmp) / "t1").mkdir()
            with patch("zeromdash.cli.check_agent_health", side_effect=fake_health), patch(
                "zeromdash.cli.run", return_value=final
            ) as run:
                result = runner.invoke(
                    main,
                    [
                        "--target",
                        "libfoo",
                        "--scan-mode",
                        "diff",
                        "--diff-file",
                        str(diff),
                    ],
                )

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(run.call_args.kwargs["scan_mode"], "diff")
        self.assertEqual(run.call_args.kwargs["diff_file"], str(diff))
        self.assertEqual(run.call_args.kwargs["diff_git"], "")

    def test_cli_threads_diff_git_to_run(self):
        runner = CliRunner()

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with TemporaryDirectory() as tmp:
            final = {"summary": "done", "task_id": "t1", "workspace_root": tmp, "errors": []}
            (Path(tmp) / "t1").mkdir()
            with patch("zeromdash.cli.check_agent_health", side_effect=fake_health), patch(
                "zeromdash.cli.run", return_value=final
            ) as run:
                result = runner.invoke(
                    main,
                    [
                        "--target",
                        "https://example.com/libfoo.git",
                        "--scan-mode",
                        "diff",
                        "--diff-git",
                        "v1.0..main",
                    ],
                )

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(run.call_args.kwargs["scan_mode"], "diff")
        self.assertEqual(run.call_args.kwargs["diff_file"], "")
        self.assertEqual(run.call_args.kwargs["diff_git"], "v1.0..main")

    def test_cli_fail_on_gate_returns_nonzero_for_block(self):
        runner = CliRunner()

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with TemporaryDirectory() as tmp:
            final = {
                "summary": "blocked",
                "task_id": "t1",
                "workspace_root": tmp,
                "errors": [],
                "gate_result": {"decision": "block"},
            }
            (Path(tmp) / "t1").mkdir()
            with patch("zeromdash.cli.check_agent_health", side_effect=fake_health), patch(
                "zeromdash.cli.run", return_value=final
            ):
                result = runner.invoke(main, ["--target", "libfoo", "--fail-on-gate"])

        self.assertEqual(result.exit_code, 2, result.output)

    def test_cli_start_from_summary_uses_workspace_without_target(self):
        runner = CliRunner()
        health_nodes = []

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            health_nodes.append(agent.name)
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace_for_libfoo"
            workspace.mkdir()
            final = {
                "summary": "summary only",
                "task_id": workspace.name,
                "workspace_root": tmp,
                "errors": [],
            }
            with patch("zeromdash.cli.check_agent_health", side_effect=fake_health), patch(
                "zeromdash.cli.run_summary_from_workspace", return_value=final
            ) as restore:
                result = runner.invoke(main, ["--start-from-summary", str(workspace)])

        self.assertEqual(result.exit_code, 0, result.output)
        restore.assert_called_once()
        self.assertEqual(restore.call_args.kwargs["workspace_path"], str(workspace))
        self.assertEqual(health_nodes, ["claude_code"])

    def test_cli_restore_modes_are_mutually_exclusive(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace_for_libfoo"
            workspace.mkdir()
            result = CliRunner().invoke(
                main,
                [
                    "--start-from-subagent",
                    str(workspace),
                    "--start-from-summary",
                    str(workspace),
                ],
            )

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("mutually exclusive", result.output)

    def test_parse_agent_config_file(self):
        with TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text(
                "common_focus: guest-to-host escape threat model\n"
                "top_K:\n"
                "  spec: 3\n"
                "  vuln: 10\n"
                "  patch: 2\n"
                "  feature: 4\n"
                "max_concurrency: 4\n"
                "node:\n"
                "  search_spec:\n"
                "    runtime: claude_code\n"
                "    config: aws_bedrock\n"
                "    provider: bedrock\n"
                "    model: claude-sonnet-test\n"
                "    focus: parser and memory safety\n"
                "    env:\n"
                "      CUSTOM_TOKEN: $HOME/token\n"
                "      REMOVE_ME: null\n"
                "  plan_by_spec:\n"
                "    runtime: trae-cli\n"
                "    config: volc_ark\n"
                "    model: \"\"\n"
                "    provider: ark\n"
                "    fallbacks:\n"
                "      - runtime: claude_code\n"
                "        config: ark-proxy\n"
                "        provider: ark\n"
                "        model: claude-fallback\n"
                "        env:\n"
                "          FALLBACK_ENV: enabled\n"
                "  critic_subtask:\n"
                "    runtime: codex\n"
                "  investigate_subtask:\n"
                "    runtime: traex\n"
                "    config: security\n"
                "    provider: ark\n"
                "    model: gpt-5.6\n"
            )
            parsed = _parse_agent_config_file(str(cfg))
            common_focus = _pop_common_focus_from_agent_config(parsed)
            top_K = _pop_top_k_from_agent_config(parsed)
            max_concurrency = _pop_max_concurrency_from_agent_config(parsed)

        self.assertEqual(common_focus, "guest-to-host escape threat model")
        self.assertEqual(top_K, {"spec": 3, "vuln": 10, "patch": 2, "feature": 4})
        self.assertEqual(max_concurrency, 4)
        self.assertEqual(parsed["search_spec"]["runtime"], "claude_code")
        self.assertEqual(
            parsed["search_spec"]["config"],
            os.path.expanduser("~/.claude/settings.aws_bedrock.json"),
        )
        self.assertEqual(parsed["search_spec"]["provider"], "bedrock")
        self.assertEqual(parsed["search_spec"]["model"], "claude-sonnet-test")
        self.assertEqual(parsed["search_spec"]["focus"], "parser and memory safety")
        self.assertEqual(parsed["search_spec"]["env"]["CUSTOM_TOKEN"], os.path.expandvars("$HOME/token"))
        self.assertIsNone(parsed["search_spec"]["env"]["REMOVE_ME"])
        self.assertEqual(parsed["plan_by_spec"]["runtime"], "traex")
        self.assertEqual(parsed["plan_by_spec"]["config"], "volc_ark")
        self.assertEqual(parsed["plan_by_spec"]["model"], "")
        self.assertEqual(
            parsed["plan_by_spec"]["fallbacks"],
            [
                {
                    "runtime": "claude_code",
                    "config": os.path.expanduser("~/.claude/settings.ark-proxy.json"),
                    "provider": "ark",
                    "model": "claude-fallback",
                    "env": {"FALLBACK_ENV": "enabled"},
                }
            ],
        )
        self.assertEqual(parsed["critic_subtask"]["runtime"], "codex")
        self.assertNotIn("config", parsed["critic_subtask"])
        self.assertNotIn("provider", parsed["critic_subtask"])
        self.assertEqual(parsed["investigate_subtask"]["runtime"], "traex")
        self.assertEqual(
            parsed["investigate_subtask"]["config"],
            "security",
        )
        self.assertEqual(
            parsed["investigate_subtask"]["provider"],
            "ark",
        )
        self.assertEqual(
            parsed["investigate_subtask"]["model"],
            "gpt-5.6",
        )

    def test_parse_agent_config_defaults_max_concurrency_to_8(self):
        with TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text("node:\n  summary:\n    runtime: codex\n")
            parsed = _parse_agent_config_file(str(cfg))
            max_concurrency = _pop_max_concurrency_from_agent_config(parsed)

        self.assertEqual(max_concurrency, 8)
        self.assertEqual(parsed["summary"]["runtime"], "codex")

    def test_parse_agent_config_target_repos(self):
        with TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text(
                "target_repos:\n"
                "  - id: core\n"
                "    url: https://example.com/core.git\n"
                "    role: main\n"
                "  - name: plugin\n"
                "    path: ./plugin\n"
            )
            parsed = _parse_agent_config_file(str(cfg))
            repos = _pop_target_repos_from_agent_config(parsed)

        self.assertEqual(
            repos,
            [
                {"id": "core", "target": "https://example.com/core.git", "role": "main"},
                {"id": "plugin", "target": str((Path(tmp) / "plugin").resolve())},
            ],
        )

    def test_parse_agent_config_rejects_duplicate_target_repo_ids(self):
        with TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text(
                "target_repos:\n"
                "  - id: core\n"
                "    target: https://example.com/core.git\n"
                "  - id: core\n"
                "    target: https://example.com/other.git\n"
            )

            with self.assertRaises(click.ClickException) as cm:
                _parse_agent_config_file(str(cfg))

        self.assertIn("duplicate target_repos id", str(cm.exception))

    def test_parse_agent_config_rejects_non_int_top_k_values(self):
        with TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text("top_K:\n  spec: \"3\"\n")

            with self.assertRaises(click.ClickException) as cm:
                _parse_agent_config_file(str(cfg))

        self.assertIn("top_K.spec", str(cm.exception))
        self.assertIn("expected int", str(cm.exception))

    def test_parse_agent_config_rejects_non_positive_top_k_values(self):
        with TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text("top_K:\n  patch: 0\n")

            with self.assertRaises(click.ClickException) as cm:
                _parse_agent_config_file(str(cfg))

        self.assertIn("top_K.patch", str(cm.exception))
        self.assertIn("expected positive int", str(cm.exception))

    def test_parse_agent_config_rejects_unknown_top_k_bucket(self):
        with TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text("top_K:\n  exploit: 3\n")

            with self.assertRaises(click.ClickException) as cm:
                _parse_agent_config_file(str(cfg))

        self.assertIn("unknown top_K key", str(cm.exception))
        self.assertIn("exploit", str(cm.exception))

    def test_parse_agent_config_rejects_invalid_max_concurrency(self):
        for value, expected in [
            ("\"8\"", "expected int"),
            ("0", "expected positive int"),
        ]:
            with self.subTest(value=value):
                with TemporaryDirectory() as tmp:
                    cfg = Path(tmp) / "agents.yaml"
                    cfg.write_text(f"max_concurrency: {value}\n")

                    with self.assertRaises(click.ClickException) as cm:
                        _parse_agent_config_file(str(cfg))

                self.assertIn("max_concurrency", str(cm.exception))
                self.assertIn(expected, str(cm.exception))

    def test_parse_agent_config_rejects_invalid_fallbacks(self):
        with TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text("node:\n  plan_by_spec:\n    runtime: codex\n    fallbacks: codex\n")

            with self.assertRaises(click.ClickException) as cm:
                _parse_agent_config_file(str(cfg))

        self.assertIn("invalid fallbacks", str(cm.exception))
        self.assertIn("expected list", str(cm.exception))

    def test_parse_agent_config_rejects_unsupported_runtime_for_native_subagent_node(self):
        with TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text(
                "node:\n"
                "  summary:\n"
                "    runtime: kimi\n"
            )

            with self.assertRaises(click.ClickException) as cm:
                _parse_agent_config_file(str(cfg))

        self.assertIn("node 'summary' requires a harness with native subagent support", str(cm.exception))
        self.assertIn("unsupported runtime(s): kimi", str(cm.exception))

    def test_parse_agent_config_rejects_unsupported_fallback_for_native_subagent_node(self):
        with TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text(
                "node:\n"
                "  critic_subtask:\n"
                "    runtime: codex\n"
                "    fallbacks:\n"
                "      - runtime: opencode\n"
            )

            with self.assertRaises(click.ClickException) as cm:
                _parse_agent_config_file(str(cfg))

        self.assertIn("node 'critic_subtask' requires a harness with native subagent support", str(cm.exception))
        self.assertIn("unsupported runtime(s): opencode", str(cm.exception))

    def test_parse_agent_config_accepts_legacy_investigate_node_alias(self):
        with TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text(
                "node:\n"
                "  investigate_subagent:\n"
                "    runtime: codex_cli\n"
                "    fallbacks:\n"
                "      - runtime: claude_code\n"
            )
            parsed = _parse_agent_config_file(str(cfg))

        self.assertNotIn("investigate_subagent", parsed)
        self.assertEqual(parsed["investigate_subtask"]["runtime"], "codex")
        self.assertEqual(
            parsed["investigate_subtask"]["fallbacks"],
            [{"runtime": "claude_code"}],
        )

    def test_parse_agent_config_accepts_legacy_critic_one_alias(self):
        with TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text(
                "node:\n"
                "  critic_one:\n"
                "    runtime: codex_cli\n"
            )
            parsed = _parse_agent_config_file(str(cfg))

        self.assertNotIn("critic_one", parsed)
        self.assertEqual(parsed["critic_subtask"]["runtime"], "codex")

    def test_agent_config_common_focus_is_used_when_cli_focus_is_empty(self):
        runner = CliRunner()

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with TemporaryDirectory() as tmp:
            final = {"summary": "done", "task_id": "workspace_for_libfoo__task-1", "workspace_root": tmp}
            final_state_path = Path(tmp) / final["task_id"] / "final_state.json"
            final_state_path.parent.mkdir(parents=True)
            cfg = Path(tmp) / "agents.yaml"
            cfg.write_text(
                "common_focus:\n"
                "  focus: guest controls VM inputs and targets host isolation\n"
                "node:\n"
                "  summary:\n"
                "    runtime: codex\n"
                "    config: doubao\n"
                "    provider: ark\n"
            )
            with patch("zeromdash.cli.check_agent_health", side_effect=fake_health), patch(
                "zeromdash.cli.run", return_value=final
            ) as run:
                result = runner.invoke(
                    main,
                    ["--target", "libfoo", "--agent-config", str(cfg)],
                )
            final_state_exists = final_state_path.exists()

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertTrue(final_state_exists)
        self.assertEqual(
            run.call_args.kwargs["common_focus"],
            "guest controls VM inputs and targets host isolation",
        )
        self.assertEqual(
            run.call_args.kwargs["agent_configs"],
            {"summary": {"runtime": "codex", "provider": "ark", "config": "doubao"}},
        )
        self.assertEqual(run.call_args.kwargs["max_concurrency"], 8)

    def test_startup_backend_resolution_does_not_auto_fallback_and_accepts_human_override(self):
        calls = []

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, env
            calls.append((agent.name, tuple(extra_args or ())))
            if agent.name == "codex" and tuple(extra_args or ()) == ("--profile", "bad"):
                return AgentHealth(name="codex", ok=False, binary="codex", message="bad codex")
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        agent_configs = {
            "analyze_attack_surface": {
                "runtime": "codex",
                "config": "bad",
                "provider": "ark",
                "fallbacks": [{"runtime": "opencode"}],
            }
        }
        with patch("zeromdash.cli.check_agent_health", side_effect=fake_health), patch(
            "zeromdash.cli.click.prompt",
            side_effect=["claude_code", "/tmp/settings.json", "anthropic", ""],
        ):
            selected, _ = _resolve_startup_backends({}, agent_configs)

        self.assertEqual(selected["analyze_attack_surface"], "claude_code")
        self.assertIn(("codex", ("--profile", "bad")), calls)
        self.assertIn(("claude_code", ("--settings", "/tmp/settings.json")), calls)
        self.assertEqual(
            agent_configs["analyze_attack_surface"],
            {"runtime": "claude_code", "config": "/tmp/settings.json", "provider": "anthropic"},
        )
        self.assertNotIn("fallbacks", agent_configs["analyze_attack_surface"])

    def test_startup_backend_resolution_checks_node_config_extra_args(self):
        calls = []

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout
            calls.append((agent.name, tuple(extra_args or ()), env or {}))
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok", extra_args=list(extra_args or []))

        with patch.dict(os.environ, {"AWS_BEARER_TOKEN_BEDROCK": "token-1"}, clear=True), patch(
            "zeromdash.cli.check_agent_health", side_effect=fake_health
        ):
            selected, cache = _resolve_startup_backends(
                {},
                {
                    "search_spec": {
                        "runtime": "claude_code",
                        "provider": "bedrock",
                        "config": "/tmp/bedrock-settings.json",
                        "model": "claude-sonnet-test",
                    },
                    "plan_by_spec": {
                        "runtime": "codex",
                        "provider": "ark",
                        "config": "doubao",
                        "model": "gpt-test",
                    },
                    "critic_subtask": {
                        "runtime": "codex",
                    },
                    "summary": {
                        "runtime": "traex",
                        "config": "work",
                        "model": "gpt-traex",
                    },
                },
            )

        self.assertEqual(selected["search_spec"], "claude_code")
        self.assertEqual(selected["plan_by_spec"], "codex")
        self.assertEqual(selected["critic_subtask"], "codex")
        self.assertEqual(selected["summary"], "traex")
        claude_call = next(
            env
            for name, args, env in calls
            if name == "claude_code"
            and args == ("--settings", "/tmp/bedrock-settings.json", "--model", "claude-sonnet-test")
        )
        self.assertEqual(claude_call["CLAUDE_CODE_USE_BEDROCK"], "1")
        self.assertEqual(claude_call["AWS_BEARER_TOKEN_BEDROCK"], "token-1")
        self.assertEqual(claude_call["ZEROMDASH_CLAUDE_SETTINGS_PATH"], "/tmp/bedrock-settings.json")
        self.assertIsNone(claude_call["ZEROMDASH_CLAUDE_MODEL"])
        self.assertIsNone(claude_call["ANTHROPIC_MODEL"])
        self.assertIsNone(claude_call["ANTHROPIC_BASE_URL"])
        self.assertIn(("codex", ("--profile", "doubao", "--model", "gpt-test"), {"ZEROMDASH_CODEX_MODEL": None}), calls)
        self.assertIn(("codex", ("--enable", "multi_agent"), {}), calls)
        self.assertIn(
            (
                "traex",
                ("--config", "features.multi_agent_v2.enabled=true", "--profile", "work", "--model", "gpt-traex"),
                {"ZEROMDASH_TRAEX_MODEL": None},
            ),
            calls,
        )
        claude_cache_key = next(
            key
            for key in cache
            if key[0] == "claude_code"
            and key[1] == ("--settings", "/tmp/bedrock-settings.json", "--model", "claude-sonnet-test")
        )
        self.assertIn(("AWS_BEARER_TOKEN_BEDROCK", "<redacted>"), claude_cache_key[2])
        self.assertIn(("CLAUDE_CODE_USE_BEDROCK", "1"), claude_cache_key[2])
        self.assertIn(("ZEROMDASH_CLAUDE_MODEL", None), claude_cache_key[2])
        self.assertIn(("ANTHROPIC_MODEL", None), claude_cache_key[2])
        self.assertIn(
            ("codex", ("--profile", "doubao", "--model", "gpt-test"), (("ZEROMDASH_CODEX_MODEL", None),)),
            cache,
        )
        self.assertIn(
            (
                "traex",
                ("--config", "features.multi_agent_v2.enabled=true", "--profile", "work", "--model", "gpt-traex"),
                (("ZEROMDASH_TRAEX_MODEL", None),),
            ),
            cache,
        )

    def test_startup_backend_resolution_checks_fallback_configs(self):
        calls = []

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout
            calls.append((agent.name, tuple(extra_args or ()), env or {}))
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        with patch("zeromdash.cli.check_agent_health", side_effect=fake_health):
            selected, _ = _resolve_startup_backends(
                {},
                {
                    "plan_by_spec": {
                        "runtime": "codex",
                        "config": "primary",
                        "fallbacks": [
                            {
                                "runtime": "claude_code",
                                "config": "/tmp/fallback-settings.json",
                                "model": "claude-fallback",
                                "provider": "ark",
                            }
                        ],
                    }
                },
            )

        self.assertEqual(selected["plan_by_spec"], "codex")
        self.assertIn(("codex", ("--profile", "primary"), {}), calls)
        self.assertIn(
            ("claude_code", ("--settings", "/tmp/fallback-settings.json", "--model", "claude-fallback"), {
                "CLAUDE_CODE_USE_BEDROCK": None,
                "AWS_BEARER_TOKEN_BEDROCK": None,
                "ZEROMDASH_CLAUDE_MODEL": None,
            }),
            calls,
        )

    def test_bedrock_agent_config_requires_exported_token_and_pauses_for_override(self):
        calls = []

        def fake_health(agent, timeout=60, extra_args=None, env=None):
            del timeout, extra_args, env
            calls.append(agent.name)
            return AgentHealth(name=agent.name, ok=True, binary=agent.name, message="ok")

        agent_configs = {
            "search_spec": {
                "runtime": "claude_code",
                "provider": "bedrock",
                "config": "/tmp/bedrock-settings.json",
            }
        }
        with patch.dict(os.environ, {}, clear=True), patch(
            "zeromdash.cli.check_agent_health", side_effect=fake_health
        ), patch(
            "zeromdash.cli.click.prompt",
            side_effect=["opencode", "", "", ""],
        ):
            selected, cache = _resolve_startup_backends({}, agent_configs)

        self.assertEqual(selected["search_spec"], "opencode")
        self.assertIn("opencode", calls)
        health = next(
            value
            for key, value in cache.items()
            if key[0] == "claude_code" and key[1] == ("--settings", "/tmp/bedrock-settings.json")
        )
        self.assertFalse(health.ok)
        self.assertIn("AWS_BEARER_TOKEN_BEDROCK", health.message)
        self.assertIn("export AWS_BEARER_TOKEN_BEDROCK", health.stderr)


if __name__ == "__main__":
    unittest.main()
