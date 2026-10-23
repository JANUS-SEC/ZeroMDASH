"""Canonical target-history patch manifest validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from zeromdash.state import ZeroMDASHState
from zeromdash.workspace import Workspace

from .constants import *
from .context import _ws
from .repository import _target_repos_from_state, _target_repos_root

def _target_history_repo_registry(state: ZeroMDASHState) -> tuple[str, list[dict[str, str]]]:
    repos = _target_repos_from_state(state)
    if repos:
        return "multi_repo", [
            {
                "repo_id": str(repo["id"]),
                "role": str(repo.get("role") or ""),
                "target": str(repo.get("target") or ""),
                "repo_path": str(_target_repos_root(_ws(state)) / str(repo["id"])),
            }
            for repo in repos
        ]
    return "single_repo", [
        {
            "repo_id": "main",
            "role": "main",
            "target": str(state.get("target") or ""),
            "repo_path": str(state.get("repo_path") or _ws(state).main_path("repo")),
        }
    ]

def _string_or_none(value: Any) -> bool:
    return value is None or isinstance(value, str)

def _string_list(value: Any, *, allow_empty: bool = True) -> bool:
    return (
        isinstance(value, list)
        and (allow_empty or bool(value))
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )

def _validate_patch_manifest(
    path: Path,
    *,
    target: str,
    repo_mode: str,
    repo_registry: list[dict[str, str]],
) -> tuple[bool, str]:
    try:
        payload = json.loads(path.read_text())
    except FileNotFoundError:
        return False, f"missing canonical patch manifest: {path}"
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"invalid patch manifest JSON: {exc}"
    if not isinstance(payload, dict):
        return False, "patch manifest must be a JSON object"
    if set(payload) != _PATCH_MANIFEST_KEYS:
        return False, "patch manifest top-level keys do not match schema v1.0"
    if payload.get("schema_version") != _PATCH_MANIFEST_SCHEMA_VERSION:
        return False, f"schema_version must be {_PATCH_MANIFEST_SCHEMA_VERSION}"
    if payload.get("target") != target:
        return False, "patch manifest target does not match workflow target"
    if payload.get("mode") != repo_mode:
        return False, f"patch manifest mode must be {repo_mode}"

    expected = {item["repo_id"]: item for item in repo_registry}
    repositories = payload.get("repositories")
    if not isinstance(repositories, list):
        return False, "repositories must be an array"
    repo_by_id: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(repositories):
        if not isinstance(item, dict):
            return False, f"repositories[{index}] must be an object"
        if set(item) != _PATCH_REPOSITORY_KEYS:
            return False, f"repositories[{index}] keys do not match schema v1.0"
        repo_id = item.get("repo_id")
        if not isinstance(repo_id, str) or not repo_id:
            return False, f"repositories[{index}].repo_id is required"
        if repo_id in repo_by_id:
            return False, f"duplicate repository repo_id: {repo_id}"
        for key in ("role", "target", "repo_path"):
            if not isinstance(item.get(key), str) or (key != "role" and not item.get(key).strip()):
                return False, f"repositories[{index}].{key} must be a string"
        for key in ("branch", "head", "describe"):
            if not _string_or_none(item.get(key)):
                return False, f"repositories[{index}].{key} must be string or null"
        repo_by_id[repo_id] = item
    if set(repo_by_id) != set(expected):
        return False, "repositories repo_ids must exactly match the target repository registry"
    for repo_id, expected_repo in expected.items():
        actual = repo_by_id[repo_id]
        for key in ("role", "target", "repo_path"):
            if actual.get(key) != expected_repo.get(key):
                return False, f"repository {repo_id} {key} does not match target registry"

    coverage = payload.get("coverage")
    if not isinstance(coverage, list):
        return False, "coverage must be an array"
    coverage_ids: list[str] = []
    for index, item in enumerate(coverage):
        if not isinstance(item, dict):
            return False, f"coverage[{index}] must be an object"
        if set(item) != _PATCH_COVERAGE_KEYS:
            return False, f"coverage[{index}] keys do not match schema v1.0"
        repo_id = item.get("repo_id")
        if repo_id not in expected:
            return False, f"coverage[{index}] references unknown repo_id"
        if item.get("status") not in _PATCH_COVERAGE_STATUSES:
            return False, f"coverage[{index}].status is invalid"
        if not _string_list(item.get("sources_checked")):
            return False, f"coverage[{index}].sources_checked must be a string array"
        if not isinstance(item.get("notes"), str):
            return False, f"coverage[{index}].notes must be a string"
        coverage_ids.append(str(repo_id))
    if len(coverage_ids) != len(set(coverage_ids)) or set(coverage_ids) != set(expected):
        return False, "coverage must contain exactly one record for every repository"

    findings = payload.get("findings")
    if not isinstance(findings, list):
        return False, "findings must be an array"
    record_ids: set[str] = set()
    for index, item in enumerate(findings):
        if not isinstance(item, dict):
            return False, f"findings[{index}] must be an object"
        if set(item) != _PATCH_FINDING_KEYS:
            return False, f"findings[{index}] keys do not match schema v1.0"
        record_id = item.get("record_id")
        if not isinstance(record_id, str) or not record_id:
            return False, f"findings[{index}].record_id is required"
        if record_id in record_ids:
            return False, f"duplicate finding record_id: {record_id}"
        record_ids.add(record_id)
        if item.get("repo_id") not in expected:
            return False, f"findings[{index}] references unknown repo_id"
        if not _string_list(item.get("advisory_ids")):
            return False, f"findings[{index}].advisory_ids must be a string array"
        for key in ("title", "root_cause_class", "lesson", "notes"):
            if not isinstance(item.get(key), str) or (key != "notes" and not item.get(key).strip()):
                return False, f"findings[{index}].{key} must be a string"
        if not _string_list(item.get("affected_locations")):
            return False, f"findings[{index}].affected_locations must be a string array"
        if item.get("applicability") not in _PATCH_APPLICABILITY:
            return False, f"findings[{index}].applicability is invalid"
        sources = item.get("sources")
        if not isinstance(sources, list) or not sources:
            return False, f"findings[{index}].sources must be a non-empty array"
        for source in sources:
            if (
                not isinstance(source, dict)
                or set(source) != _PATCH_SOURCE_KEYS
                or source.get("type") not in _PATCH_SOURCE_TYPES
                or not isinstance(source.get("url"), str)
                or not source.get("url").strip()
            ):
                return False, f"findings[{index}] has an invalid source"
        patch = item.get("patch")
        if not isinstance(patch, dict):
            return False, f"findings[{index}].patch must be an object"
        if set(patch) != _PATCH_OBJECT_KEYS:
            return False, f"findings[{index}].patch keys do not match schema v1.0"
        if patch.get("status") not in _PATCH_MANIFEST_STATUSES:
            return False, f"findings[{index}].patch.status is invalid"
        if patch.get("verification") not in _PATCH_VERIFICATIONS:
            return False, f"findings[{index}].patch.verification is invalid"
        for key in ("upstream_commits", "equivalent_commits", "fixed_versions"):
            if not _string_list(patch.get(key)):
                return False, f"findings[{index}].patch.{key} must be a string array"
        if not _string_or_none(patch.get("verified_against_head")):
            return False, f"findings[{index}].patch.verified_against_head must be string or null"
        if not isinstance(patch.get("notes"), str):
            return False, f"findings[{index}].patch.notes must be a string"
    return True, ""

__all__ = ["_target_history_repo_registry","_string_or_none","_string_list","_validate_patch_manifest"]

