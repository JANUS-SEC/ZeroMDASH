"""Unit tests for external agent health checks."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import types
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import yaml

from zeromdash.agents import (
    AgentHealth,
    AgentResult,
    CodexAgent,
    DeepAgent,
    DeepSeekHarnessAgent,
    KimiAgent,
    OpenCodeAgent,
    TraeXAgent,
    _HEALTHCHECK_TOKEN,
    _exec,
    _extract_resume_id,
    _traex_supports_native_output_schema,
    check_agent_health,
    check_required_agents,
    get_agent,
    langfuse_config,
    langfuse_is_configured,
    normalize_agent_name,
    supports_native_subagents,
)


class _FakeAgent:
    name = "fake"
    binary = "fake-bin"

    def __init__(self, *, available: bool = True, result: AgentResult | None = None, raises=None) -> None:
        self._available = available
        self._result = result or AgentResult(
            stdout=_HEALTHCHECK_TOKEN,
            stderr="",
            returncode=0,
            backend=self.name,
        )
        self._raises = raises
        self.prompts: list[str] = []
        self.timeouts: list[int | None] = []
        self.cwd = None
        self.extra_args = None
        self.env = None

    def available(self) -> bool:
        return self._available

    def run(self, prompt, cwd=None, timeout=None, extra_args=None, env=None):
        self.extra_args = extra_args
        self.env = env
        self.prompts.append(prompt)
        self.timeouts.append(timeout)
        self.cwd = cwd
        if self._raises:
            raise self._raises
        return self._result


class AgentHealthCheckTest(unittest.TestCase):
    def test_missing_binary_fails_without_running_agent(self):
        agent = _FakeAgent(available=False)

        health = check_agent_health(agent, timeout=7)

        self.assertFalse(health.ok)
        self.assertIn("binary not found", health.message)
        self.assertEqual(agent.prompts, [])

    def test_headless_response_with_expected_token_passes(self):
        agent = _FakeAgent(result=AgentResult(stdout=f"{_HEALTHCHECK_TOKEN}\n", stderr="", returncode=0, backend="fake"))

        health = check_agent_health(agent, timeout=7)

        self.assertTrue(health.ok)
        self.assertEqual(health.returncode, 0)
        self.assertEqual(agent.timeouts, [7])
        self.assertIn("zeromdash-agent-health-", agent.cwd)
        self.assertIn(_HEALTHCHECK_TOKEN, agent.prompts[0])

    def test_health_check_passes_extra_args_and_env_to_agent(self):
        agent = _FakeAgent(
            result=AgentResult(
                stdout=f"{_HEALTHCHECK_TOKEN}\n",
                stderr="",
                returncode=0,
                backend="fake",
                metadata={"command": ["fake", "--settings", "/tmp/settings.json"]},
            )
        )

        health = check_agent_health(
            agent,
            timeout=7,
            extra_args=["--settings", "/tmp/settings.json"],
            env={"CLAUDE_CODE_USE_BEDROCK": "1"},
        )

        self.assertTrue(health.ok)
        self.assertEqual(agent.extra_args, ["--settings", "/tmp/settings.json"])
        self.assertEqual(agent.env, {"CLAUDE_CODE_USE_BEDROCK": "1"})
        self.assertEqual(health.command, ["fake", "--settings", "/tmp/settings.json"])
        self.assertEqual(health.env_overlay, {"CLAUDE_CODE_USE_BEDROCK": "1"})

    def test_exec_env_can_override_and_delete_parent_env(self):
        captured = {}

        def fake_run(*args, **kwargs):
            del args
            captured["env"] = kwargs["env"]
            return subprocess.CompletedProcess(kwargs.get("cmd", ["fake"]), 0, stdout="ok", stderr="")

        with patch.dict(
            os.environ,
            {
                "AWS_BEARER_TOKEN_BEDROCK": "parent-token",
                "CLAUDE_CODE_USE_BEDROCK": "1",
                "KEEP_ME": "yes",
            },
            clear=True,
        ), patch("zeromdash.agents.subprocess.run", side_effect=fake_run):
            _exec(
                ["fake"],
                "",
                None,
                None,
                "fake",
                {"AWS_BEARER_TOKEN_BEDROCK": None, "CLAUDE_CODE_USE_BEDROCK": None},
                pipe_stdin=False,
            )

        self.assertNotIn("AWS_BEARER_TOKEN_BEDROCK", captured["env"])
        self.assertNotIn("CLAUDE_CODE_USE_BEDROCK", captured["env"])
        self.assertEqual(captured["env"]["KEEP_ME"], "yes")

    def test_nonzero_returncode_fails_with_stderr(self):
        agent = _FakeAgent(result=AgentResult(stdout="", stderr="auth failed", returncode=2, backend="fake"))

        health = check_agent_health(agent)

        self.assertFalse(health.ok)
        self.assertEqual(health.returncode, 2)
        self.assertEqual(health.stderr, "auth failed")
        self.assertIn("rc=2", health.message)

    def test_missing_expected_token_fails(self):
        agent = _FakeAgent(result=AgentResult(stdout="hello", stderr="", returncode=0, backend="fake"))

        health = check_agent_health(agent)

        self.assertFalse(health.ok)
        self.assertIn("expected token", health.message)

    def test_timeout_fails(self):
        agent = _FakeAgent(raises=subprocess.TimeoutExpired(cmd=["fake"], timeout=3, output="partial", stderr="slow"))

        health = check_agent_health(agent, timeout=3)

        self.assertFalse(health.ok)
        self.assertIn("timed out", health.message)
        self.assertEqual(health.stdout, "partial")
        self.assertEqual(health.stderr, "slow")

    def test_check_required_agents_checks_codex_and_claude(self):
        with patch("zeromdash.agents.CodexAgent", return_value="codex-agent"), patch(
            "zeromdash.agents.ClaudeCodeAgent", return_value="claude-agent"
        ), patch("zeromdash.agents.check_agent_health") as check:
            check.side_effect = [
                AgentHealth(name="codex", ok=True, message="ok"),
                AgentHealth(name="claude_code", ok=True, message="ok"),
            ]

            results = check_required_agents(timeout=9)

        self.assertEqual([r.name for r in results], ["codex", "claude_code"])
        self.assertEqual(check.call_args_list[0].args, ("codex-agent",))
        self.assertEqual(check.call_args_list[0].kwargs, {"timeout": 9})
        self.assertEqual(check.call_args_list[1].args, ("claude-agent",))
        self.assertEqual(check.call_args_list[1].kwargs, {"timeout": 9})


class LangfuseConfigTest(unittest.TestCase):
    def test_langfuse_config_empty_when_unconfigured(self):
        with patch.dict("os.environ", {}, clear=True):
            self.assertFalse(langfuse_is_configured())
            self.assertEqual(langfuse_config(), {})

    def test_langfuse_config_requires_public_and_secret_key(self):
        with patch.dict("os.environ", {"LANGFUSE_PUBLIC_KEY": "pk"}, clear=True):
            self.assertFalse(langfuse_is_configured())
            with self.assertRaisesRegex(RuntimeError, "LANGFUSE_SECRET_KEY"):
                langfuse_config()

    def test_langfuse_config_builds_callback_config_when_configured(self):
        class FakeCallbackHandler:
            pass

        langfuse_pkg = types.ModuleType("langfuse")
        langchain_mod = types.ModuleType("langfuse.langchain")
        langchain_mod.CallbackHandler = FakeCallbackHandler

        with patch.dict(
            "os.environ",
            {"LANGFUSE_PUBLIC_KEY": "pk", "LANGFUSE_SECRET_KEY": "sk"},
            clear=True,
        ), patch.dict(sys.modules, {"langfuse": langfuse_pkg, "langfuse.langchain": langchain_mod}):
            self.assertTrue(langfuse_is_configured())
            cfg = langfuse_config(run_name="run", metadata={"a": 1})

        self.assertIsInstance(cfg["callbacks"][0], FakeCallbackHandler)
        self.assertEqual(cfg["run_name"], "run")
        self.assertEqual(cfg["metadata"], {"a": 1})


class CodexAgentCommandTest(unittest.TestCase):
    def test_codex_exec_uses_current_cli_options_without_quiet(self):
        agent = CodexAgent(binary="codex-test")

        with patch.object(agent, "available", return_value=True), patch("zeromdash.agents._exec") as exec_:
            exec_.return_value = AgentResult(stdout="ok", stderr="", returncode=0, backend="codex")
            agent.run("hello", cwd="/tmp/zeromdash-sub-ws", timeout=5)

        cmd = exec_.call_args.args[0]
        self.assertEqual(cmd[:2], ["codex-test", "exec"])
        self.assertIn("--color", cmd)
        self.assertIn("never", cmd)
        self.assertIn("--skip-git-repo-check", cmd)
        self.assertIn("-C", cmd)
        self.assertIn("/tmp/zeromdash-sub-ws", cmd)
        self.assertNotIn("--quiet", cmd)
        self.assertEqual(cmd[-1], "-")

    def test_extracts_resume_id_from_cli_output(self):
        self.assertEqual(_extract_resume_id('session_id: abc-123', ""), "abc-123")
        self.assertEqual(_extract_resume_id('', '{"conversation_id":"conv-456"}'), "conv-456")

    def test_does_not_extract_resume_id_from_agent_prose(self):
        for prose in (
            "Now let me continue verification with independent reading paths.",
            "The iterator can continue searching forward safely.",
            "I will continue analyzing the remaining callers.",
            "Let's continue examining. Check the teardown path.",
        ):
            self.assertIsNone(_extract_resume_id(prose, ""), prose)


class TraeXAgentCommandTest(unittest.TestCase):
    def test_traex_exec_uses_workspace_schema_and_last_message_file(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        workspace = Path(tmp.name) / "workspace_for_libfoo"
        sub_ws = workspace / "sub_workspace" / "node_plan_by_spec"
        sub_ws.mkdir(parents=True)
        schema = sub_ws / "output.schema.json"
        schema.write_text('{"type":"object"}')
        captured_output_path = None

        def fake_exec(cmd, prompt, cwd, timeout, backend, env, pipe_stdin):
            nonlocal captured_output_path
            del timeout, env
            captured_output_path = Path(cmd[cmd.index("--output-last-message") + 1])
            captured_output_path.write_text('[{"id":"spec-001"}]')
            self.assertEqual(prompt, "hello")
            self.assertEqual(Path(cwd), sub_ws.resolve())
            self.assertEqual(backend, "traex")
            self.assertTrue(pipe_stdin)
            return AgentResult(
                stdout="event stream",
                stderr="",
                returncode=0,
                backend="traex",
                cwd=str(cwd),
                metadata={"command": cmd},
            )

        agent = TraeXAgent(binary="traecli-test")
        with patch.object(agent, "available", return_value=True), patch(
            "zeromdash.agents._exec",
            side_effect=fake_exec,
        ):
            result = agent.run("hello", cwd=sub_ws, timeout=5)

        cmd = result.metadata["command"]
        self.assertEqual(cmd[:2], ["traecli-test", "exec"])
        self.assertIn("--skip-git-repo-check", cmd)
        self.assertEqual(cmd[cmd.index("--sandbox") + 1], "workspace-write")
        self.assertNotIn("--permission-mode", cmd)
        self.assertIn("--ephemeral", cmd)
        config_overrides = [
            cmd[index + 1]
            for index, value in enumerate(cmd)
            if value == "-c"
        ]
        self.assertIn("project_root_markers=[]", config_overrides)
        self.assertIn("project_doc_max_bytes=65536", config_overrides)
        self.assertEqual(Path(cmd[cmd.index("-C") + 1]), sub_ws.resolve())
        self.assertEqual(Path(cmd[cmd.index("--add-dir") + 1]), workspace.resolve())
        self.assertEqual(Path(cmd[cmd.index("--output-schema") + 1]), schema.resolve())
        self.assertEqual(cmd[-1], "-")
        self.assertEqual(result.stdout, '[{"id":"spec-001"}]')
        self.assertTrue(result.metadata["last_message_captured"])
        self.assertIsNotNone(captured_output_path)
        self.assertFalse(captured_output_path.exists())

    def test_traex_skips_native_output_schema_for_top_level_array(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        sub_ws = Path(tmp.name) / "sub_workspace" / "node_plan_by_spec"
        sub_ws.mkdir(parents=True)
        schema = sub_ws / "output.schema.json"
        schema.write_text('{"type":"array","items":{"type":"object"}}')

        agent = TraeXAgent(binary="traecli-test")
        with patch.object(agent, "available", return_value=True), patch(
            "zeromdash.agents._exec"
        ) as exec_:
            exec_.return_value = AgentResult(
                stdout='[{"id":"spec-001"}]',
                stderr="",
                returncode=0,
                backend="traex",
            )
            agent.run("hello", cwd=sub_ws)

        self.assertNotIn("--output-schema", exec_.call_args.args[0])
        self.assertFalse(_traex_supports_native_output_schema(schema))

    def test_traex_env_overlay_can_clear_constructor_model(self):
        agent = TraeXAgent(binary="traecli-test", model="gpt-test")

        with patch.object(agent, "available", return_value=True), patch(
            "zeromdash.agents._exec"
        ) as exec_:
            exec_.return_value = AgentResult(
                stdout="ok",
                stderr="",
                returncode=0,
                backend="traex",
            )
            agent.run(
                "hello",
                cwd="/tmp/zeromdash-sub-ws",
                env={"ZEROMDASH_TRAEX_MODEL": None},
            )

        cmd = exec_.call_args.args[0]
        self.assertNotIn("--model", cmd)
        self.assertNotIn("gpt-test", cmd)


class ClaudeAgentCommandTest(unittest.TestCase):
    def test_claude_uses_json_output_and_exposes_session_id(self):
        from zeromdash.agents import ClaudeCodeAgent

        agent = ClaudeCodeAgent(binary="claude-test")

        payload = '{"type":"result","session_id":"sess-123","result":"ok"}'
        with patch.object(agent, "available", return_value=True), patch("zeromdash.agents._exec") as exec_:
            exec_.return_value = AgentResult(stdout=payload, stderr="", returncode=0, backend="claude_code")
            res = agent.run("hello", cwd="/tmp/zeromdash-sub-ws", timeout=5)

        cmd = exec_.call_args.args[0]
        self.assertIn("--output-format", cmd)
        self.assertIn("json", cmd)
        self.assertNotIn("--settings", cmd)
        self.assertEqual(exec_.call_args.args[1], "hello")
        self.assertTrue(exec_.call_args.kwargs["pipe_stdin"])
        self.assertEqual(res.stdout, "ok")
        self.assertEqual(res.metadata["session_id"], "sess-123")
        self.assertEqual(res.metadata["resume_id"], "sess-123")

    def test_claude_env_overlay_can_clear_constructor_model(self):
        from zeromdash.agents import ClaudeCodeAgent

        agent = ClaudeCodeAgent(binary="claude-test", model="glm-5.2")

        payload = '{"type":"result","session_id":"sess-123","result":"ok"}'
        with patch.object(agent, "available", return_value=True), patch("zeromdash.agents._exec") as exec_:
            exec_.return_value = AgentResult(stdout=payload, stderr="", returncode=0, backend="claude_code")
            agent.run("hello", cwd="/tmp/zeromdash-sub-ws", env={"ZEROMDASH_CLAUDE_MODEL": None})

        cmd = exec_.call_args.args[0]
        self.assertNotIn("--model", cmd)
        self.assertNotIn("glm-5.2", cmd)

    def test_claude_does_not_put_large_prompt_in_argv(self):
        from zeromdash.agents import ClaudeCodeAgent

        agent = ClaudeCodeAgent(binary="claude-test")
        prompt = "x" * 500_000
        payload = '{"type":"result","session_id":"sess-123","result":"ok"}'

        with patch.object(agent, "available", return_value=True), patch("zeromdash.agents._exec") as exec_:
            exec_.return_value = AgentResult(stdout=payload, stderr="", returncode=0, backend="claude_code")
            agent.run(prompt, cwd="/tmp/zeromdash-sub-ws")

        cmd = exec_.call_args.args[0]
        self.assertNotIn(prompt, cmd)
        self.assertEqual(exec_.call_args.args[1], prompt)
        self.assertTrue(exec_.call_args.kwargs["pipe_stdin"])

    def test_claude_bedrock_settings_path_isolates_config_dir(self):
        from zeromdash.agents import ClaudeCodeAgent

        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        settings = os.path.join(tmp.name, "settings.bedrock.json")
        with open(settings, "w") as fp:
            fp.write('{"model":"bedrock-model"}')

        agent = ClaudeCodeAgent(binary="claude-test")
        payload = '{"type":"result","session_id":"sess-123","result":"ok"}'
        with patch.object(agent, "available", return_value=True), patch("zeromdash.agents._exec") as exec_:
            exec_.return_value = AgentResult(stdout=payload, stderr="", returncode=0, backend="claude_code")
            agent.run(
                "hello",
                cwd=tmp.name,
                env={"ZEROMDASH_CLAUDE_SETTINGS_PATH": settings, "ANTHROPIC_MODEL": None},
            )

        env = exec_.call_args.args[5]
        config_dir = env["CLAUDE_CONFIG_DIR"]
        self.assertNotIn("ZEROMDASH_CLAUDE_SETTINGS_PATH", env)
        self.assertEqual(env["ANTHROPIC_MODEL"], None)
        self.assertTrue(config_dir.startswith(tmp.name))
        with open(os.path.join(config_dir, "settings.json")) as fp:
            self.assertEqual(fp.read(), '{"model":"bedrock-model"}')


class AgentRegistryTest(unittest.TestCase):
    def test_normalizes_agent_aliases(self):
        self.assertEqual(normalize_agent_name("claude-code"), "claude_code")
        self.assertEqual(normalize_agent_name("openai-codex"), "codex")
        self.assertEqual(normalize_agent_name("trae-cli"), "traex")
        self.assertEqual(normalize_agent_name("traecode"), "traex")
        self.assertEqual(normalize_agent_name("kimi-code"), "kimi")
        self.assertEqual(normalize_agent_name("deepseek-harness"), "dsh")
        self.assertEqual(normalize_agent_name("deep-agent"), "deepagent")

    def test_get_agent_supports_fallback_backends(self):
        self.assertIsInstance(get_agent("traex"), TraeXAgent)
        self.assertIsInstance(get_agent("traecli"), TraeXAgent)
        self.assertIsInstance(get_agent("kimi"), KimiAgent)
        self.assertIsInstance(get_agent("opencode"), OpenCodeAgent)
        self.assertIsInstance(get_agent("dsh"), DeepSeekHarnessAgent)
        self.assertIsInstance(get_agent("deepseek_harness_cli"), DeepSeekHarnessAgent)
        self.assertIsInstance(get_agent("deepagent"), DeepAgent)

    def test_native_subagent_capability_is_fail_closed(self):
        for runtime in ("codex", "codex_cli", "traex", "trae-cli", "claude_code", "dsh"):
            self.assertTrue(supports_native_subagents(runtime), runtime)
        for runtime in ("kimi", "opencode", "deepagent", "unknown"):
            self.assertFalse(supports_native_subagents(runtime), runtime)


class DeepSeekHarnessAgentCommandTest(unittest.TestCase):
    def test_dsh_materializes_invocation_local_files_and_keeps_prompt_out_of_argv(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        workspace = os.path.join(tmp.name, "workspace_for_libfoo")
        sub_ws = os.path.join(
            workspace,
            "sub_workspace",
            "node_investigate_subtask",
            "subtask_vuln-001",
        )
        os.makedirs(os.path.join(sub_ws, ".dsh"))
        with open(os.path.join(sub_ws, ".dsh", "AGENTS.md"), "w") as fp:
            fp.write("DSH invocation instructions")
        extra_patch = os.path.join(tmp.name, "extra.patch.yml")
        with open(extra_patch, "w") as fp:
            fp.write("[]\n")
        prompt = "x" * 1_100_000
        agent = DeepSeekHarnessAgent(binary="dsh-test")

        with patch.object(agent, "available", return_value=True), patch(
            "zeromdash.agents._exec"
        ) as exec_:
            exec_.return_value = AgentResult(
                stdout="ok",
                stderr="",
                returncode=0,
                backend="dsh",
            )
            result = agent.run(
                prompt,
                cwd=sub_ws,
                timeout=5,
                extra_args=["--patch", extra_patch],
                env={
                    "ZEROMDASH_DSH_PROVIDER": "deepseek-official",
                    "ZEROMDASH_DSH_MODEL": "deepseek-v4-pro",
                    "ZEROMDASH_DSH_REASONING_EFFORT": "max",
                },
            )

        cmd = exec_.call_args.args[0]
        self.assertEqual(cmd[:3], ["dsh-test", "--profile", "headless"])
        self.assertEqual(cmd[-1], "zeromdash-task-from-file")
        self.assertNotIn(prompt, cmd)
        self.assertIn(extra_patch, cmd)
        self.assertEqual(
            Path(exec_.call_args.args[2]),
            Path(workspace).resolve(),
        )
        self.assertFalse(exec_.call_args.kwargs["pipe_stdin"])
        child_env = exec_.call_args.args[5]
        self.assertEqual(child_env["ZEROMDASH_DSH_DEFAULT_PROVIDER"], "deepseek-official")
        self.assertEqual(child_env["ZEROMDASH_DSH_DEFAULT_MODEL"], "deepseek-v4-pro")
        self.assertEqual(child_env["ZEROMDASH_DSH_DEFAULT_REASONING_EFFORT"], "max")
        self.assertNotIn("ZEROMDASH_DSH_PROVIDER", child_env)
        self.assertNotIn("ZEROMDASH_DSH_MODEL", child_env)
        self.assertNotIn("ZEROMDASH_DSH_REASONING_EFFORT", child_env)

        local = os.path.join(sub_ws, ".dsh")
        prompt_path = os.path.join(local, "prompt.md")
        settings_path = os.path.join(local, "settings.yaml")
        manifest_path = os.path.join(local, "invocation.json")
        runtime_patch = os.path.join(local, "headless-minimal.patch.yml")
        with open(prompt_path) as fp:
            materialized_prompt = fp.read()
        self.assertIn("DSH invocation instructions", materialized_prompt)
        self.assertIn(prompt, materialized_prompt)
        self.assertNotIn("{main}", materialized_prompt)
        self.assertNotIn("{sub_workspace}", materialized_prompt)
        with open(settings_path) as fp:
            settings = yaml.safe_load(fp)
        self.assertEqual(
            settings["agent-default-model"],
            {
                "provider": "deepseek-official",
                "model": "deepseek-v4-pro",
                "reasoningEffort": "max",
            },
        )
        with open(manifest_path) as fp:
            manifest = json.load(fp)
        self.assertEqual(manifest["mode"], "minimal")
        self.assertEqual(manifest["process_cwd"], os.path.realpath(workspace))
        self.assertEqual(manifest["logical_cwd"], os.path.realpath(sub_ws))
        self.assertEqual(
            manifest["prompt_file"],
            os.path.realpath(prompt_path),
        )
        self.assertEqual(
            manifest["runtime_patch"],
            os.path.realpath(runtime_patch),
        )
        self.assertTrue(os.path.isfile(runtime_patch))
        with open(runtime_patch) as fp:
            runtime_patch_text = fp.read()
        self.assertIn("zeromdash-search-tools", runtime_patch_text)
        self.assertIn("@deepseek-ai/dsh-tool-fs-search", runtime_patch_text)
        self.assertNotIn("domain-adaptive investigation discipline", runtime_patch_text)
        self.assertTrue(os.path.isdir(os.path.join(local, "sessions")))
        self.assertEqual(result.cwd, os.path.realpath(sub_ws))
        self.assertEqual(result.metadata["mode"], "minimal")

    def test_dsh_health_directory_bootstraps_bundled_minimal_patch(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        agent = DeepSeekHarnessAgent(binary="dsh-test")

        with patch.object(agent, "available", return_value=True), patch(
            "zeromdash.agents._exec"
        ) as exec_:
            exec_.return_value = AgentResult(
                stdout="ok",
                stderr="",
                returncode=0,
                backend="dsh",
            )
            agent.run("health", cwd=tmp.name)

        self.assertTrue(
            os.path.isfile(
                os.path.join(tmp.name, ".dsh", "headless-minimal.patch.yml")
            )
        )
        self.assertEqual(
            Path(exec_.call_args.args[2]),
            Path(tmp.name).resolve(),
        )

    def test_dsh_uses_new_persisted_session_id_instead_of_reasoning_text(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        agent = DeepSeekHarnessAgent(binary="dsh-test")
        actual_session_id = "session-b3dd8da6-00c9-4f37-ace1-fcb16243cd1b"

        def fake_exec(*args, **kwargs):
            del kwargs
            child_env = args[5]
            session_dir = (
                Path(child_env["ZEROMDASH_DSH_SESSION_ROOT"])
                / "workspace-key"
                / actual_session_id
            )
            session_dir.mkdir(parents=True)
            (session_dir / "session.v4.jsonl.zstd").write_bytes(b"persisted")
            child_session_dir = (
                Path(child_env["ZEROMDASH_DSH_SESSION_ROOT"])
                / "workspace-key"
                / "643a5f90-af81-404c-88a9-87117879e2ea"
            )
            child_session_dir.mkdir(parents=True)
            (child_session_dir / "session.v4.jsonl.zstd").write_bytes(
                b"persisted child"
            )
            return AgentResult(
                stdout="Now let me continue verification with independent reading paths.",
                stderr="",
                returncode=0,
                backend="dsh",
                metadata={"resume_id": "verification"},
            )

        with patch.object(agent, "available", return_value=True), patch(
            "zeromdash.agents._exec",
            side_effect=fake_exec,
        ):
            result = agent.run("health", cwd=tmp.name)

        self.assertEqual(result.metadata["resume_id"], actual_session_id)

    def test_dsh_leaves_resume_id_unset_without_one_new_session_artifact(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        agent = DeepSeekHarnessAgent(binary="dsh-test")

        with patch.object(agent, "available", return_value=True), patch(
            "zeromdash.agents._exec"
        ) as exec_:
            exec_.return_value = AgentResult(
                stdout="Let's continue examining the teardown path.",
                stderr="",
                returncode=0,
                backend="dsh",
                metadata={"resume_id": "examining"},
            )
            result = agent.run("health", cwd=tmp.name)

        self.assertIsNone(result.metadata["resume_id"])

    def test_dsh_rejects_missing_extra_patch_before_launch(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        agent = DeepSeekHarnessAgent(binary="dsh-test")

        with patch.object(agent, "available", return_value=True), patch(
            "zeromdash.agents._exec"
        ) as exec_:
            result = agent.run(
                "hello",
                cwd=tmp.name,
                extra_args=["--patch", os.path.join(tmp.name, "missing.yml")],
            )

        self.assertFalse(result.ok)
        self.assertIn("extra patch file not found", result.stderr)
        exec_.assert_not_called()

    def test_dsh_timeout_recovers_fresh_nonempty_finding_artifact(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        workspace = Path(tmp.name) / "workspace_for_libfoo"
        sub_ws = (
            workspace
            / "sub_workspace"
            / "node_investigate_subtask"
            / "subtask_vuln-001"
        )
        sub_ws.mkdir(parents=True)
        agent = DeepSeekHarnessAgent(binary="dsh-test")

        def timeout_after_artifact(*args, **kwargs):
            del args, kwargs
            (sub_ws / "finding.json").write_text(
                json.dumps({"title": "fresh finding"}),
                encoding="utf-8",
            )
            raise subprocess.TimeoutExpired(
                cmd=["dsh-test"],
                timeout=5,
                output="partial stdout",
                stderr="partial stderr",
            )

        with patch.object(agent, "available", return_value=True), patch(
            "zeromdash.agents._exec",
            side_effect=timeout_after_artifact,
        ):
            result = agent.run("investigate", cwd=sub_ws, timeout=5)

        self.assertTrue(result.ok)
        self.assertEqual(result.stdout, "")
        self.assertIn("partial stderr", result.stderr)
        self.assertIn("recovering fresh finding.json", result.stderr)
        self.assertTrue(result.metadata["timeout_recovered_from_artifact"])
        self.assertEqual(result.metadata["timeout_seconds"], 5)
        self.assertEqual(
            result.metadata["timeout_artifact_path"],
            str((sub_ws / "finding.json").resolve()),
        )

    def test_dsh_timeout_does_not_recover_stale_finding_artifact(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        sub_ws = Path(tmp.name) / "workspace_for_libfoo"
        sub_ws.mkdir()
        (sub_ws / "finding.json").write_text(
            json.dumps({"title": "stale finding"}),
            encoding="utf-8",
        )
        agent = DeepSeekHarnessAgent(binary="dsh-test")

        with patch.object(agent, "available", return_value=True), patch(
            "zeromdash.agents._exec",
            side_effect=subprocess.TimeoutExpired(
                cmd=["dsh-test"],
                timeout=5,
            ),
        ), self.assertRaises(subprocess.TimeoutExpired):
            agent.run("investigate", cwd=sub_ws, timeout=5)

    def test_dsh_timeout_does_not_recover_invalid_finding_artifact(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        sub_ws = Path(tmp.name) / "workspace_for_libfoo"
        sub_ws.mkdir()
        agent = DeepSeekHarnessAgent(binary="dsh-test")

        def timeout_after_invalid_artifact(*args, **kwargs):
            del args, kwargs
            (sub_ws / "finding.json").write_text("{}", encoding="utf-8")
            raise subprocess.TimeoutExpired(cmd=["dsh-test"], timeout=5)

        with patch.object(agent, "available", return_value=True), patch(
            "zeromdash.agents._exec",
            side_effect=timeout_after_invalid_artifact,
        ), self.assertRaises(subprocess.TimeoutExpired):
            agent.run("investigate", cwd=sub_ws, timeout=5)


class KimiAgentCommandTest(unittest.TestCase):
    def test_kimi_prompt_mode_uses_workspace_config_without_prompt_injection(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        sub_ws = os.path.join(tmp.name, "sub_workspace", "node_summary")
        os.makedirs(sub_ws)

        agent = KimiAgent(binary="kimi-test")

        with patch.object(agent, "available", return_value=True), patch("zeromdash.agents._exec") as exec_:
            exec_.return_value = AgentResult(stdout="ok", stderr="", returncode=0, backend="kimi")
            agent.run("hello", cwd=sub_ws, timeout=5)

        cmd = exec_.call_args.args[0]
        self.assertEqual(cmd[:3], ["kimi-test", "--output-format", "stream-json"])
        self.assertIn("--add-dir", cmd)
        self.assertIn(os.path.realpath(tmp.name), cmd)
        self.assertIn("-p", cmd)
        self.assertEqual(cmd[cmd.index("-p") + 1], "hello")
        self.assertFalse(exec_.call_args.kwargs["pipe_stdin"])

    def test_kimi_env_overlay_can_clear_constructor_model(self):
        agent = KimiAgent(binary="kimi-test", model="moonshot-cn/kimi-k3")

        with patch.object(agent, "available", return_value=True), patch("zeromdash.agents._exec") as exec_:
            exec_.return_value = AgentResult(stdout="ok", stderr="", returncode=0, backend="kimi")
            agent.run("hello", cwd="/tmp/zeromdash-sub-ws", env={"ZEROMDASH_KIMI_MODEL": None})

        cmd = exec_.call_args.args[0]
        self.assertNotIn("--model", cmd)
        self.assertNotIn("moonshot-cn/kimi-k3", cmd)

    def test_kimi_stream_json_output_normalizes_assistant_content(self):
        agent = KimiAgent(binary="kimi-test")
        stream = (
            '{"role":"assistant","content":"ok"}\n'
            '{"role":"meta","type":"session.resume_hint","session_id":"sess-kimi","command":"kimi -r sess-kimi"}\n'
        )

        with patch.object(agent, "available", return_value=True), patch("zeromdash.agents._exec") as exec_:
            exec_.return_value = AgentResult(stdout=stream, stderr="", returncode=0, backend="kimi")
            res = agent.run("hello", cwd="/tmp/zeromdash-sub-ws")

        self.assertEqual(res.stdout, "ok")
        self.assertEqual(res.metadata["session_id"], "sess-kimi")
        self.assertEqual(res.metadata["resume_id"], "sess-kimi")
        self.assertEqual(res.metadata["resume_command"], "kimi -r sess-kimi")


class OpenCodeAgentCommandTest(unittest.TestCase):
    def test_opencode_run_command_uses_headless_run_mode(self):
        agent = OpenCodeAgent(binary="opencode-test", model="provider/model")

        with patch.object(agent, "available", return_value=True), patch("zeromdash.agents._exec") as exec_:
            exec_.return_value = AgentResult(stdout="ok", stderr="", returncode=0, backend="opencode")
            agent.run("hello", cwd="/tmp/zeromdash-sub-ws", timeout=5)

        cmd = exec_.call_args.args[0]
        self.assertEqual(cmd[:4], ["opencode-test", "run", "--format", "default"])
        self.assertIn("--pure", cmd)
        self.assertIn("--dir", cmd)
        self.assertIn("/tmp/zeromdash-sub-ws", cmd)
        self.assertIn("--model", cmd)
        self.assertIn("provider/model", cmd)
        self.assertEqual(cmd[-1], "hello")

    def test_opencode_env_overlay_can_clear_constructor_model(self):
        agent = OpenCodeAgent(binary="opencode-test", model="provider/model")

        with patch.object(agent, "available", return_value=True), patch("zeromdash.agents._exec") as exec_:
            exec_.return_value = AgentResult(stdout="ok", stderr="", returncode=0, backend="opencode")
            agent.run("hello", cwd="/tmp/zeromdash-sub-ws", env={"ZEROMDASH_OPENCODE_MODEL": None})

        cmd = exec_.call_args.args[0]
        self.assertNotIn("--model", cmd)
        self.assertNotIn("provider/model", cmd)


class DeepAgentLibraryTest(unittest.TestCase):
    def test_deepagent_requires_model(self):
        agent = DeepAgent(model="")

        with patch.object(agent, "available", return_value=True):
            res = agent.run("hello", cwd="/tmp/zeromdash-sub-ws")

        self.assertFalse(res.ok)
        self.assertIn("ZEROMDASH_DEEPAGENT_MODEL", res.stderr)

    def test_deepagent_uses_create_deep_agent_library(self):
        calls = {}

        class FakeApp:
            def invoke(self, payload, config=None):
                calls["payload"] = payload
                calls["config"] = config
                return {"messages": [{"role": "assistant", "content": "deep answer"}]}

        def fake_create_deep_agent(**kwargs):
            calls["kwargs"] = kwargs
            return FakeApp()

        fake_module = types.SimpleNamespace(create_deep_agent=fake_create_deep_agent)
        agent = DeepAgent(model="openai:gpt-test")

        with patch.dict("os.environ", {}, clear=True), patch.object(
            agent, "available", return_value=True
        ), patch.dict(sys.modules, {"deepagents": fake_module}):
            res = agent.run("hello", cwd="/tmp/zeromdash-sub-ws")

        self.assertTrue(res.ok)
        self.assertEqual(res.stdout, "deep answer")
        self.assertEqual(calls["kwargs"]["model"], "openai:gpt-test")
        self.assertEqual(calls["kwargs"]["tools"], [])
        self.assertIn("ZeroMDASH", calls["kwargs"]["system_prompt"])
        self.assertEqual(calls["payload"]["messages"][0]["content"], "hello")


if __name__ == "__main__":
    unittest.main()
