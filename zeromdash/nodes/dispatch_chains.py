"""Dispatch planned chain candidates into chain subtask graphs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from langgraph.constants import Send

from zeromdash.state import ChainCandidate, ZeroMDASHState

from .plan_chains import _chain_config


def _max_chain_iterations(state: ZeroMDASHState) -> int:
    config = _chain_config(state)
    try:
        value = int(config.get("max_battle_rounds", 2))
    except (TypeError, ValueError):
        return 2
    return value if value > 0 else 2


def dispatch_chains(state: ZeroMDASHState, *, backends=None) -> dict:
    del state, backends
    return {}


def _dispatch_chain_candidates(chains: list[ChainCandidate], state: ZeroMDASHState) -> list[Send]:
    sends: list[Send] = []
    for chain in chains:
        chain_id = str(chain.get("chain_id") or "")
        if not chain_id:
            continue
        child: dict[str, Any] = {
            "task_id": state["task_id"],
            "workspace_root": state["workspace_root"],
            "target": state.get("target", ""),
            "repo_path": state["repo_path"],
            "scope_path": state.get("scope_path", ""),
            "scan_scope": dict(state.get("scan_scope") or {}),
            "chain_candidate": chain,
            "chain_pool": list(state.get("chain_pool") or []),
            "iteration": 0,
            "max_chain_iterations": _max_chain_iterations(state),
            "min_critic_skills": state.get("min_critic_skills", 2),
            "agent_configs": state.get("agent_configs", {}),
            "agent_config_task_types": state.get("agent_config_task_types", {}),
            "common_focus": state.get("common_focus", ""),
            "attack_surface": state.get("attack_surface", ""),
            "domain_registry_path": state.get("domain_registry_path", ""),
            "domain_registry": dict(state.get("domain_registry") or {}),
            "spec_doc": state.get("spec_doc", ""),
            "similar_writeups": list(state.get("similar_writeups") or []),
            "feature_docs": list(state.get("feature_docs") or []),
            "chain_review_history": [],
            "selected_chain_log_dir": state.get("selected_chain_log_dir", ""),
        }
        sends.append(Send("chain_subtask", child))
    return sends


def dispatch_all_chains(state: ZeroMDASHState) -> list[Send] | str:
    disabled = set(state.get("disabled_nodes") or [])
    if "chain_investigate_subtask" in disabled or "chain_critic_subtask" in disabled:
        return "prepare_report_groups"
    sends = _dispatch_chain_candidates(list(state.get("chain_plan") or []), state)
    return sends or "prepare_report_groups"


def dispatch_selected_chains(state: ZeroMDASHState) -> list[Send] | str:
    requested = set(state.get("selected_chain_ids") or [])
    chains = [
        chain
        for chain in state.get("chain_plan", []) or []
        if str(chain.get("chain_id") or "") in requested
    ]
    sends = _dispatch_chain_candidates(chains, state)
    return sends or "collect_selected_chain_statuses"


def collect_selected_chain_statuses(state: ZeroMDASHState) -> dict:
    raw_dir = str(state.get("selected_chain_log_dir") or "").strip()
    if not raw_dir:
        raise ValueError("selected chain status collection requires an output directory")
    selected_dir = Path(raw_dir)
    errors = [str(item) for item in state.get("errors") or []]
    statuses: list[dict[str, Any]] = []
    for chain_id in state.get("selected_chain_ids") or []:
        result_path = selected_dir / "chain_res" / f"{chain_id}.json"
        candidate_path = selected_dir / "chain_candidates" / f"{chain_id}.json"
        matching_errors = [error for error in errors if chain_id in error]
        payload = {}
        if result_path.is_file():
            try:
                payload = json.loads(result_path.read_text())
            except (OSError, json.JSONDecodeError):
                payload = {}
            status = "finding"
        elif candidate_path.is_file():
            try:
                payload = json.loads(candidate_path.read_text())
            except (OSError, json.JSONDecodeError):
                payload = {}
            status = "candidate"
        else:
            status = "failed"
        review = payload.get("review") if isinstance(payload, dict) else {}
        statuses.append(
            {
                "chain_id": chain_id,
                "status": status,
                "verdict": str((review or {}).get("verdict") or ""),
                "result_path": str(result_path) if result_path.is_file() else "",
                "candidate_path": str(candidate_path) if candidate_path.is_file() else "",
                "errors": matching_errors,
            }
        )
    out = selected_dir / "selected_chain_statuses.json"
    out.write_text(json.dumps(statuses, ensure_ascii=False, indent=2))
    return {
        "selected_chain_statuses": statuses,
        "stopped_at": "selected_chains",
    }


def prepare_selected_chain_log_dir(
    *,
    workspace_base: Path,
    selected_chain_log_dir: str | Path | None = None,
) -> Path:
    if selected_chain_log_dir:
        output_dir = Path(selected_chain_log_dir).expanduser()
        if not output_dir.is_absolute():
            output_dir = (workspace_base / output_dir).resolve()
            output_dir.relative_to(workspace_base.resolve())
        else:
            output_dir = output_dir.resolve()
    else:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_dir = workspace_base / "log" / "selected_chain_runs" / timestamp
        suffix = 1
        while output_dir.exists():
            output_dir = workspace_base / "log" / "selected_chain_runs" / f"{timestamp}_{suffix}"
            suffix += 1
    if output_dir.exists():
        raise ValueError(
            "selected chain log directory already exists; choose a new "
            f"--select-chain-to-run-log-dir: {output_dir}"
        )
    for subdir in ("attempts", "investigations", "critic_reviews", "chain_res", "chain_candidates"):
        (output_dir / subdir).mkdir(parents=True, exist_ok=True)
    return output_dir


__all__ = [
    "dispatch_chains",
    "dispatch_all_chains",
    "dispatch_selected_chains",
    "collect_selected_chain_statuses",
    "prepare_selected_chain_log_dir",
]
