"""LangGraph node implementation: search_fuzz_driver."""

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

def search_fuzz_driver(state: ZeroMDASHState, *, backends=None) -> dict:
    ws = _ws(state)
    out = ws.main_path("attack_surface") / "fuzz_drivers.md"
    focus = _node_focus(state, "search_fuzz_driver_focus")
    prompt = prompts.SEARCH_FUZZ_DRIVER.format(
        target=state["target"],
        focus=focus,
        repo_path=state.get("repo_path", ""),
        out_path=out,
    )
    _, errors = _invoke_with_output_retry(
        ws,
        "search_fuzz_driver",
        prompt,
        backends,
        state,
        output_desc=str(out),
        reset=lambda: _reset_file_output(out),
        materialize=lambda res: _write_stdout_fallback_file(out, res.stdout),
        validate=lambda res: _file_has_text(out),
        focus=focus,
    )
    drivers = [
        ln.strip("- ").strip()
        for ln in _read_text_lossy(out).splitlines()
        if ln.strip()
    ]
    return {"fuzz_drivers": drivers, "errors": errors}

__all__ = ["search_fuzz_driver"]

