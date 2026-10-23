"""Critic feedback loop for one cross-workspace chain."""

from __future__ import annotations

import json
from typing import Any

from zeromdash import presets, prompts, skills as skills_mod
from zeromdash.agents import AgentResult
from zeromdash.gather_state import GatherReviewTurn, GatherState

from .core.context import _node_focus, _ws
from .core.gather_qualification import normalize_gather_review
from .core.invocation import _invoke_with_output_retry
from .core.io import _try_json


def gather_chain_critic_subtask(state: GatherState, *, backends=None) -> dict:
    ws = _ws(state)
    candidate = dict(state.get("gather_chain_candidate") or {})
    investigation = dict(state.get("gather_chain_investigation") or {})
    chain_id = str(candidate.get("chain_id") or "")
    skills = skills_mod.discover_skills([presets.default_presets_dir() / "skills"])
    catalog = skills_mod.render_catalog(skills)
    available = skills_mod.names(skills)
    min_required = int(state.get("min_critic_skills", 2))
    effective_min = min(min_required, len(available)) if available else 0
    prompt = prompts.GATHER_CHAIN_CRITIC_SUBTASK.format(
        scenario_name=state.get("scenario_name", "gather"),
        candidate_json=json.dumps(candidate, ensure_ascii=False, indent=2),
        investigation_json=json.dumps(investigation, ensure_ascii=False, indent=2),
        history_json=json.dumps(state.get("gather_review_history") or [], ensure_ascii=False, indent=2),
        evidence_pool_path=state.get("gather_evidence_pool_path", ""),
        registry_path=state.get("cross_target_registry_path", ""),
        skills_catalog=catalog,
        min_skills=effective_min,
        focus=_node_focus(state, "gather_chain_critic_subtask_focus"),
    )
    review: dict[str, Any] | None = None
    failure = ""

    def validate(res: AgentResult) -> tuple[bool, str]:
        nonlocal review, failure
        payload = _try_json(res.stdout, fallback=None)
        review = normalize_gather_review(payload, investigation)
        selected = [item for item in review.get("selected_skills") or [] if item in available]
        review["selected_skills"] = selected
        review["available_skills"] = available
        review["skill_selection_ok"] = not effective_min or len(selected) >= effective_min
        if not review["skill_selection_ok"]:
            failure = f"gather critic selected {len(selected)} skill(s); required >= {effective_min}"
            return False, failure
        if not str(review.get("reasoning") or "").strip():
            failure = "gather critic reasoning is empty"
            return False, failure
        return True, ""

    _, errors = _invoke_with_output_retry(
        ws,
        "gather_chain_critic_subtask",
        prompt,
        backends,
        state,
        output_desc="a structured cross-target chain critic review",
        validate=validate,
        subtask_id=f"{chain_id}__critic",
        attempt_log_subtask_id=f"{chain_id}.iter-{state.get('iteration', 0)}",
        artifact_filenames=("gather_chain_review.json", "review.json", "output.json"),
        focus=_node_focus(state, "gather_chain_critic_subtask_focus"),
        additional_read_roots=list(state.get("source_read_roots") or []),
    )
    if review is None:
        review = {
            "verdict": "revise",
            "reasoning": failure or "critic output validation failed",
            "feedback": {"gaps": [failure or "critic output validation failed"]},
        }
    turn: GatherReviewTurn = {
        "iteration": int(state.get("iteration", 0)),
        "investigation": investigation,
        "review": review,
    }
    return {
        "gather_chain_review": review,
        "gather_review_history": [turn],
        "errors": errors,
    }


def route_after_gather_chain_critic(state: GatherState) -> str:
    review = dict(state.get("gather_chain_review") or {})
    verdict = str(review.get("verdict") or "revise").lower()
    if verdict in {"confirm", "reject"} or int(state.get("iteration", 0)) >= int(
        state.get("max_chain_iterations", 3)
    ):
        return "gather_finalize_chain_subtask"
    return "gather_chain_investigate_subtask"


__all__ = ["gather_chain_critic_subtask", "route_after_gather_chain_critic"]
