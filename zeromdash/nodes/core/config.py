"""Per-node runtime selection and agent configuration."""

from __future__ import annotations

import copy
import os
from typing import Any, TypedDict

from zeromdash.agents import AgentEnv, normalize_agent_name, supports_native_subagents

from .constants import *

class AgentNodeConfig(TypedDict, total=False):
    runtime: str
    provider: str
    config: str
    model: str
    env: AgentEnv
    focus: str
    fallbacks: list[dict[str, Any]]

AgentConfigs = dict[str, AgentNodeConfig]
AgentConfigTaskTypes = dict[str, str]  # legacy; accepted but no longer used for fallback selection

_MODEL_ENV_BY_BACKEND = {
    "codex": "ZEROMDASH_CODEX_MODEL",
    "traex": "ZEROMDASH_TRAEX_MODEL",
    "claude_code": "ZEROMDASH_CLAUDE_MODEL",
    "kimi": "ZEROMDASH_KIMI_MODEL",
    "opencode": "ZEROMDASH_OPENCODE_MODEL",
}

def canonical_node_name(node: str) -> str:
    return NODE_NAME_ALIASES.get(str(node), str(node))

def agent_config_for_node(node: str, agent_configs: AgentConfigs | None) -> AgentNodeConfig:
    canonical = canonical_node_name(node)
    configs = agent_configs or {}
    if canonical in configs:
        return configs[canonical]
    if canonical == "investigate_subtask" and "investigate_subagent" in configs:
        return configs["investigate_subagent"]
    if canonical == "critic_subtask" and "critic_one" in configs:
        return configs["critic_one"]
    return configs.get(node, {})

def _strip_fallbacks(config: AgentNodeConfig) -> AgentNodeConfig:
    cleaned: AgentNodeConfig = dict(config)
    cleaned.pop("fallbacks", None)
    return cleaned

def runtime_for_node(
    node: str,
    backends: dict[str, str] | None,
    agent_configs: AgentConfigs | None = None,
) -> str:
    node = canonical_node_name(node)
    cfg_runtime = agent_config_for_node(node, agent_configs).get("runtime")
    overrides = backends or {}
    override = overrides.get(node)
    if override is None and node == "investigate_subtask":
        override = overrides.get("investigate_subagent")
    if override is None and node == "critic_subtask":
        override = overrides.get("critic_one")
    return normalize_agent_name(override or cfg_runtime or DEFAULT_BACKENDS[node])

def agent_config_variants_for_node(
    node: str,
    backends: dict[str, str] | None,
    agent_configs: AgentConfigs | None = None,
) -> list[AgentNodeConfig]:
    """Return primary config followed by explicit fallback runtime configs."""
    node = canonical_node_name(node)
    primary_raw = agent_config_for_node(node, agent_configs)
    primary = _strip_fallbacks(copy.deepcopy(primary_raw))
    primary["runtime"] = runtime_for_node(node, backends, agent_configs)
    variants: list[AgentNodeConfig] = [primary]
    default_fallback_runtime = primary["runtime"]
    for fallback_raw in primary_raw.get("fallbacks") or []:
        fallback: AgentNodeConfig = _strip_fallbacks(copy.deepcopy(fallback_raw))
        fallback["runtime"] = normalize_agent_name(fallback.get("runtime") or default_fallback_runtime)
        variants.append(fallback)
    validate_native_subagent_runtime_variants(node, variants)
    return variants

def validate_native_subagent_runtime_variants(
    node: str,
    variants: list[AgentNodeConfig],
) -> None:
    node = canonical_node_name(node)
    if node not in NATIVE_SUBAGENT_REQUIRED_NODES:
        return
    unsupported = sorted(
        {
            normalize_agent_name(str(variant.get("runtime") or ""))
            for variant in variants
            if not supports_native_subagents(str(variant.get("runtime") or ""))
        }
    )
    if unsupported:
        raise ValueError(
            f"node {node!r} requires a harness with native subagent support; "
            f"unsupported runtime(s): {', '.join(unsupported)}; "
            "supported runtimes: claude_code, codex, dsh, traex"
        )

def _agent_configs_with_node_variant(
    agent_configs: AgentConfigs | None,
    node: str,
    variant: AgentNodeConfig,
) -> AgentConfigs:
    node = canonical_node_name(node)
    selected: AgentConfigs = copy.deepcopy(agent_configs or {})
    selected.pop("investigate_subagent", None)
    selected.pop("critic_one", None)
    selected[node] = _strip_fallbacks(copy.deepcopy(variant))
    return selected

def agent_extra_args_for_node(
    node: str,
    backend: str,
    agent_configs: AgentConfigs | None,
    agent_config_task_types: AgentConfigTaskTypes | None = None,
    task_type_override: str | None = None,
) -> list[str]:
    del agent_config_task_types, task_type_override
    node = canonical_node_name(node)
    backend = normalize_agent_name(backend)
    config = agent_config_for_node(node, agent_configs)
    args: list[str] = []
    if node in NATIVE_SUBAGENT_REQUIRED_NODES:
        if backend == "codex":
            args += ["--enable", "multi_agent"]
        elif backend == "traex":
            args += ["--config", "features.multi_agent_v2.enabled=true"]
    value = config.get("config", "")
    if value:
        if backend == "claude_code":
            args += ["--settings", value]
        elif backend in {"codex", "traex"}:
            args += ["--profile", value]
        elif backend == "dsh":
            args += ["--patch", value]

    model = str(config.get("model", "")).strip()
    if model and backend not in {"deepagent", "dsh"}:
        args += ["--model", model]
    return args

def _clear_backend_model_env_if_configured(
    env: AgentEnv,
    backend: str,
    config: AgentNodeConfig,
) -> None:
    """Let per-node `model` own the command-line model when configured."""
    if "model" not in config:
        return
    env_name = _MODEL_ENV_BY_BACKEND.get(normalize_agent_name(backend))
    if env_name:
        env[env_name] = None

def agent_env_for_node(
    node: str,
    backend: str,
    agent_configs: AgentConfigs | None,
    agent_config_task_types: AgentConfigTaskTypes | None = None,
    task_type_override: str | None = None,
) -> AgentEnv:
    del agent_config_task_types, task_type_override
    backend = normalize_agent_name(backend)
    config = agent_config_for_node(node, agent_configs)
    explicit_env = dict(config.get("env") or {})
    if backend == "dsh":
        provider = str(config.get("provider", "")).strip()
        model = str(config.get("model", "")).strip()
        if "provider" in config:
            explicit_env["ZEROMDASH_DSH_PROVIDER"] = provider or None
        if "model" in config:
            explicit_env["ZEROMDASH_DSH_MODEL"] = model or None
        return explicit_env
    if backend != "claude_code":
        _clear_backend_model_env_if_configured(explicit_env, backend, config)
        return explicit_env

    provider = config.get("provider", "").strip().lower()
    if provider == "bedrock":
        env: AgentEnv = {
            "CLAUDE_CODE_USE_BEDROCK": "1",
            "ZEROMDASH_CLAUDE_MODEL": None,
            "ZEROMDASH_CLAUDE_SETTINGS_PATH": config.get("config", ""),
            "ANTHROPIC_AUTH_TOKEN": None,
            "ANTHROPIC_BASE_URL": None,
            "ANTHROPIC_MODEL": None,
            "ANTHROPIC_SMALL_FAST_MODEL": None,
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": None,
            "ANTHROPIC_DEFAULT_SONNET_MODEL": None,
            "ANTHROPIC_DEFAULT_OPUS_MODEL": None,
            "CLAUDE_CODE_SUBAGENT_MODEL": None,
        }
        token = os.environ.get("AWS_BEARER_TOKEN_BEDROCK")
        if token is not None:
            env["AWS_BEARER_TOKEN_BEDROCK"] = token
        env.update(explicit_env)
        _clear_backend_model_env_if_configured(env, backend, config)
        return env

    env = {
        "CLAUDE_CODE_USE_BEDROCK": None,
        "AWS_BEARER_TOKEN_BEDROCK": None,
    }
    env.update(explicit_env)
    _clear_backend_model_env_if_configured(env, backend, config)
    return env

def _resolve_backend(node: str, overrides: dict[str, str] | None) -> str:
    return normalize_agent_name((overrides or {}).get(node, DEFAULT_BACKENDS[node]))

def backend_fallback_chain(node: str, overrides: dict[str, str] | None = None) -> list[str]:
    """Return the single configured runtime for compatibility with older callers."""
    return [normalize_agent_name((overrides or {}).get(node, DEFAULT_BACKENDS[node]))]

__all__ = ["AgentNodeConfig","canonical_node_name","agent_config_for_node","_strip_fallbacks","runtime_for_node","agent_config_variants_for_node","validate_native_subagent_runtime_variants","_agent_configs_with_node_variant","agent_extra_args_for_node","_clear_backend_model_env_if_configured","agent_env_for_node","_resolve_backend","backend_fallback_chain","AgentConfigs","AgentConfigTaskTypes","_MODEL_ENV_BY_BACKEND"]

