"""Pure helpers for normalized, target-scoped gather evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from zeromdash.gather_state import GatherEvidenceUnit
from zeromdash.workspace import Workspace

from .primitive_qualification import finding_capability_provider
from .qualification import _finding_qualification_passed


def _stable_suffix(payload: dict[str, Any]) -> str:
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(data).hexdigest()[:16]


def source_ref(
    *,
    target_id: str,
    source_ws: Workspace,
    artifact_kind: str,
    snapshot_path: Path,
    snapshot_base: Path,
    local_id: str,
    payload: dict[str, Any],
    revision: str,
    json_pointer: str = "/",
) -> dict[str, Any]:
    evidence = payload.get("evidence") if isinstance(payload.get("evidence"), dict) else {}
    locations = evidence.get("code_locations") or payload.get("code_locations") or []
    return {
        "target_id": target_id,
        "workspace_id": source_ws.task_id,
        "artifact_kind": artifact_kind,
        "artifact_path": str(snapshot_path.relative_to(snapshot_base)),
        "artifact_sha256": hashlib.sha256(snapshot_path.read_bytes()).hexdigest(),
        "json_pointer": json_pointer,
        "local_id": local_id,
        "repo_id": str(payload.get("repo_id") or "main"),
        "revision": revision,
        "code_locations": [str(item) for item in locations if str(item).strip()],
    }


def unit_from_primitive(
    primitive: dict[str, Any],
    *,
    target_id: str,
    source_ref_value: dict[str, Any],
) -> GatherEvidenceUnit:
    local_id = str(primitive.get("primitive_id") or "").strip()
    if not local_id:
        local_id = "primitive-" + _stable_suffix(primitive)
    return {
        "unit_id": f"{target_id}::{local_id}",
        "local_id": local_id,
        "unit_kind": "primitive",
        "target_id": target_id,
        "component": str(primitive.get("component") or ""),
        "entry_conditions": dict(primitive.get("entry_conditions") or {}),
        "required_capabilities": list(primitive.get("required_capabilities") or []),
        "attacker_controls": list(primitive.get("attacker_controls") or []),
        "capabilities_gained": list(primitive.get("capabilities_gained") or []),
        "handoff_objects": list(primitive.get("handoff_objects") or []),
        "required_entity_states": list(primitive.get("required_entity_states") or []),
        "resulting_entity_states": list(primitive.get("resulting_entity_states") or []),
        "terminal_impact": dict(primitive.get("terminal_impact") or {}),
        "constraints": dict(primitive.get("global_constraints") or {}),
        "constituent_unit_ids": [],
        "source_refs": [source_ref_value],
        "source_payload": primitive,
    }


def unit_from_finding(
    finding: dict[str, Any],
    *,
    target_id: str,
    source_ref_value: dict[str, Any],
) -> GatherEvidenceUnit | None:
    if not _finding_qualification_passed(finding):
        return None
    provider = finding_capability_provider(finding)
    capability_view = finding.get("capability_view")
    if provider is None and not isinstance(capability_view, dict):
        return None
    source = provider or dict(capability_view)
    local_id = str(
        finding.get("subtask_id")
        or finding.get("finding_id")
        or source.get("primitive_id")
        or ""
    ).strip()
    if not local_id:
        local_id = "finding-" + _stable_suffix(finding)
    unit = unit_from_primitive(
        source,
        target_id=target_id,
        source_ref_value=source_ref_value,
    )
    unit.update(
        {
            "unit_id": f"{target_id}::{local_id}",
            "local_id": local_id,
            "unit_kind": "standalone_finding",
            "terminal_impact": dict(
                finding.get("direct_security_impact") or source.get("terminal_impact") or {}
            ),
            "source_payload": finding,
        }
    )
    return unit


def unit_from_chain(
    finding: dict[str, Any],
    *,
    target_id: str,
    source_ref_value: dict[str, Any],
) -> GatherEvidenceUnit:
    local_id = str(finding.get("chain_id") or finding.get("subtask_id") or "").strip()
    if not local_id:
        local_id = "chain-" + _stable_suffix(finding)
    constituent = [
        f"{target_id}::{item}"
        for item in finding.get("ordered_primitive_ids") or finding.get("source_primitive_ids") or []
        if str(item).strip()
    ]
    return {
        "unit_id": f"{target_id}::{local_id}",
        "local_id": local_id,
        "unit_kind": "local_chain",
        "target_id": target_id,
        "component": str(finding.get("component") or "local-chain"),
        "entry_conditions": dict(finding.get("attacker_entry") or {}),
        "required_capabilities": list(finding.get("required_capabilities") or []),
        "attacker_controls": list(finding.get("attacker_controls") or []),
        "capabilities_gained": list((finding.get("capability_view") or {}).get("capabilities_gained") or []),
        "handoff_objects": list(finding.get("handoff_objects") or []),
        "required_entity_states": list(finding.get("required_entity_states") or []),
        "resulting_entity_states": list(finding.get("resulting_entity_states") or []),
        "terminal_impact": dict(finding.get("direct_security_impact") or {}),
        "constraints": dict(finding.get("global_constraints") or {}),
        "constituent_unit_ids": constituent,
        "source_refs": [source_ref_value],
        "source_payload": finding,
    }


def evidence_index(units: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        str(unit.get("unit_id") or ""): unit
        for unit in units
        if isinstance(unit, dict) and str(unit.get("unit_id") or "")
    }


def merge_evidence_unit(
    units_by_id: dict[str, dict[str, Any]],
    unit: dict[str, Any],
    *,
    source_name: str,
) -> None:
    """Merge duplicate envelopes or fail on conflicting active evidence."""
    unit_id = str(unit.get("unit_id") or "")
    if not unit_id:
        raise ValueError(f"gather source {source_name!r} produced an empty unit id")
    existing = units_by_id.get(unit_id)
    if existing is None:
        units_by_id[unit_id] = unit
        return
    if json.dumps(existing.get("source_payload"), sort_keys=True, default=str) != json.dumps(
        unit.get("source_payload"), sort_keys=True, default=str
    ):
        raise ValueError(
            f"gather source {source_name!r} has conflicting active evidence for {unit_id}"
        )
    refs = list(existing.get("source_refs") or [])
    for ref in unit.get("source_refs") or []:
        if ref not in refs:
            refs.append(ref)
    existing["source_refs"] = refs


__all__ = [
    "evidence_index",
    "merge_evidence_unit",
    "source_ref",
    "unit_from_chain",
    "unit_from_finding",
    "unit_from_primitive",
]
