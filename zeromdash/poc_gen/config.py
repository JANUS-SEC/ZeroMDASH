"""PoC generation configuration defaults and normalization."""

from __future__ import annotations

from typing import Any

DEFAULT_POC_CONFIG: dict[str, Any] = {
    "enabled": False,
    "backend": "agent_sandbox",
    "max_findings": 8,
    "max_strategies_per_round": 3,
    "max_debug_rounds_per_strategy": 4,
    "max_no_progress_rounds": 2,
    "verification_runs": 3,
    "verification_min_matches": 2,
}
POC_CONFIG_KEYS = frozenset(DEFAULT_POC_CONFIG)
POC_PHASE_NODES = {
    "plan_poc": "plan_poc",
    "prepare_environment": "prepare_environment_and_debugger",
    "generate_poc": "generate_poc",
    "execute_poc": "build_and_execute_poc",
    "debug_poc": "debug_poc",
    "verify_poc": "verify_poc",
    "release_poc": "release_poc",
}
POC_AGENT_NODES = tuple(POC_PHASE_NODES.values())


def normalize_poc_config(value: dict[str, Any] | None, *, force_enabled: bool = False) -> dict[str, Any]:
    config = {**DEFAULT_POC_CONFIG, **dict(value or {})}
    if force_enabled:
        config["enabled"] = True
    if config["backend"] != "agent_sandbox":
        raise ValueError("only poc.backend=agent_sandbox is currently implemented")
    if config["verification_min_matches"] > config["verification_runs"]:
        raise ValueError("poc.verification_min_matches cannot exceed verification_runs")
    return config
