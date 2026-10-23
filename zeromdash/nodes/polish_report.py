"""Report-polish LangGraph node."""

from __future__ import annotations

import json
from typing import Any

from zeromdash import prompts
from zeromdash.agents import AgentResult
from zeromdash.state import ZeroMDASHState
from zeromdash.workspace import Workspace

from .core.context import _node_focus, _ws
from .core.invocation import _invoke_with_output_retry
from .core.io import _read_text_lossy
from .core.reporting import _report_format_diagnostics

def _polish_report_update(
    ws: Workspace,
    *,
    state: ZeroMDASHState,
    reports: list[dict[str, Any]],
) -> dict:
    errors = [
        f"[polish_report] {report['path']}: {issue}"
        for report in reports
        for issue in report["issues"]
    ]
    log_path = ws.log_path("review_log") / "polish_report.log"
    log_path.write_text(json.dumps({"reports": reports}, ensure_ascii=False, indent=2))
    out_en = ws.base / "summary.en.md"
    out_zh = ws.base / "summary.zh_CN.md"
    compat_out = ws.base / "summary.md"
    summary_en = _read_text_lossy(out_en)
    summary_zh = _read_text_lossy(out_zh)
    if summary_en:
        compat_out.write_text(summary_en, encoding="utf-8")
    return {
        "summary": summary_en or str(state.get("summary") or ""),
        "summary_en": summary_en,
        "summary_zh_CN": summary_zh,
        "errors": errors,
    }

def polish_report(state: ZeroMDASHState, *, backends=None) -> dict:
    """Lightweight report-format pass over existing summary Markdown files."""
    ws = _ws(state)
    out_en = ws.base / "summary.en.md"
    out_zh = ws.base / "summary.zh_CN.md"
    report_paths = [path for path in (out_en, out_zh) if path.is_file()]
    if not report_paths:
        return {
            "summary": str(state.get("summary") or ""),
            "summary_en": str(state.get("summary_en") or state.get("summary") or ""),
            "summary_zh_CN": str(state.get("summary_zh_CN") or ""),
            "errors": [],
        }

    diagnostics = [_report_format_diagnostics(path) for path in report_paths]
    focus = _node_focus(state, "summary_focus")
    prompt = prompts.POLISH_REPORT.format(
        target=state.get("target", ws.target or ws.task_id),
        focus=focus,
        out_en=out_en,
        out_zh=out_zh,
        diagnostics=json.dumps(diagnostics, ensure_ascii=False, indent=2),
    )

    def validate(res: AgentResult) -> bool:
        del res
        post_reports = [_report_format_diagnostics(path) for path in report_paths]
        return not any(report["issues"] for report in post_reports)

    _, invoke_errors = _invoke_with_output_retry(
        ws,
        "polish_report",
        prompt,
        backends,
        state,
        output_desc=f"polished {out_en} and {out_zh}",
        validate=validate,
        focus=focus,
        attempts=1,
    )
    reports = [_report_format_diagnostics(path) for path in report_paths]
    update = _polish_report_update(ws, state=state, reports=reports)
    if invoke_errors:
        update["errors"] = list(update.get("errors") or []) + invoke_errors
    return update

__all__ = ["_polish_report_update","polish_report"]

