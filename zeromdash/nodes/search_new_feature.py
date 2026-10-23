"""LangGraph node implementation: search_new_feature."""

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
    _reset_dir_output,
)
from .core.qualification import _try_json

def search_new_feature(state: ZeroMDASHState, *, backends=None) -> dict:
    ws = _ws(state)
    feature_dir = ws.main_path("feature")
    index_json = feature_dir / "_index.json"
    index_md = feature_dir / "_index.md"
    focus = _node_focus(state, "search_new_feature_focus")
    prompt = prompts.SEARCH_NEW_FEATURE.format(
        target=state["target"],
        focus=focus,
        repo_path=state.get("repo_path", ""),
        spec_dir=ws.main_path("spec"),
        fuzz_drivers=state.get("fuzz_drivers", []),
        target_writeups_dir=ws.main_path("writeup"),
        target_patches_dir=ws.main_path("patch"),
        similar_writeup_dirs=state.get("similar_writeups", []),
        similar_patch_dirs=state.get("similar_patches", []),
        feature_dir=feature_dir,
        index_json=index_json,
        index_md=index_md,
    )

    def reset_dir() -> None:
        _reset_dir_output(feature_dir)

    def materialize(res: AgentResult) -> None:
        if not _file_has_text(index_md) and res.stdout.strip():
            index_md.write_text(res.stdout)
        if not _file_has_text(index_json):
            parsed = _try_json(res.stdout, fallback=None)
            if isinstance(parsed, list):
                index_json.write_text(json.dumps(parsed, ensure_ascii=False, indent=2))
                if not _file_has_text(index_md):
                    index_md.write_text("# New / Weakly-Covered Feature Surfaces\n\nNo feature surfaces reported.\n")

    def validate(res: AgentResult) -> bool:
        del res
        if not (_file_has_text(index_json) and _file_has_text(index_md)):
            return False
        parsed = _try_json(_read_text_lossy(index_json), fallback=None)
        if not isinstance(parsed, list):
            return False
        if not parsed:
            return True
        return any(_file_has_text(path) for path in feature_dir.glob("feature-*.md"))

    _, errors = _invoke_with_output_retry(
        ws,
        "search_new_feature",
        prompt,
        backends,
        state,
        output_desc=f"{index_json} and {index_md}",
        reset=reset_dir,
        materialize=materialize,
        validate=validate,
        focus=focus,
    )
    docs = [
        str(path)
        for path in sorted(feature_dir.glob("feature-*.md"))
        if _file_has_text(path)
    ]
    if _file_has_text(index_json):
        docs.insert(0, str(index_json))
    if _file_has_text(index_md):
        docs.insert(1 if docs else 0, str(index_md))
    return {"feature_docs": docs, "errors": errors}

__all__ = ["search_new_feature"]

