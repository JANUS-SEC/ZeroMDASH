"""Adapters that drive external coding-agent runtimes.

All adapters expose the same `run(prompt, cwd, ...)` interface so nodes
in the graph can be agnostic about which backend executes a given step.

How project-level instructions reach the agent
----------------------------------------------
Each node calls ``Workspace.prepare_sub_workspace(node, subtask_id, ...)``
which materializes a per-invocation directory containing only the selected
runtime's project files plus common skills/contracts. The agent is then
invoked with ``cwd=<that sub_workspace>``:

- Claude Code automatically reads ``./CLAUDE.md``, ``./.claude/settings.json``,
  and ``./.claude/settings.local.json`` from its CWD, so per-node Claude
  instructions and sandbox/tool settings just work.
- Codex CLI reads ``./AGENTS.md`` from its working root. We pass ``-C`` to
  set that root explicitly.
- TraeX reads ``./AGENTS.md`` from its working root. We run ``traecli exec``
  with the prompt on stdin and capture its final response via
  ``--output-last-message``.
- Kimi Code reads project instructions from ``./.kimi-code/AGENTS.md`` and
  project-local workspace config from ``./.kimi-code/local.toml``.

Sandbox writability is configured to span the *whole* workspace (not just
the sub_workspace) by the selected runtime's project config.

Defaults can be overridden via env:

    ZEROMDASH_CODEX_BIN          (default: "codex")
    ZEROMDASH_CLAUDE_CODE_BIN    (default: "claude")
    ZEROMDASH_TRAEX_BIN          (default: "traecli", then "traex")
    ZEROMDASH_KIMI_BIN           (default: "kimi" or "~/.kimi-code/bin/kimi")
    ZEROMDASH_OPENCODE_BIN       (default: "opencode")
    ZEROMDASH_DEEPAGENT_MODEL    (required when using deepagent fallback)
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import importlib.util
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import yaml

AgentEnv = dict[str, str | None]

# Native harness-level delegation, not ZeroMDASH's own LangGraph fan-out.
# Native harness-level delegation, not ZeroMDASH's own LangGraph fan-out.
# DSH exposes the bounded tool-subagent path through ZeroMDASH's bundled
# headless-minimal overlay. Kimi, OpenCode, and DeepAgent do not currently have
# a verified native-subagent contract in these adapters, so they remain
# fail-closed.
NATIVE_SUBAGENT_BACKENDS = frozenset({"traex", "codex", "claude_code", "dsh"})


@dataclass
class AgentResult:
    stdout: str
    stderr: str
    returncode: int
    backend: str
    cwd: str | None = None
    metadata: dict | None = None

    @property
    def ok(self) -> bool:
        return self.returncode == 0


@dataclass
class AgentHealth:
    """Startup health status for one external agent backend."""

    name: str
    ok: bool
    message: str
    binary: str | None = None
    returncode: int | None = None
    stdout: str = ""
    stderr: str = ""
    extra_args: list[str] | None = None
    command: list[str] | None = None
    env_overlay: AgentEnv | None = None


def _safe_env_overlay(env: AgentEnv | None) -> AgentEnv:
    safe: AgentEnv = {}
    for key, value in (env or {}).items():
        if key == "AWS_BEARER_TOKEN_BEDROCK" and value is not None:
            safe[key] = "<redacted>"
        else:
            safe[key] = value
    return safe


def _agent_result_command(res: AgentResult) -> list[str] | None:
    command = (res.metadata or {}).get("command")
    return command if isinstance(command, list) else None


class Agent(Protocol):
    name: str

    def run(
        self,
        prompt: str,
        cwd: str | Path | None = None,
        timeout: int | None = None,
        extra_args: list[str] | None = None,
        env: AgentEnv | None = None,
    ) -> AgentResult: ...


# --------------------------------------------------------------------- helpers
def _exec(
    cmd: list[str],
    prompt: str,
    cwd: str | Path | None,
    timeout: int | None,
    backend: str,
    env: AgentEnv | None,
    pipe_stdin: bool,
) -> AgentResult:
    full_env = dict(os.environ)
    for key, value in (env or {}).items():
        if value is None:
            full_env.pop(key, None)
        else:
            full_env[key] = value
    proc = subprocess.run(
        cmd,
        input=prompt if pipe_stdin else None,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        timeout=timeout,
        env=full_env,
        check=False,
    )
    return AgentResult(
        stdout=proc.stdout,
        stderr=proc.stderr,
        returncode=proc.returncode,
        backend=backend,
        cwd=str(cwd) if cwd else None,
        metadata={
            "command": _redact_command(cmd),
            "resume_id": _extract_resume_id(proc.stdout, proc.stderr),
        },
    )


def _redact_command(cmd: list[str]) -> list[str]:
    redacted = list(cmd)
    for i, part in enumerate(redacted):
        if part == "--prompt" and i + 1 < len(redacted):
            redacted[i + 1] = "<prompt>"
        if part == "-p" and i + 1 < len(redacted) and not redacted[i + 1].startswith("-"):
            redacted[i + 1] = "<prompt>"
    return redacted


def _effective_model(default: str | None, env: AgentEnv | None, env_name: str) -> str | None:
    """Allow per-invocation env overlay to override or clear constructor model."""
    if env and env_name in env:
        return env[env_name] or None
    return default


def _workspace_base_from_sub_workspace(cwd: str | Path | None) -> Path | None:
    """Return the ZeroMDASH workspace base when cwd is inside sub_workspace."""
    if not cwd:
        return None
    path = Path(cwd).expanduser().resolve()
    for parent in (path, *path.parents):
        if parent.name == "sub_workspace":
            return parent.parent
    return None


def additional_read_root_args(
    backend: str,
    roots: list[str] | tuple[str, ...] | None,
) -> list[str]:
    """Translate explicit gather read roots into supported CLI arguments.

    Gather normally points these at isolated source snapshots under its own
    workspace. Keeping expansion here makes the permission boundary explicit
    and avoids letting prompts smuggle arbitrary filesystem paths into argv.
    """
    normalized_backend = normalize_agent_name(backend)
    if normalized_backend not in {"claude_code", "codex", "traex", "kimi"}:
        if roots:
            raise ValueError(
                f"runtime {normalized_backend!r} does not support additional read roots"
            )
        return []
    args: list[str] = []
    seen: set[str] = set()
    for raw in roots or []:
        path = str(Path(raw).expanduser().resolve())
        if path in seen:
            continue
        seen.add(path)
        args.extend(["--add-dir", path])
    return args


def _file_snapshot(path: Path) -> tuple[int, int, bytes] | None:
    try:
        stat = path.stat()
        return stat.st_mtime_ns, stat.st_size, path.read_bytes()
    except (FileNotFoundError, OSError):
        return None


def _fresh_nonempty_json_object(
    path: Path,
    before: tuple[int, int, bytes] | None,
) -> bool:
    after = _file_snapshot(path)
    if after is None or after == before or after[1] <= 0:
        return False
    try:
        payload = json.loads(after[2])
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False
    return isinstance(payload, dict) and bool(payload)


def _timeout_text(value: str | bytes | None) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value or ""


def _extract_resume_id(stdout: str, stderr: str) -> str | None:
    text = "\n".join(x for x in (stdout or "", stderr or "") if x)
    patterns = [
        r'"(?:session_id|conversation_id|thread_id|resume_id)"\s*:\s*"([^"\n]+)"',
        r"(?:session|conversation|thread|resume)[ _-]?id\s*[:=]\s*([A-Za-z0-9_.:@/-]+)",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


def _dsh_session_ids(session_root: Path) -> set[str]:
    """Return persisted top-level DSH headless session IDs.

    DSH stores each session under ``<root>/<workspace-key>/<session-id>/``.
    Headless sessions mint ``session-<uuid>`` IDs, while spawned subagents use
    bare UUIDs. The compressed JSONL is the durable marker that the directory
    is a real persisted session rather than an incomplete temporary directory.
    """
    try:
        return {
            artifact.parent.name
            for artifact in session_root.glob("*/*/session.v4.jsonl.zstd")
            if artifact.is_file() and artifact.parent.name.startswith("session-")
        }
    except OSError:
        return set()


def _new_dsh_session_id(session_root: Path, before: set[str]) -> str | None:
    created = _dsh_session_ids(session_root) - before
    if len(created) != 1:
        return None
    return next(iter(created))


def _normalize_claude_json_result(res: AgentResult) -> AgentResult:
    try:
        payload = json.loads(res.stdout)
    except json.JSONDecodeError:
        return res
    if not isinstance(payload, dict):
        return res

    metadata = dict(res.metadata or {})
    for key in ("session_id", "conversation_id", "thread_id"):
        if payload.get(key):
            metadata[key] = payload[key]
            metadata.setdefault("resume_id", payload[key])
            break
    for key in ("cost_usd", "duration_ms", "duration_api_ms", "num_turns", "usage"):
        if key in payload:
            metadata[key] = payload[key]
    result = payload.get("result")
    if isinstance(result, str):
        return AgentResult(
            stdout=result,
            stderr=res.stderr,
            returncode=res.returncode,
            backend=res.backend,
            cwd=res.cwd,
            metadata=metadata,
        )
    res.metadata = metadata
    return res


def _normalize_kimi_stream_result(res: AgentResult) -> AgentResult:
    assistant_parts: list[str] = []
    metadata = dict(res.metadata or {})
    saw_stream_event = False
    for line in (res.stdout or "").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        saw_stream_event = True
        role = event.get("role")
        if role == "assistant" and isinstance(event.get("content"), str):
            assistant_parts.append(event["content"])
        if role == "meta":
            session_id = event.get("session_id")
            if session_id:
                metadata.setdefault("session_id", session_id)
                metadata.setdefault("resume_id", session_id)
            command = event.get("command")
            if command:
                metadata.setdefault("resume_command", command)

    if assistant_parts:
        return AgentResult(
            stdout="".join(assistant_parts),
            stderr=res.stderr,
            returncode=res.returncode,
            backend=res.backend,
            cwd=res.cwd,
            metadata=metadata,
        )
    if saw_stream_event:
        res.metadata = metadata
    return res


def langfuse_is_configured() -> bool:
    """Return True when Langfuse has the minimum credentials to trace runs."""
    return bool(os.environ.get("LANGFUSE_PUBLIC_KEY") and os.environ.get("LANGFUSE_SECRET_KEY"))


def langfuse_config(run_name: str | None = None, metadata: dict | None = None) -> dict:
    """Build a LangChain/LangGraph config carrying Langfuse callbacks.

    If no Langfuse environment variables are set, returns an empty config. If
    only part of the credential pair is set, fail fast with a clear error.
    """
    public = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret = os.environ.get("LANGFUSE_SECRET_KEY")
    if not public and not secret:
        return {}
    if not public or not secret:
        raise RuntimeError("Langfuse requires both LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY")

    from langfuse.langchain import CallbackHandler

    config: dict = {"callbacks": [CallbackHandler()]}
    if run_name:
        config["run_name"] = run_name
    if metadata:
        config["metadata"] = metadata
    return config


# ----------------------------------------------------------------------- Codex
class CodexAgent:
    """Drives the OpenAI Codex CLI in non-interactive mode.

    Reads project-level instructions from `<cwd>/AGENTS.md`.
    """

    name = "codex"

    def __init__(self, binary: str | None = None, model: str | None = None) -> None:
        self.binary = binary or os.environ.get("ZEROMDASH_CODEX_BIN", "codex")
        self.model = model or os.environ.get("ZEROMDASH_CODEX_MODEL")

    def available(self) -> bool:
        return shutil.which(self.binary) is not None

    def run(
        self,
        prompt: str,
        cwd: str | Path | None = None,
        timeout: int | None = None,
        extra_args: list[str] | None = None,
        env: AgentEnv | None = None,
    ) -> AgentResult:
        if not self.available():
            return _dry_run(prompt, cwd, backend=self.name)
        cmd = [self.binary, "exec", "--color", "never", "--skip-git-repo-check"]
        model = _effective_model(self.model, env, "ZEROMDASH_CODEX_MODEL")
        if model:
            cmd += ["--model", model]

        if cwd:
            cmd += ["-C", str(cwd)]

        if extra_args:
            cmd += extra_args
        cmd += ["-"]  # read prompt from stdin
        return _exec(cmd, prompt, cwd, timeout, self.name, env, pipe_stdin=True)


# ----------------------------------------------------------------------- TraeX
class TraeXAgent:
    """Drive TraeX/TraeCode CLI in non-interactive ``exec`` mode.

    TraeX reads project instructions from ``<cwd>/AGENTS.md``. The primary
    sub-workspace stays the working root while ``--add-dir`` makes the complete
    ZeroMDASH task workspace writable. Structured-output nodes additionally
    pass the materialized ``output.schema.json`` to TraeX.
    """

    name = "traex"

    def __init__(self, binary: str | None = None, model: str | None = None) -> None:
        self.binary = (
            binary
            or os.environ.get("ZEROMDASH_TRAEX_BIN", "traex")
            or shutil.which("traecli")
            or shutil.which("traex")
            or "traecli"
        )
        self.model = model or os.environ.get("ZEROMDASH_TRAEX_MODEL")

    def available(self) -> bool:
        return shutil.which(self.binary) is not None

    def run(
        self,
        prompt: str,
        cwd: str | Path | None = None,
        timeout: int | None = None,
        extra_args: list[str] | None = None,
        env: AgentEnv | None = None,
    ) -> AgentResult:
        if not self.available():
            return _dry_run(prompt, cwd, backend=self.name)

        invocation_dir = Path(cwd or os.getcwd()).expanduser().resolve()
        invocation_dir.mkdir(parents=True, exist_ok=True)
        output_fd, output_name = tempfile.mkstemp(
            prefix=".zeromdash-traex-",
            suffix=".last-message",
            dir=invocation_dir,
        )
        os.close(output_fd)
        output_path = Path(output_name)
        output_path.unlink(missing_ok=True)

        cmd = [
            self.binary,
            "exec",
            "--color",
            "never",
            "--skip-git-repo-check",
            "--sandbox",
            "workspace-write",
            "--ephemeral",
            "-c",
            "project_root_markers=[]",
            "-c",
            "project_doc_max_bytes=65536",
            "-C",
            str(invocation_dir),
        ]
        workspace_base = _workspace_base_from_sub_workspace(invocation_dir)
        if workspace_base:
            cmd += ["--add-dir", str(workspace_base)]

        schema_path = invocation_dir / "output.schema.json"
        if _traex_supports_native_output_schema(schema_path):
            cmd += ["--output-schema", str(schema_path)]

        cmd += ["--output-last-message", str(output_path)]
        model = _effective_model(self.model, env, "ZEROMDASH_TRAEX_MODEL")
        if model:
            cmd += ["--model", model]
        if extra_args:
            cmd += extra_args
        cmd += ["-"]

        try:
            res = _exec(
                cmd,
                prompt,
                invocation_dir,
                timeout,
                self.name,
                env,
                pipe_stdin=True,
            )
            try:
                final_message = output_path.read_text(encoding="utf-8")
            except OSError:
                final_message = ""
            if final_message.strip():
                res.stdout = final_message
                metadata = dict(res.metadata or {})
                metadata["last_message_captured"] = True
                res.metadata = metadata
            return res
        finally:
            output_path.unlink(missing_ok=True)


def _traex_supports_native_output_schema(path: Path) -> bool:
    """Return whether TraeX can enforce this schema through its CLI.

    TraeX 0.201.1 exposes structured output as a function tool and rejects
    top-level array schemas. ZeroMDASH planners therefore keep their native
    ``Subtask[]`` response and rely on the orchestrator's existing validator,
    while object-shaped investigation/review contracts use ``--output-schema``.
    """
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return isinstance(schema, dict) and schema.get("type") == "object"


# ----------------------------------------------------------------- Claude Code
class ClaudeCodeAgent:
    """Drives Anthropic's Claude Code CLI in non-interactive (`-p`) mode.

    Reads project-level instructions from `<cwd>/CLAUDE.md` and settings
    from `<cwd>/.claude/settings.json` automatically (Claude Code looks
    these up relative to the CWD).
    """

    name = "claude_code"

    def __init__(self, binary: str | None = None, model: str | None = None) -> None:
        self.binary = binary or os.environ.get("ZEROMDASH_CLAUDE_CODE_BIN", "claude")
        self.model = model or os.environ.get("ZEROMDASH_CLAUDE_MODEL")

    def available(self) -> bool:
        return shutil.which(self.binary) is not None

    def run(
        self,
        prompt: str,
        cwd: str | Path | None = None,
        timeout: int | None = None,
        extra_args: list[str] | None = None,
        env: AgentEnv | None = None,
    ) -> AgentResult:
        if not self.available():
            return _dry_run(prompt, cwd, backend=self.name)
        env = dict(env or {})
        settings_path = env.pop("ZEROMDASH_CLAUDE_SETTINGS_PATH", None)
        if settings_path:
            base = Path(cwd) if cwd else Path(tempfile.mkdtemp(prefix="zeromdash-claude-run-"))
            config_dir = base / ".zeromdash_claude_config"
            config_dir.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(settings_path, config_dir / "settings.json")
            env["CLAUDE_CONFIG_DIR"] = str(config_dir)
        cmd = [self.binary, "-p", "--output-format", "json"]
        model = _effective_model(self.model, env, "ZEROMDASH_CLAUDE_MODEL")
        if model:
            cmd += ["--model", model]

        if extra_args:
            cmd += extra_args
        # Pass the prompt over stdin instead of argv. Summary prompts can include
        # many findings and exceed the OS command-line length limit.
        return _normalize_claude_json_result(_exec(cmd, prompt, cwd, timeout, self.name, env, pipe_stdin=True))


# ------------------------------------------------------------------------- Kimi
class KimiAgent:
    """Drives Kimi Code CLI in non-interactive prompt mode.

    Kimi Code reads its official provider/model configuration from
    ``~/.kimi-code/config.toml`` by default. ZeroMDASH therefore does not map
    ``agent-config``'s ``config`` field to a CLI flag for this runtime.
    """

    name = "kimi"

    def __init__(self, binary: str | None = None, model: str | None = None) -> None:
        self.binary = binary or os.environ.get("ZEROMDASH_KIMI_BIN") or shutil.which("kimi") or str(
            Path.home() / ".kimi-code" / "bin" / "kimi"
        )
        self.model = model or os.environ.get("ZEROMDASH_KIMI_MODEL")

    def available(self) -> bool:
        return shutil.which(self.binary) is not None

    def run(
        self,
        prompt: str,
        cwd: str | Path | None = None,
        timeout: int | None = None,
        extra_args: list[str] | None = None,
        env: AgentEnv | None = None,
    ) -> AgentResult:
        if not self.available():
            return _dry_run(prompt, cwd, backend=self.name)

        cmd = [self.binary, "--output-format", "stream-json"]
        workspace_base = _workspace_base_from_sub_workspace(cwd)
        if workspace_base:
            cmd += ["--add-dir", str(workspace_base)]

        model = _effective_model(self.model, env, "ZEROMDASH_KIMI_MODEL")
        if model:
            cmd += ["--model", model]
        if extra_args:
            cmd += extra_args

        cmd += ["-p", prompt]
        return _normalize_kimi_stream_result(_exec(cmd, "", cwd, timeout, self.name, env, pipe_stdin=False))


# -------------------------------------------------------------------- opencode
class OpenCodeAgent:
    """Drives opencode in headless `run` mode."""

    name = "opencode"

    def __init__(self, binary: str | None = None, model: str | None = None) -> None:
        self.binary = binary or os.environ.get("ZEROMDASH_OPENCODE_BIN", "opencode")
        self.model = model or os.environ.get("ZEROMDASH_OPENCODE_MODEL")

    def available(self) -> bool:
        return shutil.which(self.binary) is not None

    def run(
        self,
        prompt: str,
        cwd: str | Path | None = None,
        timeout: int | None = None,
        extra_args: list[str] | None = None,
        env: AgentEnv | None = None,
    ) -> AgentResult:
        if not self.available():
            return _dry_run(prompt, cwd, backend=self.name)
        cmd = [self.binary, "run", "--format", "default", "--pure"]
        if cwd:
            cmd += ["--dir", str(cwd)]
        model = _effective_model(self.model, env, "ZEROMDASH_OPENCODE_MODEL")
        if model:
            cmd += ["--model", model]
        if extra_args:
            cmd += extra_args
        cmd += [prompt]
        return _exec(cmd, "", cwd, timeout, self.name, env, pipe_stdin=False)


# --------------------------------------------------------- DeepSeek Harness
class DeepSeekHarnessAgent:
    """Drive the DeepSeek Harness one-shot ``headless`` profile.

    DSH accepts its task only as an argv positional and uses the process CWD as
    the session's single workspace-write root. ZeroMDASH therefore materializes
    the complete task under the invocation-local ``.dsh/`` directory and boots
    DSH from the surrounding task workspace using a bundled patch that reads
    the task file. The invocation sub-workspace remains the logical CWD exposed
    to the model.
    """

    name = "dsh"

    def __init__(
        self,
        binary: str | None = None,
        provider: str | None = None,
        model: str | None = None,
    ) -> None:
        self.binary = binary or os.environ.get("ZEROMDASH_DSH_BIN", "dsh")
        self.provider = provider or os.environ.get("ZEROMDASH_DSH_PROVIDER")
        self.model = model or os.environ.get("ZEROMDASH_DSH_MODEL")

    def available(self) -> bool:
        return shutil.which(self.binary) is not None

    def run(
        self,
        prompt: str,
        cwd: str | Path | None = None,
        timeout: int | None = None,
        extra_args: list[str] | None = None,
        env: AgentEnv | None = None,
    ) -> AgentResult:
        if not self.available():
            return _dry_run(prompt, cwd, backend=self.name)

        invocation_dir = Path(cwd or os.getcwd()).expanduser().resolve()
        invocation_dir.mkdir(parents=True, exist_ok=True)
        workspace_base = _workspace_base_from_sub_workspace(invocation_dir)
        process_cwd = workspace_base or invocation_dir
        local_dir = invocation_dir / ".dsh"
        local_dir.mkdir(parents=True, exist_ok=True)

        instructions_path = local_dir / "AGENTS.md"
        instructions = (
            instructions_path.read_text(encoding="utf-8", errors="ignore")
            if instructions_path.is_file()
            else ""
        )
        prompt_path = local_dir / "prompt.md"
        prompt_path.write_text(
            _dsh_invocation_prompt(
                prompt=prompt,
                instructions=instructions,
                invocation_dir=invocation_dir,
                workspace_base=process_cwd,
            ),
            encoding="utf-8",
        )

        settings_path = local_dir / "settings.yaml"
        child_env = dict(env or {})
        dsh_selection = _write_dsh_settings(
            settings_path,
            child_env,
            default_provider=self.provider,
            default_model=self.model,
        )
        session_root = local_dir / "sessions"
        session_root.mkdir(parents=True, exist_ok=True)
        session_ids_before = _dsh_session_ids(session_root)

        patch_path = local_dir / "headless-minimal.patch.yml"
        if not patch_path.is_file():
            bundled_patch = (
                Path(__file__).resolve().parent
                / "presets"
                / ".dsh"
                / "headless-minimal.patch.yml"
            )
            if not bundled_patch.is_file():
                return AgentResult(
                    stdout="",
                    stderr=f"missing bundled DSH runtime patch: {bundled_patch}",
                    returncode=1,
                    backend=self.name,
                    cwd=str(invocation_dir),
                )
            shutil.copyfile(bundled_patch, patch_path)

        cmd = [
            self.binary,
            "--profile",
            "headless",
            "--patch",
            str(patch_path),
        ]
        if extra_args:
            for index, value in enumerate(extra_args):
                if value == "--patch" and index + 1 < len(extra_args):
                    extra_patch = Path(extra_args[index + 1]).expanduser()
                    if not extra_patch.is_file():
                        return AgentResult(
                            stdout="",
                            stderr=f"DSH extra patch file not found: {extra_patch}",
                            returncode=1,
                            backend=self.name,
                            cwd=str(invocation_dir),
                        )
            cmd += extra_args
        cmd += ["zeromdash-task-from-file"]

        child_env.update(
            {
                "ZEROMDASH_DSH_PROMPT_FILE": str(prompt_path),
                "ZEROMDASH_DSH_SETTINGS_FILE": str(settings_path),
                "ZEROMDASH_DSH_SESSION_ROOT": str(session_root),
                "ZEROMDASH_DSH_DEFAULT_PROVIDER": dsh_selection.get("provider"),
                "ZEROMDASH_DSH_DEFAULT_MODEL": dsh_selection.get("model"),
                "ZEROMDASH_DSH_DEFAULT_REASONING_EFFORT": dsh_selection.get(
                    "reasoningEffort"
                ),
            }
        )
        for key in (
            "ZEROMDASH_DSH_PROVIDER",
            "ZEROMDASH_DSH_MODEL",
            "ZEROMDASH_DSH_REASONING_EFFORT",
        ):
            child_env.pop(key, None)

        invocation_manifest = {
            "schema_version": 1,
            "runtime": "dsh",
            "mode": "minimal",
            "process_cwd": str(process_cwd),
            "logical_cwd": str(invocation_dir),
            "prompt_file": str(prompt_path),
            "settings_file": str(settings_path),
            "runtime_patch": str(patch_path),
            "session_root": str(session_root),
            "extra_args": list(extra_args or []),
        }
        (local_dir / "invocation.json").write_text(
            json.dumps(invocation_manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        finding_path = invocation_dir / "finding.json"
        finding_before = _file_snapshot(finding_path)
        try:
            res = _exec(
                cmd,
                "",
                process_cwd,
                timeout,
                self.name,
                child_env,
                pipe_stdin=False,
            )
        except subprocess.TimeoutExpired as exc:
            if not _fresh_nonempty_json_object(finding_path, finding_before):
                raise
            timeout_seconds = exc.timeout
            res = AgentResult(
                stdout="",
                stderr=(
                    _timeout_text(exc.stderr).rstrip()
                    + (
                        "\n" if _timeout_text(exc.stderr).strip() else ""
                    )
                    + f"DSH timed out after {timeout_seconds}s; "
                    "recovering fresh finding.json through structured artifact validation."
                ),
                returncode=0,
                backend=self.name,
                cwd=str(process_cwd),
                metadata={
                    "command": _redact_command(cmd),
                    "resume_id": None,
                    "timeout_recovered_from_artifact": True,
                    "timeout_seconds": timeout_seconds,
                    "timeout_artifact_path": str(finding_path),
                },
            )
        metadata = dict(res.metadata or {})
        # Generic stdout/stderr extraction is intentionally not authoritative
        # for DSH because its reasoning stream can contain prose such as
        # "continue verification". Use the persisted session artifact created
        # by this invocation, or leave the ID unset when it is ambiguous.
        metadata["resume_id"] = _new_dsh_session_id(
            session_root,
            session_ids_before,
        )
        metadata.update(
            {
                "mode": "minimal",
                "process_cwd": str(process_cwd),
                "invocation_dir": str(invocation_dir),
                "prompt_file": str(prompt_path),
                "settings_file": str(settings_path),
                "session_root": str(session_root),
                "invocation_manifest": str(local_dir / "invocation.json"),
            }
        )
        res.cwd = str(invocation_dir)
        res.metadata = metadata
        return res


def _dsh_invocation_prompt(
    *,
    prompt: str,
    instructions: str,
    invocation_dir: Path,
    workspace_base: Path,
) -> str:
    relative_invocation = os.path.relpath(invocation_dir, workspace_base)
    rendered_instructions = instructions
    for placeholder, value in {
        "{workspace_base}": workspace_base,
        "{main}": workspace_base / "main",
        "{similar}": workspace_base / "similar",
        "{log}": workspace_base / "log",
        "{sub_workspace}": invocation_dir,
    }.items():
        rendered_instructions = rendered_instructions.replace(
            placeholder,
            str(value),
        )
    prefix = (
        "# ZeroMDASH DSH invocation\n\n"
        f"- Writable workspace root: `{workspace_base}`\n"
        f"- Logical invocation directory: `{invocation_dir}`\n"
        f"- Invocation path relative to workspace root: `{relative_invocation}`\n\n"
        "Treat the logical invocation directory as your current working "
        "directory for every relative path in the task or instructions. "
        "When using bash, pass that directory as the command workdir or change "
        "to it first. The process starts at the broader workspace root only so "
        "DSH workspace-write confinement covers the complete ZeroMDASH task. "
        "Do not write outside the writable workspace root. Approval prompts are "
        "disabled; never request sandbox escalation.\n"
    )
    if rendered_instructions.strip():
        prefix += (
            "\n# Invocation instructions\n\n"
            + rendered_instructions.strip()
            + "\n"
        )
    return prefix + "\n# Task\n\n" + prompt


def _write_dsh_settings(
    path: Path,
    env: AgentEnv,
    *,
    default_provider: str | None,
    default_model: str | None,
) -> dict[str, str]:
    dsh_home = Path(
        str(env.get("DSH_HOME") or os.environ.get("DSH_HOME") or "~/.dsh")
    ).expanduser()
    source = dsh_home / "settings.yaml"
    source_document: dict = {}
    if source.is_file():
        try:
            parsed = yaml.safe_load(source.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError):
            parsed = {}
        if isinstance(parsed, dict):
            source_document = parsed

    # Keep invocation settings narrowly model-related. In particular, never
    # copy global permissionPresets/sandbox/approval values that could override
    # the bundled workspace-write + no-approval leaf-agent policy.
    document = {
        str(key): value
        for key, value in source_document.items()
        if str(key).startswith("llm-")
    }

    selection = source_document.get("agent-default-model")
    selection = dict(selection) if isinstance(selection, dict) else {}
    provider = (
        env.get("ZEROMDASH_DSH_PROVIDER")
        if "ZEROMDASH_DSH_PROVIDER" in env
        else default_provider
    )
    model = (
        env.get("ZEROMDASH_DSH_MODEL")
        if "ZEROMDASH_DSH_MODEL" in env
        else default_model
    )
    reasoning = env.get("ZEROMDASH_DSH_REASONING_EFFORT")
    if provider:
        selection["provider"] = provider
    if model:
        selection["model"] = model
    if reasoning:
        selection["reasoningEffort"] = reasoning
    if selection:
        selection.setdefault("provider", "deepseek-official")
        selection.setdefault("model", "deepseek-v4-flash")
        document["agent-default-model"] = selection

    path.write_text(
        yaml.safe_dump(document, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return {
        str(key): str(value)
        for key, value in selection.items()
        if key in {"provider", "model", "reasoningEffort"} and value is not None
    }


# ------------------------------------------------------------------- deepagent
class DeepAgent:
    """Adapter for LangChain's `deepagents` Python library.

    This is intentionally not a subprocess backend. It imports
    ``deepagents.create_deep_agent`` and invokes the returned LangGraph app in
    process. The model must be provided as a LangChain model identifier such as
    ``openai:gpt-4.1`` or ``anthropic:claude-sonnet-4-5``.
    """

    name = "deepagent"

    def __init__(self, binary: str | None = None, model: str | None = None) -> None:
        del binary  # kept for constructor symmetry with CLI-backed agents
        self.binary = "deepagents"
        self.model = model or os.environ.get("ZEROMDASH_DEEPAGENT_MODEL", "")

    def available(self) -> bool:
        return importlib.util.find_spec("deepagents") is not None

    def run(
        self,
        prompt: str,
        cwd: str | Path | None = None,
        timeout: int | None = None,
        extra_args: list[str] | None = None,
        env: AgentEnv | None = None,
    ) -> AgentResult:
        if not self.available():
            return _dry_run(prompt, cwd, backend=self.name)
        del extra_args, env
        if not self.model:
            return AgentResult(
                stdout="",
                stderr="ZEROMDASH_DEEPAGENT_MODEL is required for deepagent backend",
                returncode=1,
                backend=self.name,
                cwd=str(cwd) if cwd else None,
            )

        try:
            result = _run_deepagent_with_timeout(
                model=self.model,
                prompt=prompt,
                cwd=str(cwd) if cwd else None,
                timeout=timeout,
            )
            return AgentResult(
                stdout=_extract_deepagent_output(result),
                stderr="",
                returncode=0,
                backend=self.name,
                cwd=str(cwd) if cwd else None,
            )
        except TimeoutError as exc:
            return AgentResult(
                stdout="",
                stderr=str(exc),
                returncode=1,
                backend=self.name,
                cwd=str(cwd) if cwd else None,
            )
        except Exception as exc:
            return AgentResult(
                stdout="",
                stderr=f"deepagent invocation failed: {type(exc).__name__}: {exc}",
                returncode=1,
                backend=self.name,
                cwd=str(cwd) if cwd else None,
            )


def _invoke_deepagent(model: str, prompt: str, cwd: str | None) -> object:
    from deepagents import create_deep_agent

    system_prompt = (
        "You are an ZeroMDASH agent running via LangChain deepagents. "
        f"The ZeroMDASH sub_workspace is: {cwd}. "
        "Follow the user's task exactly and return the final answer only."
    )
    app = create_deep_agent(
        model=model,
        tools=[],
        system_prompt=system_prompt,
    )
    config = langfuse_config(
        run_name="zeromdash:deepagent",
        metadata={"backend": "deepagent", "cwd": cwd or ""},
    )
    return app.invoke({"messages": [{"role": "user", "content": prompt}]}, config=config or None)


def _run_deepagent_with_timeout(
    model: str, prompt: str, cwd: str | None, timeout: int | None
) -> object:
    if not timeout:
        return _invoke_deepagent(model, prompt, cwd)

    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(_invoke_deepagent, model, prompt, cwd)
    try:
        return future.result(timeout=timeout)
    except FutureTimeoutError as exc:
        future.cancel()
        raise TimeoutError(f"deepagent invocation timed out after {timeout}s") from exc
    finally:
        executor.shutdown(wait=False, cancel_futures=True)


def _extract_deepagent_output(result: object) -> str:
    if isinstance(result, dict):
        messages = result.get("messages") or []
        if messages:
            last = messages[-1]
            content = getattr(last, "content", None)
            if content is None and isinstance(last, dict):
                content = last.get("content")
            if isinstance(content, list):
                parts = []
                for item in content:
                    if isinstance(item, dict):
                        parts.append(str(item.get("text") or item.get("content") or item))
                    else:
                        parts.append(str(item))
                return "\n".join(parts)
            if content is not None:
                return str(content)
    return str(result)


# ------------------------------------------------------------------- dry-run
def _dry_run(prompt: str, cwd: str | Path | None, backend: str) -> AgentResult:
    note = (
        f"[zeromdash:{backend}:dry-run] backend not installed; "
        f"prompt was {len(prompt)} chars, cwd={cwd}\n"
    )
    return AgentResult(
        stdout=note + prompt,
        stderr="",
        returncode=0,
        backend=backend,
        cwd=str(cwd) if cwd else None,
        metadata={"dry_run": True, "resume_id": None},
    )


# -------------------------------------------------------------------- registry
def normalize_agent_name(name: str) -> str:
    name = name.lower().strip().replace("-", "_")
    aliases = {
        "openai_codex": "codex",
        "codex_cli": "codex",
        "trae": "traex",
        "trae_cli": "traex",
        "traecli": "traex",
        "trae_code": "traex",
        "traecode": "traex",
        "traex": "traex",
        "claude": "claude_code",
        "claude_code": "claude_code",
        "kimi": "kimi",
        "kimi_code": "kimi",
        "kimi_cli": "kimi",
        "opencode": "opencode",
        "open_code": "opencode",
        "dsh": "dsh",
        "deepseek_harness": "dsh",
        "deepseek_harness_cli": "dsh",
        "deep_agent": "deepagent",
    }
    return aliases.get(name, name)


def supports_native_subagents(name: str) -> bool:
    """Whether this ZeroMDASH runtime adapter exposes native subagents."""
    return normalize_agent_name(name) in NATIVE_SUBAGENT_BACKENDS


def get_agent(name: str) -> Agent:
    name = normalize_agent_name(name)
    if name == "codex":
        return CodexAgent()
    if name == "traex":
        return TraeXAgent()
    if name == "claude_code":
        return ClaudeCodeAgent()
    if name == "kimi":
        return KimiAgent()
    if name == "opencode":
        return OpenCodeAgent()
    if name == "dsh":
        return DeepSeekHarnessAgent()
    if name == "deepagent":
        return DeepAgent()
    raise ValueError(f"unknown agent backend: {name!r}")


# --------------------------------------------------------------- health check
_HEALTHCHECK_TOKEN = "ZEROMDASH_HEALTHCHECK_OK"


def _agent_binary(agent: Agent) -> str | None:
    return getattr(agent, "binary", None)


def check_agent_health(
    agent: Agent,
    timeout: int = 60,
    extra_args: list[str] | None = None,
    env: AgentEnv | None = None,
) -> AgentHealth:
    """Verify that an agent binary exists and can answer headlessly.

    This intentionally does not rely on the normal dry-run fallback: startup
    should fail if the real CLI is missing, unauthenticated, or otherwise
    unable to return a non-error response in non-interactive mode.
    """
    name = agent.name
    binary = _agent_binary(agent)
    health_extra_args = list(extra_args or [])
    health_env = _safe_env_overlay(env)
    available = getattr(agent, "available", lambda: True)()
    if not available:
        return AgentHealth(
            name=name,
            ok=False,
            binary=binary,
            message=f"{name} binary not found: {binary!r}",
            extra_args=health_extra_args,
            env_overlay=health_env,
        )

    prompt = (
        "ZeroMDASH startup health check. "
        f"Reply with exactly this token and nothing else: {_HEALTHCHECK_TOKEN}"
    )
    try:
        with tempfile.TemporaryDirectory(prefix="zeromdash-agent-health-") as tmp:
            res = agent.run(
                prompt,
                cwd=tmp,
                timeout=timeout,
                extra_args=health_extra_args or None,
                env=env,
            )
    except subprocess.TimeoutExpired as exc:
        return AgentHealth(
            name=name,
            ok=False,
            binary=binary,
            message=f"{name} headless health check timed out after {timeout}s",
            stdout=exc.stdout or "",
            stderr=exc.stderr or "",
            extra_args=health_extra_args,
            env_overlay=health_env,
        )
    except Exception as exc:  # pragma: no cover - defensive around external CLIs
        return AgentHealth(
            name=name,
            ok=False,
            binary=binary,
            message=f"{name} headless health check raised {type(exc).__name__}: {exc}",
            extra_args=health_extra_args,
            env_overlay=health_env,
        )

    stdout = (res.stdout or "").strip()
    stderr = (res.stderr or "").strip()
    if not res.ok:
        return AgentHealth(
            name=name,
            ok=False,
            binary=binary,
            returncode=res.returncode,
            stdout=stdout,
            stderr=stderr,
            message=f"{name} headless health check failed with rc={res.returncode}",
            extra_args=health_extra_args,
            command=_agent_result_command(res),
            env_overlay=health_env,
        )
    if _HEALTHCHECK_TOKEN not in stdout:
        return AgentHealth(
            name=name,
            ok=False,
            binary=binary,
            returncode=res.returncode,
            stdout=stdout,
            stderr=stderr,
            message=f"{name} headless health check did not return expected token",
            extra_args=health_extra_args,
            command=_agent_result_command(res),
            env_overlay=health_env,
        )
    return AgentHealth(
        name=name,
        ok=True,
        binary=binary,
        returncode=res.returncode,
        stdout=stdout,
        stderr=stderr,
        message=f"{name} headless health check passed",
        extra_args=health_extra_args,
        command=_agent_result_command(res),
        env_overlay=health_env,
    )


def check_required_agents(
    timeout: int | None = None,
    agent_names: list[str] | tuple[str, ...] | set[str] | None = None,
) -> list[AgentHealth]:
    """Check external CLIs required by the selected ZeroMDASH workflow."""
    effective_timeout = int(
        timeout if timeout is not None else os.environ.get("ZEROMDASH_AGENT_HEALTHCHECK_TIMEOUT", "60")
    )
    names = ["codex", "claude_code"] if agent_names is None else list(agent_names)
    return [check_agent_health(get_agent(name), timeout=effective_timeout) for name in names]
