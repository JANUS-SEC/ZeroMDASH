"""Planner input/output normalization and invocation contract."""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path
from typing import Any

from zeromdash.agents import AgentResult
from zeromdash.state import Subtask, ZeroMDASHState

from .constants import _PRIORITY_REASON_FALLBACK
from .context import _attack_surface_has_risk_registry, _attack_surface_risk_ids, _ws
from .domain_registry import domain_registry_from_state, domain_registry_ids
from .hypothesis_batch import validate_hypothesis_package
from .invocation import _invoke_with_output_retry
from .io import _planner_fallback_json, _read_text_lossy, _reset_file_output
from .limits import _top_k_limit
from .locations import *
from .qualification import _normalized_flag, _try_json
from .diff_convergence import (
    _converge_diff_planner_subtasks,
    _diff_planner_contract_valid,
    _subtask_is_diff_attributable,
)

def _normalize_subtasks(items: list[dict[str, Any]], bucket: str, prefix: str) -> list[Subtask]:
    out: list[Subtask] = []
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            continue
        raw_hints = it.get("hints") or {}
        hints = dict(raw_hints) if isinstance(raw_hints, dict) else {}
        if not str(hints.get("priority_reason") or "").strip():
            hints["priority_reason"] = _PRIORITY_REASON_FALLBACK
        out.append(
            Subtask(
                id=str(it.get("id") or f"{prefix}-{i:03d}-{uuid.uuid4().hex[:6]}"),
                bucket=bucket,
                objective=str(it.get("objective", "")),
                hints=hints,
                **(
                    {"coverage_obligations": list(it.get("coverage_obligations") or [])}
                    if "coverage_obligations" in it
                    else {}
                ),
                **(
                    {"seed_hypotheses": list(it.get("seed_hypotheses") or [])}
                    if "seed_hypotheses" in it
                    else {}
                ),
            )
        )
    return out





def _apply_scan_scope_to_subtasks(
    subtasks: list[Subtask],
    state: ZeroMDASHState,
) -> list[Subtask]:
    scope = state.get("scan_scope")
    if not isinstance(scope, dict) or scope.get("mode") != "diff":
        return subtasks
    changed_set = _changed_file_set(state)
    for subtask in subtasks:
        hints = subtask.setdefault("hints", {})
        candidate_locations = _location_values(
            hints.get("candidate_code_locations") or hints.get("candidate_locations")
        )
        inferred_changed = [
            location
            for location in candidate_locations
            if _normalize_repo_location(location, state) in changed_set
        ]
        hints.setdefault("scope_relation", "unknown")
        hints.setdefault("changed_locations", inferred_changed)
        hints.setdefault(
            "context_locations",
            [location for location in candidate_locations if location not in inferred_changed],
        )
        hints.setdefault(
            "change_hypothesis",
            "Determine whether the highlighted diff introduced, enabled, or regressed "
            "the suspected security behavior.",
        )
        hints.setdefault("blocking_eligible", bool(inferred_changed))
    return subtasks


def _validate_domain_refs(
    subtasks: list[Subtask],
    state: ZeroMDASHState,
) -> tuple[bool, str]:
    registry = domain_registry_from_state(state)
    if registry.get("status") == "legacy_unavailable":
        return True, ""
    known = domain_registry_ids(registry)
    allowed_keys = {
        "entity_ids",
        "representation_ids",
        "invariant_ids",
        "transition_ids",
        "seam_ids",
    }
    for subtask in subtasks:
        hints = subtask.get("hints") or {}
        if "domain_refs" not in hints:
            return False, f"subtask {subtask.get('id')} hints.domain_refs is required"
        refs = hints.get("domain_refs")
        if not isinstance(refs, dict):
            return False, f"subtask {subtask.get('id')} hints.domain_refs must be an object"
        unexpected = set(refs) - allowed_keys
        if unexpected:
            return False, (
                f"subtask {subtask.get('id')} hints.domain_refs has unknown collection(s): "
                + ", ".join(sorted(unexpected))
            )
        invalid_shapes = [key for key, values in refs.items() if not isinstance(values, list)]
        if invalid_shapes:
            return False, (
                f"subtask {subtask.get('id')} hints.domain_refs collection(s) must be arrays: "
                + ", ".join(sorted(invalid_shapes))
            )
        unknown = {
            str(item)
            for values in refs.values()
            if isinstance(values, list)
            for item in values
            if str(item) not in known
        }
        if unknown:
            return False, (
                f"subtask {subtask.get('id')} references unknown domain id(s): "
                + ", ".join(sorted(unknown))
            )
    return True, ""


def _validate_hypothesis_packages(
    subtasks: list[Subtask],
    state: ZeroMDASHState,
) -> tuple[bool, str]:
    """Require Agent-Native hypothesis packages for registry-aware runs.

    Old workspaces have a synthetic ``legacy_unavailable`` registry and remain
    valid with their historical single-outcome plans. New planners receive an
    output schema that requires package fields; this check protects callers
    that bypass native schema enforcement.
    """
    registry = domain_registry_from_state(state)
    if registry.get("status") == "legacy_unavailable":
        return True, ""
    known_domain_ids = domain_registry_ids(registry)
    for subtask in subtasks:
        package, error = validate_hypothesis_package(subtask)
        if package is None:
            return False, error
        referenced = {
            str(item)
            for collection in (
                package.get("coverage_obligations") or [],
                package.get("seed_hypotheses") or [],
            )
            for entry in collection
            if isinstance(entry, dict)
            for values in (entry.get("domain_refs") or {}).values()
            if isinstance(values, list)
            for item in values
        }
        unknown = referenced - known_domain_ids
        if unknown:
            return False, (
                f"subtask {subtask.get('id')} hypothesis package references "
                "unknown domain id(s): "
                + ", ".join(sorted(unknown))
            )
    return True, ""

def _top_k_prompt_limit(state: ZeroMDASHState, bucket: str) -> str:
    limit = _top_k_limit(state, bucket)
    scope = state.get("scan_scope")
    if isinstance(scope, dict) and scope.get("mode") == "diff":
        cap = (
            f"top_K.{bucket}={limit} is an explicit cost cap."
            if limit is not None
            else f"top_K.{bucket} is not configured; there is no numeric dispatch cap."
        )
        return (
            f"{cap} Emit every independent diff-attributable risk surface, but converge "
            "clauses/CVEs/checks that share the same change-triggered root cause and "
            "input-to-sink data flow into one subtask. Do not emit standalone adjacent "
            "or pre-existing audits that cannot establish a diff-to-sink hypothesis."
        )
    if limit is None:
        return f"top_K.{bucket} is not configured; return all high-quality subtasks in priority order."
    return f"top_K.{bucket}={limit}; rank all subtasks, because only the first {limit} will be dispatched."

def _run_planner_with_retry(
    state: ZeroMDASHState,
    *,
    backends,
    node: str,
    prompt: str,
    out_path,
    bucket: str,
    prefix: str,
    focus: str = "",
) -> tuple[list[Subtask], list[str]]:
    ws = _ws(state)
    subtasks: list[Subtask] = []
    candidates_path = out_path.with_name(f"{out_path.stem}.candidates.json")
    convergence_path = out_path.with_name(f"{out_path.stem}.convergence.json")
    last_validation_failure = ""
    artifact_committed = False

    def write_json(path: Path, payload: Any) -> None:
        """Commit planner state with a same-directory atomic rename."""
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
        try:
            tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
            tmp_path.replace(path)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

    def prepare(raw: Any) -> tuple[list[Subtask] | None, str]:
        if not isinstance(raw, list):
            return None, "planner output must be a JSON array"
        for index, item in enumerate(raw):
            if not isinstance(item, dict):
                return None, f"planner item {index} must be an object"
            if not str(item.get("objective") or "").strip():
                return None, f"planner item {index} objective is required"
            if not isinstance(item.get("hints"), dict):
                return None, f"planner item {index} hints must be an object"

        prepared = _normalize_subtasks(raw, bucket, prefix)
        prepared = _apply_scan_scope_to_subtasks(prepared, state)
        domain_refs_ok, domain_refs_error = _validate_domain_refs(prepared, state)
        if not domain_refs_ok:
            return None, domain_refs_error
        packages_ok, packages_error = _validate_hypothesis_packages(prepared, state)
        if not packages_ok:
            return None, packages_error
        if not _diff_planner_contract_valid(prepared, state):
            return None, "planner output violates the diff planning contract"

        scope = state.get("scan_scope")
        if isinstance(scope, dict) and scope.get("mode") == "diff":
            write_json(candidates_path, prepared)
            raw_count = len(prepared)
            attributable_count = sum(
                1 for item in prepared if _subtask_is_diff_attributable(item, state)
            )
            prepared, omitted = _converge_diff_planner_subtasks(prepared, state)
            write_json(
                convergence_path,
                {
                    "schema_version": 1,
                    "raw_candidate_count": raw_count,
                    "diff_attributable_count": attributable_count,
                    "independent_risk_count": len(prepared),
                    "omitted": omitted,
                },
            )
        return prepared, ""

    def read_artifact() -> tuple[Any, str]:
        if not out_path.is_file():
            return None, f"planner artifact was not created: {out_path}"
        try:
            return json.loads(out_path.read_text()), ""
        except (OSError, json.JSONDecodeError) as exc:
            return None, f"planner artifact is not valid JSON: {exc}"

    def commit(raw: Any) -> tuple[bool, str]:
        nonlocal artifact_committed, subtasks
        prepared, detail = prepare(raw)
        if prepared is None:
            return False, detail
        write_json(out_path, prepared)
        # State is populated from the canonical artifact, never directly from
        # stdout or an in-memory intermediate representation.
        committed_payload, detail = read_artifact()
        if not isinstance(committed_payload, list):
            return False, detail or "committed planner artifact must be an array"
        subtasks = committed_payload
        artifact_committed = True
        return True, ""

    def reset() -> None:
        nonlocal artifact_committed, subtasks, last_validation_failure
        artifact_committed = False
        subtasks = []
        last_validation_failure = ""
        _reset_file_output(out_path)
        _reset_file_output(candidates_path)
        _reset_file_output(convergence_path)

    def materialize(res: AgentResult) -> None:
        nonlocal last_validation_failure
        # Agents may write the requested canonical artifact and print only a
        # small status receipt. Preserve a valid artifact instead of replacing
        # it with whatever JSON happened to be printed on stdout.
        artifact_raw, artifact_error = read_artifact()
        if artifact_error == "":
            artifact_ok, artifact_detail = commit(artifact_raw)
            if artifact_ok:
                return
            last_validation_failure = artifact_detail

        stdout_raw = _try_json(res.stdout, fallback=None)
        stdout_ok, stdout_detail = commit(stdout_raw)
        if stdout_ok:
            return

        fallback_raw = _planner_fallback_json(res)
        fallback_ok, fallback_detail = commit(fallback_raw)
        if fallback_ok:
            return
        last_validation_failure = "; ".join(
            detail
            for detail in (
                last_validation_failure or artifact_error,
                f"stdout: {stdout_detail}",
                f"plan.json: {fallback_detail}",
            )
            if detail
        )

    def validate(res: AgentResult) -> tuple[bool, str]:
        del res
        raw, detail = read_artifact()
        if detail:
            return False, last_validation_failure or detail
        if not artifact_committed:
            return False, last_validation_failure or "planner artifact was not committed"
        if raw != subtasks:
            return False, "planner artifact changed after validation"
        return True, ""

    _, errors = _invoke_with_output_retry(
        ws,
        node,
        prompt,
        backends,
        state,
        output_desc=str(out_path),
        reset=reset,
        materialize=materialize,
        validate=validate,
        focus=focus,
    )
    if not errors:
        # Reload once more after the retry helper accepts the attempt. This is
        # the commit point between the durable planner artifact and LangGraph
        # state, and prevents either representation from advancing alone.
        raw, detail = read_artifact()
        if detail:
            subtasks = []
            errors = [f"[{node}] committed planner artifact unavailable: {detail}"]
        elif not isinstance(raw, list):
            subtasks = []
            errors = [f"[{node}] committed planner artifact must be an array"]
        elif raw != subtasks:
            subtasks = []
            errors = [f"[{node}] committed planner artifact changed before state load"]
        else:
            subtasks = raw
    if errors:
        subtasks = []
        write_json(out_path, subtasks)
    return subtasks, errors

__all__ = [
    "_normalize_subtasks",
    "_apply_scan_scope_to_subtasks",
    "_top_k_prompt_limit",
    "_validate_domain_refs",
    "_validate_hypothesis_packages",
    "_run_planner_with_retry",
]

