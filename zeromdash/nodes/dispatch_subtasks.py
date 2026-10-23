"""LangGraph node implementation: dispatch_subtasks."""

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

from .core.constants import (
    DEFAULT_MAX_ITERATIONS,
    DEFAULT_MIN_CRITIC_SKILLS,
)
from .core.dispatch_selection import (
    _filter_completed_dispatch_subtasks,
    _limit_subtasks_for_bucket,
    _round_robin_subtasks,
    _select_dispatch_subtasks,
    _write_dispatch_plan,
)
from .core.invocation import _selected_log_dir

def dispatch_spec(state: ZeroMDASHState) -> list[Send]:
    return _dispatch(
        _limit_subtasks_for_bucket(state.get("spec_subtasks", []), state, "spec"),
        state,
    )

def dispatch_vuln(state: ZeroMDASHState) -> list[Send]:
    return _dispatch(
        _limit_subtasks_for_bucket(state.get("vuln_subtasks", []), state, "vuln"),
        state,
    )

def dispatch_patch(state: ZeroMDASHState) -> list[Send]:
    return _dispatch(
        _limit_subtasks_for_bucket(state.get("patch_subtasks", []), state, "patch"),
        state,
    )

def dispatch_feature(state: ZeroMDASHState) -> list[Send]:
    return _dispatch(
        _limit_subtasks_for_bucket(state.get("feature_subtasks", []), state, "feature"),
        state,
    )

def dispatch_subtasks(state: ZeroMDASHState, *, backends=None) -> dict:
    """Barrier node after all planners finish.

    LangGraph conditional Sends are emitted from this single node so the
    workflow has one fan-out point for all planner buckets. This also gives us
    a place to route directly to summary when every planner returns zero
    subtasks.
    """
    del state, backends
    return {}

def dispatch_all(state: ZeroMDASHState) -> list[Send] | str:
    selected_by_bucket, bucket_reports = _select_dispatch_subtasks(state)
    selected_by_bucket, bucket_reports = _filter_completed_dispatch_subtasks(
        selected_by_bucket,
        bucket_reports,
        state,
    )
    _write_dispatch_plan(state, bucket_reports)
    scope = state.get("scan_scope")
    if isinstance(scope, dict) and scope.get("mode") == "diff":
        ordered_subtasks = _round_robin_subtasks(selected_by_bucket)
    else:
        ordered_subtasks = [
            subtask
            for bucket in ("spec", "vuln", "patch", "feature")
            for subtask in selected_by_bucket[bucket]
        ]
    sends = _dispatch(ordered_subtasks, state)
    if sends:
        return sends
    has_existing_chain_inputs = any(
        state.get(key)
        for key in (
            "spec_findings",
            "vuln_candidates",
            "patch_findings",
            "feature_findings",
            "confirmed_primitives",
            "chain_pool",
        )
    )
    return "materialize_chain_pool" if has_existing_chain_inputs else "summary"

def dispatch_selected(state: ZeroMDASHState) -> list[Send] | str:
    requested = set(
        state.get("selected_subtask_ids")
        or state.get("selected_subagent_ids")
        or []
    )
    ordered_subtasks = [
        subtask
        for bucket in (
            "spec_subtasks",
            "vuln_subtasks",
            "patch_subtasks",
            "feature_subtasks",
        )
        for subtask in state.get(bucket, []) or []
        if str(subtask.get("id") or "") in requested
    ]
    sends = _dispatch(ordered_subtasks, state)
    return sends or "collect_selected_subtask_statuses"

def collect_selected_subtask_statuses(state: ZeroMDASHState) -> dict:
    selected_dir = _selected_log_dir(state)
    if selected_dir is None:
        raise ValueError("selected subtask status collection requires an output directory")
    errors = [str(item) for item in state.get("errors") or []]
    statuses: list[dict[str, Any]] = []
    selected_ids = (
        state.get("selected_subtask_ids")
        or state.get("selected_subagent_ids")
        or []
    )
    for subtask_id in selected_ids:
        result_path = selected_dir / "results" / f"{subtask_id}.json"
        matching_errors = [error for error in errors if subtask_id in error]
        status = "completed" if result_path.is_file() else "failed"
        verdict = ""
        severity = ""
        iterations = 0
        if result_path.is_file():
            try:
                payload = json.loads(result_path.read_text())
            except (OSError, json.JSONDecodeError):
                payload = {}
            finding = payload.get("finding") if isinstance(payload, dict) else None
            if isinstance(finding, dict):
                review = finding.get("review") or {}
                verdict = str((review or {}).get("verdict") or "")
                severity = str(finding.get("severity") or "")
                iterations = int(finding.get("iterations") or 0)
            elif isinstance(payload, dict) and payload.get("result_type") == "hypothesis_package":
                review = payload.get("review") or {}
                verdict = str(review.get("package_decision") or "")
                iterations = len(payload.get("history") or [])

        statuses.append(
            {
                "subtask_id": subtask_id,
                "status": status,
                "verdict": verdict,
                "severity": severity,
                "iterations": iterations,
                "result_path": str(result_path) if result_path.is_file() else "",
                "errors": matching_errors,
            }
        )

    out = selected_dir / "selected_subtask_statuses.json"
    out.write_text(json.dumps(statuses, ensure_ascii=False, indent=2))
    (selected_dir / "selected_subagent_statuses.json").write_text(
        json.dumps(statuses, ensure_ascii=False, indent=2)
    )
    return {
        "selected_subtask_statuses": statuses,
        "selected_subagent_statuses": statuses,
        "stopped_at": "selected_subtasks",
    }

def _dispatch(subtasks: list[Subtask], state: ZeroMDASHState) -> list[Send]:
    sends: list[Send] = []
    for st in subtasks:
        child: dict[str, Any] = {
            "task_id": state["task_id"],
            "workspace_root": state["workspace_root"],
            "target": state.get("target", ""),
            "repo_path": state["repo_path"],
            "scope_path": state.get("scope_path", ""),
            "scan_scope": dict(state.get("scan_scope") or {}),
            "subtask": st,
            "iteration": 0,
            "max_iterations": state.get("max_iterations", DEFAULT_MAX_ITERATIONS),
            "min_critic_skills": state.get("min_critic_skills", DEFAULT_MIN_CRITIC_SKILLS),
            "agent_configs": state.get("agent_configs", {}),
            "agent_config_task_types": state.get("agent_config_task_types", {}),
            # Propagate the fused attack-surface model + threat model so the
            # investigator frames its work top-down instead of bottom-up only.
            "common_focus": state.get("common_focus", ""),
            "attack_surface": state.get("attack_surface", ""),
            "domain_registry_path": state.get("domain_registry_path", ""),
            "domain_registry": dict(state.get("domain_registry") or {}),
            "spec_doc": state.get("spec_doc", ""),
            "similar_writeups": list(state.get("similar_writeups") or []),
            "feature_docs": list(state.get("feature_docs") or []),
            "review_history": [],
            "selected_subtask_log_dir": (
                state.get("selected_subtask_log_dir")
                or state.get("selected_subagent_log_dir")
                or ""
            ),
        }
        sends.append(Send("subtask", child))
    return sends

__all__ = ["dispatch_spec","dispatch_vuln","dispatch_patch","dispatch_feature","dispatch_subtasks","dispatch_all","dispatch_selected","collect_selected_subtask_statuses","_dispatch"]
