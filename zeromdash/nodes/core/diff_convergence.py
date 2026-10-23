"""Diff-mode risk-surface validation and cross-bucket convergence."""

from __future__ import annotations

import copy
import re
from typing import Any

from zeromdash.state import Subtask, ZeroMDASHState

from .context import _attack_surface_has_risk_registry, _attack_surface_risk_ids
from .locations import (
    _changed_file_set,
    _location_values,
    _locations_intersect_diff,
    _normalize_repo_location,
)
from .priority import _flatten_priority_text, _priority_tokens, _rank_subtasks_for_top_k
from .qualification import _normalized_flag

def _subtask_is_diff_attributable(subtask: Subtask, state: ZeroMDASHState) -> bool:
    hints = subtask.get("hints") or {}
    explicit = hints.get("blocking_eligible")
    relation = _normalized_flag(hints.get("scope_relation")).replace("-", "_")
    intersects = _locations_intersect_diff(
        hints.get("diff_anchor")
        or hints.get("changed_locations")
        or hints.get("candidate_code_locations")
        or hints.get("candidate_locations"),
        state,
    )
    if not intersects:
        return False
    non_attributable = ("pre_existing", "preexisting", "unrelated", "adjacent")
    if any(marker in relation for marker in non_attributable):
        return False
    if explicit is True:
        return True

    direct_relation = (
        "introduced",
        "enabled",
        "regressed",
        "diff_introduced",
        "sibling_path",
    )
    if any(marker in relation for marker in direct_relation):
        return True
    return explicit is not False

def _subtask_changed_paths(subtask: Subtask, state: ZeroMDASHState) -> set[str]:
    hints = subtask.get("hints") or {}
    changed_files = _changed_file_set(state)
    raw_locations = (
        hints.get("diff_anchor")
        or hints.get("changed_locations")
        or hints.get("candidate_code_locations")
        or hints.get("candidate_locations")
    )
    return {
        normalized
        for location in _location_values(raw_locations)
        if (normalized := _normalize_repo_location(location, state)) in changed_files
    }

def _subtask_dedup_tokens(subtask: Subtask) -> set[str]:
    hints = subtask.get("hints") or {}
    fields = [
        subtask.get("objective"),
        hints.get("change_hypothesis"),
        hints.get("bug_class"),
        hints.get("spec_clause"),
        hints.get("expected_data_flow"),
        hints.get("audit_questions"),
        hints.get("rationale"),
    ]
    return _priority_tokens(_flatten_priority_text(fields))

def _subtask_risk_surface_ids(subtask: Subtask) -> set[str]:
    hints = subtask.get("hints") or {}
    raw = hints.get("risk_surface_ids") or hints.get("risk_surface_id") or []
    values = _location_values(raw)
    risk_ids = {
        normalized
        for value in values
        if (normalized := str(value or "").strip().upper())
    }
    legacy_text = _flatten_priority_text(
        [
            subtask.get("objective"),
            hints.get("priority_reason"),
            hints.get("rationale"),
            hints.get("change_hypothesis"),
        ]
    )
    for number in re.findall(r"\bhypothes(?:is|es)\s*#\s*(\d+)\b", legacy_text, re.IGNORECASE):
        risk_ids.add(f"LEGACY-HYP-{int(number):03d}")
    return risk_ids

def _canonical_subtask_risk_ids(subtask: Subtask) -> set[str]:
    hints = subtask.get("hints") or {}
    raw = hints.get("risk_surface_id") or hints.get("risk_surface_ids") or []
    return {
        match.upper()
        for value in _location_values(raw)
        for match in re.findall(
            r"\b(?:RS-\d{3,}|RS-EXT-[A-Z0-9][A-Z0-9_-]*)\b",
            value,
            re.IGNORECASE,
        )
    }

def _risk_surface_extension_complete(hints: dict[str, Any]) -> bool:
    definition = hints.get("risk_surface_definition")
    if not isinstance(definition, dict):
        return False
    required = (
        "root_cause",
        "untrusted_input_object",
        "trust_boundary",
        "state_machine_family",
        "sink",
        "security_invariant",
    )
    return all(str(definition.get(key) or "").strip() for key in required)

def _diff_planner_contract_valid(
    subtasks: list[Subtask],
    state: ZeroMDASHState,
) -> bool:
    scope = state.get("scan_scope")
    if not isinstance(scope, dict) or scope.get("mode") != "diff":
        return True
    registered_ids = _attack_surface_risk_ids(state)
    if not _attack_surface_has_risk_registry(state):
        return True
    for subtask in subtasks:
        risk_ids = _canonical_subtask_risk_ids(subtask)
        if len(risk_ids) != 1:
            return False
        hints = subtask.get("hints") or {}
        risk_id = next(iter(risk_ids))
        if risk_id not in registered_ids and not (
            risk_id.startswith("RS-EXT-")
            and _risk_surface_extension_complete(hints)
        ):
            return False
        if not _locations_intersect_diff(hints.get("diff_anchor"), state):
            return False
        change_to_sink = [
            value.strip()
            for value in _location_values(hints.get("change_to_sink_path"))
            if value.strip()
        ]
        if len(change_to_sink) < 2:
            return False
    return True

def _overlap_coefficient(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / min(len(left), len(right))

def _jaccard_similarity(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0

def _normalized_dedup_key(value: Any) -> str:
    return " ".join(sorted(_priority_tokens(value)))

def _subtasks_share_risk_surface(
    left: Subtask,
    right: Subtask,
    state: ZeroMDASHState,
) -> bool:
    left_hints = left.get("hints") or {}
    right_hints = right.get("hints") or {}
    left_canonical_ids = _canonical_subtask_risk_ids(left)
    right_canonical_ids = _canonical_subtask_risk_ids(right)
    if left_canonical_ids and right_canonical_ids:
        return bool(left_canonical_ids & right_canonical_ids)

    left_risk_ids = _subtask_risk_surface_ids(left)
    right_risk_ids = _subtask_risk_surface_ids(right)
    if left_risk_ids and right_risk_ids:
        return bool(left_risk_ids & right_risk_ids)

    left_key = _normalized_dedup_key(left_hints.get("dedup_key"))
    right_key = _normalized_dedup_key(right_hints.get("dedup_key"))
    if left_key and left_key == right_key:
        return True

    left_paths = _subtask_changed_paths(left, state)
    right_paths = _subtask_changed_paths(right, state)
    path_overlap = _overlap_coefficient(left_paths, right_paths)
    if path_overlap < 0.66:
        return False

    left_tokens = _subtask_dedup_tokens(left)
    right_tokens = _subtask_dedup_tokens(right)
    token_overlap = _overlap_coefficient(left_tokens, right_tokens)
    token_jaccard = _jaccard_similarity(left_tokens, right_tokens)
    path_jaccard = _jaccard_similarity(left_paths, right_paths)
    return (
        token_jaccard >= 0.22
        and token_overlap >= 0.40
    ) or (
        path_jaccard >= 0.75
        and token_jaccard >= 0.18
        and token_overlap >= 0.35
    )

def _subtasks_are_cross_bucket_duplicates(
    left: Subtask,
    right: Subtask,
    state: ZeroMDASHState,
) -> bool:
    return (
        left.get("bucket") != right.get("bucket")
        and _subtasks_share_risk_surface(left, right, state)
    )

def _extend_unique_hint_values(target: dict[str, Any], source: dict[str, Any], key: str) -> None:
    combined = _location_values(target.get(key))
    for value in _location_values(source.get(key)):
        if value not in combined:
            combined.append(value)
    if combined:
        target[key] = combined

def _append_unique_hint_value(target: dict[str, Any], key: str, value: Any) -> None:
    values = _location_values(target.get(key))
    for candidate in _location_values(value):
        if candidate and candidate not in values:
            values.append(candidate)
    if values:
        target[key] = values

def _merge_duplicate_subtask(representative: Subtask, duplicate: Subtask) -> None:
    hints = representative.setdefault("hints", {})
    duplicate_hints = duplicate.get("hints") or {}
    merged = hints.setdefault("merged_subtasks", [])
    merged.append(
        {
            "id": str(duplicate.get("id") or ""),
            "bucket": str(duplicate.get("bucket") or ""),
            "objective": str(duplicate.get("objective") or ""),
        }
    )
    for prior in duplicate_hints.get("merged_subtasks") or []:
        if isinstance(prior, dict):
            merged.append(dict(prior))
    for source_key, target_key in (
        ("spec_clause", "spec_refs"),
        ("cve", "cve_refs"),
        ("patch_commit", "patch_refs"),
        ("feature_ref", "feature_refs"),
    ):
        _append_unique_hint_value(hints, target_key, hints.get(source_key))
        _append_unique_hint_value(hints, target_key, duplicate_hints.get(source_key))
    merged_risk_ids = sorted(
        _canonical_subtask_risk_ids(representative)
        | _canonical_subtask_risk_ids(duplicate)
    )
    if not merged_risk_ids:
        merged_risk_ids = sorted(
            _subtask_risk_surface_ids(representative)
            | _subtask_risk_surface_ids(duplicate)
        )
    if merged_risk_ids:
        hints["risk_surface_ids"] = merged_risk_ids
    for key in (
        "spec_refs",
        "cve_refs",
        "patch_refs",
        "feature_refs",
        "candidate_code_locations",
        "candidate_locations",
        "diff_anchor",
        "changed_locations",
        "context_locations",
        "change_to_sink_path",
        "expected_data_flow",
        "audit_questions",
    ):
        _extend_unique_hint_values(hints, duplicate_hints, key)
    if merged and "merged audit angles" not in str(representative.get("objective") or "").lower():
        representative["objective"] = (
            str(representative.get("objective") or "").rstrip()
            + " Cover every merged audit angle in hints.merged_subtasks."
        )

def _converge_diff_planner_subtasks(
    subtasks: list[Subtask],
    state: ZeroMDASHState,
) -> tuple[list[Subtask], list[dict[str, str]]]:
    scope = state.get("scan_scope")
    if not isinstance(scope, dict) or scope.get("mode") != "diff":
        return subtasks, []

    converged: list[Subtask] = []
    omitted: list[dict[str, str]] = []
    for subtask in _rank_subtasks_for_top_k(copy.deepcopy(subtasks), state):
        subtask_id = str(subtask.get("id") or "")
        if not _subtask_is_diff_attributable(subtask, state):
            omitted.append({"id": subtask_id, "reason": "not_diff_attributable"})
            continue
        representative = next(
            (
                item
                for item in converged
                if _subtasks_share_risk_surface(item, subtask, state)
            ),
            None,
        )
        if representative is None:
            converged.append(subtask)
            continue
        _merge_duplicate_subtask(representative, subtask)
        omitted.append(
            {
                "id": subtask_id,
                "reason": "same_bucket_duplicate",
                "duplicate_of": str(representative.get("id") or ""),
            }
        )
    return converged, omitted

def _deduplicate_diff_dispatch(
    selected_by_bucket: dict[str, list[Subtask]],
    bucket_reports: dict[str, dict[str, Any]],
    state: ZeroMDASHState,
) -> tuple[dict[str, list[Subtask]], dict[str, dict[str, Any]]]:
    selected = {
        bucket: [copy.deepcopy(item) for item in items]
        for bucket, items in selected_by_bucket.items()
    }
    reports = copy.deepcopy(bucket_reports)
    representatives: list[tuple[str, Subtask]] = []

    # Patch and analogue tasks usually carry the most concrete root-cause
    # evidence. Spec and feature objectives are merged into them, not discarded.
    for bucket in ("patch", "vuln", "spec", "feature"):
        retained: list[Subtask] = []
        for subtask in selected.get(bucket, []):
            duplicate_of: Subtask | None = None
            for _, representative in representatives:
                if _subtasks_are_cross_bucket_duplicates(representative, subtask, state):
                    duplicate_of = representative
                    break
            if duplicate_of is None:
                retained.append(subtask)
                representatives.append((bucket, subtask))
                continue

            _merge_duplicate_subtask(duplicate_of, subtask)
            reports[bucket]["omitted"].append(
                {
                    "id": str(subtask.get("id") or ""),
                    "reason": "cross_bucket_duplicate",
                    "duplicate_of": str(duplicate_of.get("id") or ""),
                }
            )
        selected[bucket] = retained
        reports[bucket]["selected"] = retained
        reports[bucket]["selected_count"] = len(retained)

    # Representatives may have gained merged provenance after their bucket was
    # processed, so refresh every report from the final objects.
    for bucket, items in selected.items():
        reports[bucket]["selected"] = items
    return selected, reports

__all__ = ["_subtask_is_diff_attributable","_subtask_changed_paths","_subtask_dedup_tokens","_subtask_risk_surface_ids","_canonical_subtask_risk_ids","_risk_surface_extension_complete","_diff_planner_contract_valid","_overlap_coefficient","_jaccard_similarity","_normalized_dedup_key","_subtasks_share_risk_surface","_subtasks_are_cross_bucket_duplicates","_extend_unique_hint_values","_append_unique_hint_value","_merge_duplicate_subtask","_converge_diff_planner_subtasks","_deduplicate_diff_dispatch"]

