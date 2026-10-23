"""Finding parsing, qualification, and summary compaction."""

from __future__ import annotations

import json
import re
from typing import Any

from zeromdash.cvss4 import CVSS4ValidationError, has_direct_impact, score_base_vector
from zeromdash.state import ZeroMDASHState

from .constants import *
from .io import *

def _normalized_flag(value: Any) -> str:
    return str(value or "").strip().lower().replace("_", "-").replace(" ", "-")

def _summary_status(finding: dict[str, Any]) -> str:
    review = finding.get("review")
    if isinstance(review, dict):
        status = review.get("verdict") or review.get("status")
        if status:
            return _normalized_flag(status)
    return _normalized_flag(finding.get("status") or finding.get("verdict") or "")

def _disposition_value(value: Any) -> str:
    disposition = _normalized_flag(value).replace("-", "_")
    return disposition if disposition in _DISPOSITIONS else ""

def _finding_disposition(finding: dict[str, Any]) -> str:
    review = finding.get("review") if isinstance(finding.get("review"), dict) else {}
    return _disposition_value(finding.get("disposition") or review.get("disposition"))

def _finding_qualification_passed(finding: dict[str, Any]) -> bool:
    review = finding.get("review") if isinstance(finding.get("review"), dict) else {}
    value = finding.get("qualification_gate_passed")
    if not isinstance(value, bool):
        value = review.get("qualification_gate_passed")
    if value is not True or _finding_disposition(finding) not in _VULNERABILITY_DISPOSITIONS:
        return False
    vector = finding.get("cvss4_vector") or review.get("cvss4_vector")
    try:
        score = score_base_vector(str(vector or ""))
    except CVSS4ValidationError:
        return False
    return score.score > 0.0 and has_direct_impact(score)

def _summary_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]

def _patch_status_value(value: Any) -> str:
    status = str(value or "").strip().lower()
    return status if status in _PATCH_STATUSES else ""

def _known_cve_patch_gap_ids(finding: dict[str, Any], bucket: str) -> list[str]:
    if bucket != "patch":
        return []
    if _finding_qualification_passed(finding):
        return []
    review = finding.get("review") if isinstance(finding.get("review"), dict) else {}
    if _finding_disposition(finding) not in {"", "known_cve_patch_gap"}:
        return []
    patch_status = _patch_status_value(finding.get("patch_status") or review.get("patch_status"))
    if patch_status and patch_status != "not_applied":
        return []
    payload = {
        "title": finding.get("title"),
        "detail": finding.get("detail"),
        "evidence": finding.get("evidence"),
        "review": finding.get("review"),
    }
    text = json.dumps(payload, ensure_ascii=False, default=str)
    if patch_status == "not_applied":
        return sorted({match.group(0).upper() for match in _CVE_ID_RE.finditer(text)})
    lowered = text.lower()
    if any(marker in lowered for marker in _PATCH_GAP_FULL_VULN_MARKERS):
        return []
    if not any(marker in lowered for marker in _PATCH_GAP_NOT_APPLIED_MARKERS):
        return []
    return sorted({match.group(0).upper() for match in _CVE_ID_RE.finditer(text)})

def _summary_sort_key(finding: dict[str, Any]) -> tuple[int, float, float, str]:
    status = _summary_status(finding)
    review = finding.get("review") if isinstance(finding.get("review"), dict) else {}
    cvss_score = 0.0
    if _finding_qualification_passed(finding):
        vector = finding.get("cvss4_vector") or review.get("cvss4_vector")
        cvss_score = score_base_vector(str(vector or "")).score
    confidence = finding.get("confidence", review.get("confidence", 0.0))
    try:
        confidence_value = float(confidence)
    except (TypeError, ValueError):
        confidence_value = 0.0
    return (
        _SUMMARY_STATUS_RANK.get(status, len(_SUMMARY_STATUS_RANK)),
        -cvss_score,
        -confidence_value,
        str(finding.get("subtask_id") or finding.get("id") or ""),
    )

def _direct_impact_metrics(value: Any) -> dict[str, str] | None:
    if not isinstance(value, dict):
        return None
    allowed = {"none", "low", "high"}
    metric_names = {
        "vulnerable_system": {
            "confidentiality": "VC",
            "integrity": "VI",
            "availability": "VA",
        },
        "subsequent_system": {
            "confidentiality": "SC",
            "integrity": "SI",
            "availability": "SA",
        },
    }
    values = {"none": "N", "low": "L", "high": "H"}
    result: dict[str, str] = {}
    for system, fields in metric_names.items():
        metrics = value.get(system)
        if not isinstance(metrics, dict):
            return None
        for key, metric_name in fields.items():
            impact = _normalized_flag(metrics.get(key))
            if impact not in allowed:
                return None
            result[metric_name] = values[impact]
    return result

def _direct_impact_present(value: Any) -> bool:
    metrics = _direct_impact_metrics(value)
    return metrics is not None and any(impact != "N" for impact in metrics.values())

def _force_qualification_revise(review: dict[str, Any], gaps: list[str]) -> None:
    claimed_disposition = _disposition_value(review.get("disposition"))
    if claimed_disposition in _VULNERABILITY_DISPOSITIONS:
        review["claimed_disposition"] = claimed_disposition
        review["disposition"] = "insufficient_evidence"
    review["qualification_gate_passed"] = False
    review["qualification_gate_version"] = _QUALIFICATION_GATE_VERSION
    review["severity"] = "none"
    review.pop("cvss4_score", None)
    feedback = review.setdefault("feedback", {})
    if not isinstance(feedback, dict):
        feedback = {}
        review["feedback"] = feedback
    existing = feedback.get("gaps") if isinstance(feedback.get("gaps"), list) else []
    for gap in gaps:
        _append_unique(existing, gap)
    feedback["gaps"] = existing
    requested = (
        feedback.get("requested_evidence")
        if isinstance(feedback.get("requested_evidence"), list)
        else []
    )
    _append_unique(
        requested,
        "Provide evidence for a violated security contract and direct C/I/A impact caused by this finding itself; do not borrow impact from an unproven second vulnerability.",
    )
    feedback["requested_evidence"] = requested
    if str(review.get("verdict") or "").lower() == "confirm":
        review["original_verdict"] = "confirm"
        review["verdict"] = "revise"
        review["orchestrator_override"] = "vulnerability_qualification_gate_failed"

def _normalize_qualification_review(review: dict[str, Any]) -> dict[str, Any]:
    """Enforce vulnerability qualification before CVSS scoring.

    A confirmed mechanism is not automatically a vulnerability.  Only a
    contract-violating issue with direct impact, no missing external exploit
    primitive, and a valid non-zero CVSS v4.0 Base vector passes this gate.
    """

    review["qualification_gate_version"] = _QUALIFICATION_GATE_VERSION
    outcome_type = _normalized_flag(
        review.get("outcome_type") or review.get("terminal_type") or ""
    ).replace("-", "_")
    if outcome_type:
        review["outcome_type"] = outcome_type
    if outcome_type == "confirmed_primitive":
        review["qualification_gate_passed"] = False
        review["cvss_applicable"] = False
        review["severity"] = "none"
        review["disposition"] = _disposition_value(review.get("disposition")) or "insufficient_evidence"
        review.pop("cvss4_score", None)
        review.pop("cvss4_vector", None)
        return review
    verdict = str(review.get("verdict") or "revise").lower()
    disposition = _disposition_value(review.get("disposition"))
    if not disposition:
        if verdict == "reject":
            disposition = "no_finding"
        else:
            _force_qualification_revise(
                review,
                ["critic must classify disposition before a finding can be finalized"],
            )
            review["disposition"] = "insufficient_evidence"
            return review
    review["disposition"] = disposition

    if disposition in _NON_VULNERABILITY_DISPOSITIONS:
        review["qualification_gate_passed"] = False
        review["cvss_applicable"] = False
        review["severity"] = "none"
        review.pop("cvss4_score", None)
        review.pop("cvss4_vector", None)
        return review

    gaps: list[str] = []
    documented = review.get("documented_expected_behavior")
    contract_violation = review.get("security_contract_violation")
    standalone_impact = review.get("standalone_security_impact")
    external_primitives = review.get("required_external_primitives")
    cvss_applicable = review.get("cvss_applicable")

    for field, value in (
        ("documented_expected_behavior", documented),
        ("security_contract_violation", contract_violation),
        ("standalone_security_impact", standalone_impact),
        ("cvss_applicable", cvss_applicable),
    ):
        if not isinstance(value, bool):
            gaps.append(f"{field} must be a JSON boolean")
    if documented is True and contract_violation is not True:
        gaps.append(
            "documented expected behavior without an explicit security-contract violation is not a vulnerability"
        )
    if contract_violation is not True:
        gaps.append("no violated security property or contract was established")
    if standalone_impact is not True:
        gaps.append("the finding does not establish standalone security impact")
    if not isinstance(external_primitives, list) or any(
        not isinstance(item, str) or not item.strip() for item in (external_primitives or [])
    ):
        gaps.append("required_external_primitives must be a JSON list of non-empty strings")
    elif external_primitives:
        gaps.append(
            "exploitability depends on a separate unproven vulnerability or external exploit primitive"
        )
    if not _direct_impact_present(review.get("direct_security_impact")):
        gaps.append("no direct confidentiality, integrity, or availability impact was established")
    if not str(review.get("violated_security_property") or "").strip():
        gaps.append("violated_security_property must identify the broken guarantee or invariant")
    if cvss_applicable is not True:
        gaps.append("cvss_applicable must be true for a qualified vulnerability")

    vector = str(review.get("cvss4_vector") or "").strip()
    score = None
    try:
        score = score_base_vector(vector)
    except CVSS4ValidationError as exc:
        gaps.append(f"invalid CVSS v4.0 Base vector: {exc}")
    if score is not None:
        declared_impact = _direct_impact_metrics(review.get("direct_security_impact"))
        if declared_impact is not None and any(
            score.metrics[metric] != impact for metric, impact in declared_impact.items()
        ):
            gaps.append(
                "direct_security_impact must exactly match CVSS v4.0 VC/VI/VA/SC/SI/SA metrics"
            )
        if not has_direct_impact(score) or score.score <= 0.0:
            gaps.append("CVSS v4.0 vector has no direct impact and cannot qualify a vulnerability")
        else:
            review["cvss4_vector"] = score.vector
            review["cvss4_score"] = score.score
            review["severity"] = score.severity

    if gaps:
        _force_qualification_revise(review, gaps)
        return review

    review["qualification_gate_passed"] = True
    return review

def _summary_evidence_fields(finding: dict[str, Any]) -> tuple[dict[str, Any], list[Any], list[Any], list[Any]]:
    evidence = finding.get("evidence") if isinstance(finding.get("evidence"), dict) else {}
    code_locations = evidence.get("code_locations") or evidence.get("candidate_code_locations") or []
    call_path = evidence.get("call_path") or evidence.get("call_paths") or []
    call_flow = (
        evidence.get("call_flow")
        or evidence.get("data_flow")
        or evidence.get("data_flows")
        or call_path
        or []
    )
    compact_evidence = {
        k: v
        for k, v in evidence.items()
        if k not in _SUMMARY_EVIDENCE_DROP_KEYS
    }
    return compact_evidence, _summary_list(code_locations), _summary_list(call_path), _summary_list(call_flow)

def _compact_summary_finding(finding: Any, bucket: str) -> dict[str, Any] | None:
    if not isinstance(finding, dict):
        return None
    evidence, code_locations, call_path, call_flow = _summary_evidence_fields(finding)
    review = finding.get("review") if isinstance(finding.get("review"), dict) else {}
    computed_cvss = None
    if _finding_qualification_passed(finding):
        computed_cvss = score_base_vector(
            str(finding.get("cvss4_vector") or review.get("cvss4_vector") or "")
        )
    severity = computed_cvss.severity if computed_cvss else "none"
    requires_call_path_summary = severity in {"high", "critical"}
    cve_ids = _known_cve_patch_gap_ids(finding, bucket)
    if not _finding_qualification_passed(finding) and not cve_ids:
        return None
    patch_status = _patch_status_value(finding.get("patch_status") or review.get("patch_status"))
    return {
        "id": finding.get("subtask_id") or finding.get("id") or "",
        "bucket": bucket,
        "title": finding.get("title") or "",
        "status": _summary_status(finding),
        "severity": severity,
        "disposition": _finding_disposition(finding),
        "cvss4_vector": computed_cvss.vector if computed_cvss else "",
        "cvss4_score": computed_cvss.score if computed_cvss else None,
        "confidence": finding.get("confidence", review.get("confidence", 0.0)),
        "summary_format": _SUMMARY_FORMAT_PATCH_GAP if cve_ids else _SUMMARY_FORMAT_FULL,
        "cve_ids": cve_ids,
        "patch_status": patch_status,
        "evidence": evidence,
        "code_locations": code_locations,
        "call_path": call_path,
        "call_flow": call_flow,
        "requires_call_path_summary": requires_call_path_summary,
        "skills": _summary_list(finding.get("selected_skills") or review.get("selected_skills")),
        "scope_relation": finding.get("scope_relation") or "",
        "scope_verdict": finding.get("scope_verdict") or review.get("scope_verdict") or "",
        "gate_decision": finding.get("gate_decision") or review.get("gate_decision") or "",
        "changed_locations": _summary_list(
            (finding.get("diff_evidence") or {}).get("changed_locations")
        ),
        "change_to_sink_path": _summary_list(
            (finding.get("diff_evidence") or {}).get("change_to_sink_path")
        ),
    }

def _compact_summary_buckets(state: ZeroMDASHState) -> dict[str, list[dict[str, Any]]]:
    buckets = {
        "spec_findings": ("spec", state.get("spec_findings", [])),
        "vuln_candidates": ("vuln", state.get("vuln_candidates", [])),
        "patch_findings": ("patch", state.get("patch_findings", [])),
        "feature_findings": ("feature", state.get("feature_findings", [])),
    }
    compact: dict[str, list[dict[str, Any]]] = {}
    for key, (bucket, findings) in buckets.items():
        ordered = sorted(
            (finding for finding in findings if isinstance(finding, dict)),
            key=_summary_sort_key,
        )
        compact[key] = [
            compact_finding
            for compact_finding in (_compact_summary_finding(finding, bucket) for finding in ordered)
            if compact_finding is not None and compact_finding.get("status") in {"confirm", "revise"}
        ]
    return compact

def _compact_summary_observations(state: ZeroMDASHState) -> list[dict[str, Any]]:
    compact: list[dict[str, Any]] = []
    candidates = list(state.get("observations", []))
    for bucket in (
        state.get("spec_findings", []),
        state.get("vuln_candidates", []),
        state.get("patch_findings", []),
        state.get("feature_findings", []),
    ):
        candidates.extend(
            finding
            for finding in bucket
            if isinstance(finding, dict) and not _finding_qualification_passed(finding)
        )
    seen: set[str] = set()
    for finding in candidates:
        if not isinstance(finding, dict):
            continue
        subtask_id = str(finding.get("subtask_id") or "")
        dedupe_key = subtask_id or json.dumps(finding, ensure_ascii=False, sort_keys=True, default=str)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        review = finding.get("review") if isinstance(finding.get("review"), dict) else {}
        status = _summary_status(finding)
        if status not in {"confirm", "revise"}:
            continue
        if _finding_disposition(finding) == "known_cve_patch_gap":
            continue
        compact.append(
            {
                "id": subtask_id,
                "bucket": finding.get("kind") or "",
                "title": finding.get("title") or "",
                "status": status,
                "disposition": _finding_disposition(finding),
                "confidence": finding.get("confidence", review.get("confidence", 0.0)),
                "qualification_gate_passed": False,
            }
        )
    return compact

def _investigation_json(investigation: Any) -> dict[str, Any]:
    if isinstance(investigation, dict):
        return investigation
    if isinstance(investigation, str):
        parsed = _try_json(investigation, fallback={})
        return parsed if isinstance(parsed, dict) else {}
    return {}

def _nonempty_string_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )

def _validate_investigation_output(
    investigation: Any,
) -> tuple[dict[str, Any] | None, str]:
    parsed = _investigation_json(investigation)
    if not parsed:
        return None, "output is not a parseable JSON object"
    if not str(parsed.get("title") or "").strip():
        return None, "title is empty"
    if not str(parsed.get("detail") or "").strip():
        return None, "detail is empty"
    evidence = parsed.get("evidence")
    if not isinstance(evidence, dict) or not evidence:
        return None, "evidence is empty"
    if not _nonempty_string_list(evidence.get("code_locations")):
        return None, "evidence.code_locations must contain at least one path:line"
    if not _nonempty_string_list(evidence.get("call_path")):
        return None, "evidence.call_path must contain at least one source-to-sink step"
    return parsed, ""

def _is_no_finding_investigation(investigation: Any) -> bool:
    inv = _investigation_json(investigation)
    return (
        _normalized_flag(inv.get("status")) == "no-finding"
        or _normalized_flag(inv.get("title")) == "no-finding"
    )

def _append_unique(items: list[Any], value: str) -> list[Any]:
    if value not in items:
        items.append(value)
    return items

def _first_no_finding_needs_revise(state: ZeroMDASHState) -> bool:
    iteration = int(state.get("iteration", 0))
    return (
        iteration == 1
        and _is_no_finding_investigation(state.get("investigation", ""))
    )

def _force_first_no_finding_revise(state: ZeroMDASHState, review: Any) -> Any:
    if not isinstance(review, dict):
        return review
    verdict = str(review.get("verdict", "revise")).lower()
    if verdict not in {"confirm", "reject"} or not _first_no_finding_needs_revise(state):
        return review

    review["orchestrator_override"] = "first_no_finding_requires_second_pass"
    review["original_verdict"] = review.get("verdict", verdict)
    review["verdict"] = "revise"

    reasoning = str(review.get("reasoning") or "").strip()
    override_reason = (
        "Orchestrator forced revise because a first-iteration no-finding needs "
        "one more pass to test whether the vulnerability pattern is eliminated "
        "on all plausible paths."
    )
    review["reasoning"] = f"{reasoning}\n{override_reason}".strip() if reasoning else override_reason

    feedback = review.get("feedback")
    if not isinstance(feedback, dict):
        feedback = {}
        review["feedback"] = feedback
    gaps = feedback.get("gaps") if isinstance(feedback.get("gaps"), list) else []
    feedback["gaps"] = _append_unique(gaps, _FIRST_NO_FINDING_REVISE_GAP)
    requested = (
        feedback.get("requested_evidence")
        if isinstance(feedback.get("requested_evidence"), list)
        else []
    )
    for item in _FIRST_NO_FINDING_REQUESTED_EVIDENCE:
        _append_unique(requested, item)
    feedback["requested_evidence"] = requested
    feedback["next_focus"] = feedback.get("next_focus") or _FIRST_NO_FINDING_NEXT_FOCUS
    return review

def _coerce_review_dict(review: Any, raw: str = "") -> dict[str, Any]:
    if isinstance(review, dict):
        return review
    return {
        "verdict": "revise",
        "raw": raw,
        "invalid_review_shape": type(review).__name__,
    }

def _normalize_scope_review(
    state: ZeroMDASHState,
    investigation: dict[str, Any],
    review: dict[str, Any],
) -> dict[str, Any]:
    if review.get("qualification_gate_passed") is not True:
        review["gate_decision"] = "ignore"
        scope = state.get("scan_scope")
        mode = str(scope.get("mode") or "full") if isinstance(scope, dict) else "full"
        review["scope_verdict"] = (
            "full_repository"
            if mode != "diff"
            else _normalized_flag(
                review.get("scope_verdict") or investigation.get("scope_relation") or "unknown"
            ).replace("-", "_")
        )
        return review
    scope = state.get("scan_scope")
    mode = str(scope.get("mode") or "full") if isinstance(scope, dict) else "full"
    if mode != "diff":
        review["scope_verdict"] = "full_repository"
        review["gate_decision"] = "ignore"
        return review

    allowed = {"introduced", "enabled", "regressed", "pre_existing", "unrelated", "unknown"}
    scope_verdict = _normalized_flag(
        review.get("scope_verdict") or investigation.get("scope_relation") or "unknown"
    ).replace("-", "_")
    if scope_verdict not in allowed:
        scope_verdict = "unknown"

    verdict = _normalized_flag(review.get("verdict") or "revise")
    severity = _normalized_flag(review.get("severity") or investigation.get("severity") or "")
    diff_evidence = investigation.get("evidence", {}).get("diff_evidence", {})
    if not isinstance(diff_evidence, dict):
        diff_evidence = {}
    causal_path = diff_evidence.get("change_to_sink_path")
    causal_explanation = str(diff_evidence.get("causal_explanation") or "").strip()
    causal_evidence = bool(causal_path) and bool(causal_explanation)

    blocking_scope = scope_verdict in {"introduced", "enabled", "regressed"}
    if verdict == "confirm" and blocking_scope and causal_evidence and severity in {"high", "critical"}:
        gate_decision = "block"
    elif verdict in {"confirm", "revise"} and scope_verdict not in {"unrelated"}:
        gate_decision = "warn"
    else:
        gate_decision = "ignore"

    review["scope_verdict"] = scope_verdict
    review["gate_decision"] = gate_decision
    if blocking_scope and not causal_evidence:
        feedback = review.setdefault("feedback", {})
        gaps = list(feedback.get("gaps") or [])
        gap = "diff scope attribution lacks both change_to_sink_path and causal_explanation"
        if gap not in gaps:
            gaps.append(gap)
        feedback["gaps"] = gaps
    return review

__all__ = ["_try_json","_normalized_flag","_summary_status","_disposition_value","_finding_disposition","_finding_qualification_passed","_summary_list","_patch_status_value","_known_cve_patch_gap_ids","_summary_sort_key","_direct_impact_metrics","_direct_impact_present","_force_qualification_revise","_normalize_qualification_review","_summary_evidence_fields","_compact_summary_finding","_compact_summary_buckets","_compact_summary_observations","_investigation_json","_nonempty_string_list","_validate_investigation_output","_is_no_finding_investigation","_append_unique","_first_no_finding_needs_revise","_force_first_no_finding_revise","_coerce_review_dict","_normalize_scope_review"]
