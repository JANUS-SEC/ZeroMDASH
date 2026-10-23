"""Target repository materialization and multi-repository helpers."""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

from zeromdash.state import ZeroMDASHState
from zeromdash.workspace import Workspace, slugify

from .io import _dir_has_materialized_output

def _repo_has_materialized_source(repo_path) -> bool:
    """Return True when fetch_target_repo produced a non-empty source tree.

    The workspace pre-creates ``main/repo`` before the agent runs, so existence
    alone is not enough. A git clone that leaves only ``.git`` is also treated
    as empty because downstream search/planner nodes need actual checkout
    files to inspect.
    """
    if not repo_path.is_dir():
        return False
    return any(child.name != ".git" for child in repo_path.iterdir())

def _reset_repo_dir(repo_path) -> None:
    if repo_path.exists():
        shutil.rmtree(repo_path)
    repo_path.mkdir(parents=True, exist_ok=True)

def _reset_target_repos_dirs(ws: Workspace) -> None:
    _reset_repo_dir(ws.main_path("repo"))
    _reset_repo_dir(_target_repos_root(ws))

def _target_repo_id(value: Any) -> str:
    return slugify(str(value or ""), fallback="repo")

def _target_repos_from_state(state: ZeroMDASHState) -> list[dict[str, Any]]:
    repos = state.get("target_repos") or []
    if not isinstance(repos, list):
        return []
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(repos, start=1):
        if not isinstance(item, dict):
            continue
        repo_id = _target_repo_id(item.get("id") or item.get("name") or f"repo{index}")
        if repo_id in seen:
            suffix = 2
            base = repo_id
            while f"{base}_{suffix}" in seen:
                suffix += 1
            repo_id = f"{base}_{suffix}"
        seen.add(repo_id)
        target = str(item.get("target") or item.get("url") or item.get("path") or "").strip()
        if not target:
            continue
        entry = dict(item)
        entry["id"] = repo_id
        entry["target"] = target
        normalized.append(entry)
    return normalized

def _target_repos_root(ws: Workspace) -> Path:
    return ws.main_path("repos")

def _target_repo_manifest_path(ws: Workspace) -> Path:
    return _target_repos_root(ws) / "_manifest.json"

def _repo_has_aggregate_entries(repo_path: Path, repos: list[dict[str, Any]]) -> bool:
    return all(
        _repo_has_materialized_source(repo_path / str(repo["id"]))
        for repo in repos
    )

def _write_target_repos_manifest(ws: Workspace, repos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    repos_root = _target_repos_root(ws)
    manifest_entries: list[dict[str, Any]] = []
    for repo in repos:
        repo_id = str(repo["id"])
        source_path = repos_root / repo_id
        aggregate_path = ws.main_path("repo") / repo_id
        entry = {
            "id": repo_id,
            "target": repo.get("target", ""),
            "role": repo.get("role", ""),
            "description": repo.get("description", ""),
            "source_path": str(source_path),
            "aggregate_path": str(aggregate_path),
        }
        manifest_entries.append({key: value for key, value in entry.items() if value})
    path = _target_repo_manifest_path(ws)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"repos": manifest_entries}, ensure_ascii=False, indent=2))
    return manifest_entries

def _build_aggregate_repo_view(ws: Workspace, repos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Rebuild main/repo as a stable aggregate view over main/repos/<id>."""
    aggregate_root = ws.main_path("repo")
    _reset_repo_dir(aggregate_root)
    repos_root = _target_repos_root(ws)
    manifest_entries = _write_target_repos_manifest(ws, repos)
    for entry in manifest_entries:
        repo_id = str(entry["id"])
        source_path = repos_root / repo_id
        target_path = aggregate_root / repo_id
        if not _repo_has_materialized_source(source_path):
            continue
        target_path.symlink_to(Path("..") / "repos" / repo_id, target_is_directory=True)
    (aggregate_root / "_target_repos.json").write_text(
        json.dumps({"repos": manifest_entries}, ensure_ascii=False, indent=2)
    )
    return manifest_entries

def _copy_local_target_tree(src: Path, dst: Path) -> None:
    """Copy a local target directory into the workspace without mutating it."""
    _reset_repo_dir(dst)
    ignored_top_level = {".zeromdash", ".git", ".hg", ".svn", "__pycache__", ".DS_Store"}
    ignore = shutil.ignore_patterns(
        ".zeromdash",
        ".git",
        ".hg",
        ".svn",
        "__pycache__",
        ".DS_Store",
    )
    for child in src.iterdir():
        if child.name in ignored_top_level:
            continue
        target = dst / child.name
        if child.is_dir():
            shutil.copytree(child, target, symlinks=True, ignore=ignore)
        else:
            shutil.copy2(child, target, follow_symlinks=False)

def _local_target_dir(target: str) -> Path | None:
    raw = str(target or "").strip()
    if not raw or "://" in raw:
        return None
    path = Path(raw).expanduser()
    if path.is_dir():
        return path.resolve()
    return None

def _format_target_repos_prompt_manifest(ws: Workspace, repos: list[dict[str, Any]]) -> str:
    repos_root = _target_repos_root(ws)
    entries = []
    for repo in repos:
        repo_id = str(repo["id"])
        entries.append(
            {
                "id": repo_id,
                "target": repo.get("target", ""),
                "role": repo.get("role", ""),
                "description": repo.get("description", ""),
                "destination": str(repos_root / repo_id),
            }
        )
    return json.dumps(entries, ensure_ascii=False, indent=2)

def _copy_local_target_repos(ws: Workspace, repos: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    remote_repos: list[dict[str, Any]] = []
    errors: list[str] = []
    repos_root = _target_repos_root(ws)
    repos_root.mkdir(parents=True, exist_ok=True)
    for repo in repos:
        destination = repos_root / str(repo["id"])
        local_dir = _local_target_dir(str(repo.get("target") or ""))
        if local_dir is None:
            remote_repos.append(repo)
            continue
        try:
            _copy_local_target_tree(local_dir, destination)
        except OSError as exc:
            errors.append(
                f"[fetch_target_repo/{repo['id']}] failed to copy local target {local_dir}: {exc}"
            )
            continue
        if not _repo_has_materialized_source(destination):
            errors.append(
                f"[fetch_target_repo/{repo['id']}] local target copied but materialized repo is empty: {destination}"
            )
    return remote_repos, errors

__all__ = ["_repo_has_materialized_source","_reset_repo_dir","_reset_target_repos_dirs","_target_repo_id","_target_repos_from_state","_target_repos_root","_target_repo_manifest_path","_repo_has_aggregate_entries","_write_target_repos_manifest","_build_aggregate_repo_view","_copy_local_target_tree","_local_target_dir","_format_target_repos_prompt_manifest","_copy_local_target_repos"]

