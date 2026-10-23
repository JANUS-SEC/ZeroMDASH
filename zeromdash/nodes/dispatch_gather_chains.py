"""Dispatch cross-target candidates into isolated gather-chain subgraphs."""

from __future__ import annotations

from typing import Any

from langgraph.constants import Send

from zeromdash.gather_state import GatherState


def dispatch_gather_chains(state: GatherState, *, backends=None) -> dict:
    del state, backends
    return {}


def _max_iterations(state: GatherState) -> int:
    raw = (state.get("gather_config") or {}).get("max_battle_rounds", 3)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return 3
    return value if value > 0 else 3


def dispatch_all_gather_chains(state: GatherState) -> list[Send] | str:
    sends: list[Send] = []
    for candidate in state.get("gather_chain_plan") or []:
        chain_id = str(candidate.get("chain_id") or "")
        if not chain_id:
            continue
        child: dict[str, Any] = {
            "task_id": state["task_id"],
            "workspace_root": state["workspace_root"],
            "target": state.get("target", ""),
            "scenario_name": state.get("scenario_name", ""),
            "scenario": state.get("scenario", ""),
            "manifest_hash": state.get("manifest_hash", ""),
            "input_lock_path": state.get("input_lock_path", ""),
            "gather_targets": list(state.get("gather_targets") or []),
            "source_read_roots": list(state.get("source_read_roots") or []),
            "gather_chain_candidate": candidate,
            "gather_evidence_pool": list(state.get("gather_evidence_pool") or []),
            "gather_evidence_pool_path": state.get("gather_evidence_pool_path", ""),
            "gather_attack_surface": state.get("gather_attack_surface", ""),
            "cross_target_registry_path": state.get("cross_target_registry_path", ""),
            "cross_target_registry": dict(state.get("cross_target_registry") or {}),
            "iteration": 0,
            "max_chain_iterations": _max_iterations(state),
            "min_critic_skills": state.get("min_critic_skills", 2),
            "agent_configs": state.get("agent_configs", {}),
            "agent_config_task_types": state.get("agent_config_task_types", {}),
            "common_focus": state.get("common_focus", ""),
            "gather_review_history": [],
        }
        sends.append(Send("gather_chain_subtask", child))
    return sends or "gather_prepare_report_groups"


__all__ = ["dispatch_all_gather_chains", "dispatch_gather_chains"]
