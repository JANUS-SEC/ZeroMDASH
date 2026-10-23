"""LangGraph wiring and runner for cross-workspace gather scans."""

from __future__ import annotations

import json
from functools import partial
from pathlib import Path
from typing import Any

from langgraph.graph import END, START, StateGraph

from zeromdash.agents import langfuse_config
from zeromdash.gather import prepare_gather_state
from zeromdash.gather_state import (
    GatherChainSubtaskInputState,
    GatherChainSubtaskOutputState,
    GatherChainSubtaskState,
    GatherState,
)
from zeromdash.nodes.dispatch_gather_chains import (
    dispatch_all_gather_chains,
    dispatch_gather_chains,
)
from zeromdash.nodes.gather_analyze_attack_surface import gather_analyze_attack_surface
from zeromdash.nodes.gather_chain_critic_subtask import (
    gather_chain_critic_subtask,
    route_after_gather_chain_critic,
)
from zeromdash.nodes.gather_chain_investigate_subtask import (
    gather_chain_investigate_subtask,
    route_after_gather_chain_investigation,
)
from zeromdash.nodes.gather_finalize_chain_subtask import gather_finalize_chain_subtask
from zeromdash.nodes.gather_plan_chains import gather_plan_chains
from zeromdash.nodes.gather_prepare_report_groups import gather_prepare_report_groups
from zeromdash.nodes.gather_summary import gather_summary
from zeromdash.nodes.polish_report import polish_report


def build_gather_chain_subtask_graph(backends: dict[str, str] | None = None):
    graph: StateGraph = StateGraph(
        GatherChainSubtaskState,
        input_schema=GatherChainSubtaskInputState,
        output_schema=GatherChainSubtaskOutputState,
    )

    def bind(fn):
        return partial(fn, backends=backends)

    graph.add_node("gather_chain_investigate_subtask", bind(gather_chain_investigate_subtask))
    graph.add_node("gather_chain_critic_subtask", bind(gather_chain_critic_subtask))
    graph.add_node("gather_finalize_chain_subtask", bind(gather_finalize_chain_subtask))
    graph.add_edge(START, "gather_chain_investigate_subtask")
    graph.add_conditional_edges(
        "gather_chain_investigate_subtask",
        route_after_gather_chain_investigation,
        {
            "gather_chain_critic_subtask": "gather_chain_critic_subtask",
            "gather_finalize_chain_subtask": "gather_finalize_chain_subtask",
        },
    )
    graph.add_conditional_edges(
        "gather_chain_critic_subtask",
        route_after_gather_chain_critic,
        {
            "gather_chain_investigate_subtask": "gather_chain_investigate_subtask",
            "gather_finalize_chain_subtask": "gather_finalize_chain_subtask",
        },
    )
    graph.add_edge("gather_finalize_chain_subtask", END)
    return graph.compile()


def build_gather_graph(backends: dict[str, str] | None = None):
    graph: StateGraph = StateGraph(GatherState)

    def bind(fn):
        return partial(fn, backends=backends)

    graph.add_node("gather_analyze_attack_surface", bind(gather_analyze_attack_surface))
    graph.add_node("gather_plan_chains", bind(gather_plan_chains))
    graph.add_node("dispatch_gather_chains", bind(dispatch_gather_chains))
    graph.add_node("gather_chain_subtask", build_gather_chain_subtask_graph(backends))
    graph.add_node("gather_prepare_report_groups", bind(gather_prepare_report_groups))
    graph.add_node("summary", bind(gather_summary))
    graph.add_node("polish_report", polish_report)

    graph.add_edge(START, "gather_analyze_attack_surface")
    graph.add_edge("gather_analyze_attack_surface", "gather_plan_chains")
    graph.add_edge("gather_plan_chains", "dispatch_gather_chains")
    graph.add_conditional_edges("dispatch_gather_chains", dispatch_all_gather_chains)
    graph.add_edge("gather_chain_subtask", "gather_prepare_report_groups")
    graph.add_edge("gather_prepare_report_groups", "summary")
    graph.add_edge("summary", "polish_report")
    graph.add_edge("polish_report", END)
    return graph.compile()


def run_gather(
    *,
    manifest: dict[str, Any],
    workspace_root: str,
    task_id: str | None = None,
    backends: dict[str, str] | None = None,
    min_critic_skills: int = 2,
    role_lang: str = "en",
    agent_configs: dict[str, dict[str, Any]] | None = None,
    common_focus: str = "",
    top_K: dict[str, int] | None = None,
    gather_config: dict[str, Any] | None = None,
    max_concurrency: int = 8,
) -> GatherState:
    state = prepare_gather_state(
        manifest,
        workspace_root=workspace_root,
        task_id=task_id,
        role_lang=role_lang,
        agent_configs=agent_configs,
        common_focus=common_focus,
        top_K=top_K,
        gather_config=gather_config,
        min_critic_skills=min_critic_skills,
    )
    config = langfuse_config(
        run_name=f"zeromdash:{state['task_id']}",
        metadata={
            "scan_mode": "gather",
            "scenario_name": state.get("scenario_name", ""),
            "manifest_hash": state.get("manifest_hash", ""),
            "input_lock_hash": state.get("input_lock_hash", ""),
            "target_ids": json.dumps(
                [item.get("target_id") for item in state.get("gather_targets") or []],
                ensure_ascii=False,
            ),
            "max_concurrency": str(max_concurrency),
        },
    )
    config = dict(config or {})
    config["max_concurrency"] = max_concurrency
    final = build_gather_graph(backends).invoke(state, config=config or None)
    final["gather_evidence_count"] = len(final.get("gather_evidence_pool") or [])
    final["cross_target_flow_count"] = len(
        (final.get("cross_target_registry") or {}).get("data_flows") or []
    )
    # Full evidence and topology remain in hashed workspace artifacts. Keeping
    # them out of final_state.json avoids duplicating potentially large payloads.
    final.pop("gather_evidence_pool", None)
    final.pop("cross_target_registry", None)
    return final


__all__ = ["build_gather_chain_subtask_graph", "build_gather_graph", "run_gather"]
