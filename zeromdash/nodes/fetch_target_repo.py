"""LangGraph node implementation: fetch_target_repo."""

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

from .core.config import (
    _agent_configs_with_node_variant,
    agent_config_variants_for_node,
)
from .core.constants import DEFAULT_FETCH_TARGET_REPO_ATTEMPTS
from .core.recovery import node_runtime_failure, recover_runtime
from .core.context import (
    _node_focus,
    _ws,
)
from .core.invocation import (
    _agent_errors,
    _emit_node_fallback,
    _invoke,
    _retry_feedback_block,
)
from .core.repository import (
    _build_aggregate_repo_view,
    _copy_local_target_repos,
    _copy_local_target_tree,
    _format_target_repos_prompt_manifest,
    _local_target_dir,
    _repo_has_aggregate_entries,
    _repo_has_materialized_source,
    _reset_repo_dir,
    _reset_target_repos_dirs,
    _target_repo_manifest_path,
    _target_repos_from_state,
    _target_repos_root,
)

def fetch_target_repo(state: ZeroMDASHState, *, backends=None) -> dict:
    ws = _ws(state)
    repo_path = ws.main_path("repo")
    target_repos = _target_repos_from_state(state)
    manifest_path = _target_repo_manifest_path(ws)
    log = ws.log_path("review_log") / "fetch_target_repo.log"
    log.write_text("")
    focus = _node_focus(state, "fetch_target_repo_focus")
    if target_repos:
        _reset_target_repos_dirs(ws)
        remote_repos, local_errors = _copy_local_target_repos(ws, target_repos)
        if local_errors:
            log.write_text("\n".join(local_errors) + "\n")
            return {
                "repo_path": str(repo_path),
                "target_repos_path": str(manifest_path),
                "target_repos": target_repos,
                "errors": local_errors,
            }
        if not remote_repos:
            manifest_entries = _build_aggregate_repo_view(ws, target_repos)
            if _repo_has_aggregate_entries(repo_path, target_repos):
                log.write_text(
                    "action: deterministic multi-repo local copy\n"
                    f"manifest: {manifest_path}\n"
                    f"aggregate: {repo_path}\n"
                    "status: ok\n"
                )
                return {
                    "repo_path": str(repo_path),
                    "target_repos_path": str(manifest_path),
                    "target_repos": manifest_entries,
                    "errors": [],
                }
            error = f"[fetch_target_repo] aggregate view is empty or incomplete: {repo_path}"
            log.write_text(error + "\n")
            return {
                "repo_path": str(repo_path),
                "target_repos_path": str(manifest_path),
                "target_repos": manifest_entries,
                "errors": [error],
            }

        base_prompt = prompts.FETCH_TARGET_REPOS.format(
            target=state["target"],
            focus=focus,
            diff_git=state.get("diff_git", ""),
            repo_manifest=_format_target_repos_prompt_manifest(ws, remote_repos),
        )
    else:
        base_prompt = prompts.FETCH_TARGET_REPO.format(
            target=state["target"],
            focus=focus,
            diff_git=state.get("diff_git", ""),
            repo_path=repo_path,
        )
        local_dir = _local_target_dir(state.get("target", ""))
        if local_dir is not None:
            try:
                _copy_local_target_tree(local_dir, repo_path)
            except OSError as exc:
                error = f"[fetch_target_repo] failed to copy local target {local_dir}: {exc}"
                log.write_text(f"local source: {local_dir}\ndestination: {repo_path}\nstatus: error\n{error}\n")
                return {"repo_path": str(repo_path), "errors": [error]}
            if _repo_has_materialized_source(repo_path):
                log.write_text(
                    f"local source: {local_dir}\n"
                    f"destination: {repo_path}\n"
                    "action: deterministic local copy\n"
                    "status: ok\n"
                )
                return {"repo_path": str(repo_path), "errors": []}
            error = f"[fetch_target_repo] local target copied but materialized repo is empty: {repo_path}"
            log.write_text(
                f"local source: {local_dir}\n"
                f"destination: {repo_path}\n"
                "action: deterministic local copy\n"
                "status: empty\n"
            )
            return {"repo_path": str(repo_path), "errors": [error]}

    return _fetch_target_repo_with_recovery(
        state, backends=backends, ws=ws, repo_path=repo_path,
        target_repos=target_repos, manifest_path=manifest_path, log=log,
        base_prompt=base_prompt, focus=focus,
    )


@recover_runtime(node="fetch_target_repo", failure=node_runtime_failure)
def _fetch_target_repo_with_recovery(
    state: ZeroMDASHState, *, backends, ws, repo_path, target_repos,
    manifest_path, log, base_prompt, focus,
) -> dict:
    last_res: AgentResult | None = None
    errors: list[str] = []
    variants = agent_config_variants_for_node("fetch_target_repo", backends, state.get("agent_configs"))
    for variant_index, variant in enumerate(variants, start=1):
        variant_configs = _agent_configs_with_node_variant(state.get("agent_configs"), "fetch_target_repo", variant)
        retry_feedback = ""
        previous_failure = ""
        for attempt in range(1, DEFAULT_FETCH_TARGET_REPO_ATTEMPTS + 1):
            if attempt > 1 or variant_index > 1:
                if target_repos:
                    _reset_target_repos_dirs(ws)
                    _, local_errors = _copy_local_target_repos(ws, target_repos)
                    if local_errors:
                        errors = local_errors
                        break
                else:
                    _reset_repo_dir(repo_path)

            attempt_prompt = base_prompt + retry_feedback if retry_feedback else base_prompt
            res = _invoke(
                ws, "fetch_target_repo",
                attempt_prompt,
                {"fetch_target_repo": normalize_agent_name(variant["runtime"])},
                agent_configs=variant_configs,
                agent_config_task_types=state.get("agent_config_task_types"),
                extra_context={
                    "attempt": attempt,
                    "max_attempts": DEFAULT_FETCH_TARGET_REPO_ATTEMPTS,
                    "focus": focus,
                    "previous_failure": previous_failure,
                    "fallback_index": variant_index - 1,
                    "fallback_count": len(variants) - 1,
                },
            )
            last_res = res
            with log.open("a") as fp:
                fp.write(
                    f"\n--- attempt {attempt}/{DEFAULT_FETCH_TARGET_REPO_ATTEMPTS} "
                    f"fallback {variant_index - 1}/{len(variants) - 1} "
                    f"backend={res.backend} rc={res.returncode} ---\n"
                )
                fp.write(res.stdout.rstrip() + "\n")
                if res.stderr:
                    fp.write("\n[stderr]\n" + res.stderr.rstrip() + "\n")

            errors = _agent_errors(res, "fetch_target_repo")
            if errors:
                previous_failure = errors[0]
                retry_feedback = _retry_feedback_block(
                    node="fetch_target_repo",
                    subtask_id=None,
                    attempt=attempt + 1,
                    attempts=DEFAULT_FETCH_TARGET_REPO_ATTEMPTS,
                    output_desc=str(repo_path if not target_repos else _target_repos_root(ws)),
                    failure=previous_failure,
                )
                continue
            if target_repos:
                missing = [
                    str(repo["id"])
                    for repo in target_repos
                    if not _repo_has_materialized_source(_target_repos_root(ws) / str(repo["id"]))
                ]
                if not missing:
                    manifest_entries = _build_aggregate_repo_view(ws, target_repos)
                    if _repo_has_aggregate_entries(repo_path, target_repos):
                        return {
                            "repo_path": str(repo_path),
                            "target_repos_path": str(manifest_path),
                            "target_repos": manifest_entries,
                            "errors": [],
                        }
                previous_failure = (
                    f"[fetch_target_repo] multi-repo materialization incomplete after attempt "
                    f"{attempt}/{DEFAULT_FETCH_TARGET_REPO_ATTEMPTS}: missing {', '.join(missing)}"
                )
            elif _repo_has_materialized_source(repo_path):
                return {"repo_path": str(repo_path), "errors": []}
            else:
                previous_failure = (
                    f"[fetch_target_repo] materialized repo is empty after attempt "
                    f"{attempt}/{DEFAULT_FETCH_TARGET_REPO_ATTEMPTS}: {repo_path}"
                )
            retry_feedback = _retry_feedback_block(
                node="fetch_target_repo",
                subtask_id=None,
                attempt=attempt + 1,
                attempts=DEFAULT_FETCH_TARGET_REPO_ATTEMPTS,
                output_desc=str(repo_path if not target_repos else _target_repos_root(ws)),
                failure=previous_failure,
            )
            errors = [previous_failure]
        if errors and variant_index < len(variants):
            _emit_node_fallback(
                "fetch_target_repo",
                last_res or AgentResult("", "", 1, normalize_agent_name(variant["runtime"])),
                variants[variant_index],
            )

    if last_res is None:
        errors = ["[fetch_target_repo] did not run"]
    result = {"repo_path": str(repo_path), "errors": errors}
    if target_repos:
        result["target_repos_path"] = str(manifest_path)
        result["target_repos"] = target_repos
    return result

def route_after_fetch_target_repo(state: ZeroMDASHState) -> list[str] | str:
    """Stop the workflow immediately if repository acquisition failed."""
    if state.get("errors"):
        return "__end__"
    return "prepare_scan_scope"

def route_after_prepare_scan_scope(state: ZeroMDASHState) -> list[str] | str:
    """Fan out gather nodes only after the full/diff scope is materialized."""
    if state.get("errors"):
        return "__end__"
    gather = [
        "search_spec",
        "search_fuzz_driver",
        "search_similar_software",
        "search_target_history",
    ]
    disabled = set(state.get("disabled_nodes") or [])
    return [n for n in gather if n not in disabled]

__all__ = ["fetch_target_repo","route_after_fetch_target_repo","route_after_prepare_scan_scope"]

