"""Deterministic capability compatibility checks for chain planning."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from zeromdash.state import ChainCandidate, Primitive

from .primitive_qualification import normalize_capability, normalize_capabilities

CHAIN_SCHEMA_VERSION = "2.0"

_CAPABILITY_IMPLICATIONS = {
    "arbitrary_file_read": {"relative_file_read"},
    "arbitrary_file_write": {"relative_file_write"},
    "arbitrary_memory_read": {"relative_memory_read", "address_disclosure"},
    "arbitrary_memory_write": {"relative_memory_write"},
    "code_execution": {
        "command_execution",
        "arbitrary_file_read",
        "arbitrary_file_write",
        "relative_file_read",
        "relative_file_write",
    },
    "privilege_gain": {"identity_impersonation", "security_boundary_bypass"},
}


def _string(value: Any) -> str:
    return str(value or "").strip()


def _list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return []


def _string_list(value: Any) -> list[str]:
    return [str(item).strip() for item in _list(value) if str(item or "").strip()]


def _capability_identity(value: Any) -> dict[str, Any]:
    capability = normalize_capability(value)
    capability.pop("source", None)
    for key in ("properties", "constraints"):
        if key in capability:
            capability[key] = sorted(set(_string_list(capability[key])))
    return capability


def _cap_kind_satisfies(provider_kind: str, required_kind: str) -> bool:
    if not provider_kind or not required_kind:
        return False
    if provider_kind == "custom" or required_kind == "custom":
        return False
    return provider_kind == required_kind or required_kind in _CAPABILITY_IMPLICATIONS.get(provider_kind, set())


def _field_compatible(provider: dict[str, Any], required: dict[str, Any], field: str) -> bool:
    expected = _string(required.get(field))
    actual = _string(provider.get(field))
    if not expected:
        return True
    if not actual:
        return False
    if expected == actual:
        return True
    if expected in {"any", "*"}:
        return True
    return actual in {"any", "*"}


def _constraints_compatible(provider: dict[str, Any], required: dict[str, Any]) -> bool:
    provider_constraints = set(_string_list(provider.get("constraints")))
    required_constraints = set(_string_list(required.get("constraints")))
    contradictory = {
        ("unauthenticated", "authenticated"),
        ("same-tenant", "cross-tenant"),
        ("same-process", "cross-process"),
    }
    for left, right in contradictory:
        if (
            (left in provider_constraints and right in required_constraints)
            or (right in provider_constraints and left in required_constraints)
        ):
            return False
    return True


def _handoff_present(provider_primitive: Primitive | None, consumer_primitive: Primitive | None) -> bool:
    for primitive in (provider_primitive, consumer_primitive):
        if not isinstance(primitive, dict):
            continue
        if _list(primitive.get("handoff_objects")):
            return True
    return False


def stable_edge_id(binding: dict[str, Any], index: int = 0) -> str:
    del index  # Kept for API compatibility; binding order is not edge identity.
    provider = binding.get("provider") if isinstance(binding.get("provider"), dict) else {}
    payload = json.dumps(
        {
            "consumer_primitive_id": binding.get("consumer_primitive_id", ""),
            "required_capability": _capability_identity(binding.get("required_capability")),
            "provider_type": provider.get("type", ""),
            "provider_primitive_id": provider.get("primitive_id", ""),
            "provider_capability": _capability_identity(provider.get("capability")),
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return "edge_" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def capability_compatible(
    provider: dict[str, Any],
    required: dict[str, Any],
    *,
    provider_primitive: Primitive | None = None,
    consumer_primitive: Primitive | None = None,
) -> tuple[bool, list[str]]:
    provider = normalize_capability(provider)
    required = normalize_capability(required)
    reasons: list[str] = []
    if not _cap_kind_satisfies(_string(provider.get("kind")), _string(required.get("kind"))):
        reasons.append("kind_mismatch")
    for field, reason in (
        ("object_type", "object_scope_mismatch"),
        ("principal", "principal_mismatch"),
        ("tenant", "tenant_mismatch"),
        ("scope", "scope_mismatch"),
    ):
        if not _field_compatible(provider, required, field):
            reasons.append(reason)
    provider_space = _string(provider.get("address_space"))
    required_space = _string(required.get("address_space"))
    if required_space and provider_space and required_space != provider_space:
        if not _handoff_present(provider_primitive, consumer_primitive):
            reasons.append("missing_handoff_object")
    elif required_space and not provider_space:
        reasons.append("address_space_mismatch")
    if not _constraints_compatible(provider, required):
        reasons.append("config_conflict")
    return not reasons, reasons


def primitive_requirements(primitive: Primitive) -> list[dict[str, Any]]:
    return normalize_capabilities(primitive.get("required_capabilities"))


def primitive_gains(primitive: Primitive) -> list[dict[str, Any]]:
    return normalize_capabilities(primitive.get("capabilities_gained"))


def primitive_has_terminal_impact(primitive: Primitive) -> bool:
    impact = primitive.get("terminal_impact")
    if not isinstance(impact, dict):
        return False
    systems = [
        impact.get("vulnerable_system"),
        impact.get("subsequent_system"),
    ]
    for system in systems:
        if isinstance(system, dict) and any(str(value).lower() in {"low", "high"} for value in system.values()):
            return True
    return False


def bind_requirements(
    primitive: Primitive,
    available: list[dict[str, Any]],
    *,
    primitives_by_id: dict[str, Primitive],
) -> tuple[bool, list[dict[str, Any]], list[str]]:
    bindings: list[dict[str, Any]] = []
    failures: list[str] = []
    consumer_id = _string(primitive.get("primitive_id"))
    for required in primitive_requirements(primitive):
        matched: dict[str, Any] | None = None
        match_reasons: list[str] = []
        for provider_capability in available:
            provider_id = _string(provider_capability.get("provider_primitive_id"))
            ok, reasons = capability_compatible(
                provider_capability,
                required,
                provider_primitive=primitives_by_id.get(provider_id),
                consumer_primitive=primitive,
            )
            if ok:
                matched = provider_capability
                break
            match_reasons.extend(reasons)
        if matched is None:
            failures.append(sorted(set(match_reasons))[0] if match_reasons else "missing_required_capability")
            continue
        binding = {
                "consumer_primitive_id": consumer_id,
                "required_capability": required,
                "provider": {
                    "type": "attacker_entry" if not matched.get("provider_primitive_id") else "primitive",
                    "primitive_id": matched.get("provider_primitive_id", ""),
                    "capability": {
                        key: value
                        for key, value in matched.items()
                        if key not in {"provider_primitive_id"}
                    },
                },
                "compatibility_reason": "deterministic capability compatibility checks passed",
                "deterministic_advisory": {"compatible": True, "reasons": []},
            }
        binding["edge_id"] = stable_edge_id(binding, len(bindings))
        bindings.append(binding)
    return not failures, bindings, failures


def merge_global_constraints(path: list[Primitive]) -> tuple[dict[str, Any], list[str]]:
    versions: list[list[str]] = []
    configs: list[str] = []
    repos: list[str] = []
    components: list[str] = []
    failures: list[str] = []
    root_keys: set[str] = set()
    for primitive in path:
        repos.append(_string(primitive.get("repo_id")) or "main")
        if primitive.get("component"):
            components.append(_string(primitive.get("component")))
        anchor = primitive.get("root_cause_anchor") if isinstance(primitive.get("root_cause_anchor"), dict) else {}
        root_key = json.dumps(
            {
                "repo": primitive.get("repo_id"),
                "symbol": anchor.get("symbol"),
                "locations": sorted(_string_list(anchor.get("locations"))),
            },
            sort_keys=True,
        )
        if root_key in root_keys:
            failures.append("cycle")
        root_keys.add(root_key)
        entry = primitive.get("entry_conditions") if isinstance(primitive.get("entry_conditions"), dict) else {}
        version_values = _string_list(entry.get("required_versions") or primitive.get("affected_versions"))
        if version_values:
            versions.append(version_values)
        configs.extend(_string_list(entry.get("required_config")))
    config_set = set(configs)
    for config in tuple(config_set):
        if config.startswith("not:") and config[4:] in config_set:
            failures.append("config_conflict")
        if ("not:" + config) in config_set:
            failures.append("config_conflict")
    return (
        {
            "repo_ids": sorted(set(filter(None, repos))),
            "components": sorted(set(filter(None, components))),
            "required_versions": versions,
            "required_config": sorted(config_set),
        },
        sorted(set(failures)),
    )


def stable_chain_id(primitive_ids: list[str], bindings: list[dict[str, Any]]) -> str:
    binding_identities: list[dict[str, Any]] = []
    for raw_binding in bindings:
        binding = raw_binding if isinstance(raw_binding, dict) else {}
        provider = binding.get("provider") if isinstance(binding.get("provider"), dict) else {}
        binding_identities.append(
            {
                "consumer_primitive_id": _string(binding.get("consumer_primitive_id")),
                "required_capability": _capability_identity(binding.get("required_capability")),
                "provider_type": _string(provider.get("type")),
                "provider_primitive_id": _string(provider.get("primitive_id")),
                "provider_capability": _capability_identity(provider.get("capability")),
            }
        )
    payload = json.dumps(
        {
            "schema_version": CHAIN_SCHEMA_VERSION,
            "primitive_ids": primitive_ids,
            "bindings": sorted(
                binding_identities,
                key=lambda item: json.dumps(
                    item, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                ),
            ),
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return "chain_" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def rank_chain_candidate(candidate: ChainCandidate, primitives_by_id: dict[str, Primitive]) -> float:
    primitive_ids = candidate.get("ordered_primitive_ids") or []
    confidence = 0.0
    count = 0
    for primitive_id in primitive_ids:
        primitive = primitives_by_id.get(str(primitive_id))
        confirmation = primitive.get("confirmation") if isinstance(primitive, dict) else {}
        try:
            confidence += float(confirmation.get("confidence", 0.0))
            count += 1
        except (TypeError, ValueError):
            pass
    confidence_score = confidence / count if count else 0.0
    binding_score = min(1.0, len(candidate.get("bindings") or []) / max(1, len(primitive_ids)))
    impact_score = 1.0 if candidate.get("expected_terminal_impact") else 0.0
    length_penalty = max(0.0, (len(primitive_ids) - 1) * 0.05)
    return round(max(0.0, confidence_score * 0.5 + binding_score * 0.25 + impact_score * 0.25 - length_penalty), 4)


__all__ = [
    "CHAIN_SCHEMA_VERSION",
    "capability_compatible",
    "primitive_requirements",
    "primitive_gains",
    "primitive_has_terminal_impact",
    "bind_requirements",
    "merge_global_constraints",
    "stable_chain_id",
    "rank_chain_candidate",
    "stable_edge_id",
]
