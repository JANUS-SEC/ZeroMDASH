"""Agent-Native planning of chains spanning multiple source workspaces."""

from __future__ import annotations

import json
from typing import Any

from zeromdash import prompts
from zeromdash.agents import AgentResult
from zeromdash.gather_state import GatherState

from .core.context import _node_focus, _ws
from .core.gather_qualification import normalize_gather_chain_plan
from .core.invocation import _invoke_with_output_retry
from .core.io import _planner_fallback_json, _try_json
from .materialize_chain_pool import _write_json_atomic


def _gather_top_k(state: GatherState) -> int:
    raw = (state.get("top_K") or {}).get("chain", 16)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return 16
    return value if value > 0 else 16


def _agent_payload(res: AgentResult) -> Any:
    return _try_json(res.stdout, fallback=None) or _planner_fallback_json(res)


def gather_plan_chains(state: GatherState, *, backends=None) -> dict:
    ws = _ws(state)
    plan_path = ws.state_path("gather_chain_plan.json")
    evidence = [item for item in state.get("gather_evidence_pool") or [] if isinstance(item, dict)]
    evidence_by_id = {
        str(item.get("unit_id") or ""): item
        for item in evidence
        if str(item.get("unit_id") or "")
    }
    top_k = _gather_top_k(state)
    max_chain_length = int((state.get("gather_config") or {}).get("max_chain_length") or 6)
    if len(evidence_by_id) < 2:
        payload = {"schema_version": "1.0", "chain_count": 0, "chains": [], "reason": "fewer_than_two_units"}
        _write_json_atomic(plan_path, payload)
        return {"gather_chain_plan": [], "gather_chain_plan_path": str(plan_path)}

    selected: list[dict[str, Any]] = []
    validation_errors: list[str] = []
    focus = _node_focus(state, "gather_plan_chains_focus")
    prompt = prompts.GATHER_PLAN_CHAINS.format(
        scenario_name=state.get("scenario_name", "gather"),
        scenario=state.get("scenario", ""),
        evidence_pool_path=state.get("gather_evidence_pool_path", ""),
        registry_path=state.get("cross_target_registry_path", ""),
        top_k=top_k,
        max_chain_length=max_chain_length,
        max_candidates_before_top_k=int(
            (state.get("gather_config") or {}).get("max_candidates_before_top_k") or 200
        ),
        focus=focus,
    )

    def validate(res: AgentResult) -> tuple[bool, str]:
        nonlocal selected, validation_errors
        selected, validation_errors = normalize_gather_chain_plan(
            _agent_payload(res),
            evidence_by_id=evidence_by_id,
            registry=dict(state.get("cross_target_registry") or {}),
            top_k=top_k,
            max_chain_length=max_chain_length,
        )
        return (not validation_errors, "; ".join(validation_errors[:5]))

    _, errors = _invoke_with_output_retry(
        ws,
        "gather_plan_chains",
        prompt,
        backends,
        state,
        output_desc=f"cross-target chain plan JSON at {plan_path}",
        validate=validate,
        artifact_filenames=("gather_chain_plan.json", "plan.json", "output.json"),
        focus=focus,
        additional_read_roots=list(state.get("source_read_roots") or []),
    )
    if errors:
        selected = []
    _write_json_atomic(
        plan_path,
        {
            "schema_version": "1.0",
            "chain_count": len(selected),
            "chains": selected,
            "planned_by": "agent",
            "agent_errors": errors,
            "validation_errors": validation_errors,
        },
    )
    return {
        "gather_chain_plan": selected,
        "gather_chain_plan_path": str(plan_path),
        "errors": errors,
    }


__all__ = ["gather_plan_chains"]
