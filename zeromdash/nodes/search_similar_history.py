"""LangGraph node implementation: search_similar_history."""

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
    _dir_has_materialized_output,
    _reset_dir_output,
)
from .core.search import _safe_similar_software_name

def search_similar_history(state: ZeroMDASHState, *, backends=None) -> dict:
    ws = _ws(state)
    similars = [state["similar_software"]] if state.get("similar_software") else state.get("similar_repos") or []
    writeup_dirs: list[str] = []
    patch_dirs: list[str] = []
    errors: list[str] = []
    for sw in similars:
        sw = _safe_similar_software_name(sw)
        # 跳过看起来不是名字的项 (例如 fallback 路径)
        if not sw:
            continue
        sw_dir = ws.similar_for(sw)
        wdir = sw_dir / "writeup"
        pdir = sw_dir / "patch"
        focus = _node_focus(state, "search_similar_history_focus")
        prompt = prompts.SEARCH_SIMILAR_HISTORY.format(
            similar=sw, focus=focus, writeup_dir=wdir, patch_dir=pdir,
        )
        subtask_id = slugify(sw)

        def reset_dirs(wdir=wdir, pdir=pdir) -> None:
            _reset_dir_output(wdir)
            _reset_dir_output(pdir)

        def materialize(res: AgentResult, wdir=wdir) -> None:
            if res.stdout.strip():
                (wdir / "_raw.md").write_text(res.stdout)

        _, item_errors = _invoke_with_output_retry(
            ws,
            "search_similar_history",
            prompt,
            backends,
            state,
            output_desc=f"{wdir} and {pdir}",
            reset=reset_dirs,
            materialize=materialize,
            validate=lambda res, wdir=wdir, pdir=pdir: (
                _dir_has_materialized_output(wdir)
                and _dir_has_materialized_output(pdir)
            ),
            subtask_id=subtask_id,
            focus=focus,
        )
        writeup_dirs.append(str(wdir))
        patch_dirs.append(str(pdir))
        errors += item_errors
    return {
        "similar_writeups": writeup_dirs,
        "similar_patches": patch_dirs,
        "errors": errors,
    }

__all__ = ["search_similar_history"]

