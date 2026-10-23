"""LangGraph node implementation: chain_critic_subtask."""

from __future__ import annotations

import json
from typing import Any

from zeromdash import presets, prompts, skills as skills_mod
from zeromdash.agents import AgentResult, normalize_agent_name
from zeromdash.state import ReviewTurn, ZeroMDASHState

from .core.config import _agent_configs_with_node_variant, agent_config_variants_for_node
from .core.context import _node_focus, _ws
from .core.domain_registry import domain_registry_json
from .core.invocation import (
    _agent_errors,
    _emit_node_fallback,
    _make_agent,
    _run_agent_with_config,
    _selected_log_dir,
)
from .core.chain_qualification import (
    chain_investigation_json,
    coerce_chain_review,
    normalize_chain_fact_fields,
    validate_chain_fact_verdicts,
)
from .core.qualification import _try_json
from .core.recovery import node_runtime_failure, recover_runtime


def _normalize_chain_review(
    review: dict[str, Any],
    investigation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    verdict = str(review.get("verdict") or "revise").lower()
    if verdict not in {"confirm", "reject", "revise"}:
        verdict = "revise"
    review["verdict"] = verdict
    review.setdefault("required_external_primitives", [])
    if not isinstance(review.get("required_external_primitives"), list):
        review["required_external_primitives"] = [str(review.get("required_external_primitives"))]
    for key in ("all_primitives_confirmed", "bindings_valid", "global_constraints_satisfiable"):
        if not isinstance(review.get(key), bool):
            review[key] = False
    edge_verdicts = review.get("edge_verdicts") or review.get("edge_reviews") or []
    if not isinstance(edge_verdicts, list):
        edge_verdicts = []
    review["edge_verdicts"] = edge_verdicts
    transition_verdicts = review.get("transition_verdicts") or []
    if not isinstance(transition_verdicts, list):
        transition_verdicts = []
    review["transition_verdicts"] = transition_verdicts
    emergent_verdict = review.get("emergent_impact_verdict")
    if not isinstance(emergent_verdict, dict):
        emergent_verdict = {}
    review["emergent_impact_verdict"] = emergent_verdict
    if verdict == "confirm":
        gaps: list[str] = []
        if review.get("all_primitives_confirmed") is not True:
            gaps.append("all_primitives_confirmed must be true")
        if review.get("bindings_valid") is not True:
            gaps.append("bindings_valid must be true")
        if review.get("global_constraints_satisfiable") is not True:
            gaps.append("global_constraints_satisfiable must be true")
        if review.get("required_external_primitives"):
            gaps.append("required_external_primitives must be empty")
        investigation = normalize_chain_fact_fields(investigation or {})
        expected_edge_ids = [
            str(item.get("edge_id") or "").strip()
            for item in investigation.get("binding_claims") or []
            if isinstance(item, dict) and str(item.get("edge_id") or "").strip()
        ]
        actual_edge_ids = [
            str(item.get("edge_id") or "").strip()
            for item in edge_verdicts
            if isinstance(item, dict) and str(item.get("edge_id") or "").strip()
        ]
        if (
            not expected_edge_ids
            or len(actual_edge_ids) != len(set(actual_edge_ids))
            or set(actual_edge_ids) != set(expected_edge_ids)
        ):
            gaps.append("edge_verdicts must cover every binding claim exactly once")
        expected_transition_ids = [
            str(item.get("transition_id") or "").strip()
            for item in investigation.get("emergent_transitions") or []
            if isinstance(item, dict) and str(item.get("transition_id") or "").strip()
        ]
        actual_transition_ids = [
            str(item.get("transition_id") or "").strip()
            for item in transition_verdicts
            if isinstance(item, dict) and str(item.get("transition_id") or "").strip()
        ]
        if (
            not expected_transition_ids
            or len(actual_transition_ids) != len(set(actual_transition_ids))
            or set(actual_transition_ids) != set(expected_transition_ids)
        ):
            gaps.append("transition_verdicts must cover every emergent transition exactly once")
        if emergent_verdict.get("confirmed") is not True:
            gaps.append("emergent_impact_verdict.confirmed must be true")
        _, fact_failures = validate_chain_fact_verdicts(investigation, review)
        gaps.extend(fact_failures)
        if gaps:
            review["original_verdict"] = "confirm"
            review["verdict"] = "revise"
            feedback = review.setdefault("feedback", {})
            existing = list(feedback.get("gaps") or []) if isinstance(feedback, dict) else []
            existing.extend(gap for gap in gaps if gap not in existing)
            review["feedback"] = {"gaps": existing, "requested_evidence": list(feedback.get("requested_evidence") or [])}
    return review


@recover_runtime(node="chain_critic_subtask", failure=node_runtime_failure)
def chain_critic_subtask(state: ZeroMDASHState, *, backends=None) -> dict:
    ws = _ws(state)
    chain = state["chain_candidate"]
    chain_id = str(chain.get("chain_id") or "")
    history = state.get("chain_review_history", [])
    investigation = normalize_chain_fact_fields(
        chain_investigation_json(state.get("chain_investigation", ""))
    )
    variants = agent_config_variants_for_node(
        "chain_critic_subtask",
        backends,
        state.get("agent_configs"),
    )
    res: AgentResult | None = None
    available_names: list[str] = []
    effective_min = 0
    output_valid = False
    for variant_index, variant in enumerate(variants, start=1):
        backend_name = normalize_agent_name(variant["runtime"])
        variant_configs = _agent_configs_with_node_variant(
            state.get("agent_configs"),
            "chain_critic_subtask",
            variant,
        )
        sub_ws = ws.prepare_sub_workspace(
            node="chain_critic_subtask",
            subtask_id=f"{chain_id}__critic",
            backend=backend_name,
            extra_context={
                "iteration": int(state.get("iteration", 0)),
                "chain_id": chain_id,
                "fallback_index": variant_index - 1,
                "fallback_count": len(variants) - 1,
            },
        )
        skills_catalog_dirs = [
            presets.default_presets_dir() / "skills",
            sub_ws / "skills",
        ]
        skill_list = skills_mod.discover_skills(skills_catalog_dirs)
        catalog_md = skills_mod.render_catalog(skill_list)
        available_names = skills_mod.names(skill_list)
        min_required = int(state.get("min_critic_skills", 2))
        effective_min = min(min_required, len(skill_list)) if skill_list else 0
        (sub_ws / "skills_catalog.md").write_text(catalog_md)

        prompt_text = prompts.CHAIN_CRITIC_SUBTASK.format(
            chain_candidate_json=json.dumps(chain, ensure_ascii=False, indent=2),
            chain_pool_json=json.dumps(state.get("chain_pool") or [], ensure_ascii=False, indent=2),
            domain_registry_json=domain_registry_json(state),
            chain_investigation_json=json.dumps(investigation, ensure_ascii=False, indent=2),
            history_json=json.dumps(history, ensure_ascii=False, indent=2),
            repo_path=state["repo_path"],
            attack_surface=state.get("attack_surface", ""),
            writeup_dir=str(ws.main_path("writeup")),
            patch_dir=str(ws.main_path("patch")),
            feature_docs=", ".join(state.get("feature_docs") or []),
            skills_catalog=catalog_md,
            min_skills=effective_min,
            focus=_node_focus(state, "chain_critic_subtask_focus"),
        )
        res = _run_agent_with_config(
            _make_agent(backend_name),
            "chain_critic_subtask",
            backend_name,
            prompt_text,
            sub_ws,
            None,
            variant_configs,
            state.get("agent_config_task_types"),
            _selected_log_dir(state),
        )
        parsed_output = _try_json(res.stdout, fallback=None)
        output_valid = (
            isinstance(parsed_output, dict)
            and str(parsed_output.get("verdict") or "").lower() in {"confirm", "reject", "revise"}
        )
        if (res.ok and output_valid) or variant_index == len(variants):
            break
        _emit_node_fallback("chain_critic_subtask", res, variants[variant_index])

    if res is None:
        res = AgentResult("", "chain_critic_subtask did not run", 1, "chain_critic_subtask")
    review = coerce_chain_review(
        _try_json(res.stdout, fallback={"verdict": "revise", "raw": res.stdout}),
        raw=res.stdout,
    )
    if not output_valid:
        review["output_validation_error"] = "chain critic must return a JSON review with a valid verdict"
    selected = review.get("selected_skills") or []
    if isinstance(selected, list):
        kept = [skill for skill in selected if isinstance(skill, str) and skill in available_names]
        review["selected_skills"] = kept
        review["available_skills"] = available_names
        if effective_min and len(kept) < effective_min:
            feedback = review.setdefault("feedback", {})
            gaps = list(feedback.get("gaps") or [])
            gaps.append(f"chain critic selected {len(kept)} skill(s); required >= {effective_min}")
            feedback["gaps"] = gaps
            review["skill_selection_ok"] = False
        else:
            review["skill_selection_ok"] = True
    else:
        review["selected_skills"] = []
        review["available_skills"] = available_names
        review["skill_selection_ok"] = False
    review = _normalize_chain_review(
        review,
        investigation,
    )

    selected_dir = _selected_log_dir(state)
    log = (
        selected_dir / "critic_reviews" / f"{chain_id}.chain_review.log"
        if selected_dir
        else ws.log_path("review_log") / f"{chain_id}.chain_review.log"
    )
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a") as fp:
        fp.write(
            f"\n--- iteration {state['iteration']} (skills: {review.get('selected_skills')}) ---\n"
            f"{res.stdout}\n"
        )
    turn = ReviewTurn(
        iteration=state["iteration"],
        investigation=state.get("chain_investigation", ""),
        review=review,
    )
    return {
        "chain_review": review,
        "chain_review_history": [turn],
        "errors": _agent_errors(res, "chain_critic_subtask", chain_id),
    }


def route_after_chain_critic(state: ZeroMDASHState) -> str:
    investigation = normalize_chain_fact_fields(
        chain_investigation_json(state.get("chain_investigation", ""))
    )
    review = _normalize_chain_review(
        coerce_chain_review(state.get("chain_review") or {}),
        investigation,
    )
    verdict = str(review.get("verdict", "revise")).lower()
    iteration = int(state.get("iteration", 0))
    max_iter = int(state.get("max_chain_iterations", 2))
    if verdict in {"confirm", "reject"} or iteration >= max_iter:
        return "finalize_chain_subtask"
    return "chain_investigate_subtask"


__all__ = ["chain_critic_subtask", "route_after_chain_critic"]
