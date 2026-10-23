"""LangGraph node implementation: chain_investigate_subtask."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from zeromdash import prompts
from zeromdash.agents import AgentResult
from zeromdash.state import ChainCandidate, ReviewTurn, ZeroMDASHState

from .core.context import _node_focus, _ws
from .core.domain_registry import domain_registry_json
from .core.invocation import _invoke_with_output_retry, _selected_log_dir
from .core.chain_qualification import validate_chain_investigation_output


def chain_investigate_subtask(state: ZeroMDASHState, *, backends=None) -> dict:
    ws = _ws(state)
    iteration = int(state.get("iteration", 0)) + 1
    chain = state["chain_candidate"]
    chain_id = str(chain.get("chain_id") or "")
    prev_review = state.get("chain_review")
    if isinstance(prev_review, dict) and prev_review:
        feedback_block = prompts.CHAIN_INVESTIGATE_FEEDBACK_BLOCK.format(
            review_json=json.dumps(prev_review, ensure_ascii=False),
            gaps=prev_review.get("feedback", {}).get("gaps", []),
            requested_evidence=prev_review.get("feedback", {}).get("requested_evidence", []),
        )
    else:
        feedback_block = ""

    prompt = prompts.CHAIN_INVESTIGATE_SUBTASK.format(
        repo_path=state["repo_path"],
        iteration=iteration,
        max_iterations=state.get("max_chain_iterations", 2),
        chain_candidate_json=json.dumps(chain, ensure_ascii=False, indent=2),
        chain_pool_json=json.dumps(state.get("chain_pool") or [], ensure_ascii=False, indent=2),
        domain_registry_json=domain_registry_json(state),
        attack_surface=state.get("attack_surface", ""),
        spec_doc=state.get("spec_doc", ""),
        writeup_dir=str(ws.main_path("writeup")),
        patch_dir=str(ws.main_path("patch")),
        similar_writeups=", ".join(state.get("similar_writeups") or []),
        feature_docs=", ".join(state.get("feature_docs") or []),
        focus=_node_focus(state, "chain_investigate_subtask_focus"),
        feedback_block=feedback_block,
    )
    parsed: dict[str, Any] | None = None
    validation_failure = ""

    def validate(res: AgentResult) -> tuple[bool, str]:
        nonlocal parsed, validation_failure
        parsed, validation_failure = validate_chain_investigation_output(res.stdout)
        return parsed is not None, validation_failure

    res, errors = _invoke_with_output_retry(
        ws,
        "chain_investigate_subtask",
        prompt,
        backends,
        state,
        output_desc=(
            "a JSON chain investigation with ordered_primitive_ids, bindings, "
            "evidence, direct_security_impact, and cvss4_vector"
        ),
        validate=validate,
        subtask_id=chain_id,
        attempt_log_subtask_id=f"{chain_id}.iter-{iteration}",
        focus=_node_focus(state, "chain_investigate_subtask_focus"),
        artifact_filenames=("chain.json", "chain_investigation.json", "output.json"),
        extra_context={
            "iteration": iteration,
            "chain_id": chain_id,
        },
    )
    selected_dir = _selected_log_dir(state)
    log = (
        selected_dir / "investigations" / f"{chain_id}.chain_investigation.log"
        if selected_dir
        else ws.log_path("review_log") / f"{chain_id}.chain_investigation.log"
    )
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a") as fp:
        fp.write(f"\n--- iteration {iteration} ---\n{res.stdout if res else ''}\n")

    if parsed is None:
        failure = validation_failure or "chain investigation output validation failed"
        return {
            "iteration": iteration,
            "chain_investigation": res.stdout if res else "",
            "chain_investigation_valid": False,
            "errors": list(errors) or [f"[chain_investigate_subtask/{chain_id}] {failure}"],
        }
    return {
        "iteration": iteration,
        "chain_investigation": json.dumps(parsed, ensure_ascii=False),
        "chain_investigation_valid": True,
        "errors": [],
    }


def route_after_chain_investigation(state: ZeroMDASHState) -> str:
    return "__end__" if state.get("chain_investigation_valid") is False else "chain_critic_subtask"


__all__ = ["chain_investigate_subtask", "route_after_chain_investigation"]
