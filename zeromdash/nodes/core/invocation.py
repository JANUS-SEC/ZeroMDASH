"""Agent invocation, retry, artifact, and attempt-log infrastructure."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from zeromdash.agents import (
    Agent,
    AgentResult,
    additional_read_root_args,
    get_agent,
    normalize_agent_name,
)
from zeromdash.state import ZeroMDASHState
from zeromdash.workspace import Workspace, slugify

from .config import *
from .constants import *
from .io import *
from .recovery import check_runtime_cancelled, recover_runtime, recovery_round, runtime_console

def _make_agent(name: str) -> Agent:
    return get_agent(name)

def _run_agent_with_config(
    agent: Agent,
    node: str,
    backend: str,
    prompt: str,
    sub_ws,
    timeout: int | None,
    agent_configs: AgentConfigs | None,
    agent_config_task_types: AgentConfigTaskTypes | None = None,
    command_log_dir: Path | None = None,
    additional_read_roots: list[str] | None = None,
) -> AgentResult:
    check_runtime_cancelled()
    extra_args = agent_extra_args_for_node(node, backend, agent_configs, agent_config_task_types)
    # Gather mode normally snapshots source trees below its own workspace.  The
    # explicit roots remain useful for runtimes that support external read
    # grants and for programmatic callers.  Keep this opt-in: --add-dir is a
    # permission expansion and must never be inferred from prompt text.
    extra_args += additional_read_root_args(backend, additional_read_roots)
    env = agent_env_for_node(node, backend, agent_configs, agent_config_task_types)
    _emit_node_run_start(node, backend, sub_ws, extra_args, env)
    check_runtime_cancelled()  # The start message may have waited behind a prompt.
    try:
        res = agent.run(
            prompt,
            cwd=sub_ws,
            timeout=timeout,
            extra_args=extra_args or None,
            env=env or None,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        res = AgentResult(
            stdout="", stderr=str(exc),
            returncode=124 if isinstance(exc, subprocess.TimeoutExpired) else 1,
            backend=backend, cwd=str(sub_ws),
        )
    _emit_node_run_finish(node, res)
    _write_agent_invocation_meta(
        sub_ws,
        node,
        res,
        command_log_dir=command_log_dir,
    )
    return res

def _safe_console_env(env: AgentEnv) -> AgentEnv:
    safe: AgentEnv = {}
    for key, value in env.items():
        if value is not None and any(marker in key.upper() for marker in ("TOKEN", "SECRET", "KEY", "PASSWORD")):
            safe[key] = "<redacted>"
        else:
            safe[key] = value
    return safe

def _emit_node_run_start(
    node: str,
    backend: str,
    sub_ws,
    extra_args: list[str],
    env: AgentEnv,
) -> None:
    lines = [
        f"node {node}: running runtime {backend}",
        f"  - cwd: {sub_ws}",
    ]
    if extra_args:
        lines.append(f"    extra_args: {json.dumps(extra_args, ensure_ascii=False)}")
    if env:
        lines.append(f"    env_overlay: {json.dumps(_safe_console_env(env), ensure_ascii=False)}")
    with runtime_console():
        sys.stderr.write("\n".join(lines) + "\n")
        sys.stderr.flush()

def _emit_node_run_finish(node: str, res: AgentResult) -> None:
    metadata = res.metadata or {}
    lines = [
        f"node {node}: finished runtime {res.backend} ok={str(res.ok).lower()} rc={res.returncode}",
    ]
    command = metadata.get("command")
    if command:
        lines.append(f"  - command: {json.dumps(command, ensure_ascii=False)}")
    resume_id = metadata.get("resume_id")
    if resume_id:
        lines.append(f"    resume_id: {resume_id}")
    with runtime_console():
        sys.stderr.write("\n".join(lines) + "\n")
        sys.stderr.flush()

def _emit_node_fallback(node: str, res: AgentResult, next_variant: AgentNodeConfig) -> None:
    next_backend = normalize_agent_name(next_variant.get("runtime") or "")
    lines = [
        f"node {node}: runtime {res.backend} failed rc={res.returncode}; falling back to {next_backend}",
    ]
    next_config = str(next_variant.get("config", "")).strip()
    next_model = str(next_variant.get("model", "")).strip()
    if next_config:
        lines.append(f"  - next config: {next_config}")
    if next_model:
        lines.append(f"    next model: {next_model}")
    with runtime_console():
        sys.stderr.write("\n".join(lines) + "\n")
        sys.stderr.flush()

@recover_runtime()
def _invoke(
    ws: Workspace,
    node: str,
    prompt: str,
    backends: dict[str, str] | None,
    agent_configs: AgentConfigs | None = None,
    agent_config_task_types: AgentConfigTaskTypes | None = None,
    subtask_id: str | None = None,
    extra_context: dict[str, Any] | None = None,
    timeout: int | None = None,
    additional_read_roots: list[str] | None = None,
) -> AgentResult:
    """Resolve backend, prepare sub_workspace, and run the agent.

    This low-level helper tries explicit per-node fallbacks immediately after a
    failed invocation. Callers that have their own retry policy should pass a
    single-variant agent_configs view when they need retries to exhaust first.
    """
    last_res: AgentResult | None = None
    variants = agent_config_variants_for_node(node, backends, agent_configs)
    for index, variant in enumerate(variants, start=1):
        backend_name = normalize_agent_name(variant["runtime"])
        variant_configs = _agent_configs_with_node_variant(agent_configs, node, variant)
        variant_context = dict(extra_context or {})
        raw_command_log_dir = str(
            variant_context.pop("_command_log_dir", "") or ""
        ).strip()
        command_log_dir = Path(raw_command_log_dir) if raw_command_log_dir else None
        variant_context["fallback_index"] = index - 1
        variant_context["fallback_count"] = len(variants) - 1
        sub_ws = ws.prepare_sub_workspace(
            node=node,
            subtask_id=subtask_id,
            backend=backend_name,
            extra_context=variant_context,
        )
        res = _run_agent_with_config(
            _make_agent(backend_name),
            node,
            backend_name,
            prompt,
            sub_ws,
            timeout,
            variant_configs,
            agent_config_task_types,
            command_log_dir,
            additional_read_roots,
        )
        last_res = res
        if res.ok or index == len(variants):
            return res
        _emit_node_fallback(node, res, variants[index])
    if last_res is None:
        raise RuntimeError(f"no runtime configured for node {node}")
    return last_res

def _write_agent_invocation_meta(
    sub_ws,
    node: str,
    res: AgentResult,
    *,
    command_log_dir: Path | None = None,
) -> None:
    metadata = res.metadata or {}
    meta = {
        "node": node,
        "backend": res.backend,
        "cwd": res.cwd,
        "returncode": res.returncode,
        "ok": res.ok,
        "resume_id": metadata.get("resume_id"),
        "metadata": metadata,
    }
    (sub_ws / "agent_invocation.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    _append_agent_command_log(
        sub_ws,
        node,
        res,
        metadata,
        command_log_dir=command_log_dir,
    )

def _append_agent_command_log(
    sub_ws,
    node: str,
    res: AgentResult,
    metadata: dict[str, Any],
    *,
    command_log_dir: Path | None = None,
) -> None:
    """Append one workflow-level record for the command used to start an agent.

    Per-node ``agent_invocation.json`` is useful when inspecting a single
    sub_workspace, but it is inconvenient for reconstructing the whole workflow.
    This JSONL file gives every task a single chronological log of agent
    launches under ``<workspace>/log/agent_commands.jsonl``.
    """
    sub_ws = sub_ws.resolve()
    parts = sub_ws.parts
    if "sub_workspace" not in parts:
        return
    base = sub_ws.parents[len(parts) - parts.index("sub_workspace") - 1]
    log_dir = command_log_dir or (base / "log")
    log_dir.mkdir(parents=True, exist_ok=True)
    command = metadata.get("command")
    record = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "node": node,
        "backend": res.backend,
        "cwd": res.cwd,
        "sub_workspace": str(sub_ws),
        "command": command,
        "returncode": res.returncode,
        "ok": res.ok,
        "resume_id": metadata.get("resume_id"),
    }
    with (log_dir / "agent_commands.jsonl").open("a") as fp:
        fp.write(json.dumps(record, ensure_ascii=False) + "\n")

def _agent_attempt_log_path(
    ws: Workspace,
    node: str,
    *,
    attempt: int,
    subtask_id: str | None = None,
) -> Path:
    if subtask_id:
        name = f"{slugify(subtask_id)}.{slugify(node)}.attempt-{attempt}.log"
    else:
        name = f"{slugify(node)}.attempt-{attempt}.log"
    return ws.log_path("review_log") / name

def _selected_log_dir(state: ZeroMDASHState) -> Path | None:
    raw = str(
        state.get("selected_subtask_log_dir")
        or state.get("selected_subagent_log_dir")
        or state.get("selected_chain_log_dir")
        or ""
    ).strip()
    return Path(raw) if raw else None

def _attempt_log_path_for_state(
    ws: Workspace,
    state: ZeroMDASHState,
    node: str,
    *,
    attempt: int,
    subtask_id: str | None = None,
) -> Path:
    if recovery_round():
        subtask_id = f"{subtask_id or node}.recovery-{recovery_round()}"
    selected_dir = _selected_log_dir(state)
    if selected_dir is None:
        return _agent_attempt_log_path(
            ws,
            node,
            attempt=attempt,
            subtask_id=subtask_id,
        )
    if subtask_id:
        name = f"{slugify(subtask_id)}.{slugify(node)}.attempt-{attempt}.log"
    else:
        name = f"{slugify(node)}.attempt-{attempt}.log"
    return selected_dir / "attempts" / name

def _write_agent_attempt_log(
    path: Path,
    res: AgentResult,
    *,
    node: str,
    attempt: int,
    subtask_id: str | None = None,
) -> None:
    metadata = res.metadata or {}
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"node: {node}",
        f"subtask_id: {subtask_id or ''}",
        f"attempt: {attempt}",
        f"backend: {res.backend}",
        f"returncode: {res.returncode}",
        f"ok: {str(res.ok).lower()}",
        f"cwd: {res.cwd or ''}",
    ]
    if metadata.get("command"):
        lines.append(f"command: {json.dumps(metadata['command'], ensure_ascii=False)}")
    if metadata.get("resume_id"):
        lines.append(f"resume_id: {metadata['resume_id']}")
    for key in (
        "output_source",
        "artifact_path",
        "validation_status",
        "stdout_validation_failure",
        "artifact_validation_failure",
        "validation_failure",
        "timeout_recovered_from_artifact",
        "timeout_seconds",
        "timeout_artifact_path",
    ):
        value = str(metadata.get(key) or "").strip()
        if value:
            normalized_value = re.sub(r"\s+", " ", value)
            lines.append(f"{key}: {normalized_value}")
    text = "\n".join(lines)
    text += "\n\n[stdout]\n" + (res.stdout or "").rstrip() + "\n"
    text += "\n[stderr]\n" + (res.stderr or "").rstrip() + "\n"
    path.write_text(text, encoding="utf-8")

def _agent_errors(
    res: AgentResult,
    node: str,
    subtask_id: str | None = None,
    log_path: Path | str | None = None,
) -> list[str]:
    """Surface a sub-process failure (non-zero rc) as an `errors` entry.

    Returns an empty list on success so callers can unconditionally splice
    ``"errors": _agent_errors(res, ...)`` into their state update; the
    ``operator.add`` reducer merges them into the parent state.
    """
    if res.ok:
        return []
    tag = node if not subtask_id else f"{node}/{subtask_id}"
    snippet = (res.stderr or "").strip()[:500] or "(no stderr)"
    message = f"[{tag}] backend={res.backend} rc={res.returncode}: {snippet}"
    if log_path:
        message += f" (full log: {log_path})"
    return [message]

def _agent_error_tag(node: str, subtask_id: str | None = None) -> str:
    return node if not subtask_id else f"{node}/{subtask_id}"

def _retry_feedback_block(
    *,
    node: str,
    subtask_id: str | None,
    attempt: int,
    attempts: int,
    output_desc: str,
    failure: str,
) -> str:
    tag = _agent_error_tag(node, subtask_id)
    return (
        f"\n\n{_RETRY_FEEDBACK_HEADER}\n"
        f"This is retry attempt {attempt}/{attempts} for `{tag}`.\n"
        f"The previous attempt failed: {failure}\n"
        f"Required output: {output_desc}\n"
        "Fix the cause of the failure instead of repeating the same response. "
        "Produce the required artifact exactly at the path named in the original instructions.\n"
    )

def _structured_artifact_paths(
    ws: Workspace,
    node: str,
    subtask_id: str | None,
    artifact_filenames: tuple[str, ...],
) -> list[Path]:
    sub_ws = ws.sub_workspace_root / f"node_{node}"
    if subtask_id:
        sub_ws = sub_ws / f"subtask_{slugify(subtask_id)}"
    return [sub_ws / name for name in artifact_filenames]

def _set_attempt_validation_metadata(
    res: AgentResult,
    *,
    output_source: str = "",
    artifact_path: Path | None = None,
    validation_status: str,
    stdout_failure: str = "",
    artifact_failure: str = "",
    validation_failure: str = "",
) -> None:
    metadata = dict(res.metadata or {})
    metadata.update(
        {
            "output_source": output_source,
            "artifact_path": str(artifact_path) if artifact_path else "",
            "validation_status": validation_status,
            "stdout_validation_failure": stdout_failure,
            "artifact_validation_failure": artifact_failure,
            "validation_failure": validation_failure,
        }
    )
    res.metadata = metadata

def _read_preset_attack_surface(state: ZeroMDASHState) -> tuple[str, list[str]]:
    raw_path = str(state.get("preset_attack_surface_path") or "").strip()
    if not raw_path:
        return "", []
    path = Path(raw_path).expanduser()
    try:
        return path.read_text(), []
    except OSError as exc:
        return "", [f"[analyze_attack_surface] preset attack surface unreadable: {path}: {exc}"]

def _seeded_attack_surface_has_append(path, seed_text: str) -> bool:
    text = _read_text_lossy(path)
    seed = seed_text.rstrip()
    return text.startswith(seed) and len(text.strip()) > len(seed)

@recover_runtime()
def _invoke_with_output_retry(
    ws: Workspace,
    node: str,
    prompt: str,
    backends: dict[str, str] | None,
    state: ZeroMDASHState,
    *,
    output_desc: str,
    validate,
    materialize=None,
    reset=None,
    subtask_id: str | None = None,
    focus: str = "",
    attempts: int = DEFAULT_NODE_OUTPUT_ATTEMPTS,
    artifact_filenames: tuple[str, ...] = (),
    attempt_log_subtask_id: str | None = None,
    extra_context: dict[str, Any] | None = None,
    additional_read_roots: list[str] | None = None,
) -> tuple[AgentResult | None, list[str]]:
    last_res: AgentResult | None = None
    errors: list[str] = []
    variants = agent_config_variants_for_node(node, backends, state.get("agent_configs"))
    for variant_index, variant in enumerate(variants, start=1):
        variant_configs = _agent_configs_with_node_variant(state.get("agent_configs"), node, variant)
        retry_feedback = ""
        previous_failure = ""
        for attempt in range(1, attempts + 1):
            if reset:
                reset()
            artifact_paths = _structured_artifact_paths(
                ws,
                node,
                subtask_id,
                artifact_filenames,
            )
            for artifact_path in artifact_paths:
                _reset_file_output(artifact_path)
            attempt_prompt = prompt + retry_feedback if retry_feedback else prompt
            invoke_kwargs = {
                "agent_configs": variant_configs,
                "agent_config_task_types": state.get("agent_config_task_types"),
                "subtask_id": subtask_id,
                "extra_context": {
                    **(extra_context or {}),
                    "attempt": attempt,
                    "max_attempts": attempts,
                    "focus": focus,
                    "previous_failure": previous_failure,
                    "fallback_index": variant_index - 1,
                    "fallback_count": len(variants) - 1,
                    "_command_log_dir": str(_selected_log_dir(state) or ""),
                },
            }
            if additional_read_roots:
                invoke_kwargs["additional_read_roots"] = additional_read_roots
            res = _invoke(
                ws,
                node,
                attempt_prompt,
                {node: normalize_agent_name(variant["runtime"])},
                **invoke_kwargs,
            )
            last_res = res
            log_attempt = attempt + (variant_index - 1) * attempts
            attempt_log = _attempt_log_path_for_state(
                ws,
                state,
                node,
                attempt=log_attempt,
                subtask_id=attempt_log_subtask_id or subtask_id,
            )
            runtime_errors = _agent_errors(
                res,
                node,
                subtask_id,
                log_path=attempt_log,
            )
            if runtime_errors and not artifact_filenames:
                _set_attempt_validation_metadata(
                    res,
                    validation_status="not_run",
                    validation_failure=runtime_errors[0],
                )
                _write_agent_attempt_log(
                    attempt_log,
                    res,
                    node=node,
                    attempt=log_attempt,
                    subtask_id=subtask_id,
                )
                errors = runtime_errors
                previous_failure = errors[0]
                retry_feedback = _retry_feedback_block(
                    node=node,
                    subtask_id=subtask_id,
                    attempt=attempt + 1,
                    attempts=attempts,
                    output_desc=output_desc,
                    failure=previous_failure,
                )
                continue
            if materialize and not runtime_errors:
                materialize(res)
            stdout_valid, stdout_failure = _run_output_validator(validate, res)
            if stdout_valid:
                _set_attempt_validation_metadata(
                    res,
                    output_source="stdout",
                    validation_status="valid",
                )
                _write_agent_attempt_log(
                    attempt_log,
                    res,
                    node=node,
                    attempt=log_attempt,
                    subtask_id=subtask_id,
                )
                return res, []

            artifact_failure_parts: list[str] = []
            accepted_artifact: Path | None = None
            accepted_artifact_text = ""
            for artifact_path in artifact_paths:
                if not artifact_path.is_file():
                    artifact_failure_parts.append(
                        f"{artifact_path.name}: not created by this attempt"
                    )
                    continue
                try:
                    payload = json.loads(artifact_path.read_text())
                except (OSError, json.JSONDecodeError) as exc:
                    artifact_failure_parts.append(
                        f"{artifact_path.name}: invalid JSON ({exc})"
                    )
                    continue
                artifact_text = json.dumps(payload, ensure_ascii=False)
                artifact_res = AgentResult(
                    stdout=artifact_text,
                    stderr=res.stderr,
                    returncode=res.returncode,
                    backend=res.backend,
                    cwd=res.cwd,
                    metadata=dict(res.metadata or {}),
                )
                artifact_valid, artifact_failure = _run_output_validator(
                    validate,
                    artifact_res,
                )
                if artifact_valid:
                    accepted_artifact = artifact_path
                    accepted_artifact_text = artifact_text
                    break
                artifact_failure_parts.append(
                    f"{artifact_path.name}: "
                    f"{artifact_failure or 'unspecified validation failure'}"
                )

            artifact_failure = "; ".join(artifact_failure_parts)
            if accepted_artifact is not None:
                _set_attempt_validation_metadata(
                    res,
                    output_source="artifact",
                    artifact_path=accepted_artifact,
                    validation_status="valid",
                    stdout_failure=stdout_failure,
                )
                _write_agent_attempt_log(
                    attempt_log,
                    res,
                    node=node,
                    attempt=log_attempt,
                    subtask_id=subtask_id,
                )
                return AgentResult(
                    stdout=accepted_artifact_text,
                    stderr=res.stderr,
                    returncode=res.returncode,
                    backend=res.backend,
                    cwd=res.cwd,
                    metadata=dict(res.metadata or {}),
                ), []

            validation_detail = (
                f"stdout: {stdout_failure or 'unspecified validation failure'}"
            )
            if artifact_filenames:
                validation_detail += (
                    "; artifacts: "
                    f"{artifact_failure or 'no valid artifact was produced'}"
                )
            if runtime_errors:
                validation_detail = (
                    f"{runtime_errors[0]}; structured output invalid; "
                    f"{validation_detail}"
                )
            _set_attempt_validation_metadata(
                res,
                validation_status="invalid",
                stdout_failure=stdout_failure,
                artifact_failure=artifact_failure,
                validation_failure=validation_detail,
            )
            _write_agent_attempt_log(
                attempt_log,
                res,
                node=node,
                attempt=log_attempt,
                subtask_id=subtask_id,
            )
            previous_failure = (
                f"[{_agent_error_tag(node, subtask_id)}] output validation failed after attempt "
                f"{attempt}/{attempts}: {output_desc}; "
                f"reason={validation_detail}; "
                f"stdout_preview={_preview(res.stdout) or '(empty)'}; "
                f"stderr_preview={_preview(res.stderr) or '(empty)'}"
            )
            retry_feedback = _retry_feedback_block(
                node=node,
                subtask_id=subtask_id,
                attempt=attempt + 1,
                attempts=attempts,
                output_desc=output_desc,
                failure=previous_failure,
            )
            errors = [
                (
                    f"[{_agent_error_tag(node, subtask_id)}] output invalid after attempt "
                    f"{attempt}/{attempts}: {output_desc}; reason={validation_detail}"
                    if artifact_filenames
                    else f"[{_agent_error_tag(node, subtask_id)}] output empty after attempt "
                    f"{attempt}/{attempts}: {output_desc}"
                )
            ]
        if errors and variant_index < len(variants):
            _emit_node_fallback(node, last_res or AgentResult("", "", 1, normalize_agent_name(variant["runtime"])), variants[variant_index])
    return last_res, errors

__all__ = ["_make_agent","_run_agent_with_config","_safe_console_env","_emit_node_run_start","_emit_node_run_finish","_emit_node_fallback","_invoke","_write_agent_invocation_meta","_append_agent_command_log","_agent_attempt_log_path","_selected_log_dir","_attempt_log_path_for_state","_write_agent_attempt_log","_agent_errors","_agent_error_tag","_retry_feedback_block","_structured_artifact_paths","_set_attempt_validation_metadata","_read_preset_attack_surface","_seeded_attack_surface_has_append","_invoke_with_output_retry"]
