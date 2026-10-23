"""LangGraph node implementation: search_target_history."""

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
    _reset_dir_output,
)
from .core.patch_manifest import (
    _target_history_repo_registry,
    _validate_patch_manifest,
)

def search_target_history(state: ZeroMDASHState, *, backends=None) -> dict:
    ws = _ws(state)
    writeup_dir = ws.main_path("writeup")
    patch_dir = ws.main_path("patch")
    writeup_index = writeup_dir / "_index.md"
    patch_manifest = patch_dir / "_patch_commits.json"
    repo_mode, repo_registry = _target_history_repo_registry(state)
    focus = _node_focus(state, "search_target_history_focus")
    prompt = prompts.SEARCH_TARGET_HISTORY.format(
        target=state["target"],
        focus=focus,
        repo_mode=repo_mode,
        repo_registry=json.dumps(repo_registry, ensure_ascii=False, indent=2),
        repo_path=state.get("repo_path", str(ws.main_path("repo"))),
        writeup_index=writeup_index,
        patch_manifest=patch_manifest,
        writeup_dir=writeup_dir,
        patch_dir=patch_dir,
    )

    def reset_dirs() -> None:
        _reset_dir_output(writeup_dir)
        _reset_dir_output(patch_dir)

    def materialize(res: AgentResult) -> None:
        if res.stdout.strip():
            (writeup_dir / "_raw.md").write_text(res.stdout)

    def validate(res: AgentResult) -> tuple[bool, str]:
        del res
        if not _file_has_text(writeup_index):
            return False, f"missing target-history writeup: {writeup_index}"
        return _validate_patch_manifest(
            patch_manifest,
            target=str(state["target"]),
            repo_mode=repo_mode,
            repo_registry=repo_registry,
        )

    _, errors = _invoke_with_output_retry(
        ws,
        "search_target_history",
        prompt,
        backends,
        state,
        output_desc=f"{writeup_index} and schema-valid {patch_manifest}",
        reset=reset_dirs,
        materialize=materialize,
        validate=validate,
        focus=focus,
    )
    return {
        "target_writeups": [str(writeup_dir)],
        "target_patches": [str(patch_dir)],
        "target_patch_manifest": str(patch_manifest),
        "errors": errors,
    }

__all__ = ["search_target_history"]

