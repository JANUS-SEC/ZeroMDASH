"""Load active, qualified findings from existing ZeroMDASH workspaces."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from zeromdash.nodes.core.qualification import _finding_qualification_passed
from zeromdash.nodes.core.result_artifacts import active_subtask_result_payloads
from zeromdash.workspace import Workspace

from .io import canonical_json, read_json_object, sha256_text


def _identifier(value: Any) -> str:
    return str(value or "").strip()


def _request_record(
    state: dict[str, Any],
    *,
    finding_id: str,
    finding_type: str,
    finding: dict[str, Any],
    source_payload: dict[str, Any],
    source_result_path: str,
    aliases: list[str],
    group: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source_hash = sha256_text(canonical_json(source_payload))
    identity = {
        "workspace_id": state.get("task_id", ""),
        "finding_id": finding_id,
        "finding_type": finding_type,
        "source_sha256": source_hash,
        "request_revision": 1,
    }
    return {
        "request_id": "pocreq_" + sha256_text(canonical_json(identity))[:16],
        "request_revision": 1,
        "finding_id": finding_id,
        "finding_type": finding_type,
        "finding": finding,
        "group": group or {},
        "source_result_path": source_result_path,
        "source_artifact_sha256": source_hash,
        "aliases": sorted({item for item in aliases if item}),
    }


def _group_records(state: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for group in state.get("report_groups") or []:
        if not isinstance(group, dict) or group.get("summary_format") == "patch_gap":
            continue
        finding = group.get("primary_finding")
        if not isinstance(finding, dict) or not _finding_qualification_passed(finding):
            continue
        finding_id = _identifier(group.get("group_id"))
        if not finding_id:
            continue
        chain_id = _identifier(finding.get("chain_id"))
        aliases = [
            finding_id,
            _identifier(finding.get("subtask_id")),
            chain_id,
            *[str(item) for item in group.get("source_subtasks") or []],
            *[str(item) for item in group.get("source_chains") or []],
        ]
        records.append(
            _request_record(
                state,
                finding_id=finding_id,
                finding_type="chain_finding" if chain_id else "standalone_finding",
                finding=finding,
                source_payload=group,
                source_result_path=str(state.get("report_groups_path") or ""),
                aliases=aliases,
                group=group,
            )
        )
    return records


def _standalone_records(state: dict[str, Any], ws: Workspace) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path, payload in active_subtask_result_payloads(ws):
        finding = payload.get("finding")
        if not isinstance(finding, dict):
            continue
        outcome = _identifier(payload.get("outcome_type") or finding.get("outcome_type")).replace("-", "_")
        if outcome and outcome != "standalone_finding":
            continue
        if not _finding_qualification_passed(finding):
            continue
        finding_id = _identifier(finding.get("subtask_id") or finding.get("id") or path.stem)
        if finding_id:
            records.append(
                _request_record(
                    state,
                    finding_id=finding_id,
                    finding_type="standalone_finding",
                    finding=finding,
                    source_payload=payload,
                    source_result_path=str(path),
                    aliases=[finding_id, path.stem],
                )
            )
    return records


def _chain_records(state: dict[str, Any], ws: Workspace) -> list[dict[str, Any]]:
    active = state.get("chain_findings")
    active_ids = None if not isinstance(active, list) else {
        _identifier(item.get("chain_id")) for item in active if isinstance(item, dict)
    }
    records: list[dict[str, Any]] = []
    chain_dir = ws.log_path("chain_res")
    if not chain_dir.is_dir():
        return records
    for path in sorted(chain_dir.glob("*.json")):
        payload = read_json_object(path)
        if payload.get("outcome_type") != "chain_finding":
            continue
        finding = payload.get("finding")
        if not isinstance(finding, dict) or finding.get("closure_verdict") != "closed":
            continue
        if not _finding_qualification_passed(finding):
            continue
        finding_id = _identifier(finding.get("chain_id") or finding.get("subtask_id") or path.stem)
        if not finding_id or (active_ids is not None and finding_id not in active_ids):
            continue
        records.append(
            _request_record(
                state,
                finding_id=finding_id,
                finding_type="chain_finding",
                finding=finding,
                source_payload=payload,
                source_result_path=str(path),
                aliases=[finding_id, _identifier(finding.get("subtask_id")), path.stem],
            )
        )
    return records


def load_finding_records(state: dict[str, Any], selected_id: str = "") -> list[dict[str, Any]]:
    ws = Workspace.open(state["workspace_root"], state["task_id"])
    records = _group_records(state)
    if not records:
        records = [*_standalone_records(state, ws), *_chain_records(state, ws)]
    selected = _identifier(selected_id)
    if selected:
        lowered = selected.lower()
        matches = [record for record in records if lowered in {item.lower() for item in record["aliases"]}]
        if not matches:
            available = ", ".join(record["finding_id"] for record in records) or "(none)"
            raise ValueError(f"finding {selected!r} was not found; available finding IDs: {available}")
        if len(matches) > 1:
            raise ValueError(f"finding ID {selected!r} is ambiguous")
        return matches
    return records
