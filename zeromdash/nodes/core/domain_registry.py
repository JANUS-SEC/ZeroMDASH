"""Structural helpers for the agent-produced domain invariant registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from zeromdash.state import ZeroMDASHState

DOMAIN_REGISTRY_SCHEMA_VERSION = "1.0"
_COLLECTION_IDS = {
    "entities": "entity_id",
    "representations": "representation_id",
    "invariants": "invariant_id",
    "transitions": "transition_id",
    "seams": "seam_id",
}
_REQUIRED_FIELDS = {
    "entities": ("entity_id", "kind", "name", "source_locations"),
    "representations": ("representation_id", "kind", "source_locations"),
    "invariants": ("invariant_id", "kind", "statement", "source_locations"),
    "transitions": ("transition_id", "name", "source_locations"),
    "seams": ("seam_id", "kind", "invariant_ids", "candidate_locations"),
}
_STRING_ARRAY_FIELDS = {
    "entities": ("source_locations",),
    "representations": (
        "entity_ids",
        "mutators",
        "consumers",
        "attacker_controlled_fields",
        "lifecycle_states",
        "source_locations",
    ),
    "invariants": (
        "subject_entity_ids",
        "representation_ids",
        "enforcement_points",
        "invalidating_transitions",
        "source_locations",
    ),
    "transitions": (
        "input_entity_ids",
        "output_entity_ids",
        "preconditions",
        "postconditions",
        "source_locations",
    ),
    "seams": (
        "producer_ids",
        "consumer_ids",
        "invariant_ids",
        "transition_ids",
        "candidate_locations",
    ),
}


def legacy_domain_registry(target: str = "") -> dict[str, Any]:
    return {
        "schema_version": DOMAIN_REGISTRY_SCHEMA_VERSION,
        "target": str(target or ""),
        "status": "legacy_unavailable",
        "entities": [],
        "representations": [],
        "invariants": [],
        "transitions": [],
        "seams": [],
        "notes": ["Workspace predates the Domain Model and Invariant Registry."],
    }


def validate_domain_registry(value: Any) -> tuple[dict[str, Any] | None, str]:
    if not isinstance(value, dict):
        return None, "domain registry is not a JSON object"
    if str(value.get("schema_version") or "") != DOMAIN_REGISTRY_SCHEMA_VERSION:
        return None, f"domain registry schema_version must be {DOMAIN_REGISTRY_SCHEMA_VERSION}"
    status = str(value.get("status") or "complete")
    if status not in {"complete", "partial", "legacy_unavailable"}:
        return None, f"invalid domain registry status: {status}"
    normalized = dict(value)
    all_ids: set[str] = set()
    for collection, id_key in _COLLECTION_IDS.items():
        entries = value.get(collection)
        if not isinstance(entries, list):
            return None, f"domain registry {collection} must be an array"
        normalized_entries: list[dict[str, Any]] = []
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                return None, f"domain registry {collection}[{index}] is not an object"
            item_id = str(entry.get(id_key) or "").strip()
            if not item_id:
                return None, f"domain registry {collection}[{index}].{id_key} is empty"
            if item_id in all_ids:
                return None, f"duplicate domain registry id: {item_id}"
            missing_fields = [field for field in _REQUIRED_FIELDS[collection] if field not in entry]
            if missing_fields:
                return None, (
                    f"domain registry {collection}[{index}] missing required field(s): "
                    + ", ".join(missing_fields)
                )
            for field in _STRING_ARRAY_FIELDS[collection]:
                if field not in entry:
                    continue
                field_value = entry[field]
                if not isinstance(field_value, list) or any(
                    not isinstance(item, str) for item in field_value
                ):
                    return None, (
                        f"domain registry {collection}[{index}].{field} must be an array of strings"
                    )
            for field in _REQUIRED_FIELDS[collection]:
                if field in _STRING_ARRAY_FIELDS[collection]:
                    continue
                if not isinstance(entry.get(field), str) or not entry[field].strip():
                    return None, (
                        f"domain registry {collection}[{index}].{field} must be a non-empty string"
                    )
            all_ids.add(item_id)
            normalized_entries.append(dict(entry))
        normalized[collection] = normalized_entries

    entity_ids = {str(item["entity_id"]) for item in normalized["entities"]}
    representation_ids = {str(item["representation_id"]) for item in normalized["representations"]}
    invariant_ids = {str(item["invariant_id"]) for item in normalized["invariants"]}
    transition_ids = {str(item["transition_id"]) for item in normalized["transitions"]}
    for representation in normalized["representations"]:
        unknown = set(representation.get("entity_ids") or []) - entity_ids
        if unknown:
            return None, "representation references unknown entity id(s): " + ", ".join(sorted(unknown))
    for transition in normalized["transitions"]:
        unknown = (
            set(transition.get("input_entity_ids") or [])
            | set(transition.get("output_entity_ids") or [])
        ) - entity_ids
        if unknown:
            return None, "transition references unknown entity id(s): " + ", ".join(sorted(unknown))
    for invariant in normalized["invariants"]:
        unknown = set(invariant.get("subject_entity_ids") or []) - entity_ids
        unknown |= set(invariant.get("representation_ids") or []) - representation_ids
        unknown |= set(invariant.get("invalidating_transitions") or []) - transition_ids
        if unknown:
            return None, "invariant references unknown domain id(s): " + ", ".join(sorted(unknown))
    valid_subjects = entity_ids | representation_ids
    for seam in normalized["seams"]:
        unknown = (set(seam.get("producer_ids") or []) | set(seam.get("consumer_ids") or [])) - valid_subjects
        unknown |= set(seam.get("invariant_ids") or []) - invariant_ids
        unknown |= set(seam.get("transition_ids") or []) - transition_ids
        if unknown:
            return None, "seam references unknown domain id(s): " + ", ".join(sorted(unknown))
    normalized["status"] = status
    return normalized, ""


def read_domain_registry(path: str | Path, *, target: str = "") -> dict[str, Any]:
    raw_path = str(path or "").strip()
    registry_path = Path(raw_path) if raw_path else None
    if registry_path is None or not registry_path.is_file():
        return legacy_domain_registry(target)
    try:
        payload = json.loads(registry_path.read_text())
    except (OSError, json.JSONDecodeError):
        return legacy_domain_registry(target)
    parsed, _ = validate_domain_registry(payload)
    return parsed if parsed is not None else legacy_domain_registry(target)


def domain_registry_from_state(state: ZeroMDASHState) -> dict[str, Any]:
    registry = state.get("domain_registry")
    if isinstance(registry, dict):
        parsed, _ = validate_domain_registry(registry)
        if parsed is not None:
            return parsed
    return read_domain_registry(
        str(state.get("domain_registry_path") or ""),
        target=str(state.get("target") or ""),
    )


def domain_registry_json(state: ZeroMDASHState) -> str:
    return json.dumps(domain_registry_from_state(state), ensure_ascii=False, indent=2)


def domain_registry_ids(registry: dict[str, Any]) -> set[str]:
    return {
        str(item.get(id_key) or "")
        for collection, id_key in _COLLECTION_IDS.items()
        for item in registry.get(collection, []) or []
        if isinstance(item, dict) and str(item.get(id_key) or "")
    }


__all__ = [
    "DOMAIN_REGISTRY_SCHEMA_VERSION",
    "legacy_domain_registry",
    "validate_domain_registry",
    "read_domain_registry",
    "domain_registry_from_state",
    "domain_registry_json",
    "domain_registry_ids",
]
