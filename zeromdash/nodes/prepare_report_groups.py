"""Prepare deterministic report groups before the summary node."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from zeromdash import prompts
from zeromdash.agents import AgentResult
from zeromdash.state import Finding, ZeroMDASHState

from .core.context import _node_focus, _ws
from .core.invocation import _invoke_with_output_retry
from .core.qualification import _summary_list
from .core.report_dedup import apply_report_group_adjudication, build_report_groups


ADJUDICATOR_NODE = "report_group_adjudicator"


def _write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    os.replace(tmp, path)


def _standalone_findings(state: ZeroMDASHState) -> list[Finding]:
    findings: list[Finding] = []
    for bucket in (
        state.get("spec_findings", []),
        state.get("vuln_candidates", []),
        state.get("patch_findings", []),
        state.get("feature_findings", []),
    ):
        findings.extend(item for item in bucket if isinstance(item, dict))
    return findings


def _dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _string(value: Any) -> str:
    return str(value or "").strip()


def _truncate(value: Any, limit: int = 1400) -> str:
    text = _string(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def _group_for_adjudication(group: dict[str, Any]) -> dict[str, Any]:
    primary = _dict(group.get("primary_finding"))
    review = _dict(primary.get("review"))
    primitive = _dict(primary.get("primitive")) or _dict(review.get("primitive"))
    anchor = _dict(primitive.get("root_cause_anchor"))
    evidence = _dict(primary.get("evidence"))
    return {
        "group_id": group.get("group_id", ""),
        "group_key": group.get("group_key", ""),
        "title": group.get("title", ""),
        "summary_format": group.get("summary_format", "full"),
        "severity": group.get("severity", ""),
        "cvss4_score": group.get("cvss4_score"),
        "cvss4_vector": group.get("cvss4_vector", ""),
        "confidence": group.get("confidence", 0.0),
        "source_subtasks": group.get("source_subtasks", []),
        "source_chains": group.get("source_chains", []),
        "source_primitive_ids": group.get("source_primitive_ids", []),
        "primary_id": primary.get("chain_id") or primary.get("subtask_id") or "",
        "primary_kind": primary.get("kind", ""),
        "violated_security_property": (
            primary.get("violated_security_property")
            or review.get("violated_security_property")
            or ""
        ),
        "root_cause_anchor": {
            "symbol": anchor.get("symbol", ""),
            "locations": anchor.get("locations", []),
        },
        "code_locations": _summary_list(evidence.get("code_locations"))[:10],
        "call_path_tail": (
            _summary_list(evidence.get("call_path"))
            or _summary_list(evidence.get("call_paths"))
        )[-4:],
        "direct_security_impact": (
            primary.get("direct_security_impact")
            or review.get("direct_security_impact")
            or {}
        ),
        "detail_excerpt": _truncate(primary.get("detail") or review.get("reasoning")),
    }


def _validate_adjudication_output(res: AgentResult) -> bool:
    try:
        payload = json.loads(res.stdout)
    except json.JSONDecodeError:
        return False
    if not isinstance(payload, dict):
        return False
    merge_groups = payload.get("merge_groups")
    if not isinstance(merge_groups, list):
        return False
    for index, item in enumerate(merge_groups):
        if not isinstance(item, dict):
            return False
        source_ids = [
            _string(group_id)
            for group_id in _summary_list(item.get("source_group_ids"))
            if _string(group_id)
        ]
        if len(source_ids) < 2 or len(source_ids) != len(set(source_ids)):
            return False
        if not _string(item.get("reasoning")):
            return False
    return True


def _run_report_group_adjudicator(
    state: ZeroMDASHState,
    groups: list[dict[str, Any]],
    *,
    backends=None,
) -> tuple[dict[str, Any] | None, list[str]]:
    ws = _ws(state)
    disabled = set(state.get("disabled_nodes") or [])
    full_groups = [group for group in groups if group.get("summary_format") != "patch_gap"]
    if ADJUDICATOR_NODE in disabled or len(full_groups) < 2:
        return None, []
    prompt = prompts.REPORT_GROUP_ADJUDICATOR.format(
        target=state.get("target", ""),
        focus=_node_focus(state, "report_group_adjudicator_focus"),
        groups_json=json.dumps(
            [_group_for_adjudication(group) for group in full_groups],
            ensure_ascii=False,
            indent=2,
        ),
    )
    res, errors = _invoke_with_output_retry(
        ws,
        ADJUDICATOR_NODE,
        prompt,
        backends,
        state,
        output_desc="a JSON report-group adjudication with merge_groups",
        validate=_validate_adjudication_output,
        focus=_node_focus(state, "report_group_adjudicator_focus"),
    )
    if errors or res is None:
        return None, errors
    try:
        payload = json.loads(res.stdout)
    except json.JSONDecodeError:
        return None, ["report-group adjudicator output is not parseable JSON"]
    return payload if isinstance(payload, dict) else None, []


def prepare_report_groups(state: ZeroMDASHState, *, backends=None) -> dict:
    ws = _ws(state)
    groups = build_report_groups(
        standalone_findings=_standalone_findings(state),
        chain_findings=[
            finding
            for finding in state.get("chain_findings", []) or []
            if isinstance(finding, dict)
        ],
    )
    adjudication, adjudication_errors = _run_report_group_adjudicator(
        state,
        groups,
        backends=backends,
    )
    dedup_errors: list[str] = []
    if adjudication is not None:
        merged, dedup_errors = apply_report_group_adjudication(groups, adjudication)
        if not dedup_errors:
            groups = merged
    out = ws.log / "report_groups.json"
    _write_json_atomic(
        out,
        {
            "schema_version": "2.0",
            "group_count": len(groups),
            "groups": groups,
            "adjudication": adjudication or {},
            "adjudication_errors": list(adjudication_errors or []) + dedup_errors,
        },
    )
    return {
        "report_groups": groups,
        "report_groups_path": str(out),
    }


__all__ = ["prepare_report_groups"]
