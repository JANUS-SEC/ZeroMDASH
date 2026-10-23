"""Investigate one planned cross-workspace attack chain."""

from __future__ import annotations

import json
from typing import Any

from zeromdash import prompts
from zeromdash.agents import AgentResult
from zeromdash.gather_state import GatherState

from .core.context import _node_focus, _ws
from .core.gather_qualification import validate_gather_investigation
from .core.invocation import _invoke_with_output_retry
from .core.io import _try_json


def gather_chain_investigate_subtask(state: GatherState, *, backends=None) -> dict:
    ws = _ws(state)
    iteration = int(state.get("iteration", 0)) + 1
    candidate = dict(state.get("gather_chain_candidate") or {})
    chain_id = str(candidate.get("chain_id") or "")
    previous = state.get("gather_chain_review")
    feedback_block = (
        "Previous critic review:\n" + json.dumps(previous, ensure_ascii=False, indent=2)
        if isinstance(previous, dict) and previous
        else ""
    )
    prompt = prompts.GATHER_CHAIN_INVESTIGATE_SUBTASK.format(
        iteration=iteration,
        max_iterations=state.get("max_chain_iterations", 3),
        scenario=state.get("scenario", ""),
        candidate_json=json.dumps(candidate, ensure_ascii=False, indent=2),
        evidence_pool_path=state.get("gather_evidence_pool_path", ""),
        registry_path=state.get("cross_target_registry_path", ""),
        targets_json=json.dumps(state.get("gather_targets") or [], ensure_ascii=False, indent=2),
        feedback_block=feedback_block,
        focus=_node_focus(state, "gather_chain_investigate_subtask_focus"),
    )
    parsed: dict[str, Any] | None = None
    failure = ""

    def validate(res: AgentResult) -> tuple[bool, str]:
        nonlocal parsed, failure
        parsed, failure = validate_gather_investigation(_try_json(res.stdout, fallback=None))
        return parsed is not None, failure

    _, errors = _invoke_with_output_retry(
        ws,
        "gather_chain_investigate_subtask",
        prompt,
        backends,
        state,
        output_desc="a structured cross-target chain investigation",
        validate=validate,
        subtask_id=chain_id,
        attempt_log_subtask_id=f"{chain_id}.iter-{iteration}",
        artifact_filenames=("gather_chain_investigation.json", "investigation.json", "output.json"),
        focus=_node_focus(state, "gather_chain_investigate_subtask_focus"),
        additional_read_roots=list(state.get("source_read_roots") or []),
    )
    if parsed is None:
        return {
            "iteration": iteration,
            "gather_chain_investigation": {},
            "gather_chain_investigation_valid": False,
            "errors": list(errors) or [f"[gather_chain_investigate_subtask/{chain_id}] {failure}"],
        }
    return {
        "iteration": iteration,
        "gather_chain_investigation": parsed,
        "gather_chain_investigation_valid": True,
        "errors": [],
    }


def route_after_gather_chain_investigation(state: GatherState) -> str:
    if state.get("gather_chain_investigation_valid") is False:
        return "gather_finalize_chain_subtask"
    return "gather_chain_critic_subtask"


__all__ = [
    "gather_chain_investigate_subtask",
    "route_after_gather_chain_investigation",
]
