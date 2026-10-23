"""Primitive normalization and qualification helpers for chain analysis."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from zeromdash.state import Finding, Primitive, Subtask

from .qualification import _direct_impact_present, _summary_list
from .domain_registry import domain_registry_ids

PRIMITIVE_SCHEMA_VERSION = "2.0"

CAPABILITY_KINDS = {
    "controlled_request",
    "authenticated_session",
    "credential_access",
    "object_reference",
    "address_disclosure",
    "relative_file_read",
    "arbitrary_file_read",
    "relative_file_write",
    "arbitrary_file_write",
    "relative_memory_read",
    "arbitrary_memory_read",
    "relative_memory_write",
    "arbitrary_memory_write",
    "command_execution",
    "code_execution",
    "identity_impersonation",
    "privilege_gain",
    "sandbox_escape",
    "security_boundary_bypass",
    "denial_trigger",
    "custom",
}


def _as_dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return []


def _clean_string(value: Any) -> str:
    return str(value or "").strip()


def _clean_string_list(value: Any) -> list[str]:
    return [
        item.strip()
        for item in _summary_list(value)
        if isinstance(item, str) and item.strip()
    ]


def _strict_string_list(value: Any) -> list[str]:
    if not isinstance(value, (list, tuple)):
        return []
    return [
        item.strip()
        for item in value
        if isinstance(item, str) and item.strip()
    ]


def normalize_capability(value: Any) -> dict[str, Any]:
    raw = _as_dict(value)
    kind = _clean_string(raw.get("kind")).lower()
    if kind not in CAPABILITY_KINDS:
        kind = "custom" if kind else ""
    normalized = {
        "kind": kind,
        "object_type": _clean_string(raw.get("object_type")),
        "object_id": _clean_string(raw.get("object_id")),
        "scope": _clean_string(raw.get("scope")),
        "principal": _clean_string(raw.get("principal")),
        "tenant": _clean_string(raw.get("tenant")),
        "address_space": _clean_string(raw.get("address_space")),
        "domain_entity_id": _clean_string(raw.get("domain_entity_id")),
        "representation_id": _clean_string(raw.get("representation_id")),
        "trust_zone": _clean_string(raw.get("trust_zone")),
        "access_mode": _clean_string(raw.get("access_mode")),
        "lifecycle_state": _clean_string(raw.get("lifecycle_state")),
        "properties": sorted(set(_clean_string_list(raw.get("properties")))),
        "constraints": sorted(set(_clean_string_list(raw.get("constraints")))),
        "source": _clean_string(raw.get("source")),
    }
    return {key: value for key, value in normalized.items() if value not in ("", [], {})}


def normalize_capabilities(value: Any) -> list[dict[str, Any]]:
    return [
        cap
        for cap in (normalize_capability(item) for item in _as_list(value))
        if cap.get("kind")
    ]


def capability_signature(capability: dict[str, Any]) -> str:
    identity = normalize_capability(capability)
    # `source` is evidence/provenance prose, not capability identity.
    identity.pop("source", None)
    return json.dumps(
        identity,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def primitive_signature_core(primitive: Primitive) -> dict[str, Any]:
    anchor = _as_dict(primitive.get("root_cause_anchor"))
    def stable_json_items(value: Any) -> list[str]:
        return sorted(
            json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            for item in _as_list(value)
        )

    return {
        "schema_version": PRIMITIVE_SCHEMA_VERSION,
        "repo_id": _clean_string(primitive.get("repo_id")) or "main",
        "revision": _clean_string(primitive.get("revision")),
        "component": _clean_string(primitive.get("component")),
        "root_symbol": _clean_string(anchor.get("symbol")),
        "root_locations": sorted(_clean_string_list(anchor.get("locations"))),
        "required": sorted(
            capability_signature(cap)
            for cap in normalize_capabilities(primitive.get("required_capabilities"))
        ),
        "gained": sorted(
            capability_signature(cap)
            for cap in normalize_capabilities(primitive.get("capabilities_gained"))
        ),
        "domain_refs": normalize_domain_refs(primitive.get("domain_refs")),
        "required_entity_states": stable_json_items(primitive.get("required_entity_states")),
        "resulting_entity_states": stable_json_items(primitive.get("resulting_entity_states")),
        "violated_invariant_ids": sorted(
            _clean_string_list(primitive.get("violated_invariant_ids"))
        ),
    }


def stable_primitive_id(primitive: Primitive) -> str:
    payload = json.dumps(
        primitive_signature_core(primitive),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return "prim_" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _default_evidence(inv: dict[str, Any], review: dict[str, Any], primitive: dict[str, Any]) -> dict[str, Any]:
    evidence = _as_dict(primitive.get("evidence")) or _as_dict(review.get("evidence")) or _as_dict(inv.get("evidence"))
    inv_evidence = _as_dict(inv.get("evidence"))
    if inv_evidence:
        evidence.setdefault("code_locations", inv_evidence.get("code_locations") or [])
        evidence.setdefault("call_path", inv_evidence.get("call_path") or inv_evidence.get("call_paths") or [])
        if inv_evidence.get("writeup_refs"):
            evidence.setdefault("writeup_refs", inv_evidence.get("writeup_refs"))
        if inv_evidence.get("patch_refs"):
            evidence.setdefault("patch_refs", inv_evidence.get("patch_refs"))
    return evidence


def _root_anchor(inv: dict[str, Any], primitive: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    anchor = _as_dict(primitive.get("root_cause_anchor"))
    locations = _clean_string_list(anchor.get("locations")) or _clean_string_list(evidence.get("code_locations"))
    symbol = _clean_string(anchor.get("symbol")) or _clean_string(primitive.get("root_cause")) or _clean_string(inv.get("title"))
    return {
        "symbol": symbol,
        "locations": locations,
    }


def _subtask_repo_id(subtask: Subtask) -> str:
    hints = _as_dict(subtask.get("hints"))
    return _clean_string(hints.get("repo_id")) or _clean_string(hints.get("repository")) or "main"


def normalize_domain_refs(value: Any) -> dict[str, list[str]]:
    raw = _as_dict(value)
    return {
        key: sorted(set(_strict_string_list(raw.get(key))))
        for key in (
            "entity_ids",
            "representation_ids",
            "invariant_ids",
            "transition_ids",
            "seam_ids",
        )
        if _strict_string_list(raw.get(key))
    }


def build_confirmed_primitive(
    *,
    subtask: Subtask,
    investigation: dict[str, Any],
    review: dict[str, Any],
    domain_registry: dict[str, Any] | None = None,
) -> tuple[Primitive | None, list[str]]:
    """Build a normalized primitive from confirmed investigator/critic output."""
    primitive_raw = _as_dict(review.get("primitive")) or _as_dict(investigation.get("primitive"))
    evidence = _default_evidence(investigation, review, primitive_raw)
    capabilities_gained = normalize_capabilities(
        primitive_raw.get("capabilities_gained")
        or review.get("capabilities_gained")
        or investigation.get("capabilities_gained")
    )
    required_capabilities = normalize_capabilities(
        primitive_raw.get("required_capabilities")
        or review.get("required_capabilities")
        or investigation.get("required_capabilities")
    )
    root_anchor = _root_anchor(investigation, primitive_raw, evidence)
    hints = _as_dict(subtask.get("hints"))
    primitive: Primitive = {
        "schema_version": PRIMITIVE_SCHEMA_VERSION,
        "source_subtask_ids": [_clean_string(subtask.get("id"))],
        "repo_id": _clean_string(primitive_raw.get("repo_id")) or _subtask_repo_id(subtask),
        "revision": _clean_string(primitive_raw.get("revision")) or _clean_string(hints.get("revision")),
        "component": _clean_string(primitive_raw.get("component")) or _clean_string(hints.get("component")),
        "root_cause_anchor": root_anchor,
        "entry_conditions": _as_dict(primitive_raw.get("entry_conditions")) or _as_dict(review.get("entry_conditions")),
        "required_capabilities": required_capabilities,
        "attacker_controls": _as_list(primitive_raw.get("attacker_controls") or review.get("attacker_controls")),
        "capabilities_gained": capabilities_gained,
        "handoff_objects": _as_list(primitive_raw.get("handoff_objects") or review.get("handoff_objects")),
        "reliability": _as_dict(primitive_raw.get("reliability")) or {
            "level": _clean_string(review.get("reliability")) or "unknown"
        },
        "evidence": evidence,
        "terminal_impact": _as_dict(primitive_raw.get("terminal_impact")) or _as_dict(review.get("terminal_impact")),
        "missing_next_capabilities": normalize_capabilities(
            primitive_raw.get("missing_next_capabilities") or review.get("missing_next_capabilities")
        ),
        "confirmation": {
            "critic_verdict": _clean_string(review.get("verdict")),
            "confidence": review.get("confidence", 0.0),
            "reasoning": _clean_string(review.get("reasoning")),
        },
        "domain_refs": normalize_domain_refs(
            primitive_raw.get("domain_refs")
            or review.get("domain_refs")
            or investigation.get("domain_refs")
            or hints.get("domain_refs")
        ),
        "required_entity_states": _as_list(primitive_raw.get("required_entity_states")),
        "resulting_entity_states": _as_list(primitive_raw.get("resulting_entity_states")),
        "violated_invariant_ids": _clean_string_list(primitive_raw.get("violated_invariant_ids")),
    }
    primitive["primitive_id"] = stable_primitive_id(primitive)

    errors: list[str] = []
    if _clean_string(review.get("verdict")).lower() != "confirm":
        errors.append("primitive requires critic verdict=confirm")
    if not root_anchor.get("symbol") and not root_anchor.get("locations"):
        errors.append("primitive requires root_cause_anchor symbol or locations")
    if not capabilities_gained:
        errors.append("primitive requires at least one capabilities_gained item")
    if not _clean_string_list(evidence.get("code_locations")):
        errors.append("primitive evidence requires code_locations")
    if not _clean_string_list(evidence.get("call_path") or evidence.get("call_paths")):
        errors.append("primitive evidence requires call_path")
    if _direct_impact_present(review.get("direct_security_impact")) and not required_capabilities:
        errors.append(
            "primitive with direct impact must declare the required capabilities that prevent standalone closure"
        )
    registry = domain_registry or {}
    if registry.get("status") != "legacy_unavailable":
        raw_domain_refs = (
            primitive_raw.get("domain_refs")
            or review.get("domain_refs")
            or investigation.get("domain_refs")
            or hints.get("domain_refs")
            or {}
        )
        if isinstance(raw_domain_refs, dict):
            invalid_ref_shapes = [
                key
                for key, values in raw_domain_refs.items()
                if not isinstance(values, (list, tuple))
            ]
            if invalid_ref_shapes:
                errors.append(
                    "primitive domain_refs collection(s) must be arrays: "
                    + ", ".join(sorted(invalid_ref_shapes))
                )
        referenced_ids = {
            item
            for values in primitive.get("domain_refs", {}).values()
            for item in values
        }
        referenced_ids |= set(primitive.get("violated_invariant_ids") or [])
        for capability in (*required_capabilities, *capabilities_gained):
            referenced_ids |= {
                _clean_string(capability.get(key))
                for key in ("domain_entity_id", "representation_id")
                if _clean_string(capability.get(key))
            }
        for entity_state in (
            *primitive.get("required_entity_states", []),
            *primitive.get("resulting_entity_states", []),
        ):
            if not isinstance(entity_state, dict):
                continue
            referenced_ids |= {
                _clean_string(entity_state.get(key))
                for key in ("entity_id", "representation_id")
                if _clean_string(entity_state.get(key))
            }
        unknown_refs = referenced_ids - domain_registry_ids(registry)
        if unknown_refs:
            errors.append("primitive references unknown domain registry id(s): " + ", ".join(sorted(unknown_refs)))
    return (primitive if not errors else None), errors


def finding_capability_provider(finding: Finding) -> Primitive | None:
    """Convert a qualified standalone finding's capability_view into a pool item."""
    capability_view = _as_dict(finding.get("capability_view"))
    capabilities_gained = normalize_capabilities(capability_view.get("capabilities_gained"))
    if not capabilities_gained:
        return None
    evidence = _as_dict(capability_view.get("evidence")) or _as_dict(finding.get("evidence"))
    primitive: Primitive = {
        "schema_version": PRIMITIVE_SCHEMA_VERSION,
        "source_subtask_ids": _clean_string_list(finding.get("subtask_id")),
        "source_finding_ids": _clean_string_list(finding.get("subtask_id") or finding.get("id")),
        "repo_id": _clean_string(capability_view.get("repo_id")) or "main",
        "revision": _clean_string(capability_view.get("revision")),
        "component": _clean_string(capability_view.get("component")),
        "root_cause_anchor": _as_dict(capability_view.get("root_cause_anchor")) or {
            "symbol": _clean_string(finding.get("title")),
            "locations": _clean_string_list(evidence.get("code_locations")),
        },
        "entry_conditions": _as_dict(capability_view.get("entry_conditions")),
        "required_capabilities": normalize_capabilities(capability_view.get("required_capabilities")),
        "attacker_controls": _as_list(capability_view.get("attacker_controls")),
        "capabilities_gained": capabilities_gained,
        "handoff_objects": _as_list(capability_view.get("handoff_objects")),
        "reliability": _as_dict(capability_view.get("reliability")) or {"level": "standalone-confirmed"},
        "evidence": evidence,
        "terminal_impact": _as_dict(finding.get("direct_security_impact")),
        "missing_next_capabilities": normalize_capabilities(capability_view.get("missing_next_capabilities")),
        "confirmation": {
            "critic_verdict": "confirm",
            "confidence": finding.get("confidence", 0.0),
            "source": "standalone_finding",
        },
        "domain_refs": normalize_domain_refs(capability_view.get("domain_refs")),
        "required_entity_states": _as_list(capability_view.get("required_entity_states")),
        "resulting_entity_states": _as_list(capability_view.get("resulting_entity_states")),
        "violated_invariant_ids": _clean_string_list(capability_view.get("violated_invariant_ids")),
    }
    primitive["primitive_id"] = stable_primitive_id(primitive)
    return primitive


def dedupe_primitives(primitives: list[Primitive]) -> list[Primitive]:
    by_id: dict[str, Primitive] = {}
    for primitive in primitives:
        if not isinstance(primitive, dict):
            continue
        normalized = dict(primitive)
        normalized["required_capabilities"] = normalize_capabilities(normalized.get("required_capabilities"))
        normalized["capabilities_gained"] = normalize_capabilities(normalized.get("capabilities_gained"))
        normalized["domain_refs"] = normalize_domain_refs(normalized.get("domain_refs"))
        normalized.setdefault("schema_version", PRIMITIVE_SCHEMA_VERSION)
        normalized["primitive_id"] = stable_primitive_id(normalized)
        primitive_id = str(normalized["primitive_id"])
        if primitive_id not in by_id:
            by_id[primitive_id] = normalized
            continue
        existing = by_id[primitive_id]
        for key in ("source_subtask_ids", "source_finding_ids"):
            merged = sorted(set(_clean_string_list(existing.get(key)) + _clean_string_list(normalized.get(key))))
            if merged:
                existing[key] = merged
    return sorted(by_id.values(), key=lambda item: str(item.get("primitive_id") or ""))


def review_outcome_type(review: dict[str, Any]) -> str:
    raw = _clean_string(review.get("outcome_type") or review.get("terminal_type")).lower()
    return raw.replace("-", "_").replace(" ", "_")


__all__ = [
    "PRIMITIVE_SCHEMA_VERSION",
    "CAPABILITY_KINDS",
    "normalize_capability",
    "normalize_capabilities",
    "capability_signature",
    "primitive_signature_core",
    "stable_primitive_id",
    "build_confirmed_primitive",
    "finding_capability_provider",
    "dedupe_primitives",
    "review_outcome_type",
    "normalize_domain_refs",
]
