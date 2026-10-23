"""LangGraph node implementation: plan_by_new_feature."""

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
from .core.domain_registry import domain_registry_json
from .core.planner_contract import (
    _run_planner_with_retry,
    _top_k_prompt_limit,
)

def plan_by_new_feature(state: ZeroMDASHState, *, backends=None) -> dict:
    ws = _ws(state)
    focus = _node_focus(state, "plan_by_new_feature_focus")
    feature_dir = ws.main_path("feature")
    subtasks, errors = _run_planner_with_retry(
        state,
        backends=backends,
        node="plan_by_new_feature",
        prompt=prompts.PLAN_BY_NEW_FEATURE.format(
            target=state["target"],
            focus=focus or "(none)",
            top_k=_top_k_prompt_limit(state, "feature"),
            repo_path=state["repo_path"],
            attack_surface=state.get("attack_surface", ""),
            domain_registry=domain_registry_json(state),
            feature_dir=feature_dir,
            feature_index=feature_dir / "_index.json",
        ),
        out_path=ws.state_path("plan_by_feature.json"),
        bucket="feature",
        prefix="feat",
        focus=focus,
    )
    return {"feature_subtasks": subtasks, "errors": errors}

__all__ = ["plan_by_new_feature"]

