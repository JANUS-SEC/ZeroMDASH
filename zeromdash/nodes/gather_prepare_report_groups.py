"""Build canonical report groups from confirmed gather-chain findings."""

from __future__ import annotations

import json
import hashlib
from typing import Any

from zeromdash import prompts
from zeromdash.agents import AgentResult
from zeromdash.gather_state import GatherState

from .core.context import _node_focus, _ws
from .core.invocation import _invoke_with_output_retry
from .core.io import _try_json
from .core.report_dedup import apply_report_group_adjudication, _report_group_from_findings
from .materialize_chain_pool import _write_json_atomic
from .prepare_report_groups import _group_for_adjudication, _validate_adjudication_output


def gather_prepare_report_groups(state: GatherState, *, backends=None) -> dict:
    ws = _ws(state)
    findings = [
        item
        for item in state.get("gather_chain_findings") or []
        if isinstance(item, dict) and item.get("qualification_gate_passed") is True
    ]
    grouped: dict[str, list[dict[str, Any]]] = {}
    for finding in findings:
        sequence = list(finding.get("target_sequence") or [])
        material = {
            "security_property": finding.get("violated_security_property")
            or (finding.get("review") or {}).get("violated_security_property")
            or finding.get("title"),
            "final_target": sequence[-1] if sequence else "",
            "target_sequence": sequence,
            "root_cause": (finding.get("evidence") or {}).get("root_cause_anchor") or {},
        }
        key = hashlib.sha256(
            json.dumps(material, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
        ).hexdigest()[:16]
        grouped.setdefault(key, []).append(finding)
    ordered = sorted(
        grouped.items(),
        key=lambda item: (
            -max(float(finding.get("cvss4_score") or 0.0) for finding in item[1]),
            -max(float(finding.get("confidence") or 0.0) for finding in item[1]),
            item[0],
        ),
    )
    groups = [
        _report_group_from_findings(index, key, group_findings)
        for index, (key, group_findings) in enumerate(ordered, start=1)
    ]
    adjudication: dict[str, Any] | None = None
    errors: list[str] = []
    if len(groups) >= 2:
        focus = _node_focus(state, "gather_report_group_adjudicator_focus")
        prompt = prompts.GATHER_REPORT_GROUP_ADJUDICATOR.format(
            scenario_name=state.get("scenario_name", "gather"),
            focus=focus,
            groups_json=json.dumps(
                [_group_for_adjudication(group) for group in groups],
                ensure_ascii=False,
                indent=2,
            ),
        )

        def validate(res: AgentResult) -> tuple[bool, str]:
            ok = _validate_adjudication_output(res)
            return ok, "invalid gather report-group adjudication" if not ok else ""

        result, errors = _invoke_with_output_retry(
            ws,
            "gather_report_group_adjudicator",
            prompt,
            backends,
            state,
            output_desc="a JSON gather report-group adjudication",
            validate=validate,
            artifact_filenames=("gather_report_group_adjudication.json", "output.json"),
            focus=focus,
        )
        if result is not None and not errors:
            payload = _try_json(result.stdout, fallback=None)
            adjudication = payload if isinstance(payload, dict) else None
    dedup_errors: list[str] = []
    if adjudication is not None:
        merged, dedup_errors = apply_report_group_adjudication(groups, adjudication)
        if not dedup_errors:
            groups = merged
    out = ws.log / "gather_report_groups.json"
    _write_json_atomic(
        out,
        {
            "schema_version": "1.0",
            "group_count": len(groups),
            "groups": groups,
            "adjudication": adjudication or {},
            "adjudication_errors": [*errors, *dedup_errors],
        },
    )
    return {
        "gather_report_groups": groups,
        "gather_report_groups_path": str(out),
        "errors": errors + dedup_errors,
    }


__all__ = ["gather_prepare_report_groups"]
