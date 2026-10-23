"""Build the normalized primitive pool consumed by chain planning."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from zeromdash.state import Finding, Primitive, ZeroMDASHState

from .core.context import _ws
from .core.primitive_qualification import dedupe_primitives, finding_capability_provider
from .core.qualification import _finding_qualification_passed
from .core.result_artifacts import (
    active_subtask_result_payloads,
    declared_package_ids,
    primitive_has_package_source,
)


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def _write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    os.replace(tmp, path)


def _state_standalone_findings(state: ZeroMDASHState) -> list[Finding]:
    findings: list[Finding] = []
    for bucket in (
        state.get("spec_findings", []),
        state.get("vuln_candidates", []),
        state.get("patch_findings", []),
        state.get("feature_findings", []),
    ):
        findings.extend(item for item in bucket if isinstance(item, dict))
    return findings


def _disk_primitives(ws, package_ids: set[str]) -> list[Primitive]:
    primitives: list[Primitive] = []
    primitive_dir = ws.log_path("primitive_res")
    if not primitive_dir.is_dir():
        return primitives
    for path in sorted(primitive_dir.glob("*.json")):
        payload = _read_json(path)
        if isinstance(payload, dict):
            if primitive_has_package_source(payload, package_ids):
                # Package primitives are recovered from the active atomic
                # artifacts below. This avoids resurrecting a primitive file
                # left behind by an earlier package rerun.
                continue
            primitives.append(payload)
    return primitives


def _subtask_res_primitives(
    payloads: list[tuple[Path, dict[str, Any]]],
) -> list[Primitive]:
    primitives: list[Primitive] = []
    for _, payload in payloads:
        primitive = payload.get("primitive")
        if isinstance(primitive, dict):
            primitives.append(primitive)
    return primitives


def materialize_chain_pool(state: ZeroMDASHState, *, backends=None) -> dict:
    del backends
    ws = _ws(state)
    result_payloads = active_subtask_result_payloads(ws)
    package_ids = declared_package_ids(ws)
    primitives: list[Primitive] = []
    primitives.extend(item for item in state.get("confirmed_primitives", []) if isinstance(item, dict))
    primitives.extend(_disk_primitives(ws, package_ids))
    primitives.extend(_subtask_res_primitives(result_payloads))

    for finding in _state_standalone_findings(state):
        if _finding_qualification_passed(finding):
            provider = finding_capability_provider(finding)
            if provider is not None:
                primitives.append(provider)

    chain_pool = dedupe_primitives(primitives)
    out = ws.state_path("chain_pool.json")
    _write_json_atomic(
        out,
        {
            "schema_version": "2.0",
            "primitive_count": len(chain_pool),
            "primitives": chain_pool,
        },
    )
    return {
        "chain_pool": chain_pool,
        "chain_pool_path": str(out),
    }


__all__ = ["materialize_chain_pool"]
