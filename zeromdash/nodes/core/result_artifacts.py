"""Resolve and classify the committed view of persisted subtask results.

A hypothesis package is committed by its parent manifest. Per-hypothesis files
are written first, so files left by an older rerun must not become inputs to
restore, chain planning, or reporting unless the current manifest lists them.
This module enforces that structural publication boundary and the shared
live/restore classification rules for each published atomic result.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from zeromdash.workspace import Workspace

from .qualification import (
    _finding_disposition,
    _finding_qualification_passed,
    _known_cve_patch_gap_ids,
)


def _finding_bucket_key(finding: dict[str, Any]) -> str:
    return {
        "spec": "spec_findings",
        "vuln": "vuln_candidates",
        "feature": "feature_findings",
    }.get(str(finding.get("kind") or ""), "patch_findings")


def append_finalized_result_state(
    update: dict[str, list[dict[str, Any]]],
    *,
    finding: Any,
    outcome_type: str = "",
    primitive: Any = None,
    legacy_unclassified: bool = False,
) -> None:
    """Classify one persisted result exactly as live finalization does.

    Package closure is deliberately absent from this decision: the parent
    manifest publishes its listed atoms, while each atom's terminal outcome
    decides which state channel receives it.  Unversioned legacy results did
    not record outcome or qualification metadata, so callers may retain their
    historical bucket-only restore behavior with ``legacy_unclassified``.
    """
    if not isinstance(finding, dict):
        return
    outcome = str(outcome_type or finding.get("outcome_type") or "").strip().lower()
    if outcome == "rejected":
        return
    if legacy_unclassified:
        update.setdefault(_finding_bucket_key(finding), []).append(finding)
        return
    if outcome == "confirmed_primitive":
        if isinstance(primitive, dict):
            update.setdefault("confirmed_primitives", []).append(primitive)
        update.setdefault("observations", []).append(finding)
        return
    if outcome != "standalone_finding" or not _finding_qualification_passed(finding):
        if (
            str(finding.get("kind") or "") == "patch_miss"
            and str(finding.get("patch_status") or "") == "not_applied"
            and _finding_disposition(finding) == "known_cve_patch_gap"
            and _known_cve_patch_gap_ids(finding, "patch")
        ):
            update.setdefault("patch_findings", []).append(finding)
        update.setdefault("observations", []).append(finding)
        return
    update.setdefault(_finding_bucket_key(finding), []).append(finding)


def _read_payload(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def subtask_result_payloads(
    ws: Workspace,
) -> list[tuple[Path, dict[str, Any]]]:
    """Read every parseable persisted result, before publication filtering."""
    return [
        (path, payload)
        for path in ws.subtask_result_files()
        if (payload := _read_payload(path)) is not None
    ]


def active_subtask_result_payloads(
    ws: Workspace,
) -> list[tuple[Path, dict[str, Any]]]:
    """Return legacy results plus only manifest-published package atoms."""
    payloads = subtask_result_payloads(ws)
    package_artifacts: dict[str, set[str]] = {}
    for _, payload in payloads:
        package_id = str(payload.get("package_id") or "").strip()
        if payload.get("result_type") != "hypothesis_package" or not package_id:
            continue
        package_artifacts[package_id] = {
            Path(str(artifact.get("path") or "")).name
            for artifact in payload.get("artifacts", []) or []
            if isinstance(artifact, dict)
            and Path(str(artifact.get("path") or "")).name
        }

    active: list[tuple[Path, dict[str, Any]]] = []
    for path, payload in payloads:
        if payload.get("result_type") == "hypothesis_package":
            active.append((path, payload))
            continue
        finding = payload.get("finding")
        parent_id = (
            str(finding.get("parent_subtask_id") or "").strip()
            if isinstance(finding, dict)
            else ""
        )
        if not parent_id:
            parent_id = str(payload.get("package_id") or "").strip()
        if parent_id and path.name not in package_artifacts.get(parent_id, set()):
            continue
        active.append((path, payload))
    return active


def active_subtask_result_files(ws: Workspace) -> list[Path]:
    return [path for path, _ in active_subtask_result_payloads(ws)]


def declared_package_ids(ws: Workspace) -> set[str]:
    """Return package IDs declared by manifests or atomic result records."""
    return {
        str(payload.get("package_id") or "").strip()
        for _, payload in subtask_result_payloads(ws)
        if str(payload.get("package_id") or "").strip()
    }


def primitive_has_package_source(
    primitive: Any,
    package_ids: set[str],
) -> bool:
    if not isinstance(primitive, dict):
        return False
    source_ids = {
        str(item).strip()
        for item in primitive.get("source_subtask_ids", []) or []
        if str(item).strip()
    }
    return any(
        source_id.startswith(f"{package_id}--")
        for source_id in source_ids
        for package_id in package_ids
    )


__all__ = [
    "active_subtask_result_files",
    "active_subtask_result_payloads",
    "append_finalized_result_state",
    "declared_package_ids",
    "primitive_has_package_source",
    "subtask_result_payloads",
]
