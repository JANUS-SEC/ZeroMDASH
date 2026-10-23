"""Subtask selection, ranking, top-K limiting, and dispatch-plan output."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any

from zeromdash.state import Subtask, ZeroMDASHState
from zeromdash.workspace import Workspace

from .constants import _PRIORITY_REASON_FALLBACK, _PRIORITY_STOP_WORDS
from .context import _ws
from .diff_convergence import (
    _converge_diff_planner_subtasks,
    _deduplicate_diff_dispatch,
    _subtask_is_diff_attributable,
)
from .invocation import _selected_log_dir
from .limits import _configured_bucket_limit, _top_k_limit
from .priority import _rank_subtasks_for_top_k

def _select_dispatch_subtasks(
    state: ZeroMDASHState,
) -> tuple[dict[str, list[Subtask]], dict[str, dict[str, Any]]]:
    bucket_inputs = {
        "spec": list(state.get("spec_subtasks", [])),
        "vuln": list(state.get("vuln_subtasks", [])),
        "patch": list(state.get("patch_subtasks", [])),
        "feature": list(state.get("feature_subtasks", [])),
    }
    selected_by_bucket: dict[str, list[Subtask]] = {}
    bucket_reports: dict[str, dict[str, Any]] = {}
    for bucket, subtasks in bucket_inputs.items():
        selected, report = _select_subtasks_for_bucket(subtasks, state, bucket)
        selected_by_bucket[bucket] = selected
        bucket_reports[bucket] = report

    if isinstance(state.get("scan_scope"), dict) and state["scan_scope"].get("mode") == "diff":
        selected_by_bucket, bucket_reports = _deduplicate_diff_dispatch(
            selected_by_bucket,
            bucket_reports,
            state,
        )
    return selected_by_bucket, bucket_reports

def _filter_completed_dispatch_subtasks(
    selected_by_bucket: dict[str, list[Subtask]],
    bucket_reports: dict[str, dict[str, Any]],
    state: ZeroMDASHState,
) -> tuple[dict[str, list[Subtask]], dict[str, dict[str, Any]]]:
    completed = {
        str(item).strip()
        for item in state.get("completed_subtask_ids", [])
        if str(item).strip()
    }
    if not completed:
        return selected_by_bucket, bucket_reports

    filtered: dict[str, list[Subtask]] = {}
    reports = copy.deepcopy(bucket_reports)
    for bucket, subtasks in selected_by_bucket.items():
        retained: list[Subtask] = []
        report = reports.setdefault(bucket, {})
        omitted = list(report.get("omitted") or [])
        for subtask in subtasks:
            subtask_id = str(subtask.get("id") or "").strip()
            if subtask_id and subtask_id in completed:
                omitted.append({"id": subtask_id, "reason": "already_completed"})
                continue
            retained.append(subtask)
        filtered[bucket] = retained
        report["selected"] = retained
        report["selected_count"] = len(retained)
        report["omitted"] = omitted
    return filtered, reports

def _round_robin_subtasks(
    selected_by_bucket: dict[str, list[Subtask]],
) -> list[Subtask]:
    buckets = ("spec", "vuln", "patch", "feature")
    ordered: list[Subtask] = []
    max_length = max(
        (len(selected_by_bucket.get(bucket, [])) for bucket in buckets),
        default=0,
    )
    for index in range(max_length):
        for bucket in buckets:
            subtasks = selected_by_bucket.get(bucket, [])
            if index < len(subtasks):
                ordered.append(subtasks[index])
    return ordered

def _select_subtasks_for_bucket(
    subtasks: list[Subtask],
    state: ZeroMDASHState,
    bucket: str,
) -> tuple[list[Subtask], dict[str, Any]]:
    scope = state.get("scan_scope")
    is_diff = isinstance(scope, dict) and scope.get("mode") == "diff"
    limit = _top_k_limit(state, bucket)

    if not is_diff:
        ranked = (
            _rank_subtasks_for_top_k(list(subtasks), state)
            if limit is not None
            else list(subtasks)
        )
        selected = ranked if limit is None else ranked[:limit]
        selected_ids = {str(item.get("id") or "") for item in selected}
        omitted = [
            {"id": str(item.get("id") or ""), "reason": "top_k_limit"}
            for item in ranked
            if str(item.get("id") or "") not in selected_ids
        ]
        return selected, {
            "candidate_count": len(ranked),
            "diff_attributable_count": None,
            "selected_count": len(selected),
            "effective_limit": limit,
            "selected": selected,
            "omitted": omitted,
        }

    ranked = _rank_subtasks_for_top_k(list(subtasks), state)
    attributable_count = sum(
        1 for item in ranked if _subtask_is_diff_attributable(item, state)
    )
    converged, convergence_omitted = _converge_diff_planner_subtasks(ranked, state)
    selected = converged if limit is None else converged[:limit]

    selected_ids = {str(item.get("id") or "") for item in selected}
    omitted: list[dict[str, str]] = list(convergence_omitted)
    converged_ids = {str(item.get("id") or "") for item in converged}
    omitted_ids = {str(item.get("id") or "") for item in omitted}
    for item in converged:
        item_id = str(item.get("id") or "")
        if item_id in selected_ids or item_id in omitted_ids:
            continue
        omitted.append({"id": item_id, "reason": "top_k_limit"})
    for item in ranked:
        item_id = str(item.get("id") or "")
        if item_id not in converged_ids and item_id not in omitted_ids:
            omitted.append({"id": item_id, "reason": "not_diff_attributable"})
    return selected, {
        "candidate_count": len(ranked),
        "diff_attributable_count": attributable_count,
        "independent_risk_count": len(converged),
        "selected_count": len(selected),
        "effective_limit": limit,
        "selected": selected,
        "omitted": omitted,
    }

def _write_dispatch_plan(
    state: ZeroMDASHState,
    buckets: dict[str, dict[str, Any]],
) -> None:
    scope = state.get("scan_scope")
    if not isinstance(scope, dict) or scope.get("mode") != "diff":
        return
    workspace_root = state.get("workspace_root")
    task_id = state.get("task_id")
    if not workspace_root or not task_id:
        return
    ws = Workspace.open(str(workspace_root), str(task_id))
    if not ws.base.is_dir():
        return
    totals = {
        "candidates": sum(int(report["candidate_count"]) for report in buckets.values()),
        "selected": sum(int(report["selected_count"]) for report in buckets.values()),
    }
    payload = {
        "schema_version": 1,
        "scan_mode": str((state.get("scan_scope") or {}).get("mode") or "full"),
        "policy": {
            "top_K": dict(state.get("top_K") or {}),
            "diff_numeric_cap": False,
            "diff_selection": (
                "dispatch every independent diff-attributable risk surface; "
                "merge duplicate root-cause/data-flow checks across buckets"
            ),
        },
        "totals": totals,
        "buckets": buckets,
    }
    out = ws.state_path("dispatch_plan.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2))

def _limit_subtasks_for_bucket(subtasks: list[Subtask], state: ZeroMDASHState, bucket: str) -> list[Subtask]:
    selected, _ = _select_subtasks_for_bucket(list(subtasks), state, bucket)
    return selected









__all__ = [
    "_select_dispatch_subtasks",
    "_filter_completed_dispatch_subtasks",
    "_round_robin_subtasks",
    "_select_subtasks_for_bucket",
    "_write_dispatch_plan",
    "_limit_subtasks_for_bucket",
]

