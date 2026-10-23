"""LangGraph node implementation: finalize one legacy or batched subtask."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from zeromdash.state import Finding, Subtask, ZeroMDASHState
from zeromdash.workspace import slugify

from .core.context import _ws
from .core.domain_registry import domain_registry_from_state
from .core.hypothesis_batch import (
    hypothesis_package_closed,
    is_hypothesis_batch,
    is_hypothesis_package,
)
from .core.invocation import _selected_log_dir
from .core.primitive_qualification import (
    build_confirmed_primitive,
    review_outcome_type,
)
from .core.qualification import (
    _coerce_review_dict,
    _disposition_value,
    _investigation_json,
    _normalize_qualification_review,
    _patch_status_value,
    _validate_investigation_output,
)
from .core.result_artifacts import append_finalized_result_state


def _atomic_subtask(subtask: Subtask, hypothesis_id: str) -> Subtask:
    atomic = Subtask(**subtask)
    atomic["id"] = f"{subtask.get('id', '')}--{hypothesis_id}"
    return atomic


def _finding_and_primitive(
    state: ZeroMDASHState,
    *,
    subtask: Subtask,
    investigation: dict[str, Any],
    review: dict[str, Any],
    parent_subtask_id: str = "",
    hypothesis_id: str = "",
) -> tuple[Finding, dict[str, Any] | None, list[str], str, str]:
    review = _normalize_qualification_review(dict(review))
    verdict = str(review.get("verdict", "revise")).lower()
    outcome_type = review_outcome_type(review)
    inv_patch_status = _patch_status_value(investigation.get("patch_status"))
    review_patch_status = _patch_status_value(review.get("patch_status"))
    finding: Finding = {
        "kind": subtask.get("bucket", "vuln"),
        "subtask_id": subtask.get("id", ""),
        "title": investigation.get("title") or subtask.get("objective", ""),
        "detail": investigation.get("detail") or "",
        "evidence": investigation.get("evidence") or {},
        "severity": review.get("severity") or "none",
        "confidence": review.get("confidence", 0.0),
        "review": review,
        "iterations": int(state.get("iteration", 0)),
        "selected_skills": list(review.get("selected_skills") or []),
        "scope_relation": str(investigation.get("scope_relation") or ""),
        "diff_evidence": (
            dict(investigation.get("evidence", {}).get("diff_evidence") or {})
            if isinstance(investigation.get("evidence"), dict)
            else {}
        ),
        "scope_verdict": str(review.get("scope_verdict") or ""),
        "gate_decision": str(review.get("gate_decision") or ""),
        "disposition": _disposition_value(review.get("disposition")) or "insufficient_evidence",
        "qualification_gate_passed": review.get("qualification_gate_passed") is True,
        "cvss_applicable": review.get("cvss_applicable") is True,
        "cvss4_vector": str(review.get("cvss4_vector") or ""),
        "direct_security_impact": review.get("direct_security_impact") or {},
        "violated_security_property": str(review.get("violated_security_property") or ""),
        "documented_expected_behavior": review.get("documented_expected_behavior") is True,
        "security_contract_violation": review.get("security_contract_violation") is True,
        "standalone_security_impact": review.get("standalone_security_impact") is True,
        "required_external_primitives": list(review.get("required_external_primitives") or []),
    }
    if parent_subtask_id:
        finding["parent_subtask_id"] = parent_subtask_id
    if hypothesis_id:
        finding["hypothesis_id"] = hypothesis_id
    capability_view = (
        review.get("capability_view")
        if isinstance(review.get("capability_view"), dict)
        else investigation.get("capability_view")
        if isinstance(investigation.get("capability_view"), dict)
        else None
    )
    if capability_view is not None:
        finding["capability_view"] = capability_view
    if review.get("cvss4_score") is not None:
        finding["cvss4_score"] = float(review["cvss4_score"])
    patch_status = review_patch_status or inv_patch_status
    if patch_status:
        finding["patch_status"] = patch_status
    if verdict == "reject":
        outcome_type = "rejected"
    elif not outcome_type:
        outcome_type = (
            "standalone_finding"
            if finding["qualification_gate_passed"]
            else "observation"
        )
    finding["outcome_type"] = outcome_type

    primitive = None
    primitive_errors: list[str] = []
    if outcome_type == "confirmed_primitive":
        primitive, primitive_errors = build_confirmed_primitive(
            subtask=subtask,
            investigation=investigation,
            review=review,
            domain_registry=domain_registry_from_state(state),
        )
        if primitive is not None:
            finding["source_primitive_ids"] = [primitive["primitive_id"]]
    return finding, primitive, primitive_errors, outcome_type, patch_status


def _atomic_artifact_stem(parent_id: str, hypothesis_id: str) -> str:
    exact = f"{parent_id}--{hypothesis_id}"
    digest = hashlib.sha256(exact.encode("utf-8")).hexdigest()[:8]
    return f"{slugify(parent_id)}--{slugify(hypothesis_id)}-{digest}"


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    os.replace(tmp_path, path)


def _result_dir(state: ZeroMDASHState) -> Path:
    selected_dir = _selected_log_dir(state)
    return (
        selected_dir / "results"
        if selected_dir
        else _ws(state).log_path("subtask_res")
    )


def _primitive_dir(state: ZeroMDASHState) -> Path:
    selected_dir = _selected_log_dir(state)
    return (
        selected_dir / "primitive_res"
        if selected_dir
        else _ws(state).log_path("primitive_res")
    )


def _append_finalized(
    update: dict[str, list[Any]],
    *,
    state: ZeroMDASHState,
    subtask: Subtask,
    finding: Finding,
    primitive: dict[str, Any] | None,
    primitive_errors: list[str],
    outcome_type: str,
) -> None:
    if outcome_type == "rejected":
        return
    if outcome_type == "confirmed_primitive":
        if primitive is None:
            update.setdefault("errors", []).append(
                f"[finalize_subtask/{subtask.get('id', '')}] invalid confirmed_primitive: "
                + "; ".join(primitive_errors)
            )
        else:
            _write_json_atomic(
                _primitive_dir(state) / f"{primitive['primitive_id']}.json",
                primitive,
            )
            finding["primitive_gate_passed"] = True
    append_finalized_result_state(
        update,
        finding=finding,
        outcome_type=outcome_type,
        primitive=primitive,
    )


def _mark_primitive_gate(
    finding: Finding,
    *,
    primitive: dict[str, Any] | None,
    primitive_errors: list[str],
    outcome_type: str,
) -> None:
    if outcome_type != "confirmed_primitive":
        return
    finding["primitive_gate_passed"] = primitive is not None
    if primitive is None:
        finding["primitive_gate_errors"] = primitive_errors


def _finalize_legacy(state: ZeroMDASHState, subtask: Subtask) -> dict:
    review = _coerce_review_dict(state.get("review") or {})
    inv, validation_failure = _validate_investigation_output(state.get("investigation", ""))
    if inv is None:
        return {
            "errors": [
                f"[finalize_subtask/{subtask.get('id', '')}] "
                f"refusing to persist invalid investigation: {validation_failure}"
            ]
        }
    finding, primitive, primitive_errors, outcome_type, _ = _finding_and_primitive(
        state, subtask=subtask, investigation=inv, review=review
    )
    _mark_primitive_gate(
        finding,
        primitive=primitive,
        primitive_errors=primitive_errors,
        outcome_type=outcome_type,
    )
    _write_json_atomic(
        _result_dir(state) / f"{subtask['id']}.json",
        {
            "schema_version": "2.0",
            "outcome_type": outcome_type,
            "finding": finding,
            "primitive": primitive,
            "history": state.get("review_history", []),
        },
    )
    update: dict[str, Any] = {}
    _append_finalized(
        update,
        state=state,
        subtask=subtask,
        finding=finding,
        primitive=primitive,
        primitive_errors=primitive_errors,
        outcome_type=outcome_type,
    )
    return update


def _inconclusive_review(batch_review: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "verdict": "revise",
        "outcome_type": "inconclusive",
        "reasoning": reason,
        "disposition": "insufficient_evidence",
        "cvss_applicable": False,
        "selected_skills": list(batch_review.get("selected_skills") or []),
        "skill_perspectives": dict(batch_review.get("skill_perspectives") or {}),
        "feedback": dict(batch_review.get("feedback") or {}),
    }


def _terminal_item_review(
    item_reviews: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, str]:
    if len(item_reviews) != 1:
        return None, (
            "the hypothesis requires exactly one critic verdict; "
            f"received {len(item_reviews)}"
        )
    item_review = item_reviews[0]
    if str(item_review.get("verdict") or "").lower() not in {"confirm", "reject"}:
        return item_review, "the hypothesis critic verdict is not terminal"
    if not str(item_review.get("reasoning") or "").strip():
        return item_review, "the hypothesis critic verdict has no reasoning"
    return item_review, ""


def _finalize_batch(state: ZeroMDASHState, subtask: Subtask) -> dict:
    investigation = _investigation_json(state.get("investigation", ""))
    batch_review = _coerce_review_dict(state.get("review") or {})
    results = [
        item
        for item in investigation.get("hypothesis_results", [])
        if isinstance(item, dict) and str(item.get("hypothesis_id") or "").strip()
    ]
    if not results:
        return {
            "errors": [
                f"[finalize_subtask/{subtask.get('id', '')}] "
                "refusing to persist empty hypothesis batch"
            ]
        }
    verdicts_by_id: dict[str, list[dict[str, Any]]] = {}
    for item in batch_review.get("hypothesis_verdicts", []) or []:
        if not isinstance(item, dict):
            continue
        hypothesis_id = str(item.get("hypothesis_id") or "").strip()
        if hypothesis_id:
            verdicts_by_id.setdefault(hypothesis_id, []).append(item)
    contract_errors = list(batch_review.get("batch_contract_errors") or [])
    closed = hypothesis_package_closed(batch_review)
    exhausted = int(state.get("iteration", 0)) >= int(state.get("max_iterations", 0))
    update: dict[str, Any] = {}
    artifacts: list[dict[str, str]] = []
    retained_definitions = [
        item
        for item in (state.get("hypothesis_manifest") or {}).get("hypotheses", [])
        if isinstance(item, dict) and str(item.get("hypothesis_id") or "").strip()
    ]
    result_by_id = {str(item["hypothesis_id"]): item for item in results}
    if not retained_definitions:
        retained_definitions = [
            {"hypothesis_id": str(item["hypothesis_id"])}
            for item in results
        ]
    elif contract_errors:
        # A package-level accounting failure prevents the monotonic manifest
        # from advancing.  Do not let that discard a newly discovered sibling
        # that already has its own unique, reasoned terminal verdict.  The
        # incomplete parent manifest still records that coverage did not close.
        retained_ids = {str(item["hypothesis_id"]) for item in retained_definitions}
        for inv in results:
            hypothesis_id = str(inv["hypothesis_id"])
            _, item_error = _terminal_item_review(
                verdicts_by_id.get(hypothesis_id, [])
            )
            if hypothesis_id in retained_ids or item_error:
                continue
            retained_definitions.append(
                {
                    "hypothesis_id": hypothesis_id,
                    "statement": str(inv.get("title") or hypothesis_id),
                }
            )
            retained_ids.add(hypothesis_id)
    for definition in retained_definitions:
        hypothesis_id = str(definition["hypothesis_id"])
        inv = result_by_id.get(hypothesis_id)
        missing_investigation = inv is None
        if inv is None:
            inv = {
                "hypothesis_id": hypothesis_id,
                "title": str(definition.get("statement") or hypothesis_id),
                "detail": (
                    "The critic added this required hypothesis after the final "
                    "investigation pass, so it has no investigation result."
                ),
                "evidence": {"code_locations": [], "call_path": []},
                "status": "missing-input",
            }
        atomic = _atomic_subtask(subtask, hypothesis_id)
        item_reviews = verdicts_by_id.get(hypothesis_id, [])
        item_review, item_error = _terminal_item_review(item_reviews)
        if missing_investigation:
            item_error = "the hypothesis has no investigation result"
        if item_error:
            reason = (
                "Hypothesis reached finalization without a structurally valid terminal "
                f"per-hypothesis critic verdict: {item_error}."
            )
            item_review = _inconclusive_review(batch_review, reason)
        finding, primitive, primitive_errors, outcome_type, _ = _finding_and_primitive(
            state,
            subtask=atomic,
            investigation=inv,
            review=item_review,
            parent_subtask_id=str(subtask.get("id") or ""),
            hypothesis_id=hypothesis_id,
        )
        finding["package_status"] = "closed" if closed else "incomplete"
        finding["package_coverage_closed"] = closed
        if contract_errors:
            finding["package_contract_errors"] = contract_errors
        _mark_primitive_gate(
            finding,
            primitive=primitive,
            primitive_errors=primitive_errors,
            outcome_type=outcome_type,
        )
        stem = _atomic_artifact_stem(str(subtask.get("id") or ""), hypothesis_id)
        item_path = _result_dir(state) / f"{stem}.json"
        _write_json_atomic(
            item_path,
            {
                "schema_version": "3.0",
                "package_id": subtask.get("id", ""),
                "hypothesis_id": hypothesis_id,
                "outcome_type": outcome_type,
                "package_status": "closed" if closed else "incomplete",
                "package_contract_errors": contract_errors,
                "finding": finding,
                "primitive": primitive,
                "history": state.get("review_history", []),
            },
        )
        artifacts.append({"hypothesis_id": hypothesis_id, "path": str(item_path)})
        _append_finalized(
            update,
            state=state,
            subtask=atomic,
            finding=finding,
            primitive=primitive,
            primitive_errors=primitive_errors,
            outcome_type=outcome_type,
        )

    package_path = _result_dir(state) / f"{subtask['id']}.json"
    _write_json_atomic(
        package_path,
        {
            "schema_version": "3.0",
            "result_type": "hypothesis_package",
            "package_id": subtask.get("id", ""),
            "closed": closed,
            "status": "closed" if closed else "incomplete",
            "exhausted": exhausted,
            "contract_errors": contract_errors,
            "manifest": state.get("hypothesis_manifest") or {},
            "investigation": investigation,
            "review": batch_review,
            "artifacts": artifacts,
            "history": state.get("review_history", []),
        },
    )
    if not closed:
        reason = (
            "contract repair exhausted: " + "; ".join(contract_errors)
            if contract_errors
            else "exhausted before critic confirmed coverage closure"
        )
        update.setdefault("errors", []).append(
            f"[finalize_subtask/{subtask.get('id', '')}] hypothesis package {reason}"
        )
    return update


def finalize_subtask(state: ZeroMDASHState, *, backends=None) -> dict:
    del backends
    subtask = state["subtask"]
    investigation = _investigation_json(state.get("investigation", ""))
    if is_hypothesis_package(subtask) and is_hypothesis_batch(investigation):
        return _finalize_batch(state, subtask)
    return _finalize_legacy(state, subtask)


__all__ = ["finalize_subtask"]
