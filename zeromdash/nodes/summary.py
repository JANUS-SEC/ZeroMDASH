"""Final bilingual summary LangGraph node."""

from __future__ import annotations

import json
import re
from pathlib import Path

from zeromdash import prompts
from zeromdash.agents import AgentResult
from zeromdash.state import ZeroMDASHState

from .core.constants import _SUMMARY_FORMAT_PATCH_GAP
from .core.context import _node_focus, _ws
from .core.invocation import _invoke_with_output_retry
from .core.io import _file_has_text, _read_text_lossy, _reset_file_output
from .core.qualification import (
    _compact_summary_buckets,
    _compact_summary_finding,
    _compact_summary_observations,
    _finding_qualification_passed,
    _summary_list,
)
from .core.report_dedup import compact_report_group
from .core.result_artifacts import active_subtask_result_files
from .core.reporting import _each_vulnerability_has_both_diagrams


def _primitive_compact_for_summary(primitive: dict) -> dict:
    evidence = primitive.get("evidence") if isinstance(primitive.get("evidence"), dict) else {}
    return {
        "primitive_id": primitive.get("primitive_id", ""),
        "source_subtask_ids": _summary_list(primitive.get("source_subtask_ids")),
        "component": primitive.get("component", ""),
        "root_cause_anchor": primitive.get("root_cause_anchor") or {},
        "entry_conditions": primitive.get("entry_conditions") or {},
        "capabilities_gained": _summary_list(primitive.get("capabilities_gained")),
        "handoff_objects": _summary_list(primitive.get("handoff_objects")),
        "terminal_impact": primitive.get("terminal_impact") or {},
        "missing_next_capabilities": _summary_list(primitive.get("missing_next_capabilities")),
        "evidence": {
            "code_locations": _summary_list(evidence.get("code_locations"))[:12],
            "call_path": _summary_list(evidence.get("call_path"))[:6],
            "patch_refs": _summary_list(evidence.get("patch_refs"))[:6],
            "writeup_refs": _summary_list(evidence.get("writeup_refs"))[:6],
        },
    }


def summary(state: ZeroMDASHState, *, backends=None) -> dict:
    ws = _ws(state)
    out_en = ws.base / "summary.en.md"
    out_zh = ws.base / "summary.zh_CN.md"
    compat_out = ws.base / "summary.md"
    focus = _node_focus(state, "summary_focus")
    compact = _compact_summary_buckets(state)
    chain_findings = [
        compact_finding
        for compact_finding in (
            _compact_summary_finding(finding, "chain")
            for finding in sorted(
                (finding for finding in state.get("chain_findings", []) if isinstance(finding, dict)),
                key=lambda item: str(item.get("chain_id") or item.get("subtask_id") or ""),
            )
        )
        if compact_finding is not None
    ]
    report_groups = [
        compact_report_group(group)
        for group in state.get("report_groups", []) or []
        if isinstance(group, dict)
    ]
    observations = _compact_summary_observations(state)
    confirmed_primitives = [
        _primitive_compact_for_summary(primitive)
        for primitive in state.get("confirmed_primitives", []) or []
        if isinstance(primitive, dict)
    ]
    compact_findings = [
        finding for bucket in compact.values() for finding in bucket
    ] + chain_findings + report_groups
    has_findings = bool(compact_findings)
    has_full_findings = any(
        finding.get("summary_format") != _SUMMARY_FORMAT_PATCH_GAP
        for finding in compact_findings
    )
    patch_gap_findings = [
        finding
        for finding in compact_findings
        if finding.get("summary_format") == _SUMMARY_FORMAT_PATCH_GAP
    ]
    has_patch_gap_findings = bool(patch_gap_findings)
    patch_gap_cve_ids = sorted(
        {
            cve_id
            for finding in patch_gap_findings
            for cve_id in _summary_list(finding.get("cve_ids"))
        }
    )
    prompt = prompts.SUMMARY.format(
        target=state["target"],
        focus=focus,
        repo_path=state.get("repo_path", str(ws.main_path("repo"))),
        subtask_res_dir=ws.log_path("subtask_res"),
        subtask_result_files="\n".join(
            str(path) for path in active_subtask_result_files(ws)
        ),
        chain_res_dir=ws.log_path("chain_res"),
        primitive_res_dir=ws.log_path("primitive_res"),
        report_groups_path=state.get("report_groups_path", str(ws.log / "report_groups.json")),
        report_groups=json.dumps(report_groups, ensure_ascii=False, indent=2),
        chain_findings=json.dumps(chain_findings, ensure_ascii=False, indent=2),
        target_writeup_dir=ws.main_path("writeup"),
        target_patch_dir=ws.main_path("patch"),
        similar_dir=ws.similar,
        spec_findings=json.dumps(compact["spec_findings"], ensure_ascii=False, indent=2),
        vuln_candidates=json.dumps(compact["vuln_candidates"], ensure_ascii=False, indent=2),
        patch_findings=json.dumps(compact["patch_findings"], ensure_ascii=False, indent=2),
        feature_findings=json.dumps(compact["feature_findings"], ensure_ascii=False, indent=2),
        confirmed_primitives=json.dumps(confirmed_primitives, ensure_ascii=False, indent=2),
        observations=json.dumps(observations, ensure_ascii=False, indent=2),
        out_en=out_en,
        out_zh=out_zh,
    )

    def reset_outputs() -> None:
        _reset_file_output(out_en)
        _reset_file_output(out_zh)
        _reset_file_output(compat_out)

    def materialize(res: AgentResult) -> None:
        if not (_file_has_text(out_en) and _file_has_text(out_zh)):
            return
        compat_out.write_text(_read_text_lossy(out_en))

    def report_has_required_structure(path: Path, *, chinese: bool) -> bool:
        text = _read_text_lossy(path)
        if not text.strip():
            return False
        if confirmed_primitives:
            primitive_marker = "## 已确认原语" if chinese else "## Confirmed Primitives"
            if primitive_marker not in text:
                return False
            primitive_ids = {
                str(item.get("primitive_id") or "")
                for item in confirmed_primitives
                if str(item.get("primitive_id") or "")
            }
            if not primitive_ids.issubset(set(re.findall(r"\bprim_[0-9A-Za-z_:-]+\b", text))):
                return False
        if not has_findings:
            return True
        full_ok = True
        if has_full_findings:
            required = (
                (
                    "## 漏洞详情",
                    "#### 漏洞介绍",
                    "#### 威胁模型",
                    "#### 触发条件",
                    "#### 数据流向图",
                    "#### 攻击时序图",
                    "#### 代码证据",
                    "#### CVSS v4.0",
                    "#### 版本影响范围",
                )
                if chinese
                else (
                    "## Vulnerability Details",
                    "#### Vulnerability Description",
                    "#### Threat Model",
                    "#### Trigger Conditions",
                    "#### Data Flow",
                    "#### Attack Sequence",
                    "#### Code Evidence",
                    "#### CVSS v4.0",
                    "#### Affected Versions",
                )
            )
            full_ok = (
                all(marker in text for marker in required)
                and _each_vulnerability_has_both_diagrams(text)
                and bool(re.search(r"```(?!mermaid\b)[A-Za-z0-9_+.-]+\s*\n", text))
            )
        patch_gap_ok = True
        if has_patch_gap_findings:
            patch_required = (
                (
                    "## 已知 CVE 补丁缺口",
                    "#### CVE-",
                    "补丁状态：未应用",
                )
                if chinese
                else (
                    "## Known CVE Patch Gaps",
                    "#### CVE-",
                    "Patch status: not applied",
                )
            )
            patch_gap_ok = all(marker in text for marker in patch_required) and all(
                cve_id in text for cve_id in patch_gap_cve_ids
            )
        return full_ok and patch_gap_ok

    def validate(res: AgentResult) -> bool:
        del res
        if not (
            report_has_required_structure(out_en, chinese=False)
            and report_has_required_structure(out_zh, chinese=True)
        ):
            return False
        if has_full_findings:
            group_pattern = re.compile(r"^###\s+(VULN-\d{3}):", re.MULTILINE)
            en_groups = group_pattern.findall(_read_text_lossy(out_en))
            zh_groups = group_pattern.findall(_read_text_lossy(out_zh))
            if not en_groups or en_groups != zh_groups or len(en_groups) != len(set(en_groups)):
                return False
        if has_patch_gap_findings:
            cve_pattern = re.compile(r"^####\s+(CVE-\d{4}-\d{4,7})\b", re.MULTILINE)
            en_cves = cve_pattern.findall(_read_text_lossy(out_en))
            zh_cves = cve_pattern.findall(_read_text_lossy(out_zh))
            if en_cves != zh_cves or not set(patch_gap_cve_ids).issubset(set(en_cves)):
                return False
        compat_out.write_text(_read_text_lossy(out_en))
        return _file_has_text(compat_out)

    _, errors = _invoke_with_output_retry(
        ws,
        "summary",
        prompt,
        backends,
        state,
        output_desc=f"{out_en} and {out_zh}",
        reset=reset_outputs,
        materialize=materialize,
        validate=validate,
        focus=focus,
    )
    summary_en = _read_text_lossy(out_en)
    summary_zh = _read_text_lossy(out_zh)
    gate_result_path = ws.base / "gate_result.json"
    scope = state.get("scan_scope") if isinstance(state.get("scan_scope"), dict) else {}
    findings = [
        finding
        for bucket in (
            state.get("spec_findings", []),
            state.get("vuln_candidates", []),
            state.get("patch_findings", []),
            state.get("feature_findings", []),
            state.get("chain_findings", []),
        )
        for finding in bucket
        if isinstance(finding, dict) and _finding_qualification_passed(finding)
    ]
    gate_findings = [
        {
            "subtask_id": finding.get("subtask_id", ""),
            "kind": finding.get("kind", ""),
            "title": finding.get("title", ""),
            "severity": finding.get("severity", ""),
            "cvss4_score": finding.get("cvss4_score"),
            "cvss4_vector": finding.get("cvss4_vector", ""),
            "disposition": finding.get("disposition", ""),
            "confidence": finding.get("confidence", 0.0),
            "scope_verdict": finding.get("scope_verdict", ""),
            "gate_decision": finding.get("gate_decision", ""),
            "changed_locations": finding.get("diff_evidence", {}).get("changed_locations", []),
            "change_to_sink_path": finding.get("diff_evidence", {}).get("change_to_sink_path", []),
        }
        for finding in findings
    ]
    gate_result = {
        "scan_mode": scope.get("mode", state.get("scan_mode", "full")),
        "scope_path": state.get("scope_path", ""),
        "diff_hash": scope.get("diff_hash", ""),
        "decision": (
            "block"
            if any(item["gate_decision"] == "block" for item in gate_findings)
            else "warn"
            if any(item["gate_decision"] == "warn" for item in gate_findings)
            else "pass"
        ),
        "blocking_findings": [
            item for item in gate_findings if item["gate_decision"] == "block"
        ],
        "warning_findings": [
            item for item in gate_findings if item["gate_decision"] == "warn"
        ],
        "ignored_findings": [
            item for item in gate_findings if item["gate_decision"] == "ignore"
        ],
        "non_vulnerability_observations": observations,
        "confirmed_primitives": confirmed_primitives,
    }
    gate_result_path.write_text(json.dumps(gate_result, ensure_ascii=False, indent=2))
    return {
        "summary": summary_en,
        "summary_en": summary_en,
        "summary_zh_CN": summary_zh,
        "gate_result": gate_result,
        "gate_result_path": str(gate_result_path),
        "errors": errors,
    }

__all__ = ["summary"]
