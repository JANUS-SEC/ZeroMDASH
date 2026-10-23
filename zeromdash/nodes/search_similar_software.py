"""LangGraph node implementation: search_similar_software."""

from __future__ import annotations

import copy
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any

from langgraph.constants import Send

from zeromdash import prompts, skills as skills_mod
from zeromdash.agents import AgentResult, normalize_agent_name
from zeromdash.scope import materialize_scan_scope
from zeromdash.state import Finding, ReviewTurn, Subtask, ZeroMDASHState
from zeromdash.workspace import Workspace, slugify

from .core.context import (
    _node_focus,
    _ws,
)
from .core.invocation import _invoke_with_output_retry
from .core.io import (
    _file_has_text,
    _read_text_lossy,
    _reset_file_output,
    _write_stdout_fallback_file,
)
from .core.search import (
    _parse_candidate_names,
    _safe_similar_software_name,
)

def search_similar_software(state: ZeroMDASHState, *, backends=None) -> dict:
    ws = _ws(state)
    # 先把候选清单落到 similar/_candidates.json
    out = ws.similar / "_candidates.json"
    focus = _node_focus(state, "search_similar_software_focus")
    prompt = prompts.SEARCH_SIMILAR_SOFTWARE.format(
        target=state["target"],
        focus=focus,
        out_path=out,
    )
    names: list[str] = []

    def materialize(res: AgentResult) -> None:
        _write_stdout_fallback_file(out, res.stdout)

    def validate(res: AgentResult) -> bool:
        nonlocal names
        file_valid, file_names, _ = _parse_candidate_names(_read_text_lossy(out))
        if file_valid and _file_has_text(out):
            names = file_names
            return True
        stdout_valid, stdout_names, stdout_payload = _parse_candidate_names(res.stdout)
        if stdout_valid:
            names = stdout_names
            out.write_text(json.dumps(stdout_payload, ensure_ascii=False, indent=2))
            return _file_has_text(out)
        return False

    _, errors = _invoke_with_output_retry(
        ws,
        "search_similar_software",
        prompt,
        backends,
        state,
        output_desc=str(out),
        reset=lambda: _reset_file_output(out),
        materialize=materialize,
        validate=validate,
        focus=focus,
    )
    # 为每个候选预创建 similar/<slug>/{repo,writeup,patch}
    for nm in names:
        ws.similar_for(nm)
    return {
        "similar_repos": names,
        "errors": errors,
    }

def dispatch_similar_history(state: ZeroMDASHState) -> list[Send] | str:
    """Fan out one search_similar_history invocation per similar software."""
    sends: list[Send] = []
    for sw in state.get("similar_repos") or []:
        sw_name = _safe_similar_software_name(sw)
        # Skip fallback paths / malformed entries. search_similar_software should
        # normally return normalized names, but keeping this guard lets an empty
        # or failed candidate parse route straight to the analyzer barrier.
        if not sw_name:
            continue
        child: dict[str, Any] = {
            "task_id": state["task_id"],
            "workspace_root": state["workspace_root"],
            "target": state.get("target", ""),
            "common_focus": state.get("common_focus", ""),
            "scope_path": state.get("scope_path", ""),
            "scan_scope": dict(state.get("scan_scope") or {}),
            "agent_configs": state.get("agent_configs", {}),
            "agent_config_task_types": state.get("agent_config_task_types", {}),
            "similar_software": sw_name,
        }
        sends.append(Send("search_similar_history", child))
    return sends or "search_similar_history"

__all__ = ["search_similar_software","dispatch_similar_history"]

