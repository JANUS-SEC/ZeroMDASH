"""Validation and closure gates for chain investigation results."""

from __future__ import annotations

import hashlib
from typing import Any

from zeromdash.cvss4 import CVSS4ValidationError, has_direct_impact, score_base_vector
from zeromdash.state import ChainCandidate, ChainFinding, Primitive

from .chain_compatibility import (
    merge_global_constraints,
    primitive_gains,
    primitive_requirements,
    stable_edge_id,
)
from .domain_registry import domain_registry_ids
from .primitive_qualification import capability_signature, normalize_capabilities
from .qualification import _direct_impact_metrics, _direct_impact_present, _try_json


def _dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return []


def _string(value: Any) -> str:
    return str(value or "").strip()


def chain_investigation_json(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        parsed = _try_json(value, fallback={})
        return parsed if isinstance(parsed, dict) else {}
    return {}


_CHAIN_FACT_FIELDS = {
    "blocking_unmet_facts": "blocking_unmet_fact",
    "validation_gaps": "validation_gap",
    "deployment_constraints": "deployment_constraint",
    "impact_limits": "impact_limit",
}
_CHAIN_FACT_CLASSIFICATIONS = frozenset(_CHAIN_FACT_FIELDS.values())


def _stable_chain_fact_id(source_field: str, statement: str, index: int) -> str:
    payload = f"{source_field}\0{index}\0{statement.strip()}"
    return "fact_" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _normalize_chain_fact_item(
    value: Any,
    *,
    source_field: str,
    classification: str,
    index: int,
) -> dict[str, Any]:
    if isinstance(value, dict):
        item = dict(value)
        statement = _string(
            item.get("statement")
            or item.get("claim")
            or item.get("detail")
            or item.get("fact")
        )
        evidence = _list(item.get("evidence"))
        fact_id = _string(item.get("fact_id"))
    else:
        item = {}
        statement = _string(value)
        evidence = []
        fact_id = ""
    return {
        **item,
        "fact_id": fact_id or _stable_chain_fact_id(source_field, statement, index),
        "statement": statement,
        "evidence": evidence,
        "proposed_classification": classification,
        "source_field": source_field,
    }


def normalize_chain_fact_fields(
    investigation: dict[str, Any],
) -> dict[str, Any]:
    """Assign stable IDs without making a security classification decision.

    New outputs propose one of four classifications. Legacy `unmet_facts` are
    preserved as `legacy_unclassified`; only a chain critic may reclassify
    them through `fact_verdicts`.
    """
    normalized = dict(investigation)
    closure_facts: list[dict[str, Any]] = []
    for field, classification in _CHAIN_FACT_FIELDS.items():
        values = investigation.get(field)
        values = list(values) if isinstance(values, (list, tuple)) else []
        normalized_items = [
            _normalize_chain_fact_item(
                value,
                source_field=field,
                classification=classification,
                index=index,
            )
            for index, value in enumerate(values)
        ]
        normalized[field] = normalized_items
        closure_facts.extend(normalized_items)

    legacy = investigation.get("unmet_facts")
    legacy_values = list(legacy) if isinstance(legacy, (list, tuple)) else []
    legacy_items = [
        _normalize_chain_fact_item(
            value,
            source_field="unmet_facts",
            classification="legacy_unclassified",
            index=index,
        )
        for index, value in enumerate(legacy_values)
    ]
    normalized["legacy_unmet_facts"] = legacy_items
    closure_facts.extend(legacy_items)
    normalized["closure_facts"] = closure_facts
    return normalized


def validate_chain_fact_verdicts(
    investigation: dict[str, Any],
    review: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    facts = [item for item in investigation.get("closure_facts") or [] if isinstance(item, dict)]
    fact_ids = [_string(item.get("fact_id")) for item in facts]
    failures: list[str] = []
    if any(not fact_id for fact_id in fact_ids):
        failures.append("chain fact has empty fact_id")
    if len(fact_ids) != len(set(fact_ids)):
        failures.append("duplicate chain fact id")

    verdicts: dict[str, dict[str, Any]] = {}
    for item in review.get("fact_verdicts") or []:
        if not isinstance(item, dict):
            continue
        fact_id = _string(item.get("fact_id"))
        if not fact_id:
            failures.append("chain fact verdict has empty fact_id")
            continue
        if fact_id in verdicts:
            failures.append(f"duplicate chain fact verdict for {fact_id}")
            continue
        verdicts[fact_id] = item
        if _string(item.get("classification")) not in _CHAIN_FACT_CLASSIFICATIONS:
            failures.append(f"chain fact verdict {fact_id} has invalid classification")
        if not isinstance(item.get("blocking"), bool):
            failures.append(f"chain fact verdict {fact_id} blocking must be boolean")
        if not isinstance(item.get("resolved"), bool):
            failures.append(f"chain fact verdict {fact_id} resolved must be boolean")
        if not _string(item.get("reasoning")):
            failures.append(f"chain fact verdict {fact_id} has no reasoning")
        if not isinstance(item.get("evidence"), list):
            failures.append(f"chain fact verdict {fact_id} evidence must be an array")

    missing = set(fact_ids) - set(verdicts)
    unexpected = set(verdicts) - set(fact_ids)
    if missing:
        failures.append("missing chain fact verdict(s): " + ", ".join(sorted(missing)))
    if unexpected:
        failures.append("unknown chain fact verdict id(s): " + ", ".join(sorted(unexpected)))

    closure_verdict = _string(review.get("closure_verdict")).lower()
    if closure_verdict not in {"closed", "open"}:
        failures.append("chain critic closure_verdict must be closed or open")
    elif closure_verdict != "closed":
        failures.append("chain critic closure_verdict is not closed")
    if closure_verdict == "closed":
        unresolved_blockers = [
            fact_id
            for fact_id, verdict in verdicts.items()
            if verdict.get("blocking") is True and verdict.get("resolved") is not True
        ]
        if unresolved_blockers:
            failures.append(
                "chain has unresolved blocking fact(s): "
                + ", ".join(sorted(unresolved_blockers))
            )
    return facts, failures


def validate_chain_investigation_output(value: Any) -> tuple[dict[str, Any] | None, str]:
    parsed = chain_investigation_json(value)
    if not parsed:
        return None, "output is not a parseable JSON object"
    if not _string(parsed.get("title")):
        return None, "title is empty"
    if not _list(parsed.get("ordered_primitive_ids")):
        return None, "ordered_primitive_ids is empty"
    if not _list(parsed.get("bindings")):
        return None, "bindings is empty"
    if not _list(parsed.get("binding_claims")):
        return None, "binding_claims is empty"
    if not _list(parsed.get("emergent_transitions")):
        return None, "emergent_transitions is empty"
    has_new_fact_contract = all(field in parsed for field in _CHAIN_FACT_FIELDS)
    has_legacy_fact_contract = isinstance(parsed.get("unmet_facts"), list)
    if not has_new_fact_contract and not has_legacy_fact_contract:
        return None, "chain fact arrays are missing"
    for field in _CHAIN_FACT_FIELDS:
        if field in parsed and not isinstance(parsed.get(field), list):
            return None, f"{field} must be an array"
        for index, item in enumerate(parsed.get(field) or []):
            if not isinstance(item, dict):
                return None, f"{field}[{index}] must be an object"
            if not _string(item.get("fact_id")):
                return None, f"{field}[{index}].fact_id is empty"
            if not _string(item.get("statement")):
                return None, f"{field}[{index}].statement is empty"
            if not isinstance(item.get("evidence"), list):
                return None, f"{field}[{index}].evidence must be an array"
    parsed = normalize_chain_fact_fields(parsed)
    fact_ids = [_string(item.get("fact_id")) for item in parsed.get("closure_facts") or []]
    if len(fact_ids) != len(set(fact_ids)):
        return None, "duplicate chain fact id"
    if not _dict(parsed.get("evidence")):
        return None, "evidence is empty"
    if not _dict(parsed.get("direct_security_impact")):
        return None, "direct_security_impact is empty"
    return parsed, ""


def _review_json(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        parsed = _try_json(value, fallback={})
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _capabilities_after_path(path: list[Primitive]) -> list[dict[str, Any]]:
    available: list[dict[str, Any]] = []
    for primitive in path:
        primitive_id = _string(primitive.get("primitive_id"))
        for capability in _list(primitive.get("capabilities_gained")):
            if isinstance(capability, dict):
                available.append({**capability, "provider_primitive_id": primitive_id})
    return available


def _validated_binding_claims(
    investigation: dict[str, Any],
    review: dict[str, Any],
    candidate: ChainCandidate,
    primitives_by_id: dict[str, Primitive],
) -> tuple[list[dict[str, Any]], list[str]]:
    bindings = [dict(item) for item in investigation.get("bindings") or candidate.get("bindings") or [] if isinstance(item, dict)]
    for index, binding in enumerate(bindings):
        binding.setdefault("edge_id", stable_edge_id(binding, index))
    claim_items = [item for item in investigation.get("binding_claims") or [] if isinstance(item, dict)]
    claims: dict[str, dict[str, Any]] = {}
    duplicate_claims: set[str] = set()
    for item in claim_items:
        edge_id = _string(item.get("edge_id"))
        if not edge_id:
            continue
        if edge_id in claims:
            duplicate_claims.add(edge_id)
        claims[edge_id] = item
    verdict_items = review.get("edge_verdicts") or review.get("edge_reviews") or []
    verdicts: dict[str, dict[str, Any]] = {}
    duplicate_verdicts: set[str] = set()
    for item in verdict_items:
        if not isinstance(item, dict):
            continue
        edge_id = _string(item.get("edge_id"))
        if not edge_id:
            continue
        if edge_id in verdicts:
            duplicate_verdicts.add(edge_id)
        verdicts[edge_id] = item
    failures: list[str] = []
    failures.extend(f"duplicate binding claim for {edge_id}" for edge_id in sorted(duplicate_claims))
    failures.extend(f"duplicate edge verdict for {edge_id}" for edge_id in sorted(duplicate_verdicts))
    seen_edges: set[str] = set()
    ordered_ids = [
        _string(item)
        for item in investigation.get("ordered_primitive_ids")
        or candidate.get("ordered_primitive_ids")
        or []
    ]
    candidate_entry_signatures = {
        capability_signature(item)
        for item in normalize_capabilities(
            _dict(candidate.get("attacker_entry")).get("capabilities")
        )
    }
    covered_requirements: dict[str, list[str]] = {}
    for binding in bindings:
        edge_id = _string(binding.get("edge_id"))
        if edge_id in seen_edges:
            failures.append(f"duplicate binding edge id {edge_id}")
        seen_edges.add(edge_id)
        consumer_id = _string(binding.get("consumer_primitive_id"))
        provider = _dict(binding.get("provider"))
        provider_type = _string(provider.get("type"))
        provider_id = _string(provider.get("primitive_id"))
        if consumer_id not in ordered_ids:
            failures.append(f"binding {edge_id} references unknown consumer {consumer_id}")
        elif consumer_id in primitives_by_id:
            required_signature = capability_signature(binding.get("required_capability") or {})
            known_requirements = {
                capability_signature(item)
                for item in primitive_requirements(primitives_by_id[consumer_id])
            }
            if required_signature not in known_requirements:
                failures.append(
                    f"binding {edge_id} references an unknown confirmed requirement"
                )
            covered_requirements.setdefault(consumer_id, []).append(required_signature)
        provider_signature = capability_signature(provider.get("capability") or {})
        if provider_type == "primitive":
            if provider_id not in ordered_ids:
                failures.append(f"binding {edge_id} references unknown provider {provider_id}")
            elif consumer_id in ordered_ids and ordered_ids.index(provider_id) >= ordered_ids.index(consumer_id):
                failures.append(f"binding {edge_id} provider does not precede consumer")
            elif provider_id in primitives_by_id:
                known_gains = {
                    capability_signature(item)
                    for item in primitive_gains(primitives_by_id[provider_id])
                }
                if provider_signature not in known_gains:
                    failures.append(
                        f"binding {edge_id} invents a capability not gained by {provider_id}"
                    )
        elif provider_type == "attacker_entry":
            if provider_signature not in candidate_entry_signatures:
                failures.append(f"binding {edge_id} invents an attacker-entry capability")
        elif provider_type != "attacker_entry":
            failures.append(f"binding {edge_id} has invalid provider type")
        if edge_id not in claims:
            failures.append(f"missing binding claim for {edge_id}")
        else:
            claim = claims[edge_id]
            if not _string(claim.get("claim")):
                failures.append(f"binding claim {edge_id} has no semantic claim")
            if not _list(claim.get("evidence")):
                failures.append(f"binding claim {edge_id} has no evidence")
            if not isinstance(claim.get("registry_refs"), list):
                failures.append(f"binding claim {edge_id} registry_refs must be an array")
        verdict = verdicts.get(edge_id)
        if verdict is None:
            failures.append(f"missing edge verdict for {edge_id}")
        elif _string(verdict.get("verdict")).lower() != "confirm":
            failures.append(f"edge {edge_id} is not confirmed")
        elif not _string(verdict.get("reasoning")):
            failures.append(f"edge verdict {edge_id} has no reasoning")
        elif not _list(verdict.get("evidence")):
            failures.append(f"edge verdict {edge_id} has no evidence")
    unexpected_claims = set(claims) - seen_edges
    if unexpected_claims:
        failures.append(
            "binding claim references unknown edge id(s): "
            + ", ".join(sorted(unexpected_claims))
        )
    unexpected_verdicts = set(verdicts) - seen_edges
    if unexpected_verdicts:
        failures.append(
            "edge verdict references unknown edge id(s): "
            + ", ".join(sorted(unexpected_verdicts))
        )
    for primitive_id in ordered_ids:
        if primitive_id not in primitives_by_id:
            continue
        required_signatures = sorted(
            capability_signature(item)
            for item in primitive_requirements(primitives_by_id[primitive_id])
        )
        if sorted(covered_requirements.get(primitive_id, [])) != required_signatures:
            failures.append(
                f"primitive {primitive_id} bindings do not cover its confirmed "
                "requirements exactly once"
            )
    return bindings, failures


def _emergent_impact_confirmed(investigation: dict[str, Any], review: dict[str, Any]) -> tuple[bool, list[str]]:
    transitions = [item for item in investigation.get("emergent_transitions") or [] if isinstance(item, dict)]
    transition_ids = [_string(item.get("transition_id")) for item in transitions]
    verdict_items = [item for item in review.get("transition_verdicts") or [] if isinstance(item, dict)]
    verdicts: dict[str, dict[str, Any]] = {}
    verdict = _dict(review.get("emergent_impact_verdict"))
    failures: list[str] = []
    if not transitions:
        failures.append("emergent_transitions is empty")
    if any(not transition_id for transition_id in transition_ids):
        failures.append("emergent transition has empty transition id")
    if len(transition_ids) != len(set(transition_ids)):
        failures.append("duplicate emergent transition id")
    for transition in transitions:
        transition_id = _string(transition.get("transition_id"))
        if not isinstance(transition.get("violated_invariant_ids"), list):
            failures.append(
                f"emergent transition {transition_id} violated_invariant_ids must be an array"
            )
    for item in verdict_items:
        transition_id = _string(item.get("transition_id"))
        if not transition_id:
            failures.append("transition verdict has empty transition id")
            continue
        if transition_id in verdicts:
            failures.append(f"duplicate transition verdict for {transition_id}")
            continue
        verdicts[transition_id] = item
    for transition_id in transition_ids:
        transition_verdict = verdicts.get(transition_id)
        if transition_verdict is None:
            failures.append(f"missing transition verdict for {transition_id}")
        elif _string(transition_verdict.get("verdict")).lower() != "confirm":
            failures.append(f"emergent transition {transition_id} is not confirmed")
        elif not _string(transition_verdict.get("reasoning")):
            failures.append(f"transition verdict {transition_id} has no reasoning")
        elif not _list(transition_verdict.get("evidence")):
            failures.append(f"transition verdict {transition_id} has no evidence")
    unexpected_verdicts = set(verdicts) - set(transition_ids)
    if unexpected_verdicts:
        failures.append(
            "transition verdict references unknown transition id(s): "
            + ", ".join(sorted(unexpected_verdicts))
        )
    if verdict.get("confirmed") is not True:
        failures.append("chain critic did not confirm emergent impact")
    elif not _string(verdict.get("reasoning")):
        failures.append("emergent impact verdict has no reasoning")
    elif not _list(verdict.get("evidence")):
        failures.append("emergent impact verdict has no evidence")
    return not failures, failures


def close_chain_candidate(
    *,
    candidate: ChainCandidate,
    investigation: dict[str, Any],
    review: dict[str, Any],
    chain_pool: list[Primitive],
    domain_registry: dict[str, Any] | None = None,
) -> tuple[ChainFinding | None, ChainCandidate | None, list[str]]:
    investigation = normalize_chain_fact_fields(investigation)
    primitives_by_id = {
        _string(primitive.get("primitive_id")): primitive
        for primitive in chain_pool
        if isinstance(primitive, dict) and _string(primitive.get("primitive_id"))
    }
    ordered_ids = [
        _string(item)
        for item in (
            investigation.get("ordered_primitive_ids")
            or candidate.get("ordered_primitive_ids")
            or []
        )
        if _string(item)
    ]
    failures: list[str] = []
    planned_ids = [
        _string(item)
        for item in candidate.get("ordered_primitive_ids") or []
        if _string(item)
    ]
    if ordered_ids != planned_ids:
        failures.append("investigation primitive order differs from planned candidate")
    if len(ordered_ids) < 2:
        failures.append("chain requires at least two primitives")
    missing = [primitive_id for primitive_id in ordered_ids if primitive_id not in primitives_by_id]
    if missing:
        failures.append("unconfirmed primitive id(s): " + ", ".join(missing))
    if len(ordered_ids) != len(set(ordered_ids)):
        failures.append("cycle")

    path = [primitives_by_id[primitive_id] for primitive_id in ordered_ids if primitive_id in primitives_by_id]
    all_bindings, binding_failures = _validated_binding_claims(
        investigation,
        review,
        candidate,
        primitives_by_id,
    )
    failures.extend(binding_failures)

    global_constraints, constraint_failures = merge_global_constraints(path)
    # Deterministic constraint checks are advisory evidence. The agent-native
    # chain critic owns the semantic coexistence verdict.
    deterministic_advisories = [
        {"kind": "global_constraint", "reason": reason}
        for reason in constraint_failures
    ]
    _, emergent_failures = _emergent_impact_confirmed(investigation, review)
    failures.extend(emergent_failures)
    closure_facts, fact_failures = validate_chain_fact_verdicts(investigation, review)
    failures.extend(fact_failures)
    if _string(review.get("verdict")).lower() != "confirm":
        failures.append("chain critic did not confirm")
    if review.get("all_primitives_confirmed") is not True:
        failures.append("chain critic did not confirm all primitives")
    if review.get("bindings_valid") is not True:
        failures.append("chain critic did not confirm bindings")
    if review.get("global_constraints_satisfiable") is not True:
        failures.append("chain critic did not confirm global constraints")
    if _list(review.get("required_external_primitives")):
        failures.append("depends on unconfirmed external primitive")
    registry = domain_registry or {}
    if registry.get("status") != "legacy_unavailable":
        known_registry_ids = domain_registry_ids(registry)
        primitive_registry_ids: set[str] = set()
        for primitive in path:
            refs = primitive.get("domain_refs")
            if isinstance(refs, dict):
                primitive_registry_ids |= {
                    _string(ref)
                    for values in refs.values()
                    if isinstance(values, list)
                    for ref in values
                    if _string(ref)
                }
            primitive_registry_ids |= {
                _string(ref)
                for ref in primitive.get("violated_invariant_ids") or []
                if _string(ref)
            }
            for capability in (
                *_list(primitive.get("required_capabilities")),
                *_list(primitive.get("capabilities_gained")),
            ):
                if not isinstance(capability, dict):
                    continue
                primitive_registry_ids |= {
                    _string(capability.get(key))
                    for key in ("domain_entity_id", "representation_id")
                    if _string(capability.get(key))
                }
            for entity_state in (
                *_list(primitive.get("required_entity_states")),
                *_list(primitive.get("resulting_entity_states")),
            ):
                if not isinstance(entity_state, dict):
                    continue
                primitive_registry_ids |= {
                    _string(entity_state.get(key))
                    for key in ("entity_id", "representation_id")
                    if _string(entity_state.get(key))
                }
        unknown_primitive_registry_ids = primitive_registry_ids - known_registry_ids
        if unknown_primitive_registry_ids:
            failures.append(
                "chain primitive references unknown domain registry id(s): "
                + ", ".join(sorted(unknown_primitive_registry_ids))
            )
        cited_registry_ids = {
            _string(ref)
            for claim in investigation.get("binding_claims") or []
            if isinstance(claim, dict)
            for ref in claim.get("registry_refs") or []
            if _string(ref)
        }
        cited_registry_ids |= {
            _string(ref)
            for transition in investigation.get("emergent_transitions") or []
            if isinstance(transition, dict)
            for ref in transition.get("violated_invariant_ids") or []
            if _string(ref)
        }
        unknown_registry_ids = cited_registry_ids - known_registry_ids
        if unknown_registry_ids:
            failures.append("chain references unknown domain registry id(s): " + ", ".join(sorted(unknown_registry_ids)))

    direct_impact = _dict(review.get("direct_security_impact")) or _dict(investigation.get("direct_security_impact"))
    if not _direct_impact_present(direct_impact):
        failures.append("missing final direct C/I/A impact")

    vector = _string(review.get("cvss4_vector") or investigation.get("cvss4_vector"))
    score = None
    try:
        score = score_base_vector(vector)
    except CVSS4ValidationError as exc:
        failures.append(f"invalid CVSS v4.0 Base vector: {exc}")
    if score is not None:
        declared = _direct_impact_metrics(direct_impact)
        if declared is not None and any(score.metrics[metric] != impact for metric, impact in declared.items()):
            failures.append("direct_security_impact does not match CVSS impact metrics")
        if not has_direct_impact(score):
            failures.append("CVSS v4.0 vector has no direct impact")

    if failures:
        failed: ChainCandidate = {
            **dict(candidate),
            "status": "inconclusive",
            "failure_reasons": sorted(set(failures)),
            "investigation": investigation,
            "review": review,
        }
        return None, failed, sorted(set(failures))

    finding: ChainFinding = {
        "schema_version": "2.0",
        "kind": "chain",
        "chain_id": _string(candidate.get("chain_id")),
        "subtask_id": _string(candidate.get("chain_id")),
        "title": _string(investigation.get("title")) or "Confirmed attack chain",
        "detail": _string(investigation.get("detail")) or _string(review.get("reasoning")),
        "evidence": _dict(investigation.get("evidence")),
        "severity": score.severity if score else "none",
        "confidence": review.get("confidence", investigation.get("confidence", 0.0)),
        "review": review,
        "iterations": int(review.get("iterations") or investigation.get("iterations") or 0),
        "selected_skills": _list(review.get("selected_skills")),
        "disposition": "confirmed_vulnerability",
        "qualification_gate_passed": True,
        "cvss_applicable": True,
        "cvss4_vector": score.vector if score else vector,
        "cvss4_score": score.score if score else 0.0,
        "direct_security_impact": direct_impact,
        "violated_security_property": _string(review.get("violated_security_property") or investigation.get("violated_security_property")),
        "documented_expected_behavior": False,
        "security_contract_violation": True,
        "standalone_security_impact": False,
        "required_external_primitives": [],
        "ordered_primitive_ids": ordered_ids,
        "source_primitive_ids": ordered_ids,
        "bindings": all_bindings or _list(investigation.get("bindings")) or _list(candidate.get("bindings")),
        "global_constraints": global_constraints,
        "deterministic_advisories": [
            *(_list(candidate.get("deterministic_advisories"))),
            *deterministic_advisories,
        ],
        "attacker_entry": _dict(candidate.get("attacker_entry")),
        "attack_path": _list(investigation.get("attack_path")),
        "binding_claims": _list(investigation.get("binding_claims")),
        "emergent_transitions": _list(investigation.get("emergent_transitions")),
        "blocking_unmet_facts": _list(investigation.get("blocking_unmet_facts")),
        "validation_gaps": _list(investigation.get("validation_gaps")),
        "deployment_constraints": _list(investigation.get("deployment_constraints")),
        "impact_limits": _list(investigation.get("impact_limits")),
        "closure_facts": closure_facts,
        "fact_verdicts": _list(review.get("fact_verdicts")),
        "closure_verdict": _string(review.get("closure_verdict")),
        "scope_verdict": _string(review.get("scope_verdict")) or "full_repository",
        "gate_decision": _string(review.get("gate_decision")) or "ignore",
    }
    return finding, None, []


def coerce_chain_review(value: Any, raw: str = "") -> dict[str, Any]:
    review = _review_json(value)
    if review:
        return review
    return {
        "verdict": "revise",
        "raw": raw,
        "invalid_review_shape": type(value).__name__,
        "feedback": {
            "gaps": ["chain critic output was not a JSON object"],
            "requested_evidence": ["Return the required chain review JSON object."],
        },
    }


__all__ = [
    "chain_investigation_json",
    "normalize_chain_fact_fields",
    "validate_chain_fact_verdicts",
    "validate_chain_investigation_output",
    "close_chain_candidate",
    "coerce_chain_review",
]
