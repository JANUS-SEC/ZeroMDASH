"""Generate the final bilingual report for a gather scan."""

from __future__ import annotations

import json
import re

from zeromdash import prompts
from zeromdash.agents import AgentResult
from zeromdash.gather_state import GatherState

from .core.context import _node_focus, _ws
from .core.invocation import _invoke_with_output_retry
from .core.io import _file_has_text, _read_text_lossy, _reset_file_output
from .core.reporting import _each_vulnerability_has_both_diagrams


def gather_summary(state: GatherState, *, backends=None) -> dict:
    ws = _ws(state)
    out_en = ws.base / "summary.en.md"
    out_zh = ws.base / "summary.zh_CN.md"
    compat_out = ws.base / "summary.md"
    groups = [item for item in state.get("gather_report_groups") or [] if isinstance(item, dict)]
    focus = _node_focus(state, "summary_focus")
    prompt = prompts.GATHER_SUMMARY.format(
        scenario_name=state.get("scenario_name", "gather"),
        scenario=state.get("scenario", ""),
        registry_path=state.get("cross_target_registry_path", ""),
        input_lock_path=state.get("input_lock_path", ""),
        report_groups_json=json.dumps(groups, ensure_ascii=False, indent=2),
        unclosed_candidates_json=json.dumps(
            state.get("gather_chain_candidates") or [], ensure_ascii=False, indent=2
        ),
        errors_json=json.dumps(state.get("errors") or [], ensure_ascii=False, indent=2),
        out_en=out_en,
        out_zh=out_zh,
        focus=focus,
    )

    def reset() -> None:
        for path in (out_en, out_zh, compat_out):
            _reset_file_output(path)

    def materialize(res: AgentResult) -> None:
        del res
        if _file_has_text(out_en):
            compat_out.write_text(_read_text_lossy(out_en), encoding="utf-8")

    def validate(res: AgentResult) -> tuple[bool, str]:
        del res
        if not _file_has_text(out_en) or not _file_has_text(out_zh):
            return False, "both gather summary files must be non-empty"
        if not groups:
            return True, ""
        en = _read_text_lossy(out_en)
        zh = _read_text_lossy(out_zh)
        required_en = (
            "## Scenario and Target Topology",
            "## Cross-target Flow Registry",
            "## Vulnerability Details",
            "#### Cross-target Bindings",
            "#### Data Flow",
            "#### Attack Sequence",
        )
        required_zh = (
            "## 业务场景与目标拓扑",
            "## 跨目标数据流清单",
            "## 漏洞详情",
            "#### 跨目标绑定",
            "#### 数据流向图",
            "#### 攻击时序图",
        )
        if not all(marker in en for marker in required_en) or not all(
            marker in zh for marker in required_zh
        ):
            return False, "gather reports are missing required cross-target sections"
        pattern = re.compile(r"^###\s+(VULN-\d{3}):", re.MULTILINE)
        en_ids = pattern.findall(en)
        zh_ids = pattern.findall(zh)
        if not en_ids or en_ids != zh_ids or len(en_ids) != len(set(en_ids)):
            return False, "gather reports have inconsistent vulnerability group ids"
        if not _each_vulnerability_has_both_diagrams(en) or not _each_vulnerability_has_both_diagrams(zh):
            return False, "one or more gather findings lack data-flow and sequence diagrams"
        return True, ""

    _, errors = _invoke_with_output_retry(
        ws,
        "summary",
        prompt,
        backends,
        state,
        output_desc=f"{out_en} and {out_zh}",
        validate=validate,
        materialize=materialize,
        reset=reset,
        focus=focus,
        additional_read_roots=list(state.get("source_read_roots") or []),
    )
    summary_en = _read_text_lossy(out_en)
    summary_zh = _read_text_lossy(out_zh)
    if summary_en:
        compat_out.write_text(summary_en, encoding="utf-8")
    findings = [
        dict(group.get("primary_finding") or {})
        for group in groups
        if isinstance(group.get("primary_finding"), dict)
    ]
    gate = {
        "scan_mode": "gather",
        "scenario": state.get("scenario_name", "gather"),
        "source_workspaces": [
            {
                "target_id": item.get("target_id", ""),
                "workspace_path": item.get("workspace_path", ""),
            }
            for item in state.get("gather_targets") or []
        ],
        "decision": (
            "block"
            if any(item.get("gate_decision") == "block" for item in findings)
            else "warn"
            if any(item.get("gate_decision") == "warn" for item in findings)
            else "pass"
        ),
        "blocking_findings": [item for item in findings if item.get("gate_decision") == "block"],
        "warning_findings": [item for item in findings if item.get("gate_decision") == "warn"],
        "unclosed_candidates": list(state.get("gather_chain_candidates") or []),
        "input_lock_hash": state.get("input_lock_hash", ""),
    }
    gate_path = ws.base / "gate_result.json"
    gate_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "summary": summary_en,
        "summary_en": summary_en,
        "summary_zh_CN": summary_zh,
        "gate_result": gate,
        "gate_result_path": str(gate_path),
        "errors": errors,
    }


__all__ = ["gather_summary"]
