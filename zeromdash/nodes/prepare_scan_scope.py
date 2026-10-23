"""LangGraph node implementation: prepare_scan_scope."""

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

from .core.context import _ws

def prepare_scan_scope(state: ZeroMDASHState, *, backends=None) -> dict:
    del backends
    ws = _ws(state)
    scope_dir = ws.main_path("scope")
    mode = str(state.get("scan_mode") or "full").strip().lower()
    try:
        scope = materialize_scan_scope(
            scope_dir=scope_dir,
            repo_path=Path(state["repo_path"]),
            mode=mode,
            diff_file=str(state.get("diff_file") or ""),
            diff_git=str(state.get("diff_git") or ""),
        )
    except (OSError, ValueError) as exc:
        return {
            "scope_path": str(scope_dir / "scope.json"),
            "scan_scope": {},
            "errors": [f"[prepare_scan_scope] {exc}"],
        }
    missing = (
        scope.get("patched_repo_validation", {}).get("missing_non_deleted_paths", [])
        if isinstance(scope, dict)
        else []
    )
    if missing:
        return {
            "scope_path": str(scope_dir / "scope.json"),
            "scan_scope": scope,
            "errors": [
                "[prepare_scan_scope] patched repository does not contain "
                f"{len(missing)} non-deleted diff path(s): {', '.join(missing[:10])}"
            ],
        }
    return {
        "scope_path": str(scope_dir / "scope.json"),
        "scan_scope": scope,
        "errors": [],
    }

__all__ = ["prepare_scan_scope"]

