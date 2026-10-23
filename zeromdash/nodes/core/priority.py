"""Shared planner and dispatch priority scoring."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from zeromdash.state import Subtask, ZeroMDASHState

from .constants import _PRIORITY_STOP_WORDS
from .io import _read_text_lossy
from .locations import _location_values, _locations_intersect_diff
from .qualification import _normalized_flag

def _rank_subtasks_for_top_k(subtasks: list[Subtask], state: ZeroMDASHState) -> list[Subtask]:
    scored: list[tuple[tuple[int, int, int, int], Subtask]] = []
    for index, subtask in enumerate(subtasks):
        focus_score, reachability_score = _subtask_priority_scores(subtask, state)
        combined = focus_score + reachability_score
        scored.append(((combined, focus_score, reachability_score, -index), subtask))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [subtask for _, subtask in scored]

def _subtask_priority_scores(subtask: Subtask, state: ZeroMDASHState) -> tuple[int, int]:
    subtask_text = _flatten_priority_text(subtask)
    focus_score = _token_overlap_score(state.get("common_focus", ""), subtask_text)
    attack_surface_text = _attack_surface_priority_text(state)
    reachability_score = _token_overlap_score(attack_surface_text, subtask_text)
    reachability_score += _candidate_location_reachability_score(
        subtask.get("hints") or {},
        attack_surface_text,
    )
    reachability_score += _diff_scope_priority_score(subtask.get("hints") or {}, state)
    return focus_score, reachability_score

def _flatten_priority_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(
            f"{key} {_flatten_priority_text(item)}"
            for key, item in value.items()
        )
    if isinstance(value, (list, tuple, set)):
        return " ".join(_flatten_priority_text(item) for item in value)
    return str(value or "")

def _priority_tokens(text: Any) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9_]+|[\u4e00-\u9fff]+", str(text or "").lower())
        if len(token) >= 3 and token not in _PRIORITY_STOP_WORDS
    }

def _token_overlap_score(query: Any, candidate: Any) -> int:
    query_tokens = _priority_tokens(query)
    if not query_tokens:
        return 0
    candidate_tokens = _priority_tokens(candidate)
    return len(query_tokens & candidate_tokens)

def _attack_surface_priority_text(state: ZeroMDASHState) -> str:
    raw = str(state.get("attack_surface") or "")
    if not raw:
        return ""
    path = Path(raw)
    if path.is_file():
        return _read_text_lossy(path)
    return raw

def _candidate_location_reachability_score(hints: dict[str, Any], attack_surface_text: str) -> int:
    if not attack_surface_text:
        return 0
    raw_locations = hints.get("candidate_code_locations") or hints.get("candidate_locations") or []
    if isinstance(raw_locations, str):
        locations = [raw_locations]
    elif isinstance(raw_locations, list):
        locations = [str(item) for item in raw_locations]
    else:
        locations = []

    score = 0
    for location in locations:
        location = location.strip()
        if not location:
            continue
        path_part = location.split(":", 1)[0]
        if location in attack_surface_text:
            score += 4
        elif path_part and path_part in attack_surface_text:
            score += 3
    return score

def _diff_scope_priority_score(hints: dict[str, Any], state: ZeroMDASHState) -> int:
    scope = state.get("scan_scope")
    if not isinstance(scope, dict) or scope.get("mode") != "diff":
        return 0
    changed_locations = _location_values(hints.get("changed_locations"))
    score = 12 if changed_locations else 0
    if _locations_intersect_diff(
        hints.get("candidate_code_locations") or hints.get("candidate_locations"),
        state,
    ):
        score += 8
    relation = _normalized_flag(hints.get("scope_relation")).replace("-", "_")
    if relation in {"introduced", "enabled", "regressed", "diff_introduced"}:
        score += 6
    return score

__all__ = ["_rank_subtasks_for_top_k","_subtask_priority_scores","_flatten_priority_text","_priority_tokens","_token_overlap_score","_attack_surface_priority_text","_candidate_location_reachability_score","_diff_scope_priority_score"]

