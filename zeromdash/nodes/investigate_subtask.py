"""LangGraph node implementation: investigate_subtask."""

from __future__ import annotations

import copy
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any

from langgraph.constants import Send

from zeromdash import prompts, skills as skills_mod
from zeromdash.agents import AgentResult, normalize_agent_name
from zeromdash.scope import materialize_scan_scope
from zeromdash.state import Finding, ReviewTurn, Subtask, ZeroMDASHState
from zeromdash.workspace import Workspace, slugify

from .core.constants import DEFAULT_MAX_ITERATIONS
from .core.context import (
    _node_focus,
    _ws,
)
from .core.domain_registry import domain_registry_json
from .core.invocation import (
    _invoke_with_output_retry,
    _selected_log_dir,
)
from .core.hypothesis_batch import (
    initial_hypothesis_manifest,
    is_hypothesis_package,
    validate_hypothesis_investigation,
)
from .core.qualification import _investigation_json, _validate_investigation_output

def investigate_subtask(state: ZeroMDASHState, *, backends=None) -> dict:
    """Investigate ONE Subtask. Re-run on each `revise` verdict, with the
    previous critic's feedback prepended to the prompt.
    """
    ws = _ws(state)
    iteration = int(state.get("iteration", 0)) + 1
    subtask = state["subtask"]

    batch_mode = is_hypothesis_package(subtask)
    manifest = state.get("hypothesis_manifest")
    if batch_mode and not isinstance(manifest, dict):
        try:
            manifest = initial_hypothesis_manifest(subtask)
        except ValueError as exc:
            return {
                "iteration": iteration,
                "investigation_valid": False,
                "errors": [f"[investigate_subtask/{subtask.get('id', '')}] {exc}"],
            }

    prev_review = state.get("review")
    if prev_review:
        feedback_block = prompts.INVESTIGATE_FEEDBACK_BLOCK.format(
            review_json=json.dumps(prev_review, ensure_ascii=False),
            gaps=prev_review.get("feedback", {}).get("gaps", []),
            requested_evidence=prev_review.get("feedback", {}).get("requested_evidence", []),
        )
    else:
        feedback_block = ""

    prompt = prompts.INVESTIGATE_SUBTASK.format(
            repo_path=state["repo_path"],
            iteration=iteration,
            max_iterations=state.get("max_iterations", DEFAULT_MAX_ITERATIONS),
            subtask_json=json.dumps(subtask, ensure_ascii=False, indent=2),
            attack_surface=state.get("attack_surface", ""),
            domain_registry=domain_registry_json(state),
            spec_doc=state.get("spec_doc", ""),
            writeup_dir=str(ws.main_path("writeup")),
            patch_dir=str(ws.main_path("patch")),
            similar_writeups=", ".join(state.get("similar_writeups") or []),
            feature_docs=", ".join(state.get("feature_docs") or []),
            focus=_node_focus(state, "investigate_subtask_focus"),
            feedback_block=feedback_block,
            hypothesis_manifest_json=json.dumps(manifest or {}, ensure_ascii=False, indent=2),
        )
    parsed_investigation: dict[str, Any] | None = None
    validation_failure = ""

    def validate(res: AgentResult) -> tuple[bool, str]:
        nonlocal parsed_investigation, validation_failure
        if batch_mode:
            parsed_investigation, validation_failure = validate_hypothesis_investigation(
                _investigation_json(res.stdout),
                subtask=subtask,
                prior_manifest=manifest,
            )
        else:
            parsed_investigation, validation_failure = _validate_investigation_output(
                res.stdout
            )
        return parsed_investigation is not None, validation_failure

    res, errors = _invoke_with_output_retry(
        ws,
        "investigate_subtask",
        prompt,
        backends,
        state,
        output_desc=(
            "a complete hypothesis-batch Investigation with monotonic IDs, "
            "coverage mapping, and evidence for every result"
            if batch_mode
            else "a JSON Investigation with non-empty title, detail, "
            "evidence.code_locations, and evidence.call_path"
        ),
        validate=validate,
        subtask_id=subtask["id"],
        attempt_log_subtask_id=f"{subtask['id']}.iter-{iteration}",
        focus=_node_focus(state, "investigate_subtask_focus"),
        artifact_filenames=("finding.json", "investigation.json", "output.json"),
        extra_context={
            "iteration": iteration,
            "bucket": subtask.get("bucket", ""),
            "objective": subtask.get("objective", ""),
        },
    )
    selected_dir = _selected_log_dir(state)
    log = (
        selected_dir / "investigations" / f"{subtask['id']}.investigation.log"
        if selected_dir
        else ws.log_path("review_log") / f"{subtask['id']}.investigation.log"
    )
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a") as fp:
        fp.write(
            f"\n--- iteration {iteration} ---\n"
            f"{res.stdout if res else ''}\n"
        )

    if parsed_investigation is None:
        failure = validation_failure or "investigation output validation failed"
        return {
            "iteration": iteration,
            "investigation": res.stdout if res else "",
            "investigation_valid": False,
            "hypothesis_manifest": manifest or {},
            "errors": list(errors) or [
                f"[investigate_subtask/{subtask['id']}] {failure}"
            ],
        }
    return {
        "iteration": iteration,
        "investigation": json.dumps(parsed_investigation, ensure_ascii=False),
        "investigation_valid": True,
        **({"hypothesis_manifest": manifest} if batch_mode else {}),
        "errors": [],
    }

def route_after_investigation(state: ZeroMDASHState) -> str:
    return "__end__" if state.get("investigation_valid") is False else "critic_subtask"

__all__ = ["investigate_subtask","route_after_investigation"]

