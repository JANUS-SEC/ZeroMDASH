"""Finalize one cross-workspace chain with fail-closed qualification."""

from __future__ import annotations

import json

from zeromdash import prompts
from zeromdash.agents import AgentResult
from zeromdash.cvss4 import CVSS4ValidationError, score_base_vector
from zeromdash.gather import source_drift_errors
from zeromdash.gather_state import GatherState

from .core.context import _node_focus, _ws
from .core.gather_qualification import close_gather_chain
from .core.invocation import _invoke_with_output_retry
from .core.io import _try_json
from .materialize_chain_pool import _write_json_atomic


def _validate_finalizer(value: object) -> tuple[dict | None, str]:
    if not isinstance(value, dict):
        return None, "gather finalizer output is not a JSON object"
    if value.get("decision") not in {"accept", "reject"}:
        return None, "gather finalizer decision must be accept or reject"
    for key in (
        "chain_is_valid",
        "deterministic_failures_are_contract_only",
        "all_units_confirmed",
        "bindings_valid",
        "global_constraints_satisfiable",
        "no_external_primitives_required",
    ):
        if not isinstance(value.get(key), bool):
            return None, f"gather finalizer {key} must be boolean"
    if not str(value.get("reasoning") or "").strip():
        return None, "gather finalizer reasoning is empty"
    if value.get("decision") == "accept":
        if not str(value.get("title") or "").strip() or not str(value.get("detail") or "").strip():
            return None, "accepted gather finalizer verdict needs title and detail"
        try:
            score_base_vector(str(value.get("cvss4_vector") or ""))
        except CVSS4ValidationError as exc:
            return None, f"gather finalizer CVSS is invalid: {exc}"
    return dict(value), ""


def _contract_only(failures: list[str], review: dict) -> bool:
    return (
        bool(failures)
        and all(item.startswith("contract:") for item in failures)
        and review.get("verdict") == "confirm"
        and review.get("all_units_confirmed") is True
        and review.get("bindings_valid") is True
        and review.get("global_constraints_satisfiable") is True
        and not review.get("required_external_primitives")
    )


def gather_finalize_chain_subtask(state: GatherState, *, backends=None) -> dict:
    ws = _ws(state)
    candidate = dict(state.get("gather_chain_candidate") or {})
    investigation = dict(state.get("gather_chain_investigation") or {})
    review = dict(state.get("gather_chain_review") or {})
    review["iterations"] = int(state.get("iteration", 0))
    chain_id = str(candidate.get("chain_id") or "")
    evidence_by_id = {
        str(item.get("unit_id") or ""): item
        for item in state.get("gather_evidence_pool") or []
        if isinstance(item, dict) and str(item.get("unit_id") or "")
    }
    finding, failures = close_gather_chain(
        candidate=candidate,
        investigation=investigation,
        review=review,
        evidence_by_id=evidence_by_id,
        registry=dict(state.get("cross_target_registry") or {}),
        drift_errors=source_drift_errors(state),
    )
    finalizer_verdict: dict | None = None
    finalizer_errors: list[str] = []
    if finding is None and _contract_only(failures, review):
        parsed: dict | None = None

        def validate(res: AgentResult) -> tuple[bool, str]:
            nonlocal parsed
            parsed, failure = _validate_finalizer(_try_json(res.stdout, fallback=None))
            return parsed is not None, failure

        result, finalizer_errors = _invoke_with_output_retry(
            ws,
            "gather_chain_finalizer_subtask",
            prompts.GATHER_CHAIN_FINALIZER_SUBTASK.format(
                focus=_node_focus(state, "gather_chain_finalizer_subtask_focus"),
                candidate_json=json.dumps(candidate, ensure_ascii=False, indent=2),
                investigation_json=json.dumps(investigation, ensure_ascii=False, indent=2),
                review_json=json.dumps(review, ensure_ascii=False, indent=2),
                failures_json=json.dumps(failures, ensure_ascii=False, indent=2),
                evidence_pool_path=state.get("gather_evidence_pool_path", ""),
                registry_path=state.get("cross_target_registry_path", ""),
            ),
            backends,
            state,
            output_desc="a JSON gather chain finalizer verdict",
            validate=validate,
            subtask_id=chain_id,
            artifact_filenames=("gather_chain_finalizer.json", "output.json"),
            focus=_node_focus(state, "gather_chain_finalizer_subtask_focus"),
            additional_read_roots=list(state.get("source_read_roots") or []),
        )
        if result is not None:
            finalizer_verdict = parsed
        if finalizer_verdict and all(
            finalizer_verdict.get(key) is True
            for key in (
                "chain_is_valid",
                "deterministic_failures_are_contract_only",
                "all_units_confirmed",
                "bindings_valid",
                "global_constraints_satisfiable",
                "no_external_primitives_required",
            )
        ) and finalizer_verdict.get("decision") == "accept":
            reconciled_candidate = dict(candidate)
            reconciled_candidate["ordered_unit_ids"] = list(
                investigation.get("ordered_unit_ids") or candidate.get("ordered_unit_ids") or []
            )
            reconciled_candidate["target_sequence"] = [
                evidence_by_id[unit_id].get("target_id", "")
                for unit_id in reconciled_candidate["ordered_unit_ids"]
                if unit_id in evidence_by_id
            ]
            reconciled_investigation = {
                **investigation,
                "title": finalizer_verdict.get("title"),
                "detail": finalizer_verdict.get("detail"),
                "direct_security_impact": finalizer_verdict.get("direct_security_impact"),
                "evidence": finalizer_verdict.get("evidence"),
            }
            reconciled_review = {
                **review,
                "direct_security_impact": finalizer_verdict.get("direct_security_impact"),
                "cvss4_vector": finalizer_verdict.get("cvss4_vector"),
                "confidence": finalizer_verdict.get("confidence"),
                "violated_security_property": finalizer_verdict.get("violated_security_property"),
            }
            finding, retry_failures = close_gather_chain(
                candidate=reconciled_candidate,
                investigation=reconciled_investigation,
                review=reconciled_review,
                evidence_by_id=evidence_by_id,
                registry=dict(state.get("cross_target_registry") or {}),
                drift_errors=[],
            )
            if finding is not None:
                finding["review"] = {
                    **reconciled_review,
                    "finalizer_verdict": finalizer_verdict,
                    "deterministic_gate_failures": failures,
                }
                failures = []
            else:
                failures = retry_failures
        elif finalizer_errors:
            failures = [*failures, *finalizer_errors]
    if finding is not None:
        out = ws.log / "gather_chain_res" / f"{chain_id}.json"
        _write_json_atomic(
            out,
            {
                "schema_version": "1.0",
                "outcome_type": "gather_chain_finding",
                "chain_id": chain_id,
                "finding": finding,
                "review": review,
                "finalizer": finalizer_verdict or {},
                "history": state.get("gather_review_history") or [],
            },
        )
        return {"gather_chain_findings": [finding]}

    failed = {
        **candidate,
        "status": "rejected" if str(review.get("verdict") or "") == "reject" else "inconclusive",
        "failure_reasons": failures,
        "investigation": investigation,
        "review": review,
    }
    out = ws.log / "gather_chain_candidates" / f"{chain_id}.json"
    _write_json_atomic(
        out,
        {
            "schema_version": "1.0",
            "outcome_type": "gather_chain_candidate",
            "chain_id": chain_id,
            "candidate": failed,
            "review": review,
            "history": state.get("gather_review_history") or [],
        },
    )
    return {"gather_chain_candidates": [failed]}


__all__ = ["gather_finalize_chain_subtask"]
