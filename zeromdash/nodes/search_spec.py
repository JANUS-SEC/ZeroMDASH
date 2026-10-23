"""LangGraph node implementation: search_spec."""

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
    _reset_file_output,
    _write_stdout_fallback_file,
)

def search_spec(state: ZeroMDASHState, *, backends=None) -> dict:
    ws = _ws(state)
    out = ws.main_path("spec") / "spec.md"
    focus = _node_focus(state, "search_spec_focus")
    prompt = prompts.SEARCH_SPEC.format(target=state["target"], focus=focus, out_path=out)
    _, errors = _invoke_with_output_retry(
        ws,
        "search_spec",
        prompt,
        backends,
        state,
        output_desc=str(out),
        reset=lambda: _reset_file_output(out),
        materialize=lambda res: _write_stdout_fallback_file(out, res.stdout),
        validate=lambda res: _file_has_text(out),
        focus=focus,
    )
    return {"spec_doc": str(out), "errors": errors}

__all__ = ["search_spec"]

