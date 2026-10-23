"""Validation and qualification helpers for cross-workspace gather chains."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from zeromdash.cvss4 import CVSS4ValidationError, has_direct_impact, score_base_vector

from .qualification import _direct_impact_metrics, _direct_impact_present


_FLOW_STATUSES = {"confirmed", "scenario_asserted", "hypothesized", "contradicted"}


def _string(value: Any) -> str:
    return str(value or "").strip()


def _list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, (list, tuple)) else []


def validate_cross_target_registry(
    payload: Any,
    *,
    target_ids: set[str],
) -> tuple[dict[str, Any] | None, str]:
    if not isinstance(payload, dict):
        return None, "cross-target registry is not a JSON object"
    if not _string(payload.get("scenario")):
        return None, "cross-target registry scenario is empty"
    for key in (
        "targets",
        "interfaces",
        "cross_target_invariants",
        "deployment_assumptions",
        "unresolved_gaps",
    ):
        if not isinstance(payload.get(key), list):
            return None, f"cross-target registry {key} must be an array"
    flows = payload.get("data_flows")
    if not isinstance(flows, list):
        return None, "cross-target registry data_flows must be an array"
    declared_targets = {
        _string(item.get("target_id"))
        for item in payload.get("targets") or []
        if isinstance(item, dict) and _string(item.get("target_id"))
    }
    if declared_targets != target_ids:
        missing = sorted(target_ids - declared_targets)
        extra = sorted(declared_targets - target_ids)
        return None, (
            "cross-target registry target set mismatch"
            + (f"; missing={','.join(missing)}" if missing else "")
            + (f"; unknown={','.join(extra)}" if extra else "")
        )
    seen: set[str] = set()
    for item in flows:
        if not isinstance(item, dict):
            return None, "cross-target registry contains a non-object flow"
        flow_id = _string(item.get("flow_id"))
        producer = _string(item.get("producer_target_id"))
        consumer = _string(item.get("consumer_target_id"))
        status = _string(item.get("status"))
        if not flow_id or flow_id in seen:
            return None, f"cross-target registry has empty or duplicate flow_id: {flow_id!r}"
        if producer not in target_ids or consumer not in target_ids:
            return None, f"flow {flow_id} references an unknown target"
        if producer == consumer:
            return None, f"flow {flow_id} is not cross-target"
        if status not in _FLOW_STATUSES:
            return None, f"flow {flow_id} has invalid status {status!r}"
        if not _string(item.get("data_object")):
            return None, f"flow {flow_id} has no data_object"
        if not isinstance(item.get("source_refs"), list):
            return None, f"flow {flow_id} source_refs must be an array"
        if status == "confirmed":
            ref_targets = {
                _string(ref.get("target_id"))
                for ref in item.get("source_refs") or []
                if isinstance(ref, dict)
            }
            if not {producer, consumer}.issubset(ref_targets):
                return None, f"confirmed flow {flow_id} lacks bilateral source refs"
        seen.add(flow_id)
    normalized = dict(payload)
    normalized.setdefault("schema_version", "1.0")
    normalized.setdefault("targets", [])
    normalized.setdefault("interfaces", [])
    normalized.setdefault("cross_target_invariants", [])
    normalized.setdefault("deployment_assumptions", [])
    normalized.setdefault("unresolved_gaps", [])
    return normalized, ""


def stable_gather_chain_id(candidate: dict[str, Any]) -> str:
    bindings = []
    for item in candidate.get("bindings") or []:
        if not isinstance(item, dict):
            continue
        bindings.append(
            {
                "provider_unit_id": _string(item.get("provider_unit_id")),
                "consumer_unit_id": _string(item.get("consumer_unit_id")),
                "flow_id": _string(item.get("flow_id")),
            }
        )
    material = {
        "target_sequence": [_string(item) for item in candidate.get("target_sequence") or []],
        "ordered_unit_ids": [_string(item) for item in candidate.get("ordered_unit_ids") or []],
        "bindings": sorted(
            bindings,
            key=lambda item: (
                item["consumer_unit_id"],
                item["provider_unit_id"],
                item["flow_id"],
            ),
        ),
    }
    digest = hashlib.sha256(
        json.dumps(material, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]
    return f"gchain_{digest}"


def normalize_gather_chain_plan(
    payload: Any,
    *,
    evidence_by_id: dict[str, dict[str, Any]],
    registry: dict[str, Any],
    top_k: int,
    max_chain_length: int = 6,
) -> tuple[list[dict[str, Any]], list[str]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("chains"), list):
        return [], ["gather chain plan must be an object with a chains array"]
    flow_ids = {
        _string(item.get("flow_id"))
        for item in registry.get("data_flows") or []
        if isinstance(item, dict) and _string(item.get("flow_id"))
    }
    normalized: list[dict[str, Any]] = []
    errors: list[str] = []
    seen: set[str] = set()
    for index, raw in enumerate(payload["chains"], start=1):
        if not isinstance(raw, dict):
            errors.append(f"chains[{index}] is not an object")
            continue
        candidate = dict(raw)
        unit_ids = [_string(item) for item in candidate.get("ordered_unit_ids") or [] if _string(item)]
        if len(unit_ids) < 2 or len(unit_ids) != len(set(unit_ids)):
            errors.append(f"chains[{index}] ordered_unit_ids must contain at least two unique ids")
            continue
        if len(unit_ids) > max_chain_length:
            errors.append(
                f"chains[{index}] has {len(unit_ids)} units, exceeding gather.max_chain_length={max_chain_length}"
            )
            continue
        missing = [unit_id for unit_id in unit_ids if unit_id not in evidence_by_id]
        if missing:
            errors.append(f"chains[{index}] references unknown unit(s): {', '.join(missing)}")
            continue
        target_sequence = []
        for unit_id in unit_ids:
            target_id = _string(evidence_by_id[unit_id].get("target_id"))
            if target_id and (not target_sequence or target_sequence[-1] != target_id):
                target_sequence.append(target_id)
        declared_targets = [_string(item) for item in candidate.get("target_sequence") or [] if _string(item)]
        if declared_targets and declared_targets != target_sequence:
            errors.append(f"chains[{index}] target_sequence does not match ordered units")
            continue
        if len(set(target_sequence)) < 2:
            errors.append(f"chains[{index}] does not cross targets")
            continue
        bindings = candidate.get("bindings")
        if not isinstance(bindings, list) or not bindings:
            errors.append(f"chains[{index}] bindings must be non-empty")
            continue
        cross_count = 0
        binding_failed = False
        for binding_index, binding in enumerate(bindings, start=1):
            if not isinstance(binding, dict):
                errors.append(f"chains[{index}].bindings[{binding_index}] is not an object")
                binding_failed = True
                continue
            provider = _string(binding.get("provider_unit_id"))
            consumer = _string(binding.get("consumer_unit_id"))
            if provider not in evidence_by_id or consumer not in evidence_by_id:
                errors.append(f"chains[{index}].bindings[{binding_index}] references an unknown unit")
                binding_failed = True
                continue
            if unit_ids.index(provider) >= unit_ids.index(consumer):
                errors.append(
                    f"chains[{index}].bindings[{binding_index}] provider must precede consumer"
                )
                binding_failed = True
            if not _string(binding.get("compatibility_reason")):
                errors.append(
                    f"chains[{index}].bindings[{binding_index}] compatibility_reason is empty"
                )
                binding_failed = True
            if not isinstance(binding.get("source_refs"), list):
                errors.append(
                    f"chains[{index}].bindings[{binding_index}] source_refs must be an array"
                )
                binding_failed = True
            provider_target = _string(evidence_by_id[provider].get("target_id"))
            consumer_target = _string(evidence_by_id[consumer].get("target_id"))
            if provider_target != consumer_target:
                cross_count += 1
                flow_id = _string(binding.get("flow_id"))
                if flow_id not in flow_ids:
                    errors.append(
                        f"chains[{index}].bindings[{binding_index}] cross-target edge has unknown flow_id {flow_id!r}"
                    )
                    binding_failed = True
        if binding_failed or not cross_count:
            if not cross_count:
                errors.append(f"chains[{index}] has no cross-target binding")
            continue
        selected = set(unit_ids)
        duplicate_constituents = sorted(
            {
                constituent
                for unit_id in unit_ids
                if evidence_by_id[unit_id].get("unit_kind") == "local_chain"
                for constituent in evidence_by_id[unit_id].get("constituent_unit_ids") or []
                if constituent in selected
            }
        )
        if duplicate_constituents:
            errors.append(
                f"chains[{index}] repeats local-chain constituent(s): {', '.join(duplicate_constituents)}"
            )
            continue
        candidate["schema_version"] = "1.0"
        candidate["ordered_unit_ids"] = unit_ids
        candidate["target_sequence"] = target_sequence
        candidate.setdefault("attacker_entry", {})
        candidate.setdefault("global_constraints", {})
        candidate.setdefault("expected_terminal_impact", {})
        candidate.setdefault("emergent_impact_hypothesis", {})
        candidate.setdefault("deterministic_advisories", [])
        if not _string(candidate.get("agent_reasoning")):
            errors.append(f"chains[{index}] agent_reasoning is empty")
            continue
        try:
            candidate["rank_score"] = float(candidate.get("rank_score") or 0.0)
        except (TypeError, ValueError):
            errors.append(f"chains[{index}] rank_score must be numeric")
            continue
        candidate["chain_id"] = stable_gather_chain_id(candidate)
        if candidate["chain_id"] in seen:
            continue
        seen.add(candidate["chain_id"])
        normalized.append(candidate)
    normalized.sort(key=lambda item: (-float(item.get("rank_score") or 0.0), item["chain_id"]))
    if len(normalized) > top_k:
        return [], [f"agent returned {len(normalized)} gather chains, exceeding top_K.chain={top_k}"]
    return normalized, errors


def validate_gather_investigation(value: Any) -> tuple[dict[str, Any] | None, str]:
    if not isinstance(value, dict):
        return None, "gather investigation is not a JSON object"
    required_lists = ("ordered_unit_ids", "bindings", "binding_claims", "closure_facts")
    for key in required_lists:
        if not isinstance(value.get(key), list) or not value.get(key):
            return None, f"gather investigation {key} must be a non-empty array"
    if not _string(value.get("title")) or not _string(value.get("detail")):
        return None, "gather investigation title/detail must be non-empty"
    if not isinstance(value.get("direct_security_impact"), dict):
        return None, "gather investigation direct_security_impact must be an object"
    fact_ids = [_string(item.get("fact_id")) for item in value["closure_facts"] if isinstance(item, dict)]
    if len(fact_ids) != len(value["closure_facts"]) or any(not item for item in fact_ids):
        return None, "every gather closure fact must have a fact_id"
    if len(fact_ids) != len(set(fact_ids)):
        return None, "gather closure fact ids must be unique"
    return dict(value), ""


def normalize_gather_review(
    value: Any,
    investigation: dict[str, Any],
) -> dict[str, Any]:
    review = dict(value) if isinstance(value, dict) else {}
    verdict = _string(review.get("verdict")).lower()
    review["verdict"] = verdict if verdict in {"confirm", "reject", "revise"} else "revise"
    for key in ("all_units_confirmed", "bindings_valid", "global_constraints_satisfiable"):
        if not isinstance(review.get(key), bool):
            review[key] = False
    review["required_external_primitives"] = _list(review.get("required_external_primitives"))
    review["edge_verdicts"] = _list(review.get("edge_verdicts"))
    review["fact_verdicts"] = _list(review.get("fact_verdicts"))
    review["selected_skills"] = _list(review.get("selected_skills"))
    review.setdefault("feedback", {})
    if review["verdict"] == "confirm":
        failures = _review_failures(investigation, review)
        if failures:
            review["original_verdict"] = "confirm"
            review["verdict"] = "revise"
            feedback = review.get("feedback") if isinstance(review.get("feedback"), dict) else {}
            feedback["gaps"] = list(dict.fromkeys([*_list(feedback.get("gaps")), *failures]))
            review["feedback"] = feedback
    return review


def _review_failures(investigation: dict[str, Any], review: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if review.get("all_units_confirmed") is not True:
        failures.append("all_units_confirmed must be true")
    if review.get("bindings_valid") is not True:
        failures.append("bindings_valid must be true")
    if review.get("global_constraints_satisfiable") is not True:
        failures.append("global_constraints_satisfiable must be true")
    if review.get("required_external_primitives"):
        failures.append("required_external_primitives must be empty")
    claims = {
        _string(item.get("edge_id"))
        for item in investigation.get("binding_claims") or []
        if isinstance(item, dict) and _string(item.get("edge_id"))
    }
    edge_verdicts = {
        _string(item.get("edge_id")): item
        for item in review.get("edge_verdicts") or []
        if isinstance(item, dict) and _string(item.get("edge_id"))
    }
    if not claims or set(edge_verdicts) != claims:
        failures.append("edge_verdicts must cover every binding claim exactly once")
    else:
        if any(_string(item.get("verdict")) != "confirm" for item in edge_verdicts.values()):
            failures.append("every gather edge verdict must confirm")
        if any(
            not _string(item.get("reasoning"))
            or not isinstance(item.get("evidence"), list)
            for item in edge_verdicts.values()
        ):
            failures.append("every gather edge verdict needs reasoning and evidence")
    facts = {
        _string(item.get("fact_id"))
        for item in investigation.get("closure_facts") or []
        if isinstance(item, dict) and _string(item.get("fact_id"))
    }
    verdicts = {
        _string(item.get("fact_id")): item
        for item in review.get("fact_verdicts") or []
        if isinstance(item, dict) and _string(item.get("fact_id"))
    }
    if set(verdicts) != facts:
        failures.append("fact_verdicts must cover every closure fact exactly once")
    else:
        if any(item.get("blocking") is True and item.get("resolved") is not True for item in verdicts.values()):
            failures.append("gather chain has unresolved blocking facts")
        if any(
            _string(item.get("classification"))
            not in {"blocking_unmet_fact", "validation_gap", "deployment_constraint", "impact_limit"}
            or not isinstance(item.get("blocking"), bool)
            or not isinstance(item.get("resolved"), bool)
            or not _string(item.get("reasoning"))
            or not isinstance(item.get("evidence"), list)
            for item in verdicts.values()
        ):
            failures.append("every gather fact verdict needs a valid classification and evidence")
    if _string(review.get("closure_verdict")) != "closed":
        failures.append("closure_verdict must be closed")
    return failures


def close_gather_chain(
    *,
    candidate: dict[str, Any],
    investigation: dict[str, Any],
    review: dict[str, Any],
    evidence_by_id: dict[str, dict[str, Any]],
    registry: dict[str, Any],
    drift_errors: list[str],
) -> tuple[dict[str, Any] | None, list[str]]:
    failures = list(drift_errors)
    if _string(review.get("verdict")) != "confirm":
        failures.append("gather chain critic did not confirm")
    failures.extend(_review_failures(investigation, review))
    unit_ids = [_string(item) for item in candidate.get("ordered_unit_ids") or []]
    investigation_unit_ids = [
        _string(item) for item in investigation.get("ordered_unit_ids") or []
    ]
    if investigation_unit_ids != unit_ids:
        failures.append("contract: investigation ordered_unit_ids differ from candidate")
    if any(unit_id not in evidence_by_id for unit_id in unit_ids):
        failures.append("gather chain references an unknown evidence unit")
    targets = {_string(evidence_by_id[item].get("target_id")) for item in unit_ids if item in evidence_by_id}
    if len(targets) < 2:
        failures.append("gather chain does not cross at least two targets")
    flows = {
        _string(item.get("flow_id")): item
        for item in registry.get("data_flows") or []
        if isinstance(item, dict)
    }
    allowed_refs = {
        (
            _string(ref.get("target_id")),
            _string(ref.get("artifact_path")),
            _string(ref.get("artifact_sha256")),
        )
        for unit in evidence_by_id.values()
        for ref in unit.get("source_refs") or []
        if isinstance(ref, dict)
    }
    cross_edges = 0
    for claim in investigation.get("binding_claims") or []:
        if not isinstance(claim, dict):
            continue
        provider = _string(claim.get("provider_unit_id"))
        consumer = _string(claim.get("consumer_unit_id"))
        if provider not in evidence_by_id or consumer not in evidence_by_id:
            failures.append("gather binding claim references an unknown evidence unit")
            continue
        if evidence_by_id[provider].get("target_id") == evidence_by_id[consumer].get("target_id"):
            continue
        cross_edges += 1
        flow_id = _string(claim.get("flow_id"))
        flow = flows.get(flow_id)
        if not flow:
            failures.append(f"gather binding claim references unknown flow {flow_id!r}")
        if _string(claim.get("flow_status")) != "confirmed":
            failures.append(f"cross-target edge {_string(claim.get('edge_id'))} is not confirmed")
        refs = claim.get("source_refs")
        ref_targets = {
            _string(ref.get("target_id"))
            for ref in refs or []
            if isinstance(ref, dict)
        }
        expected_ref_targets = {
            _string(evidence_by_id[provider].get("target_id")),
            _string(evidence_by_id[consumer].get("target_id")),
        }
        if (
            not isinstance(refs, list)
            or len(refs) < 2
            or not expected_ref_targets.issubset(ref_targets)
        ):
            failures.append(f"cross-target edge {_string(claim.get('edge_id'))} lacks bilateral source refs")
        elif any(
            (
                _string(ref.get("target_id")),
                _string(ref.get("artifact_path")),
                _string(ref.get("artifact_sha256")),
            )
            not in allowed_refs
            for ref in refs
            if isinstance(ref, dict)
        ):
            failures.append(f"cross-target edge {_string(claim.get('edge_id'))} has an unknown source ref")
    if not cross_edges:
        failures.append("gather chain has no cross-target edge")
    direct_impact = review.get("direct_security_impact")
    if not isinstance(direct_impact, dict) or not _direct_impact_present(direct_impact):
        failures.append("gather chain has no direct C/I/A impact")
    vector = _string(review.get("cvss4_vector"))
    score = None
    try:
        score = score_base_vector(vector)
    except CVSS4ValidationError as exc:
        failures.append(f"invalid CVSS v4.0 Base vector: {exc}")
    if score is not None:
        declared = _direct_impact_metrics(direct_impact)
        if declared is not None and any(score.metrics[key] != value for key, value in declared.items()):
            failures.append("direct_security_impact does not match CVSS impact metrics")
        if not has_direct_impact(score):
            failures.append("CVSS v4.0 vector has no direct impact")
    if failures:
        return None, list(dict.fromkeys(failures))
    finding = {
        "schema_version": "1.0",
        "kind": "gather_chain",
        "chain_id": candidate["chain_id"],
        "subtask_id": candidate["chain_id"],
        "title": _string(investigation.get("title")),
        "detail": _string(investigation.get("detail")),
        "target_sequence": list(candidate.get("target_sequence") or []),
        "ordered_unit_ids": unit_ids,
        "source_primitive_ids": unit_ids,
        "bindings": list(investigation.get("bindings") or candidate.get("bindings") or []),
        "binding_claims": list(investigation.get("binding_claims") or []),
        "attack_path": list(investigation.get("attack_path") or []),
        "global_constraints": dict(investigation.get("global_constraints") or candidate.get("global_constraints") or {}),
        "evidence": dict(investigation.get("evidence") or {}),
        "review": review,
        "iterations": int(review.get("iterations") or 0),
        "selected_skills": list(review.get("selected_skills") or []),
        "disposition": "confirmed_vulnerability",
        "qualification_gate_passed": True,
        "cvss_applicable": True,
        "cvss4_vector": score.vector,
        "cvss4_score": score.score,
        "severity": score.severity,
        "confidence": float(review.get("confidence") or 0.0),
        "direct_security_impact": direct_impact,
        "violated_security_property": _string(review.get("violated_security_property")),
        "documented_expected_behavior": False,
        "security_contract_violation": True,
        "standalone_security_impact": False,
        "required_external_primitives": [],
        "closure_facts": list(investigation.get("closure_facts") or []),
        "fact_verdicts": list(review.get("fact_verdicts") or []),
        "closure_verdict": "closed",
        "scope_verdict": "full_repository",
        "gate_decision": _string(review.get("gate_decision")) or "block",
    }
    return finding, []


__all__ = [
    "close_gather_chain",
    "normalize_gather_chain_plan",
    "normalize_gather_review",
    "stable_gather_chain_id",
    "validate_cross_target_registry",
    "validate_gather_investigation",
]
