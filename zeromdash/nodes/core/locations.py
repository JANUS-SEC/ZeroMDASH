"""Repository-location normalization shared by planning helpers."""

from __future__ import annotations

from typing import Any

from zeromdash.state import ZeroMDASHState


def _location_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return []


def _normalize_repo_location(location: Any, state: ZeroMDASHState) -> str:
    raw = str(location or "").strip().replace("\\", "/")
    if not raw:
        return ""
    path_part = raw.split(":", 1)[0]
    repo_path = str(state.get("repo_path") or "").replace("\\", "/").rstrip("/")
    workspace_root = str(state.get("workspace_root") or "").replace("\\", "/").rstrip("/")
    task_id = str(state.get("task_id") or "").strip()
    prefixes = [prefix for prefix in (repo_path, f"{workspace_root}/{task_id}/main/repo") if prefix]
    normalized = path_part
    for prefix in prefixes:
        if normalized == prefix:
            normalized = ""
            break
        if normalized.startswith(prefix + "/"):
            normalized = normalized[len(prefix) + 1 :]
            break
    for marker in ("main/repo/", "repo/"):
        if marker in normalized:
            normalized = normalized.split(marker, 1)[1]
            break
    return normalized.lstrip("./")


def _changed_file_set(state: ZeroMDASHState) -> set[str]:
    scope = state.get("scan_scope")
    if not isinstance(scope, dict):
        return set()
    return {
        normalized
        for item in scope.get("changed_files") or []
        if (normalized := _normalize_repo_location(item, state))
    }


def _locations_intersect_diff(locations: Any, state: ZeroMDASHState) -> bool:
    changed = _changed_file_set(state)
    if not changed:
        return False
    normalized = {_normalize_repo_location(item, state) for item in _location_values(locations)}
    return bool(changed & {item for item in normalized if item})


__all__ = [
    "_location_values",
    "_normalize_repo_location",
    "_changed_file_set",
    "_locations_intersect_diff",
]
