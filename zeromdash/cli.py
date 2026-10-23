"""`zeromdash` command-line entry point."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import click
import yaml
from dotenv import load_dotenv

from zeromdash import nodes
from zeromdash.agents import (
    AgentEnv,
    AgentHealth,
    check_agent_health,
    get_agent,
    langfuse_is_configured,
    normalize_agent_name,
)
from zeromdash.graph import (
    run,
    run_from_chain_workspace,
    run_from_subtask_workspace,
    run_polish_report_from_workspace,
    run_summary_from_workspace,
)
from zeromdash.gather import load_gather_manifest
from zeromdash.gather_graph import run_gather
from zeromdash.nodes.core.recovery import (
    RecoveryRequest,
    RuntimeRecovery,
    RuntimeRecoveryAborted,
)

# 从 ./.env 加载环境变量(Langfuse 凭据、后端可执行文件等)。
load_dotenv()

_AGENT_CONFIG_COMMON_FOCUS_KEY = "__common_focus__"
_AGENT_CONFIG_TOP_K_KEY = "__top_K__"
_AGENT_CONFIG_CHAIN_KEY = "__chain__"
_AGENT_CONFIG_GATHER_KEY = "__gather__"
_AGENT_CONFIG_MAX_CONCURRENCY_KEY = "__max_concurrency__"
_AGENT_CONFIG_TARGET_REPOS_KEY = "__target_repos__"
DEFAULT_MAX_CONCURRENCY = 8
_TOP_K_BUCKETS = {"spec", "vuln", "patch", "feature", "chain"}
_START_FROM_SUBTASK_DISABLED_NODES = {
    "fetch_target_repo",
    "prepare_scan_scope",
    "search_spec",
    "search_fuzz_driver",
    "search_similar_software",
    "search_similar_history",
    "search_target_history",
    "search_new_feature",
    "analyze_attack_surface",
    "plan_by_spec",
    "plan_by_vuln_similar",
    "plan_by_vuln_patch",
    "plan_by_new_feature",
}
_START_FROM_CHAIN_DISABLED_NODES = {
    *_START_FROM_SUBTASK_DISABLED_NODES,
    "investigate_subtask",
    "critic_subtask",
}
_TILL_ANALYZE_DISABLED_NODES = {
    "plan_by_spec",
    "plan_by_vuln_similar",
    "plan_by_vuln_patch",
    "plan_by_new_feature",
    "plan_chains",
    "investigate_subtask",
    "critic_subtask",
    "chain_investigate_subtask",
    "chain_critic_subtask",
    "chain_finalizer_subtask",
    "report_group_adjudicator",
    "summary",
    "polish_report",
}
_TILL_PLAN_DISABLED_NODES = {
    "investigate_subtask",
    "critic_subtask",
    "plan_chains",
    "chain_investigate_subtask",
    "chain_critic_subtask",
    "chain_finalizer_subtask",
    "report_group_adjudicator",
    "summary",
    "polish_report",
}
_START_FROM_SUMMARY_DISABLED_NODES = set(nodes.DEFAULT_BACKENDS) - {"summary", "polish_report"}
_START_FROM_POLISH_REPORT_DISABLED_NODES = set(nodes.DEFAULT_BACKENDS) - {"polish_report"}
_GATHER_ONLY_NODES = {
    "gather_analyze_attack_surface",
    "gather_plan_chains",
    "gather_chain_investigate_subtask",
    "gather_chain_critic_subtask",
    "gather_chain_finalizer_subtask",
    "gather_report_group_adjudicator",
}
_GATHER_GRAPH_AGENT_NODES = {*_GATHER_ONLY_NODES, "summary", "polish_report"}


def _expand_config_value(value: object) -> str:
    if value is None:
        return ""
    return os.path.expandvars(os.path.expanduser(str(value).strip()))


def _is_path_like_config(value: str) -> bool:
    return (
        "/" in value
        or value.startswith(("~", "$"))
        or value.endswith((".json", ".toml", ".yaml", ".yml"))
    )


def _normalize_config_value(runtime: str, value: object) -> str:
    raw = "" if value is None else str(value).strip()
    if not raw:
        return ""
    runtime = normalize_agent_name(runtime)
    if runtime == "claude_code" and not _is_path_like_config(raw):
        return os.path.expanduser(f"~/.claude/settings.{raw}.json")
    expanded = _expand_config_value(raw)
    if runtime == "dsh":
        return str(Path(expanded).resolve())
    return expanded


def _normalize_model_value(value: object) -> str:
    if value is None:
        return ""
    return os.path.expandvars(str(value).strip())


def _parse_env(value: object, *, node: str) -> AgentEnv:
    if value in (None, ""):
        return {}
    if not isinstance(value, dict):
        raise click.ClickException(f"invalid env for node {node!r}: expected mapping")
    env: AgentEnv = {}
    for key, raw in value.items():
        if not isinstance(key, str) or not key:
            raise click.ClickException(f"invalid env key for node {node!r}: {key!r}")
        env[key] = None if raw is None else os.path.expandvars(str(raw))
    return env


def _parse_node_runtime_config(
    raw_cfg: object,
    *,
    node: str,
    default_runtime: str,
    allow_focus: bool = True,
) -> nodes.AgentNodeConfig:
    if raw_cfg is None:
        return {}
    if not isinstance(raw_cfg, dict):
        raise click.ClickException(f"invalid config for node {node!r}: expected mapping")
    cfg: nodes.AgentNodeConfig = {}
    if raw_cfg.get("runtime"):
        cfg["runtime"] = normalize_agent_name(str(raw_cfg["runtime"]))
    node_runtime = cfg.get("runtime") or default_runtime
    if raw_cfg.get("provider"):
        cfg["provider"] = str(raw_cfg["provider"]).strip().lower()
    if "config" in raw_cfg:
        cfg["config"] = _normalize_config_value(node_runtime, raw_cfg.get("config"))
    if "model" in raw_cfg:
        cfg["model"] = _normalize_model_value(raw_cfg.get("model"))
    if "env" in raw_cfg:
        cfg["env"] = _parse_env(raw_cfg.get("env"), node=node)
    if allow_focus and "focus" in raw_cfg:
        cfg["focus"] = "" if raw_cfg.get("focus") is None else str(raw_cfg.get("focus")).strip()
    return cfg


def _parse_top_k(value: object) -> dict[str, int]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise click.ClickException("invalid top_K section in --agent-config: expected mapping")

    unknown_keys = sorted(str(key) for key in value if key not in _TOP_K_BUCKETS)
    if unknown_keys:
        raise click.ClickException(f"unknown top_K key(s) in --agent-config: {', '.join(unknown_keys)}")

    parsed: dict[str, int] = {}
    for bucket, raw in value.items():
        if not isinstance(raw, int) or isinstance(raw, bool):
            raise click.ClickException(f"invalid top_K.{bucket} in --agent-config: expected int")
        if raw <= 0:
            raise click.ClickException(f"invalid top_K.{bucket} in --agent-config: expected positive int")
        parsed[str(bucket)] = raw
    return parsed


def _parse_max_concurrency(value: object) -> int:
    if value is None:
        return DEFAULT_MAX_CONCURRENCY
    if not isinstance(value, int) or isinstance(value, bool):
        raise click.ClickException("invalid max_concurrency in --agent-config: expected int")
    if value <= 0:
        raise click.ClickException("invalid max_concurrency in --agent-config: expected positive int")
    return value


def _parse_chain_config(value: object) -> dict[str, object]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise click.ClickException("invalid chain section in --agent-config: expected mapping")
    allowed = {
        "enabled",
        "max_length",
        "max_successors_per_capability",
        "beam_width",
        "max_candidates_before_top_k",
        "max_battle_rounds",
        "attacker_entry_capabilities",
    }
    unknown = sorted(str(key) for key in value if key not in allowed)
    if unknown:
        raise click.ClickException(f"unknown chain key(s) in --agent-config: {', '.join(unknown)}")
    parsed: dict[str, object] = {}
    for key, raw in value.items():
        if key == "enabled":
            if not isinstance(raw, bool):
                raise click.ClickException("invalid chain.enabled in --agent-config: expected bool")
            parsed[key] = raw
            continue
        if key == "attacker_entry_capabilities":
            if not isinstance(raw, list):
                raise click.ClickException("invalid chain.attacker_entry_capabilities in --agent-config: expected list")
            parsed[key] = raw
            continue
        if not isinstance(raw, int) or isinstance(raw, bool) or raw <= 0:
            raise click.ClickException(f"invalid chain.{key} in --agent-config: expected positive int")
        parsed[str(key)] = raw
    return parsed


def _parse_gather_config(value: object) -> dict[str, object]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise click.ClickException("invalid gather section in --agent-config: expected mapping")
    allowed = {
        "max_pair_passes",
        "max_chain_length",
        "max_candidates_before_top_k",
        "max_battle_rounds",
        "require_cross_target",
    }
    unknown = sorted(str(key) for key in value if key not in allowed)
    if unknown:
        raise click.ClickException(f"unknown gather key(s) in --agent-config: {', '.join(unknown)}")
    parsed: dict[str, object] = {}
    for key, raw in value.items():
        if key == "require_cross_target":
            if not isinstance(raw, bool):
                raise click.ClickException("invalid gather.require_cross_target: expected bool")
            parsed[key] = raw
        elif not isinstance(raw, int) or isinstance(raw, bool) or raw <= 0:
            raise click.ClickException(f"invalid gather.{key}: expected positive int")
        else:
            parsed[key] = raw
    return parsed


def _parse_target_repos(
    value: object,
    *,
    config_dir: Path | None = None,
) -> list[dict[str, str]]:
    if value in (None, ""):
        return []
    if not isinstance(value, list):
        raise click.ClickException("invalid target_repos in --agent-config: expected list")
    parsed: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, raw in enumerate(value, start=1):
        if not isinstance(raw, dict):
            raise click.ClickException(
                f"invalid target_repos[{index}] in --agent-config: expected mapping"
            )
        repo_id = str(raw.get("id") or raw.get("name") or "").strip()
        path_value = str(raw.get("path") or "").strip()
        target = str(raw.get("target") or raw.get("url") or path_value or "").strip()
        if not repo_id:
            raise click.ClickException(f"invalid target_repos[{index}]: missing id")
        if not target:
            raise click.ClickException(f"invalid target_repos[{index}] ({repo_id}): missing target")
        if repo_id in seen:
            raise click.ClickException(f"duplicate target_repos id in --agent-config: {repo_id}")
        seen.add(repo_id)
        expanded_target = _expand_config_value(target)
        is_relative_path = (
            bool(path_value)
            or expanded_target.startswith(("./", "../"))
        ) and "://" not in expanded_target
        if is_relative_path and config_dir is not None:
            candidate = Path(expanded_target)
            if not candidate.is_absolute():
                expanded_target = str((config_dir / candidate).resolve())
        entry = {
            "id": repo_id,
            "target": expanded_target,
            "role": str(raw.get("role") or "").strip(),
            "description": str(raw.get("description") or "").strip(),
        }
        parsed.append({key: item for key, item in entry.items() if item})
    return parsed


def _parse_agent_config_file(path: str | None) -> nodes.AgentConfigs:
    """Load global focus and per-node agent runtime/config/model/provider/env from YAML."""
    if not path:
        return {}
    cfg_path = Path(os.path.expandvars(os.path.expanduser(path))).resolve()
    try:
        data = yaml.safe_load(cfg_path.read_text())
    except FileNotFoundError as exc:
        raise click.ClickException(f"--agent-config file not found: {cfg_path}") from exc
    except yaml.YAMLError as exc:
        raise click.ClickException(f"invalid --agent-config YAML {cfg_path}: {exc}") from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise click.ClickException(
            "--agent-config YAML must be a mapping with common_focus/max_concurrency/top_K/node sections"
        )

    parsed: nodes.AgentConfigs = {}
    allowed_top_level = {"common_focus", "max_concurrency", "node", "target_repos", "top_K", "chain", "gather"}
    unknown_keys = sorted(str(key) for key in data if key not in allowed_top_level)
    if unknown_keys:
        raise click.ClickException(f"unknown top-level key(s) in --agent-config: {', '.join(unknown_keys)}")

    raw_common_focus = data.get("common_focus", "")
    if isinstance(raw_common_focus, dict):
        raw_common_focus = raw_common_focus.get("focus", "")
    parsed[_AGENT_CONFIG_COMMON_FOCUS_KEY] = {
        "focus": "" if raw_common_focus is None else str(raw_common_focus).strip()
    }
    top_K = _parse_top_k(data.get("top_K"))
    if top_K:
        parsed[_AGENT_CONFIG_TOP_K_KEY] = {"top_K": top_K}
    chain_config = _parse_chain_config(data.get("chain"))
    if chain_config:
        parsed[_AGENT_CONFIG_CHAIN_KEY] = {"chain": chain_config}
    gather_config = _parse_gather_config(data.get("gather"))
    if gather_config:
        parsed[_AGENT_CONFIG_GATHER_KEY] = {"gather": gather_config}
    parsed[_AGENT_CONFIG_MAX_CONCURRENCY_KEY] = {
        "max_concurrency": _parse_max_concurrency(data.get("max_concurrency"))
    }
    target_repos = _parse_target_repos(data.get("target_repos"), config_dir=cfg_path.parent)
    if target_repos:
        parsed[_AGENT_CONFIG_TARGET_REPOS_KEY] = {"target_repos": target_repos}

    node_data = data.get("node") or {}
    if not isinstance(node_data, dict):
        raise click.ClickException("invalid node section in --agent-config: expected mapping of node name -> config")
    normalized_node_data: dict[str, object] = {}
    for raw_node, raw_cfg in node_data.items():
        node = nodes.canonical_node_name(str(raw_node))
        if node in normalized_node_data:
            raise click.ClickException(
                f"duplicate node config after alias normalization: {node}"
            )
        normalized_node_data[node] = raw_cfg
    node_data = normalized_node_data
    unknown_nodes = sorted(str(node) for node in node_data if node not in nodes.DEFAULT_BACKENDS)
    if unknown_nodes:
        raise click.ClickException(f"unknown node(s) in --agent-config node section: {', '.join(unknown_nodes)}")

    for node, raw_cfg in node_data.items():
        if raw_cfg is None:
            continue
        if not isinstance(raw_cfg, dict):
            raise click.ClickException(f"invalid config for node {node!r}: expected mapping")
        cfg = _parse_node_runtime_config(
            raw_cfg,
            node=str(node),
            default_runtime=nodes.DEFAULT_BACKENDS[str(node)],
            allow_focus=True,
        )
        if "fallbacks" in raw_cfg:
            raw_fallbacks = raw_cfg.get("fallbacks")
            if raw_fallbacks in (None, ""):
                cfg["fallbacks"] = []
            elif not isinstance(raw_fallbacks, list):
                raise click.ClickException(f"invalid fallbacks for node {node!r}: expected list")
            else:
                primary_runtime = cfg.get("runtime") or nodes.DEFAULT_BACKENDS[str(node)]
                parsed_fallbacks: list[dict[str, object]] = []
                for index, fallback_raw in enumerate(raw_fallbacks, start=1):
                    fallback_cfg = _parse_node_runtime_config(
                        fallback_raw,
                        node=f"{node}.fallbacks[{index}]",
                        default_runtime=primary_runtime,
                        allow_focus=False,
                    )
                    if fallback_cfg:
                        parsed_fallbacks.append(fallback_cfg)
                cfg["fallbacks"] = parsed_fallbacks
        parsed[str(node)] = cfg
        try:
            # Resolve inherited fallback runtimes before enforcing the native
            # subagent capability gate. A fallback that only changes model or
            # config inherits the primary runtime and must remain valid.
            nodes.agent_config_variants_for_node(
                str(node),
                None,
                {str(node): cfg},
            )
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
    return parsed


def _pop_common_focus_from_agent_config(agent_configs: nodes.AgentConfigs) -> str:
    """Remove and return top-level common_focus parsed from agent-config YAML."""
    cfg = agent_configs.pop(_AGENT_CONFIG_COMMON_FOCUS_KEY, {})
    return str((cfg or {}).get("focus") or "").strip()


def _pop_top_k_from_agent_config(agent_configs: nodes.AgentConfigs) -> dict[str, int]:
    """Remove and return top-level top_K parsed from agent-config YAML."""
    cfg = agent_configs.pop(_AGENT_CONFIG_TOP_K_KEY, {})
    top_K = (cfg or {}).get("top_K") or {}
    return dict(top_K)


def _pop_chain_config_from_agent_config(agent_configs: nodes.AgentConfigs) -> dict[str, object]:
    """Remove and return top-level chain config parsed from agent-config YAML."""
    cfg = agent_configs.pop(_AGENT_CONFIG_CHAIN_KEY, {})
    chain = (cfg or {}).get("chain") or {}
    return dict(chain)


def _pop_gather_config_from_agent_config(agent_configs: nodes.AgentConfigs) -> dict[str, object]:
    """Remove and return top-level gather config parsed from agent-config YAML."""
    cfg = agent_configs.pop(_AGENT_CONFIG_GATHER_KEY, {})
    gather = (cfg or {}).get("gather") or {}
    return dict(gather)


def _pop_max_concurrency_from_agent_config(agent_configs: nodes.AgentConfigs) -> int:
    """Remove and return top-level max_concurrency parsed from agent-config YAML."""
    cfg = agent_configs.pop(_AGENT_CONFIG_MAX_CONCURRENCY_KEY, {})
    raw = (cfg or {}).get("max_concurrency")
    return raw if isinstance(raw, int) and not isinstance(raw, bool) else DEFAULT_MAX_CONCURRENCY


def _pop_target_repos_from_agent_config(agent_configs: nodes.AgentConfigs) -> list[dict[str, str]]:
    """Remove and return top-level target_repos parsed from agent-config YAML."""
    cfg = agent_configs.pop(_AGENT_CONFIG_TARGET_REPOS_KEY, {})
    repos = (cfg or {}).get("target_repos") or []
    return [dict(item) for item in repos if isinstance(item, dict)]


def _write_final_state(final: dict) -> Path:
    selected_log_dir = str(
        final.get("selected_subtask_log_dir")
        or final.get("selected_subagent_log_dir")
        or final.get("selected_chain_log_dir")
        or ""
    ).strip()
    if selected_log_dir:
        out = Path(selected_log_dir).expanduser().resolve() / "final_state.json"
        out.write_text(json.dumps(final, default=str, ensure_ascii=False, indent=2))
        return out
    workspace_root = final.get("workspace_root")
    task_id = final.get("task_id")
    if not workspace_root or not task_id:
        raise click.ClickException("workflow final state is missing workspace_root/task_id; cannot write final_state.json")
    out = Path(str(workspace_root)).expanduser().resolve() / str(task_id) / "final_state.json"
    out.write_text(json.dumps(final, default=str, ensure_ascii=False, indent=2))
    return out


def _health_key(
    backend: str,
    extra_args: list[str],
    env: AgentEnv | None = None,
) -> tuple[str, tuple[str, ...], tuple[tuple[str, str | None], ...]]:
    safe_env = tuple(
        sorted(
            (
                key,
                "<redacted>" if key == "AWS_BEARER_TOKEN_BEDROCK" and value is not None else value,
            )
            for key, value in (env or {}).items()
        )
    )
    return (backend, tuple(extra_args), safe_env)


def _bedrock_env_health_error(backend: str, env: AgentEnv) -> AgentHealth | None:
    """Fail early with a clear message when Claude Code Bedrock env is incomplete."""
    if backend != "claude_code" or env.get("CLAUDE_CODE_USE_BEDROCK") != "1":
        return None
    if env.get("AWS_BEARER_TOKEN_BEDROCK"):
        return None
    agent = get_agent(backend)
    return AgentHealth(
        name=backend,
        ok=False,
        binary=getattr(agent, "binary", None),
        message=(
            "claude_code bedrock provider requires AWS_BEARER_TOKEN_BEDROCK "
            "to be exported in the parent process"
        ),
        stderr=(
            "AWS_BEARER_TOKEN_BEDROCK is missing from os.environ. "
            "Set it with `export AWS_BEARER_TOKEN_BEDROCK=...` before running ZeroMDASH."
        ),
        env_overlay={
            key: "<redacted>" if key == "AWS_BEARER_TOKEN_BEDROCK" and value is not None else value
            for key, value in env.items()
        },
    )


def _format_health_failure(node: str, health: AgentHealth) -> str:
    lines = [f"node {node}: runtime {health.name} is unhealthy: {health.message}"]
    args = f" args={health.extra_args}" if health.extra_args else ""
    lines.append(f"  - {health.name}{args} ({health.binary or 'unknown binary'})")
    if health.command:
        lines.append(f"    command: {json.dumps(health.command, ensure_ascii=False)}")
    if health.env_overlay:
        lines.append(f"    env_overlay: {json.dumps(health.env_overlay, ensure_ascii=False)}")
    if health.stderr:
        lines.append(f"    stderr: {health.stderr}")
    if health.stdout:
        lines.append(f"    stdout: {health.stdout}")
    return "\n".join(lines)


def _temporary_node_config(
    node: str, current: nodes.AgentNodeConfig, current_runtime: str,
    *, reason: str = "health check failed",
) -> nodes.AgentNodeConfig:
    click.echo(f"ZeroMDASH paused: {reason} for node {node!r}.", err=True)
    click.echo("Please provide a temporary runtime/config/provider/model for this node.", err=True)
    runtime = click.prompt("runtime", default=current_runtime, show_default=True)
    config = click.prompt("config", default=current.get("config", ""), show_default=True)
    provider = click.prompt("provider", default=current.get("provider", ""), show_default=True)
    model = click.prompt("model", default=current.get("model", ""), show_default=True)
    next_cfg = dict(current)
    next_cfg["runtime"] = normalize_agent_name(runtime)
    next_cfg["config"] = _normalize_config_value(next_cfg["runtime"], config)
    next_cfg["provider"] = str(provider).strip().lower()
    normalized_model = _normalize_model_value(model)
    if "model" in current or normalized_model:
        next_cfg["model"] = normalized_model
    else:
        next_cfg.pop("model", None)
    next_cfg.pop("fallbacks", None)
    return next_cfg


def _recover_runtime_config(request: RecoveryRequest) -> nodes.AgentNodeConfig:
    """Called with the recovery coordinator's terminal lock held."""
    click.echo(
        f"Runtime recovery: node={request.node} subtask={request.subtask_id or '-'}\n"
        f"Failure: {request.failure}\nLogs: {request.log_dir}",
        err=True,
    )
    current = request.current
    timeout = int(os.environ.get("ZEROMDASH_AGENT_HEALTHCHECK_TIMEOUT", "60"))
    while True:
        try:
            current = _temporary_node_config(
                request.node, current, current["runtime"],
                reason="automatic retries and explicit fallbacks exhausted",
            )
        except (click.Abort, EOFError, KeyboardInterrupt) as exc:
            raise RuntimeRecoveryAborted("no temporary configuration was provided") from exc
        try:
            configs = {request.node: current}
            nodes.agent_config_variants_for_node(request.node, None, configs)
            backend = current["runtime"]
            agent = get_agent(backend)
            args = nodes.agent_extra_args_for_node(request.node, backend, configs)
            env = nodes.agent_env_for_node(request.node, backend, configs)
            health = _bedrock_env_health_error(backend, env) or check_agent_health(
                agent, timeout=timeout, extra_args=args or None, env=env or None,
            )
        except (ValueError, OSError) as exc:
            click.echo(f"Invalid temporary configuration: {exc}", err=True)
            continue
        if health.ok:
            click.echo(f"Temporary configuration verified; retrying {request.node}.", err=True)
            return current
        click.echo(_format_health_failure(request.node, health), err=True)


def _resolve_startup_backends(
    overrides: dict[str, str],
    agent_configs: nodes.AgentConfigs | None = None,
    disabled_nodes: set[str] | None = None,
) -> tuple[dict[str, str], dict[tuple[str, tuple[str, ...], tuple[tuple[str, str | None], ...]], AgentHealth]]:
    """Health-check each node's configured primary runtime and explicit fallbacks."""
    unknown_nodes = sorted(set(overrides) - set(nodes.DEFAULT_BACKENDS))
    if unknown_nodes:
        raise click.ClickException(f"unknown --backend node(s): {', '.join(unknown_nodes)}")

    disabled = set(disabled_nodes or [])
    timeout = int(os.environ.get("ZEROMDASH_AGENT_HEALTHCHECK_TIMEOUT", "60"))
    health_cache: dict[tuple[str, tuple[str, ...], tuple[tuple[str, str | None], ...]], AgentHealth] = {}
    selected: dict[str, str] = {}
    agent_configs = agent_configs if agent_configs is not None else {}

    for node in nodes.DEFAULT_BACKENDS:
        if node in disabled:
            continue
        while True:
            variants = nodes.agent_config_variants_for_node(node, overrides, agent_configs)
            unhealthy: tuple[str, nodes.AgentNodeConfig, AgentHealth] | None = None
            for variant in variants:
                backend = normalize_agent_name(variant["runtime"])
                variant_configs = nodes._agent_configs_with_node_variant(agent_configs, node, variant)
                extra_args = nodes.agent_extra_args_for_node(node, backend, variant_configs)
                env = nodes.agent_env_for_node(node, backend, variant_configs)
                key = _health_key(backend, extra_args, env)
                if key not in health_cache:
                    health_cache[key] = _bedrock_env_health_error(backend, env) or check_agent_health(
                        get_agent(backend), timeout=timeout, extra_args=extra_args or None, env=env or None
                    )
                health = health_cache[key]
                if not health.ok:
                    unhealthy = (backend, variant, health)
                    break
            if unhealthy is None:
                selected[node] = normalize_agent_name(variants[0]["runtime"])
                break
            backend, failed_variant, health = unhealthy
            click.echo(_format_health_failure(node, health), err=True)
            try:
                agent_configs[node] = _temporary_node_config(
                    node, failed_variant, backend
                )
            except (click.Abort, EOFError) as exc:
                raise click.ClickException(
                    "ZeroMDASH startup agent health check failed and no temporary "
                    f"configuration was provided.\n{_format_health_failure(node, health)}"
                ) from exc

    return selected, health_cache


@click.command()
@click.option("--target", default=None, help="Target software identifier / path / URL.")
@click.option(
    "--scan-mode",
    type=click.Choice(["full", "diff", "gather"]),
    default="full",
    show_default=True,
    help="Run a full scan, a diff-highlighted scan, or gather completed workspaces into cross-target chains.",
)
@click.option(
    "--gather-workspace-to-chain",
    "gather_workspace_to_chain",
    type=click.Path(exists=True, dir_okay=False, path_type=str),
    default=None,
    metavar="MULTI_TARGET_CONFIG",
    help="Aggregate completed target workspaces into cross-target attack chains.",
)
@click.option(
    "--diff-file",
    type=click.Path(exists=True, dir_okay=False, path_type=str),
    default=None,
    metavar="PATCH",
    help="Unified git diff describing changes already present in the target repository.",
)
@click.option(
    "--diff-git",
    default=None,
    metavar="BEFORE..AFTER",
    help="Generate the highlighted diff from two refs in the fetched remote git repository.",
)
@click.option(
    "--common-focus",
    "--focus",
    "common_focus",
    default="",
    show_default=False,
    hidden=True,
    help="Optional global focus / analysis hint shared by focus-aware stages. --focus is kept as an alias.",
)
@click.option(
    "--fetch-target-repo-focus",
    default="",
    show_default=False,
    hidden=True,
    help="Optional focus hint used only by the repository acquisition stage.",
)
@click.option(
    "--search-fuzz-driver-focus",
    default="",
    show_default=False,
    hidden=True,
    help="Optional focus hint used only when searching fuzz drivers.",
)
@click.option(
    "--search-similar-software-focus",
    default="",
    show_default=False,
    hidden=True,
    help="Optional focus hint used only when searching similar software.",
)
@click.option(
    "--search-target-history-focus",
    default="",
    show_default=False,
    hidden=True,
    help="Optional focus hint used only when searching target vulnerability history.",
)
@click.option(
    "--search-new-feature-focus",
    default="",
    show_default=False,
    hidden=True,
    help="Optional focus hint used only when searching new or weakly-covered feature surfaces.",
)
@click.option(
    "--analyze-attack-surface-focus",
    default="",
    show_default=False,
    hidden=True,
    help="Optional focus hint used only by attack-surface analysis.",
)
@click.option(
    "--summary-focus",
    default="",
    show_default=False,
    hidden=True,
    help="Optional focus hint used only by final summary.",
)
@click.option(
    "--workspace-root",
    default="./.zeromdash",
    show_default=True,
    help="Directory under which a per-task workspace is created.",
)
@click.option("--task-id", default=None, help="Override auto-generated task id.")
@click.option(
    "--max-iterations",
    default=3,
    show_default=True,
    type=int,
    help="Max investigate<->critic feedback rounds per subtask.",
)
@click.option(
    "--min-critic-skills",
    default=2,
    show_default=True,
    type=int,
    help="Critic must select at least this many expert skills per review.",
)
@click.option(
    "--role-lang",
    default="en",
    show_default=True,
    help="Language for node role cards. Use zh_CN for Chinese role prompts.",
)
@click.option(
    "--backend",
    "backends",
    multiple=True,
    metavar="NODE=AGENT",
    hidden=True,
    help="Override the agent backend for a given node (repeatable). "
         "Example: --backend search_spec=codex --backend summary=claude_code",
)
@click.option(
    "--agent-config",
    "agent_config_path",
    type=click.Path(dir_okay=False, path_type=str),
    default=None,
    metavar="YAML_FILE",
    help="YAML file mapping node name to runtime/config/provider/env. "
         "Example: --agent-config ./zeromdash-agents.yaml",
)
@click.option(
    "--preset-attack-surface",
    "preset_attack_surface_path",
    type=click.Path(exists=True, dir_okay=False, path_type=str),
    default=None,
    metavar="ATTACK_SURFACE_MD",
    help="Seed main/attack_surface/attack_surface.md from this Markdown file; "
         "analyze_attack_surface appends its findings to the seeded report.",
)
@click.option(
    "--disable-spec",
    "disable_spec",
    is_flag=True,
    default=False,
    help="Skip the spec track: search_spec + plan_by_spec. spec subtasks are "
         "starved of subtasks and do not run either. Useful to cut cost when "
         "spec-compliance checking is not the priority.",
)
@click.option(
    "--disable-target-history",
    "disable_target_history",
    is_flag=True,
    default=False,
    help="Skip target-history analysis: search_target_history + plan_by_vuln_patch. "
         "Useful for private software where target vulnerability history is "
         "unavailable or should not be searched.",
)
@click.option(
    "--disable-new-feature",
    "disable_new_feature",
    is_flag=True,
    default=False,
    help="Skip new-feature coverage-gap analysis: search_new_feature + plan_by_new_feature.",
)
@click.option(
    "--disable-chain",
    "disable_chain",
    is_flag=True,
    default=False,
    help="Skip cross-primitive chain planning and chain agent battles.",
)
@click.option(
    "--till-node",
    type=click.Choice(["analyze", "plan"]),
    default=None,
    help="Stop after a pipeline stage: analyze stops after analyze_attack_surface; "
         "plan stops after all enabled planners materialize plan JSON.",
)
@click.option(
    "--start-from-subtask",
    "--start-from-subagent",
    "start_from_subtask",
    type=click.Path(file_okay=False, path_type=str),
    default=None,
    metavar="WORKSPACE",
    help="Restore from an existing ZeroMDASH workspace and start at subtask dispatch "
         "using materialized planner JSON files under log/state/ (with legacy "
         "log/review_log/ fallback).",
)
@click.option(
    "--start-from-summary",
    "start_from_summary",
    type=click.Path(file_okay=False, path_type=str),
    default=None,
    metavar="WORKSPACE",
    help="Restore from an existing ZeroMDASH workspace and run only summary "
         "using log/subtask_res/*.json (with legacy log/review_res fallback).",
)
@click.option(
    "--start-from-chain",
    "start_from_chain",
    type=click.Path(file_okay=False, path_type=str),
    default=None,
    metavar="WORKSPACE",
    help="Restore from an existing ZeroMDASH workspace and start at chain planning "
         "using log/subtask_res and log/primitive_res (with legacy review_res fallback).",
)
@click.option(
    "--start-from-polish-report",
    "start_from_polish_report",
    type=click.Path(file_okay=False, path_type=str),
    default=None,
    metavar="WORKSPACE",
    help="Restore from an existing ZeroMDASH workspace and run only the "
         "lightweight report polish/formatting pass over existing summary files.",
)
@click.option(
    "--select-subtask-to-run",
    "--select-subagent-to-run",
    "select_subtask_to_run",
    default=None,
    metavar="ID[,ID...]",
    help="With --start-from-subtask, rerun only the selected planner subtask IDs. "
         "This mode stops after subtask status collection and does not run summary.",
)
@click.option(
    "--select-subtask-to-run-log-dir",
    "--select-subagent-to-run-log-dir",
    "select_subtask_to_run_log_dir",
    type=click.Path(file_okay=False, path_type=str),
    default=None,
    metavar="DIR",
    help="Output directory for a selected-subtask run. Relative paths are resolved "
         "under the workspace. By default a new log/selected_temp_<timestamp>/ "
         "directory is created.",
)
@click.option(
    "--select-chain-to-run",
    "select_chain_to_run",
    default=None,
    metavar="ID[,ID...]",
    help="With --start-from-chain, rerun only the selected chain IDs. "
         "This mode stops after chain status collection and does not run summary.",
)
@click.option(
    "--select-chain-to-run-log-dir",
    "select_chain_to_run_log_dir",
    type=click.Path(file_okay=False, path_type=str),
    default=None,
    metavar="DIR",
    help="Output directory for a selected-chain run. Relative paths are resolved "
         "under the workspace. By default a new log/selected_chain_runs/<timestamp>/ "
         "directory is created.",
)
@click.option(
    "--fail-on-gate",
    is_flag=True,
    default=False,
    help="Return a non-zero exit code when diff/gather gate_result.json decides block.",
)
def main(
    target: str | None,
    scan_mode: str,
    gather_workspace_to_chain: str | None,
    diff_file: str | None,
    diff_git: str | None,
    common_focus: str,
    fetch_target_repo_focus: str,
    search_fuzz_driver_focus: str,
    search_similar_software_focus: str,
    search_target_history_focus: str,
    search_new_feature_focus: str,
    analyze_attack_surface_focus: str,
    summary_focus: str,
    workspace_root: str,
    task_id: str | None,
    max_iterations: int,
    min_critic_skills: int,
    role_lang: str,
    backends: tuple[str, ...],
    agent_config_path: str | None,
    preset_attack_surface_path: str | None,
    disable_spec: bool,
    disable_target_history: bool,
    disable_new_feature: bool,
    disable_chain: bool,
    till_node: str | None,
    start_from_subtask: str | None,
    start_from_chain: str | None,
    start_from_summary: str | None,
    start_from_polish_report: str | None,
    select_subtask_to_run: str | None,
    select_subtask_to_run_log_dir: str | None,
    select_chain_to_run: str | None,
    select_chain_to_run_log_dir: str | None,
    fail_on_gate: bool,
) -> None:
    restore_modes = [
        bool(start_from_subtask),
        bool(start_from_chain),
        bool(start_from_summary),
        bool(start_from_polish_report),
    ]
    if sum(restore_modes) > 1:
        raise click.ClickException(
            "--start-from-subtask, --start-from-chain, --start-from-summary, and "
            "--start-from-polish-report are mutually exclusive"
        )
    selected_subtask_ids = [
        item.strip()
        for item in (select_subtask_to_run or "").split(",")
        if item.strip()
    ]
    if select_subtask_to_run is not None and not start_from_subtask:
        raise click.ClickException(
            "--select-subtask-to-run requires --start-from-subtask"
        )
    if select_subtask_to_run is not None and not selected_subtask_ids:
        raise click.ClickException(
            "--select-subtask-to-run requires at least one subtask id"
        )
    if (
        select_subtask_to_run_log_dir is not None
        and select_subtask_to_run is None
    ):
        raise click.ClickException(
            "--select-subtask-to-run-log-dir requires --select-subtask-to-run"
        )
    selected_chain_ids = [
        item.strip()
        for item in (select_chain_to_run or "").split(",")
        if item.strip()
    ]
    if select_chain_to_run is not None and not start_from_chain:
        raise click.ClickException(
            "--select-chain-to-run requires --start-from-chain"
        )
    if select_chain_to_run is not None and not selected_chain_ids:
        raise click.ClickException(
            "--select-chain-to-run requires at least one chain id"
        )
    if select_chain_to_run_log_dir is not None and select_chain_to_run is None:
        raise click.ClickException(
            "--select-chain-to-run-log-dir requires --select-chain-to-run"
        )
    overrides: dict[str, str] = {}
    for spec in backends:
        if "=" not in spec:
            click.echo(f"invalid --backend value: {spec!r}", err=True)
            sys.exit(2)
        node, agent = spec.split("=", 1)
        overrides[nodes.canonical_node_name(node.strip())] = agent.strip()

    gather_manifest: dict[str, object] | None = None
    if scan_mode == "gather":
        if not gather_workspace_to_chain:
            raise click.ClickException(
                "--scan-mode gather requires --gather-workspace-to-chain"
            )
        if target:
            raise click.ClickException("--scan-mode gather cannot be combined with --target")
        if any(restore_modes):
            raise click.ClickException("--scan-mode gather cannot be combined with single-workspace restore modes")
        if diff_file or diff_git:
            raise click.ClickException("--scan-mode gather cannot be combined with --diff-file or --diff-git")
        if preset_attack_surface_path:
            raise click.ClickException("--scan-mode gather cannot be combined with --preset-attack-surface")
        if disable_spec or disable_target_history or disable_new_feature or disable_chain:
            raise click.ClickException("--scan-mode gather cannot be combined with discovery/chain disable flags")
        if till_node:
            raise click.ClickException("--scan-mode gather does not support --till-node")
        try:
            gather_manifest = load_gather_manifest(gather_workspace_to_chain)
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
        if not agent_config_path:
            agent_config_path = str(gather_manifest.get("gather_agent_config") or "") or None
    elif gather_workspace_to_chain:
        raise click.ClickException(
            "--gather-workspace-to-chain requires --scan-mode gather"
        )

    agent_configs = _parse_agent_config_file(agent_config_path)
    config_common_focus = _pop_common_focus_from_agent_config(agent_configs)
    top_K = _pop_top_k_from_agent_config(agent_configs)
    chain_config = _pop_chain_config_from_agent_config(agent_configs)
    gather_config = _pop_gather_config_from_agent_config(agent_configs)
    if scan_mode == "gather" and gather_config.get("require_cross_target") is False:
        raise click.ClickException("gather.require_cross_target cannot be false in --scan-mode gather")
    max_concurrency = _pop_max_concurrency_from_agent_config(agent_configs)
    target_repos = _pop_target_repos_from_agent_config(agent_configs)
    common_focus = common_focus or config_common_focus
    if scan_mode != "gather" and not target and target_repos and not any(restore_modes):
        target = "multi-repo-target"
    if scan_mode != "gather" and not target and not any(restore_modes):
        raise click.ClickException("--target is required unless a restore mode is used")
    if scan_mode == "diff" and not (diff_file or diff_git) and not any(restore_modes):
        raise click.ClickException("--scan-mode diff requires --diff-file or --diff-git")
    if diff_file and diff_git:
        raise click.ClickException("--diff-file and --diff-git are mutually exclusive")
    if scan_mode == "full" and (diff_file or diff_git) and not any(restore_modes):
        raise click.ClickException("--diff-file/--diff-git require --scan-mode diff")
    if any(restore_modes) and (diff_file or diff_git):
        raise click.ClickException("restore modes cannot be combined with --diff-file or --diff-git")
    if diff_git and target and Path(target).expanduser().is_dir():
        raise click.ClickException(
            "--diff-git is for remotely fetched git targets; local directory targets use --diff-file"
        )
    if target_repos and scan_mode != "full":
        raise click.ClickException(
            "multi-repo target_repos currently support --scan-mode full only"
        )
    disabled_nodes: set[str] = set()
    if disable_spec:
        disabled_nodes.update({"search_spec", "plan_by_spec"})
    if disable_target_history:
        disabled_nodes.update({"search_target_history", "plan_by_vuln_patch"})
    if disable_new_feature:
        disabled_nodes.update({"search_new_feature", "plan_by_new_feature"})
    if disable_chain:
        disabled_nodes.update({"plan_chains", "chain_investigate_subtask", "chain_critic_subtask"})
    if any(restore_modes) and till_node:
        raise click.ClickException("restore modes cannot be combined with --till-node")
    if any(restore_modes) and preset_attack_surface_path:
        raise click.ClickException("restore modes cannot be combined with --preset-attack-surface")

    startup_disabled_nodes = set(disabled_nodes)
    if scan_mode == "gather":
        if target_repos:
            raise click.ClickException("gather agent config cannot define target_repos")
        startup_disabled_nodes.update(set(nodes.DEFAULT_BACKENDS) - _GATHER_GRAPH_AGENT_NODES)
    else:
        startup_disabled_nodes.update(_GATHER_ONLY_NODES)
    if start_from_subtask:
        startup_disabled_nodes.update(_START_FROM_SUBTASK_DISABLED_NODES)
        if select_subtask_to_run is not None:
            startup_disabled_nodes.update({"summary", "polish_report"})
        elif disable_chain:
            startup_disabled_nodes.update({"chain_investigate_subtask", "chain_critic_subtask"})
    elif start_from_chain:
        startup_disabled_nodes.update(_START_FROM_CHAIN_DISABLED_NODES)
        if select_chain_to_run is not None:
            startup_disabled_nodes.update({"summary", "polish_report"})
        elif disable_chain:
            startup_disabled_nodes.update({"chain_investigate_subtask", "chain_critic_subtask"})
    elif start_from_summary:
        startup_disabled_nodes.update(_START_FROM_SUMMARY_DISABLED_NODES)
    elif start_from_polish_report:
        startup_disabled_nodes.update(_START_FROM_POLISH_REPORT_DISABLED_NODES)
    elif till_node == "analyze":
        startup_disabled_nodes.update(_TILL_ANALYZE_DISABLED_NODES)
    elif till_node == "plan":
        startup_disabled_nodes.update(_TILL_PLAN_DISABLED_NODES)
    try:
        selected_backends, _health = _resolve_startup_backends(
            overrides, agent_configs, startup_disabled_nodes
        )
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    def execute_workflow():
        if scan_mode == "gather":
            assert gather_manifest is not None
            try:
                final = run_gather(
                    manifest=gather_manifest,
                    workspace_root=workspace_root,
                    task_id=task_id,
                    backends=selected_backends,
                    min_critic_skills=min_critic_skills,
                    role_lang=role_lang,
                    agent_configs=agent_configs,
                    common_focus=common_focus,
                    top_K=top_K,
                    gather_config=gather_config,
                    max_concurrency=max_concurrency,
                )
            except ValueError as exc:
                raise click.ClickException(str(exc)) from exc
        elif start_from_subtask:
            try:
                final = run_from_subtask_workspace(
                    workspace_path=start_from_subtask,
                    backends=selected_backends,
                    max_iterations=max_iterations,
                    min_critic_skills=min_critic_skills,
                    common_focus=common_focus,
                    agent_configs=agent_configs,
                    top_K=top_K,
                    chain_config=chain_config,
                    disabled_nodes=disabled_nodes,
                    max_concurrency=max_concurrency,
                    selected_subtask_ids=(
                        selected_subtask_ids
                        if select_subtask_to_run is not None
                        else None
                    ),
                    selected_subtask_log_dir=select_subtask_to_run_log_dir,
                    run_summary=select_subtask_to_run is None,
                )
            except ValueError as exc:
                raise click.ClickException(str(exc)) from exc
        elif start_from_chain:
            try:
                final = run_from_chain_workspace(
                    workspace_path=start_from_chain,
                    backends=selected_backends,
                    max_iterations=max_iterations,
                    min_critic_skills=min_critic_skills,
                    common_focus=common_focus,
                    agent_configs=agent_configs,
                    top_K=top_K,
                    chain_config=chain_config,
                    disabled_nodes=disabled_nodes,
                    max_concurrency=max_concurrency,
                    selected_chain_ids=(
                        selected_chain_ids if select_chain_to_run is not None else None
                    ),
                    selected_chain_log_dir=select_chain_to_run_log_dir,
                    run_summary=select_chain_to_run is None,
                )
            except ValueError as exc:
                raise click.ClickException(str(exc)) from exc
        elif start_from_summary:
            try:
                final = run_summary_from_workspace(
                    workspace_path=start_from_summary,
                    backends=selected_backends,
                    common_focus=common_focus,
                    agent_configs=agent_configs,
                    max_concurrency=max_concurrency,
                )
            except ValueError as exc:
                raise click.ClickException(str(exc)) from exc
        elif start_from_polish_report:
            try:
                final = run_polish_report_from_workspace(
                    workspace_path=start_from_polish_report,
                    common_focus=common_focus,
                    agent_configs=agent_configs,
                    max_concurrency=max_concurrency,
                )
            except ValueError as exc:
                raise click.ClickException(str(exc)) from exc
        else:
            final = run(
                target=target or "",
                workspace_root=workspace_root,
                task_id=task_id,
                backends=selected_backends,
                max_iterations=max_iterations,
                min_critic_skills=min_critic_skills,
                common_focus=common_focus,
                scan_mode=scan_mode,
                diff_file=diff_file or "",
                diff_git=diff_git or "",
                fetch_target_repo_focus=fetch_target_repo_focus,
                search_fuzz_driver_focus=search_fuzz_driver_focus,
                search_similar_software_focus=search_similar_software_focus,
                search_target_history_focus=search_target_history_focus,
                search_new_feature_focus=search_new_feature_focus,
                analyze_attack_surface_focus=analyze_attack_surface_focus,
                summary_focus=summary_focus,
                role_lang=role_lang,
                agent_configs=agent_configs,
                preset_attack_surface_path=preset_attack_surface_path,
                target_repos=target_repos,
                top_K=top_K,
                chain_config=chain_config,
                max_concurrency=max_concurrency,
                disabled_nodes=disabled_nodes,
                till_node=till_node,
            )
        return final

    recovery = RuntimeRecovery(_recover_runtime_config)
    try:
        final = recovery.run(execute_workflow)
    except RuntimeRecoveryAborted as exc:
        raise click.ClickException(str(exc)) from exc
    if recovery.overrides():
        final["agent_configs"] = {
            **(final.get("agent_configs") or agent_configs), **recovery.overrides(),
        }

    # 短进程退出前 flush Langfuse,避免末尾 trace 丢失。
    if langfuse_is_configured():
        from langfuse import get_client

        get_client().flush()

    final_state_path = _write_final_state(final)
    click.echo(f"final state written to {final_state_path}", err=True)
    if select_subtask_to_run is not None:
        click.echo("\n=== selected subtask statuses ===\n")
        for item in final.get("selected_subtask_statuses") or []:
            click.echo(
                f"{item.get('subtask_id', '')}: {item.get('status', '')}"
                f" verdict={item.get('verdict', '')}"
                f" severity={item.get('severity', '')}"
                f" iterations={item.get('iterations', 0)}"
            )
    elif select_chain_to_run is not None:
        click.echo("\n=== selected chain statuses ===\n")
        for item in final.get("selected_chain_statuses") or []:
            click.echo(
                f"{item.get('chain_id', '')}: {item.get('status', '')}"
                f" verdict={item.get('verdict', '')}"
            )
    else:
        click.echo("\n=== summary ===\n")
        click.echo(final.get("summary", ""))
    if fail_on_gate and final.get("gate_result", {}).get("decision") == "block":
        raise click.exceptions.Exit(2)


if __name__ == "__main__":
    main()
