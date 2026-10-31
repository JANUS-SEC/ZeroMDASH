"""LangGraph wiring for ZeroMDASH.

Top-level edges (left half):

    START -> fetch_target_repo
        -- failure / empty repo after retries --> END
        -- success --> prepare_scan_scope
        -- scope success --> search_spec
                  --> search_fuzz_driver
                  --> search_similar_software --(conditional Send)--> [N x search_similar_history]
                  --> search_target_history
    {spec, fuzz, sim_history, target_history} => search_new_feature
        -> analyze_attack_surface

`--disable-target-history` skips `search_target_history` and
`plan_by_vuln_patch`; the attack-surface barrier and planner barrier drop
those nodes the same way `--disable-spec` drops spec nodes.

Per-bucket fan-out (right half):

    analyze_attack_surface
        -> plan_by_spec         --(conditional Send)--> [N x investigate_subtask]
        -> plan_by_vuln_similar --(conditional Send)--> [M x investigate_subtask]
        -> plan_by_vuln_patch   --(conditional Send)--> [K x investigate_subtask]
        -> plan_by_new_feature  --(conditional Send)--> [F x investigate_subtask]

Each subtask graph runs an Agent-Native hypothesis-set loop:

    investigate_subtask -> critic_subtask
        -- "revise"            --> investigate_subtask   (FEEDBACK edge)
        -- package coverage closed --> finalize_subtask
           (except first-iteration no-finding, which gets one revise pass)
        -- iteration >= max    --> finalize_subtask

`finalize_subtask` writes zero or more per-hypothesis Findings into the correct
bucket on the parent state (via operator.add). All subtask buckets converge to:

    materialize_chain_pool -> plan_chains -> ... -> summary -> polish_report -> END
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from functools import partial
from pathlib import Path
from typing import Any

from langgraph.graph import END, START, StateGraph

from zeromdash.agents import langfuse_config
from zeromdash import nodes
from zeromdash.state import (
    ChainSubtaskInputState,
    ChainSubtaskOutputState,
    ChainSubtaskState,
    ZeroMDASHState,
    SubtaskInputState,
    SubtaskOutputState,
    SubtaskState,
)
from zeromdash.workspace import Workspace
from zeromdash.nodes.core.result_artifacts import (
    active_subtask_result_payloads,
    append_finalized_result_state,
    declared_package_ids,
    primitive_has_package_source,
)


def build_graph(
    backends: dict[str, str] | None = None,
    disabled_nodes: set[str] | None = None,
    till_node: str | None = None,
    poc_enabled: bool = False,
):
    """Construct the ZeroMDASH LangGraph.

    `backends` maps node names to any registered agent runtime, such as
    ``codex``, ``claude_code``, or ``traex``. See
    ``zeromdash.nodes.DEFAULT_BACKENDS`` for the full set of overridable nodes.

    `disabled_nodes` skips the named nodes and drops them from the
    attack-surface / planner barriers. ``--disable-spec`` passes
    ``{"search_spec", "plan_by_spec"}``; skipping ``plan_by_spec`` also
    leaves the spec bucket without subtasks, so it does not run either.

    `till_node` can stop the graph after attack-surface analysis ("analyze")
    or after all enabled planners have materialized plan JSON ("plan").
    """
    if till_node not in {None, "analyze", "plan", "summary"}:
        raise ValueError(f"unknown till_node: {till_node!r}")
    disabled = set(disabled_nodes or [])
    g: StateGraph = StateGraph(ZeroMDASHState)

    def _bind(fn):
        return partial(fn, backends=backends)

    # ---------------- gather (left half) ----------------
    g.add_node("fetch_target_repo",       _bind(nodes.fetch_target_repo))
    g.add_node("prepare_scan_scope",      _bind(nodes.prepare_scan_scope))
    if "search_spec" not in disabled:
        g.add_node("search_spec",         _bind(nodes.search_spec))
    g.add_node("search_fuzz_driver",      _bind(nodes.search_fuzz_driver))
    g.add_node("search_similar_software", _bind(nodes.search_similar_software))
    g.add_node("search_similar_history",  _bind(nodes.search_similar_history))
    if "search_target_history" not in disabled:
        g.add_node("search_target_history", _bind(nodes.search_target_history))
    if "search_new_feature" not in disabled:
        g.add_node("search_new_feature", _bind(nodes.search_new_feature))

    # ---------------- fuse / surface --------------------
    g.add_node("analyze_attack_surface",  _bind(nodes.analyze_attack_surface))

    if till_node != "analyze":
        # ---------------- planners --------------------------
        if "plan_by_spec" not in disabled:
            g.add_node("plan_by_spec",        _bind(nodes.plan_by_spec))
        g.add_node("plan_by_vuln_similar",    _bind(nodes.plan_by_vuln_similar))
        if "plan_by_vuln_patch" not in disabled:
            g.add_node("plan_by_vuln_patch",  _bind(nodes.plan_by_vuln_patch))
        if "plan_by_new_feature" not in disabled:
            g.add_node("plan_by_new_feature", _bind(nodes.plan_by_new_feature))

    if till_node in {None, "summary"}:
        # ---------------- subtask dispatch / loop -----------
        g.add_node("dispatch_subtasks",     _bind(nodes.dispatch_subtasks))

        # Compile the investigate/critic/finalize loop as a nested graph so
        # per-subtask scratch keys (iteration, investigation, review, ...) stay
        # isolated and only final Finding buckets merge back into the parent graph.
        g.add_node("subtask", build_subtask_graph(backends))
        g.add_node("materialize_chain_pool", _bind(nodes.materialize_chain_pool))
        g.add_node("plan_chains", _bind(nodes.plan_chains))
        g.add_node("dispatch_chains", _bind(nodes.dispatch_chains))
        g.add_node("chain_subtask", build_chain_subtask_graph(backends))
        g.add_node("prepare_report_groups", _bind(nodes.prepare_report_groups))

        # ---------------- summary / polish ------------------
        g.add_node("summary",                 _bind(nodes.summary))
        if till_node is None:
            g.add_node("polish_report",       nodes.polish_report)
            if poc_enabled:
                g.add_node("poc_gen",         _bind(nodes.poc_gen))
    elif till_node == "plan":
        g.add_node("finish_plan", lambda state: {"stopped_at": "plan"})

    # ============================== EDGES =============================
    g.add_edge(START, "fetch_target_repo")

    # left half — kicked off in parallel only if fetch_target_repo succeeded.
    # If repo materialization fails after retries, stop before every downstream
    # node to avoid analysing an empty source tree.
    g.add_conditional_edges("fetch_target_repo", nodes.route_after_fetch_target_repo)
    g.add_conditional_edges("prepare_scan_scope", nodes.route_after_prepare_scan_scope)
    g.add_conditional_edges("search_similar_software", nodes.dispatch_similar_history)

    # red lines: attack-surface depends on spec + fuzz + writeups. Use a
    # multi-source edge as a barrier; separate edges would trigger the analyzer
    # once per completed predecessor and duplicate all downstream fan-out work.
    # Drop disabled gather nodes so the barrier only waits for nodes that run.
    gather_barrier = [
        n for n in (
            "search_spec",
            "search_fuzz_driver",
            "search_similar_history",
            "search_target_history",
        )
        if n not in disabled
    ]
    if "search_new_feature" not in disabled:
        g.add_edge(gather_barrier, "search_new_feature")
        g.add_edge("search_new_feature", "analyze_attack_surface")
    else:
        g.add_edge(gather_barrier, "analyze_attack_surface")

    if till_node == "analyze":
        g.add_edge("analyze_attack_surface", END)
        return g.compile()

    # planners run after attack-surface analysis
    planner_nodes = [
        n for n in ("plan_by_spec", "plan_by_vuln_similar", "plan_by_vuln_patch", "plan_by_new_feature")
        if n not in disabled
    ]
    for planner in planner_nodes:
        g.add_edge("analyze_attack_surface", planner)

    if till_node == "plan":
        g.add_edge(planner_nodes, "finish_plan")
        g.add_edge("finish_plan", END)
        return g.compile()

    # ---- dynamic fan-out: after all planners finish, emit one Send per subtask ----
    # Use a planner barrier so subtasks are dispatched once from a complete
    # view of all buckets. If all planners return zero subtasks, dispatch_all
    # routes directly to summary so the workflow still produces an output.
    g.add_edge(planner_nodes, "dispatch_subtasks")
    g.add_conditional_edges("dispatch_subtasks", nodes.dispatch_all)

    # The nested subtask graph returns aggregated findings and primitives.
    # A second barrier materializes the primitive pool before chain planning.
    g.add_edge("subtask", "materialize_chain_pool")
    g.add_edge("materialize_chain_pool", "plan_chains")
    g.add_edge("plan_chains", "dispatch_chains")
    g.add_conditional_edges("dispatch_chains", nodes.dispatch_all_chains)
    g.add_edge("chain_subtask", "prepare_report_groups")
    g.add_edge("prepare_report_groups", "summary")

    if till_node == "summary":
        g.add_edge("summary", END)
    else:
        g.add_edge("summary", "polish_report")
        if poc_enabled:
            g.add_edge("polish_report", "poc_gen")
            g.add_edge("poc_gen", END)
        else:
            g.add_edge("polish_report", END)
    return g.compile()


def build_subtask_graph(backends: dict[str, str] | None = None):
    """Construct one isolated investigate -> critic feedback loop."""
    g: StateGraph = StateGraph(
        SubtaskState,
        input_schema=SubtaskInputState,
        output_schema=SubtaskOutputState,
    )

    def _bind(fn):
        return partial(fn, backends=backends)

    def _route_after_critic(state):
        return nodes.route_after_critic(state)

    def _route_after_investigation(state):
        return nodes.route_after_investigation(state)

    g.add_node("investigate_subtask", _bind(nodes.investigate_subtask))
    g.add_node("critic_subtask", _bind(nodes.critic_subtask))
    g.add_node("finalize_subtask", _bind(nodes.finalize_subtask))

    g.add_edge(START, "investigate_subtask")
    g.add_conditional_edges(
        "investigate_subtask",
        _route_after_investigation,
        {
            "critic_subtask": "critic_subtask",
            "__end__": END,
        },
    )
    g.add_conditional_edges(
        "critic_subtask",
        _route_after_critic,
        {
            "investigate_subtask": "investigate_subtask",
            "finalize_subtask": "finalize_subtask",
        },
    )
    g.add_edge("finalize_subtask", END)
    return g.compile()


def build_subtask_restore_graph(backends: dict[str, str] | None = None, poc_enabled: bool = False):
    """Construct the restore graph that starts at planner fan-out."""
    g: StateGraph = StateGraph(ZeroMDASHState)

    def _bind(fn):
        return partial(fn, backends=backends)

    g.add_node("dispatch_subtasks", _bind(nodes.dispatch_subtasks))
    g.add_node("subtask", build_subtask_graph(backends))
    g.add_node("materialize_chain_pool", _bind(nodes.materialize_chain_pool))
    g.add_node("plan_chains", _bind(nodes.plan_chains))
    g.add_node("dispatch_chains", _bind(nodes.dispatch_chains))
    g.add_node("chain_subtask", build_chain_subtask_graph(backends))
    g.add_node("prepare_report_groups", _bind(nodes.prepare_report_groups))
    g.add_node("summary", _bind(nodes.summary))
    g.add_node("polish_report", nodes.polish_report)

    g.add_edge(START, "dispatch_subtasks")
    g.add_conditional_edges("dispatch_subtasks", nodes.dispatch_all)
    g.add_edge("subtask", "materialize_chain_pool")
    g.add_edge("materialize_chain_pool", "plan_chains")
    g.add_edge("plan_chains", "dispatch_chains")
    g.add_conditional_edges("dispatch_chains", nodes.dispatch_all_chains)
    g.add_edge("chain_subtask", "prepare_report_groups")
    g.add_edge("prepare_report_groups", "summary")
    g.add_edge("summary", "polish_report")
    if poc_enabled:
        g.add_node("poc_gen", partial(nodes.poc_gen, backends=backends))
        g.add_edge("polish_report", "poc_gen")
        g.add_edge("poc_gen", END)
    else:
        g.add_edge("polish_report", END)
    return g.compile()


def build_chain_subtask_graph(backends: dict[str, str] | None = None):
    """Construct one isolated chain investigate -> critic feedback loop."""
    g: StateGraph = StateGraph(
        ChainSubtaskState,
        input_schema=ChainSubtaskInputState,
        output_schema=ChainSubtaskOutputState,
    )

    def _bind(fn):
        return partial(fn, backends=backends)

    def _route_after_chain_investigation(state):
        return nodes.route_after_chain_investigation(state)

    def _route_after_chain_critic(state):
        return nodes.route_after_chain_critic(state)

    g.add_node("chain_investigate_subtask", _bind(nodes.chain_investigate_subtask))
    g.add_node("chain_critic_subtask", _bind(nodes.chain_critic_subtask))
    g.add_node("finalize_chain_subtask", _bind(nodes.finalize_chain_subtask))

    g.add_edge(START, "chain_investigate_subtask")
    g.add_conditional_edges(
        "chain_investigate_subtask",
        _route_after_chain_investigation,
        {
            "chain_critic_subtask": "chain_critic_subtask",
            "__end__": END,
        },
    )
    g.add_conditional_edges(
        "chain_critic_subtask",
        _route_after_chain_critic,
        {
            "chain_investigate_subtask": "chain_investigate_subtask",
            "finalize_chain_subtask": "finalize_chain_subtask",
        },
    )
    g.add_edge("finalize_chain_subtask", END)
    return g.compile()


def build_chain_restore_graph(backends: dict[str, str] | None = None, poc_enabled: bool = False):
    """Construct the restore graph that starts at chain planning."""
    g: StateGraph = StateGraph(ZeroMDASHState)

    def _bind(fn):
        return partial(fn, backends=backends)

    g.add_node("materialize_chain_pool", _bind(nodes.materialize_chain_pool))
    g.add_node("plan_chains", _bind(nodes.plan_chains))
    g.add_node("dispatch_chains", _bind(nodes.dispatch_chains))
    g.add_node("chain_subtask", build_chain_subtask_graph(backends))
    g.add_node("prepare_report_groups", _bind(nodes.prepare_report_groups))
    g.add_node("summary", _bind(nodes.summary))
    g.add_node("polish_report", nodes.polish_report)

    g.add_edge(START, "materialize_chain_pool")
    g.add_edge("materialize_chain_pool", "plan_chains")
    g.add_edge("plan_chains", "dispatch_chains")
    g.add_conditional_edges("dispatch_chains", nodes.dispatch_all_chains)
    g.add_edge("chain_subtask", "prepare_report_groups")
    g.add_edge("prepare_report_groups", "summary")
    g.add_edge("summary", "polish_report")
    if poc_enabled:
        g.add_node("poc_gen", partial(nodes.poc_gen, backends=backends))
        g.add_edge("polish_report", "poc_gen")
        g.add_edge("poc_gen", END)
    else:
        g.add_edge("polish_report", END)
    return g.compile()


def build_selected_chain_restore_graph(backends: dict[str, str] | None = None):
    """Run selected restored chain candidates and collect status without summary."""
    g: StateGraph = StateGraph(ZeroMDASHState)

    def _bind(fn):
        return partial(fn, backends=backends)

    g.add_node("materialize_chain_pool", _bind(nodes.materialize_chain_pool))
    g.add_node("plan_chains", _bind(nodes.plan_chains))
    g.add_node("dispatch_chains", _bind(nodes.dispatch_chains))
    g.add_node("chain_subtask", build_chain_subtask_graph(backends))
    g.add_node("collect_selected_chain_statuses", nodes.collect_selected_chain_statuses)

    g.add_edge(START, "materialize_chain_pool")
    g.add_edge("materialize_chain_pool", "plan_chains")
    g.add_edge("plan_chains", "dispatch_chains")
    g.add_conditional_edges("dispatch_chains", nodes.dispatch_selected_chains)
    g.add_edge("chain_subtask", "collect_selected_chain_statuses")
    g.add_edge("collect_selected_chain_statuses", END)
    return g.compile()


def build_selected_subtask_restore_graph(
    backends: dict[str, str] | None = None,
):
    """Run selected restored subtasks and collect status without summary."""
    g: StateGraph = StateGraph(ZeroMDASHState)

    def _bind(fn):
        return partial(fn, backends=backends)

    g.add_node("dispatch_subtasks", _bind(nodes.dispatch_subtasks))
    g.add_node("subtask", build_subtask_graph(backends))
    g.add_node(
        "collect_selected_subtask_statuses",
        nodes.collect_selected_subtask_statuses,
    )

    g.add_edge(START, "dispatch_subtasks")
    g.add_conditional_edges("dispatch_subtasks", nodes.dispatch_selected)
    g.add_edge("subtask", "collect_selected_subtask_statuses")
    g.add_edge("collect_selected_subtask_statuses", END)
    return g.compile()


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except OSError as exc:
        raise ValueError(f"required restore file is unreadable: {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"required restore file is not valid JSON: {path}: {exc}") from exc


def _load_plan_file(path: Path, bucket: str) -> list[dict[str, Any]]:
    payload = _read_json(path)
    if not isinstance(payload, list):
        raise ValueError(f"required restore plan is not a JSON array: {path}")
    tasks: list[dict[str, Any]] = []
    for i, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ValueError(f"invalid subtask at {path}:{i}: expected object")
        task = dict(item)
        task.setdefault("bucket", bucket)
        task.setdefault("hints", {})
        if not task.get("id"):
            raise ValueError(f"invalid subtask at {path}:{i}: missing id")
        tasks.append(task)
    return tasks


def _has_text(path: Path) -> bool:
    try:
        return path.is_file() and bool(path.read_text(encoding="utf-8", errors="ignore").strip())
    except OSError:
        return False


def _workspace_from_base(workspace_path: str | Path) -> Workspace:
    base = Path(workspace_path).expanduser().resolve()
    if not base.is_dir():
        raise ValueError(f"--start-from-subtask workspace does not exist: {base}")
    return Workspace.open(base.parent, base.name)


def _similar_writeup_dirs(ws: Workspace) -> list[str]:
    if not ws.similar.is_dir():
        return []
    return [
        str(path)
        for path in sorted(ws.similar.glob("*/writeup"))
        if path.is_dir()
    ]


def _subtask_res_payloads(ws: Workspace, *, require_findings: bool) -> list[tuple[Path, dict[str, Any]]]:
    result_dirs = list(ws.subtask_result_dirs())
    if not result_dirs:
        raise ValueError(
            "restore workspace is missing subtask results directory: "
            f"{ws.log_path('subtask_res')} (legacy fallback: {ws.log_path('review_res')})"
        )
    payloads = active_subtask_result_payloads(ws)
    loaded_findings = sum(
        isinstance(payload.get("finding"), dict)
        for _, payload in payloads
    )
    if require_findings and loaded_findings == 0:
        raise ValueError(
            "restore workspace has no findings in subtask results: "
            + ", ".join(str(path) for path in result_dirs)
        )
    return payloads


def _primitive_res_payloads(ws: Workspace) -> list[dict[str, Any]]:
    primitive_dir = ws.log_path("primitive_res")
    result_payloads = active_subtask_result_payloads(ws)
    package_ids = declared_package_ids(ws)
    primitives: list[dict[str, Any]] = []
    for path in sorted(primitive_dir.glob("*.json")) if primitive_dir.is_dir() else []:
        payload = _read_json(path)
        if isinstance(payload, dict) and not primitive_has_package_source(
            payload, package_ids
        ):
            primitives.append(payload)
    primitives.extend(
        primitive
        for _, payload in result_payloads
        if isinstance((primitive := payload.get("primitive")), dict)
    )
    return primitives


def _chain_findings_from_chain_res(ws: Workspace) -> list[dict[str, Any]]:
    chain_dir = ws.log_path("chain_res")
    if not chain_dir.is_dir():
        return []
    findings: list[dict[str, Any]] = []
    for path in sorted(chain_dir.glob("*.json")):
        payload = _read_json(path)
        if isinstance(payload, dict) and isinstance(payload.get("finding"), dict):
            findings.append(payload["finding"])
    return findings


def _chain_candidates_from_disk(ws: Workspace) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    plan = ws.resolve_state_path("chain_plan.json")
    if plan.is_file():
        payload = _read_json(plan)
        if isinstance(payload, dict) and isinstance(payload.get("chains"), list):
            candidates.extend(item for item in payload["chains"] if isinstance(item, dict))
        elif isinstance(payload, list):
            candidates.extend(item for item in payload if isinstance(item, dict))
    candidate_dir = ws.log_path("chain_candidates")
    if candidate_dir.is_dir():
        for path in sorted(candidate_dir.glob("*.json")):
            payload = _read_json(path)
            candidate = payload.get("candidate") if isinstance(payload, dict) else None
            if isinstance(candidate, dict):
                candidates.append(candidate)
    return candidates


def _report_groups_from_workspace(ws: Workspace) -> list[dict[str, Any]]:
    path = ws.log / "report_groups.json"
    if not path.is_file():
        return []
    payload = _read_json(path)
    if isinstance(payload, dict) and isinstance(payload.get("groups"), list):
        return [item for item in payload["groups"] if isinstance(item, dict)]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def _completed_subtask_ids_from_subtask_res(ws: Workspace) -> list[str]:
    completed: set[str] = set()
    for path, payload in _subtask_res_payloads(ws, require_findings=False):
        package_id = str(payload.get("package_id") or "").strip()
        if payload.get("result_type") == "hypothesis_package" and package_id:
            completed.add(package_id)
            continue
        finding = payload.get("finding")
        if isinstance(finding, dict) and str(finding.get("subtask_id") or "").strip():
            # Atomic hypothesis artifacts are written before the package
            # manifest. Only the manifest marks the parent package complete.
            if str(finding.get("parent_subtask_id") or "").strip():
                continue
            completed.add(str(finding["subtask_id"]).strip())
        elif path.stem:
            completed.add(path.stem)
    return sorted(completed)


def _finding_buckets_from_subtask_res(
    ws: Workspace,
    *,
    require_findings: bool = True,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    restored = _subtask_state_from_subtask_res(
        ws,
        require_findings=require_findings,
    )
    return (
        restored.get("spec_findings", []),
        restored.get("vuln_candidates", []),
        restored.get("patch_findings", []),
        restored.get("feature_findings", []),
    )


def _subtask_state_from_subtask_res(
    ws: Workspace,
    *,
    require_findings: bool = True,
) -> dict[str, list[dict[str, Any]]]:
    restored: dict[str, list[dict[str, Any]]] = {}
    payloads = _subtask_res_payloads(ws, require_findings=require_findings)
    for _, payload in payloads:
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if not isinstance(finding, dict):
            continue
        outcome_type = str(
            payload.get("outcome_type") or finding.get("outcome_type") or ""
        ).strip()
        append_finalized_result_state(
            restored,
            finding=finding,
            outcome_type=outcome_type,
            primitive=payload.get("primitive"),
            legacy_unclassified=not outcome_type,
        )
    return restored


def _filter_findings_by_subtask_ids(
    findings: list[dict[str, Any]],
    selected_ids: set[str],
) -> list[dict[str, Any]]:
    return [
        finding
        for finding in findings
        if str(
            finding.get("parent_subtask_id")
            or finding.get("subtask_id")
            or ""
        ).strip() in selected_ids
    ]


def _normalize_selected_subtask_id(value: str) -> str:
    raw = str(value or "").strip().lower()
    match = re.fullmatch(r"(spec|vuln|patch|feat|feature)-?(\d+)", raw)
    if not match:
        return raw
    prefix, number = match.groups()
    if prefix == "feature":
        prefix = "feat"
    return f"{prefix}-{int(number):03d}"


def _select_restore_subtasks(
    state: ZeroMDASHState,
    selected_subtask_ids: list[str],
    selected_subtask_log_dir: str | Path | None = None,
) -> ZeroMDASHState:
    requested: list[str] = []
    for value in selected_subtask_ids:
        normalized = _normalize_selected_subtask_id(value)
        if normalized and normalized not in requested:
            requested.append(normalized)
    if not requested:
        raise ValueError("--select-subtask-to-run requires at least one subtask id")

    buckets = {
        "spec_subtasks": list(state.get("spec_subtasks") or []),
        "vuln_subtasks": list(state.get("vuln_subtasks") or []),
        "patch_subtasks": list(state.get("patch_subtasks") or []),
        "feature_subtasks": list(state.get("feature_subtasks") or []),
    }
    by_id = {
        str(subtask.get("id") or ""): subtask
        for subtasks in buckets.values()
        for subtask in subtasks
    }
    missing = [subtask_id for subtask_id in requested if subtask_id not in by_id]
    if missing:
        raise ValueError(
            "selected subtask id(s) not found in planner outputs: "
            + ", ".join(missing)
        )

    selected = set(requested)
    for key, subtasks in buckets.items():
        state[key] = [
            subtask
            for subtask in subtasks
            if str(subtask.get("id") or "") in selected
        ]
    state["selected_subtask_ids"] = requested
    state["selected_subagent_ids"] = requested
    state["completed_subtask_ids"] = []
    state["spec_findings"] = []
    state["vuln_candidates"] = []
    state["patch_findings"] = []
    state["feature_findings"] = []

    ws = Workspace.open(state["workspace_root"], state["task_id"])
    if selected_subtask_log_dir:
        output_dir = Path(selected_subtask_log_dir).expanduser()
        if not output_dir.is_absolute():
            output_dir = (ws.base / output_dir).resolve()
            try:
                output_dir.relative_to(ws.base.resolve())
            except ValueError as exc:
                raise ValueError(
                    "relative --select-subtask-to-run-log-dir must stay "
                    f"inside the workspace: {output_dir}"
                ) from exc
        else:
            output_dir = output_dir.resolve()
    else:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_dir = ws.log / f"selected_temp_{timestamp}"
        suffix = 1
        while output_dir.exists():
            output_dir = ws.log / f"selected_temp_{timestamp}_{suffix}"
            suffix += 1
    if output_dir.exists():
        raise ValueError(
            "selected subtask log directory already exists; choose a new "
            f"--select-subtask-to-run-log-dir: {output_dir}"
        )
    output_dir.mkdir(parents=True)
    for subdir in ("attempts", "investigations", "critic_reviews", "results"):
        (output_dir / subdir).mkdir()
    state["selected_subtask_log_dir"] = str(output_dir)
    state["selected_subagent_log_dir"] = str(output_dir)
    return state


def _restore_state_from_workspace(
    workspace_path: str | Path,
    *,
    max_iterations: int,
    min_critic_skills: int,
    common_focus: str = "",
    agent_configs: nodes.AgentConfigs | None = None,
    agent_config_task_types: nodes.AgentConfigTaskTypes | None = None,
    top_K: dict[str, int] | None = None,
    chain_config: dict[str, Any] | None = None,
    disabled_nodes: set[str] | None = None,
    extra_state: dict[str, Any] | None = None,
) -> ZeroMDASHState:
    ws = _workspace_from_base(workspace_path)
    base = ws.base
    if not (base / "workspace.json").is_file():
        raise ValueError(f"required restore metadata is missing: {base / 'workspace.json'}")

    prior = {}
    final_state_path = base / "final_state.json"
    if final_state_path.is_file():
        payload = _read_json(final_state_path)
        if isinstance(payload, dict):
            prior = payload

    repo_path = ws.main_path("repo")
    if not nodes._repo_has_materialized_source(repo_path):
        raise ValueError(f"restore workspace has no materialized source tree: {repo_path}")

    attack_surface = ws.main_path("attack_surface") / "attack_surface.md"
    if not _has_text(attack_surface):
        raise ValueError(f"restore workspace is missing attack-surface report: {attack_surface}")
    domain_registry_path = ws.main_path("attack_surface") / "domain_invariant_registry.json"
    domain_registry = nodes.read_domain_registry(
        domain_registry_path,
        target=str(prior.get("target") or ws.target or ws.task_id),
    )

    selected_disabled_nodes = set(prior.get("disabled_nodes") or [])
    selected_disabled_nodes.update(disabled_nodes or set())

    spec_subtasks = [] if "plan_by_spec" in selected_disabled_nodes else _load_plan_file(ws.resolve_state_path("plan_by_spec.json"), "spec")
    vuln_subtasks = _load_plan_file(ws.resolve_state_path("plan_by_vuln.json"), "vuln")
    patch_subtasks = (
        []
        if "plan_by_vuln_patch" in selected_disabled_nodes
        else _load_plan_file(ws.resolve_state_path("plan_by_patch.json"), "patch_miss")
    )
    feature_plan = ws.resolve_state_path("plan_by_feature.json")
    feature_subtasks = (
        []
        if "plan_by_new_feature" in selected_disabled_nodes or not feature_plan.is_file()
        else _load_plan_file(feature_plan, "feature")
    )

    spec_doc = ws.main_path("spec") / "spec.md"
    if spec_subtasks and not _has_text(spec_doc):
        raise ValueError(f"restore workspace has spec subtasks but no spec report: {spec_doc}")

    scope_path = ws.main_path("scope") / "scope.json"
    if scope_path.is_file():
        scope_payload = _read_json(scope_path)
        scan_scope = scope_payload if isinstance(scope_payload, dict) else {}
    else:
        scan_scope = {
            "mode": "full",
            "repo_path": str(repo_path),
            "changed_files": [],
            "policy": {"finding_must_intersect_diff": False},
        }

    selected_agent_configs = dict(agent_configs or prior.get("agent_configs") or {})
    selected_top_K = dict(top_K or prior.get("top_K") or {})
    selected_chain_config = dict(chain_config or prior.get("chain_config") or {})
    completed_subtask_ids = _completed_subtask_ids_from_subtask_res(ws)
    restored_subtasks = _subtask_state_from_subtask_res(
        ws,
        require_findings=False,
    )
    spec_findings = restored_subtasks.get("spec_findings", [])
    vuln_candidates = restored_subtasks.get("vuln_candidates", [])
    patch_findings = restored_subtasks.get("patch_findings", [])
    feature_findings = restored_subtasks.get("feature_findings", [])
    observations = restored_subtasks.get("observations", [])
    chain_findings = _chain_findings_from_chain_res(ws)
    report_groups = _report_groups_from_workspace(ws)
    state: ZeroMDASHState = {
        "target": str(prior.get("target") or ws.target or ws.task_id),
        "target_repos": list(prior.get("target_repos") or []),
        "common_focus": common_focus or str(prior.get("common_focus") or prior.get("focus") or ""),
        "role_lang": str(prior.get("role_lang") or ws.role_lang),
        "task_id": ws.task_id,
        "workspace_root": str(ws.root),
        "repo_path": str(repo_path),
        "target_repos_path": str(ws.main_path("repos") / "_manifest.json"),
        "scan_mode": str(scan_scope.get("mode") or "full"),
        "diff_file": "",
        "scope_path": str(scope_path),
        "scan_scope": scan_scope,
        "spec_doc": str(spec_doc),
        "attack_surface": str(attack_surface),
        "domain_registry_path": str(domain_registry_path),
        "domain_registry": domain_registry,
        "target_patch_manifest": str(ws.main_path("patch") / "_patch_commits.json"),
        "similar_writeups": _similar_writeup_dirs(ws),
        "max_iterations": int(prior.get("max_iterations") or max_iterations),
        "min_critic_skills": int(prior.get("min_critic_skills") or min_critic_skills),
        "agent_configs": selected_agent_configs,
        "agent_config_task_types": dict(agent_config_task_types or prior.get("agent_config_task_types") or {}),
        "top_K": selected_top_K,
        "chain_config": selected_chain_config,
        "disabled_nodes": sorted(selected_disabled_nodes),
        "spec_subtasks": spec_subtasks,
        "vuln_subtasks": vuln_subtasks,
        "patch_subtasks": patch_subtasks,
        "feature_subtasks": feature_subtasks,
        "completed_subtask_ids": completed_subtask_ids,
        "spec_findings": spec_findings,
        "vuln_candidates": vuln_candidates,
        "patch_findings": patch_findings,
        "feature_findings": feature_findings,
        "observations": observations,
        "confirmed_primitives": _primitive_res_payloads(ws),
        "chain_findings": chain_findings,
        "report_groups": report_groups,
        "report_groups_path": str(ws.log / "report_groups.json") if report_groups else "",
        **(extra_state or {}),
    }
    selected_by_bucket, _ = nodes._select_dispatch_subtasks(state)
    selected_ids = {
        str(subtask.get("id") or "").strip()
        for subtasks in selected_by_bucket.values()
        for subtask in subtasks
        if str(subtask.get("id") or "").strip()
    }
    state["completed_subtask_ids"] = [
        subtask_id for subtask_id in completed_subtask_ids if subtask_id in selected_ids
    ]
    state["spec_findings"] = _filter_findings_by_subtask_ids(spec_findings, selected_ids)
    state["vuln_candidates"] = _filter_findings_by_subtask_ids(vuln_candidates, selected_ids)
    state["patch_findings"] = _filter_findings_by_subtask_ids(patch_findings, selected_ids)
    state["feature_findings"] = _filter_findings_by_subtask_ids(feature_findings, selected_ids)
    state["observations"] = _filter_findings_by_subtask_ids(observations, selected_ids)
    return state


def _summary_state_from_workspace(
    workspace_path: str | Path,
    *,
    common_focus: str = "",
    agent_configs: nodes.AgentConfigs | None = None,
    agent_config_task_types: nodes.AgentConfigTaskTypes | None = None,
    extra_state: dict[str, Any] | None = None,
    require_findings: bool = True,
) -> ZeroMDASHState:
    ws = _workspace_from_base(workspace_path)
    base = ws.base
    if not (base / "workspace.json").is_file():
        raise ValueError(f"required restore metadata is missing: {base / 'workspace.json'}")

    prior = {}
    final_state_path = base / "final_state.json"
    if final_state_path.is_file():
        payload = _read_json(final_state_path)
        if isinstance(payload, dict):
            prior = payload

    repo_path = ws.main_path("repo")
    if not nodes._repo_has_materialized_source(repo_path):
        raise ValueError(f"restore workspace has no materialized source tree: {repo_path}")

    attack_surface = ws.main_path("attack_surface") / "attack_surface.md"
    if not _has_text(attack_surface):
        raise ValueError(f"restore workspace is missing attack-surface report: {attack_surface}")
    domain_registry_path = ws.main_path("attack_surface") / "domain_invariant_registry.json"
    domain_registry = nodes.read_domain_registry(
        domain_registry_path,
        target=str(prior.get("target") or ws.target or ws.task_id),
    )

    scope_path = ws.main_path("scope") / "scope.json"
    if scope_path.is_file():
        scope_payload = _read_json(scope_path)
        scan_scope = scope_payload if isinstance(scope_payload, dict) else {}
    else:
        scan_scope = {
            "mode": "full",
            "repo_path": str(repo_path),
            "changed_files": [],
            "policy": {"finding_must_intersect_diff": False},
        }

    restored_subtasks = _subtask_state_from_subtask_res(ws, require_findings=require_findings)
    chain_findings = _chain_findings_from_chain_res(ws)
    report_groups = _report_groups_from_workspace(ws)
    return {
        "target": str(prior.get("target") or ws.target or ws.task_id),
        "target_repos": list(prior.get("target_repos") or []),
        "common_focus": common_focus or str(prior.get("common_focus") or prior.get("focus") or ""),
        "role_lang": str(prior.get("role_lang") or ws.role_lang),
        "task_id": ws.task_id,
        "workspace_root": str(ws.root),
        "repo_path": str(repo_path),
        "target_repos_path": str(ws.main_path("repos") / "_manifest.json"),
        "scan_mode": str(scan_scope.get("mode") or "full"),
        "diff_file": "",
        "scope_path": str(scope_path),
        "scan_scope": scan_scope,
        "attack_surface": str(attack_surface),
        "domain_registry_path": str(domain_registry_path),
        "domain_registry": domain_registry,
        "target_patch_manifest": str(ws.main_path("patch") / "_patch_commits.json"),
        "agent_configs": dict(agent_configs or prior.get("agent_configs") or {}),
        "agent_config_task_types": dict(agent_config_task_types or prior.get("agent_config_task_types") or {}),
        "disabled_nodes": list(prior.get("disabled_nodes") or []),
        "spec_findings": restored_subtasks.get("spec_findings", []),
        "vuln_candidates": restored_subtasks.get("vuln_candidates", []),
        "patch_findings": restored_subtasks.get("patch_findings", []),
        "feature_findings": restored_subtasks.get("feature_findings", []),
        "observations": restored_subtasks.get("observations", []),
        "confirmed_primitives": _primitive_res_payloads(ws),
        "chain_findings": chain_findings,
        "report_groups": report_groups,
        "report_groups_path": str(ws.log / "report_groups.json") if report_groups else "",
        "summary": str(prior.get("summary") or ""),
        "summary_en": str(prior.get("summary_en") or ""),
        "summary_zh_CN": str(prior.get("summary_zh_CN") or ""),
        "gate_result": dict(prior.get("gate_result") or {}),
        "poc_results": list(prior.get("poc_results") or []),
        **(extra_state or {}),
    }


def _polish_report_state_from_workspace(
    workspace_path: str | Path,
    *,
    common_focus: str = "",
    agent_configs: nodes.AgentConfigs | None = None,
    agent_config_task_types: nodes.AgentConfigTaskTypes | None = None,
    extra_state: dict[str, Any] | None = None,
) -> ZeroMDASHState:
    ws = _workspace_from_base(workspace_path)
    base = ws.base
    if not (base / "workspace.json").is_file():
        raise ValueError(f"required restore metadata is missing: {base / 'workspace.json'}")

    prior = {}
    final_state_path = base / "final_state.json"
    if final_state_path.is_file():
        payload = _read_json(final_state_path)
        if isinstance(payload, dict):
            prior = payload
    if not ((base / "summary.en.md").is_file() or (base / "summary.zh_CN.md").is_file()):
        raise ValueError(
            "restore workspace is missing summary report files: "
            f"{base / 'summary.en.md'} or {base / 'summary.zh_CN.md'}"
        )

    return {
        "target": str(prior.get("target") or ws.target or ws.task_id),
        "target_repos": list(prior.get("target_repos") or []),
        "common_focus": common_focus or str(prior.get("common_focus") or prior.get("focus") or ""),
        "role_lang": str(prior.get("role_lang") or ws.role_lang),
        "task_id": ws.task_id,
        "workspace_root": str(ws.root),
        "repo_path": str(ws.main_path("repo")),
        "target_repos_path": str(ws.main_path("repos") / "_manifest.json"),
        "scan_mode": str(prior.get("scan_mode") or "full"),
        "agent_configs": dict(agent_configs or prior.get("agent_configs") or {}),
        "agent_config_task_types": dict(agent_config_task_types or prior.get("agent_config_task_types") or {}),
        "disabled_nodes": list(prior.get("disabled_nodes") or []),
        **(extra_state or {}),
    }


def _till_node_validation_errors(final: ZeroMDASHState, till_node: str | None) -> list[str]:
    if till_node is None:
        return []
    ws = Workspace.open(final["workspace_root"], final["task_id"])
    if till_node == "analyze":
        attack_surface = ws.main_path("attack_surface") / "attack_surface.md"
        registry_path = ws.main_path("attack_surface") / "domain_invariant_registry.json"
        registry = nodes.read_domain_registry(registry_path, target=ws.target)
        errors: list[str] = []
        if not _has_text(attack_surface):
            errors.append(f"[till-node/analyze] missing output: {attack_surface}")
        if registry.get("status") == "legacy_unavailable":
            errors.append(f"[till-node/analyze] missing or invalid output: {registry_path}")
        return errors
    if till_node == "plan":
        disabled = set(final.get("disabled_nodes") or [])
        required = [("plan_by_vuln.json", "vuln")]
        if "plan_by_spec" not in disabled:
            required.append(("plan_by_spec.json", "spec"))
        if "plan_by_vuln_patch" not in disabled:
            required.append(("plan_by_patch.json", "patch_miss"))
        if "plan_by_new_feature" not in disabled:
            required.append(("plan_by_feature.json", "feature"))
        errors: list[str] = []
        for filename, bucket in required:
            path = ws.resolve_state_path(filename)
            try:
                _load_plan_file(path, bucket)
            except ValueError as exc:
                errors.append(f"[till-node/plan] {exc}")
        return errors
    if till_node == "summary":
        errors = []
        for filename in ("summary.en.md", "summary.zh_CN.md", "summary.md"):
            path = ws.base / filename
            if not _has_text(path):
                errors.append(f"[till-node/summary] missing output: {path}")
        return errors
    return [f"[till-node] unknown value: {till_node}"]


def run(
    target: str,
    workspace_root: str,
    task_id: str | None = None,
    backends: dict[str, str] | None = None,
    max_iterations: int = 3,
    min_critic_skills: int = 2,
    common_focus: str = "",
    scan_mode: str = "full",
    diff_file: str = "",
    diff_git: str = "",
    fetch_target_repo_focus: str = "",
    search_fuzz_driver_focus: str = "",
    search_similar_software_focus: str = "",
    search_target_history_focus: str = "",
    search_new_feature_focus: str = "",
    analyze_attack_surface_focus: str = "",
    summary_focus: str = "",
    role_lang: str = "en",
    agent_configs: nodes.AgentConfigs | None = None,
    agent_config_task_types: nodes.AgentConfigTaskTypes | None = None,
    preset_attack_surface_path: str | None = None,
    target_repos: list[dict[str, str]] | None = None,
    top_K: dict[str, int] | None = None,
    chain_config: dict[str, Any] | None = None,
    max_concurrency: int = 8,
    disabled_nodes: set[str] | None = None,
    till_node: str | None = None,
    extra_state: dict[str, Any] | None = None,
    poc_config: dict[str, Any] | None = None,
) -> ZeroMDASHState:
    if target_repos and (scan_mode != "full" or diff_file or diff_git):
        raise ValueError(
            "multi-repo target_repos currently support full scan mode only; "
            "per-repository diff attribution is not implemented"
        )
    ws = Workspace.create(workspace_root, target=target, task_id=task_id, role_lang=role_lang)
    state: ZeroMDASHState = {
        "target": target,
        "target_repos": [dict(item) for item in (target_repos or [])],
        "scan_mode": scan_mode,
        "diff_file": diff_file,
        "diff_git": diff_git,
        "common_focus": common_focus,
        "fetch_target_repo_focus": fetch_target_repo_focus,
        "search_fuzz_driver_focus": search_fuzz_driver_focus,
        "search_similar_software_focus": search_similar_software_focus,
        "search_target_history_focus": search_target_history_focus,
        "search_new_feature_focus": search_new_feature_focus,
        "analyze_attack_surface_focus": analyze_attack_surface_focus,
        "summary_focus": summary_focus,
        "role_lang": role_lang,
        "task_id": ws.task_id,
        "workspace_root": str(ws.root),
        "max_iterations": max_iterations,
        "min_critic_skills": min_critic_skills,
        "agent_configs": agent_configs or {},
        "agent_config_task_types": agent_config_task_types or {},
        "preset_attack_surface_path": preset_attack_surface_path or "",
        "top_K": dict(top_K or {}),
        "chain_config": dict(chain_config or {}),
        "poc_config": dict(poc_config or {}),
        "disabled_nodes": sorted(disabled_nodes or []),
        **(extra_state or {}),
    }
    graph = build_graph(
        backends,
        disabled_nodes=disabled_nodes,
        till_node=till_node,
        poc_enabled=bool((poc_config or {}).get("enabled")),
    )

    # ---- Langfuse 可观测(仅当环境变量配置时启用)----
    # 需设置 LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY；自建实例另设
    # LANGFUSE_BASE_URL。未配置时行为与原来完全一致。
    config = langfuse_config(
        run_name=f"zeromdash:{ws.task_id}",
        metadata={
            "target": target,
            "scan_mode": scan_mode,
            "diff_file": diff_file,
            "diff_git": diff_git,
            "common_focus": common_focus,
            "fetch_target_repo_focus": fetch_target_repo_focus,
            "search_fuzz_driver_focus": search_fuzz_driver_focus,
            "search_similar_software_focus": search_similar_software_focus,
            "search_target_history_focus": search_target_history_focus,
            "search_new_feature_focus": search_new_feature_focus,
            "analyze_attack_surface_focus": analyze_attack_surface_focus,
            "summary_focus": summary_focus,
            "role_lang": role_lang,
            "task_id": ws.task_id,
            "agent_configs": json.dumps(agent_configs or {}, ensure_ascii=False, sort_keys=True),
            "agent_config_task_types": json.dumps(agent_config_task_types or {}, ensure_ascii=False, sort_keys=True),
            "preset_attack_surface_path": preset_attack_surface_path or "",
            "target_repos": json.dumps(target_repos or [], ensure_ascii=False, sort_keys=True),
            "top_K": json.dumps(top_K or {}, ensure_ascii=False, sort_keys=True),
            "chain_config": json.dumps(chain_config or {}, ensure_ascii=False, sort_keys=True),
            "max_concurrency": str(max_concurrency),
            "till_node": till_node or "",
        },
    )

    config = dict(config or {})
    config["max_concurrency"] = max_concurrency
    final = graph.invoke(state, config=config or None)
    validation_errors = _till_node_validation_errors(final, till_node)
    if validation_errors:
        final["errors"] = list(final.get("errors") or []) + validation_errors
    if till_node:
        final["stopped_at"] = till_node
    return final


def run_from_subtask_workspace(
    workspace_path: str | Path,
    backends: dict[str, str] | None = None,
    max_iterations: int = 3,
    min_critic_skills: int = 2,
    common_focus: str = "",
    agent_configs: nodes.AgentConfigs | None = None,
    agent_config_task_types: nodes.AgentConfigTaskTypes | None = None,
    top_K: dict[str, int] | None = None,
    chain_config: dict[str, Any] | None = None,
    disabled_nodes: set[str] | None = None,
    max_concurrency: int = 8,
    selected_subtask_ids: list[str] | None = None,
    selected_subtask_log_dir: str | Path | None = None,
    run_summary: bool = True,
    extra_state: dict[str, Any] | None = None,
    poc_config: dict[str, Any] | None = None,
) -> ZeroMDASHState:
    """Resume an existing workspace from planner outputs into subtasks."""
    if not run_summary and selected_subtask_ids is None:
        raise ValueError("run_summary=False requires selected_subtask_ids")
    if run_summary and selected_subtask_ids is not None:
        raise ValueError("selected_subtask_ids require run_summary=False")
    state = _restore_state_from_workspace(
        workspace_path,
        max_iterations=max_iterations,
        min_critic_skills=min_critic_skills,
        common_focus=common_focus,
        agent_configs=agent_configs,
        agent_config_task_types=agent_config_task_types,
        top_K=top_K,
        chain_config=chain_config,
        disabled_nodes=disabled_nodes,
        extra_state=extra_state,
    )
    if selected_subtask_ids is not None:
        state = _select_restore_subtasks(
            state,
            selected_subtask_ids,
            selected_subtask_log_dir,
        )
    state["poc_config"] = dict(poc_config or {})
    graph = (
        build_subtask_restore_graph(backends, poc_enabled=bool((poc_config or {}).get("enabled")))
        if run_summary
        else build_selected_subtask_restore_graph(backends)
    )
    config = langfuse_config(
        run_name=f"zeromdash:restore-subtask:{state['task_id']}",
        metadata={
            "target": state.get("target", ""),
            "common_focus": state.get("common_focus", ""),
            "task_id": state["task_id"],
            "workspace_path": str(Path(workspace_path).expanduser().resolve()),
            "agent_configs": json.dumps(agent_configs or {}, ensure_ascii=False, sort_keys=True),
            "top_K": json.dumps(top_K or {}, ensure_ascii=False, sort_keys=True),
            "chain_config": json.dumps(chain_config or {}, ensure_ascii=False, sort_keys=True),
            "max_concurrency": str(max_concurrency),
            "restore_mode": "start_from_subtask",
            "selected_subtask_ids": json.dumps(
                selected_subtask_ids or [],
                ensure_ascii=False,
            ),
            "run_summary": str(run_summary),
            "selected_subtask_log_dir": state.get("selected_subtask_log_dir", ""),
        },
    )
    config = dict(config or {})
    config["max_concurrency"] = max_concurrency
    return graph.invoke(state, config=config or None)


def run_from_chain_workspace(
    workspace_path: str | Path,
    backends: dict[str, str] | None = None,
    max_iterations: int = 3,
    min_critic_skills: int = 2,
    common_focus: str = "",
    agent_configs: nodes.AgentConfigs | None = None,
    agent_config_task_types: nodes.AgentConfigTaskTypes | None = None,
    top_K: dict[str, int] | None = None,
    chain_config: dict[str, Any] | None = None,
    disabled_nodes: set[str] | None = None,
    max_concurrency: int = 8,
    selected_chain_ids: list[str] | None = None,
    selected_chain_log_dir: str | Path | None = None,
    run_summary: bool = True,
    extra_state: dict[str, Any] | None = None,
    poc_config: dict[str, Any] | None = None,
) -> ZeroMDASHState:
    """Resume an existing workspace from confirmed primitives into chain analysis."""
    if not run_summary and selected_chain_ids is None:
        raise ValueError("run_summary=False requires selected_chain_ids")
    if run_summary and selected_chain_ids is not None:
        raise ValueError("selected_chain_ids require run_summary=False")
    state = _restore_state_from_workspace(
        workspace_path,
        max_iterations=max_iterations,
        min_critic_skills=min_critic_skills,
        common_focus=common_focus,
        agent_configs=agent_configs,
        agent_config_task_types=agent_config_task_types,
        top_K=top_K,
        chain_config=chain_config,
        disabled_nodes=disabled_nodes,
        extra_state=extra_state,
    )
    if selected_chain_ids is not None:
        ws = _workspace_from_base(workspace_path)
        selected = []
        for chain_id in selected_chain_ids:
            value = str(chain_id or "").strip()
            if value and value not in selected:
                selected.append(value)
        if not selected:
            raise ValueError("--select-chain-to-run requires at least one chain id")
        output_dir = nodes.prepare_selected_chain_log_dir(
            workspace_base=ws.base,
            selected_chain_log_dir=selected_chain_log_dir,
        )
        state["selected_chain_ids"] = selected
        state["selected_chain_log_dir"] = str(output_dir)
    state["poc_config"] = dict(poc_config or {})
    graph = (
        build_chain_restore_graph(backends, poc_enabled=bool((poc_config or {}).get("enabled")))
        if run_summary
        else build_selected_chain_restore_graph(backends)
    )
    config = langfuse_config(
        run_name=f"zeromdash:restore-chain:{state['task_id']}",
        metadata={
            "target": state.get("target", ""),
            "common_focus": state.get("common_focus", ""),
            "task_id": state["task_id"],
            "workspace_path": str(Path(workspace_path).expanduser().resolve()),
            "agent_configs": json.dumps(agent_configs or {}, ensure_ascii=False, sort_keys=True),
            "top_K": json.dumps(top_K or {}, ensure_ascii=False, sort_keys=True),
            "chain_config": json.dumps(chain_config or {}, ensure_ascii=False, sort_keys=True),
            "max_concurrency": str(max_concurrency),
            "restore_mode": "start_from_chain",
            "selected_chain_ids": json.dumps(selected_chain_ids or [], ensure_ascii=False),
            "run_summary": str(run_summary),
            "selected_chain_log_dir": state.get("selected_chain_log_dir", ""),
        },
    )
    config = dict(config or {})
    config["max_concurrency"] = max_concurrency
    return graph.invoke(state, config=config or None)


# Deprecated Python API aliases. New code should use the subtask terminology.
build_subagent_graph = build_subtask_graph
build_subagent_restore_graph = build_subtask_restore_graph
build_selected_subagent_restore_graph = build_selected_subtask_restore_graph


def run_from_subagent_workspace(
    workspace_path: str | Path,
    backends: dict[str, str] | None = None,
    max_iterations: int = 3,
    min_critic_skills: int = 2,
    common_focus: str = "",
    agent_configs: nodes.AgentConfigs | None = None,
    agent_config_task_types: nodes.AgentConfigTaskTypes | None = None,
    top_K: dict[str, int] | None = None,
    chain_config: dict[str, Any] | None = None,
    disabled_nodes: set[str] | None = None,
    max_concurrency: int = 8,
    selected_subagent_ids: list[str] | None = None,
    selected_subagent_log_dir: str | Path | None = None,
    run_summary: bool = True,
    extra_state: dict[str, Any] | None = None,
) -> ZeroMDASHState:
    """Deprecated wrapper preserving the former keyword argument names."""
    return run_from_subtask_workspace(
        workspace_path=workspace_path,
        backends=backends,
        max_iterations=max_iterations,
        min_critic_skills=min_critic_skills,
        common_focus=common_focus,
        agent_configs=agent_configs,
        agent_config_task_types=agent_config_task_types,
        top_K=top_K,
        chain_config=chain_config,
        disabled_nodes=disabled_nodes,
        max_concurrency=max_concurrency,
        selected_subtask_ids=selected_subagent_ids,
        selected_subtask_log_dir=selected_subagent_log_dir,
        run_summary=run_summary,
        extra_state=extra_state,
    )


def run_summary_from_workspace(
    workspace_path: str | Path,
    backends: dict[str, str] | None = None,
    common_focus: str = "",
    agent_configs: nodes.AgentConfigs | None = None,
    agent_config_task_types: nodes.AgentConfigTaskTypes | None = None,
    max_concurrency: int = 8,
    extra_state: dict[str, Any] | None = None,
    poc_config: dict[str, Any] | None = None,
) -> ZeroMDASHState:
    """Restore an existing workspace and run summary followed by report polish."""
    state = _summary_state_from_workspace(
        workspace_path,
        common_focus=common_focus,
        agent_configs=agent_configs,
        agent_config_task_types=agent_config_task_types,
        extra_state=extra_state,
    )
    state["poc_config"] = dict(poc_config or {})
    graph = StateGraph(ZeroMDASHState)
    graph.add_node("summary", partial(nodes.summary, backends=backends))
    graph.add_node("polish_report", nodes.polish_report)
    graph.add_edge(START, "summary")
    graph.add_edge("summary", "polish_report")
    if (poc_config or {}).get("enabled"):
        graph.add_node("poc_gen", partial(nodes.poc_gen, backends=backends))
        graph.add_edge("polish_report", "poc_gen")
        graph.add_edge("poc_gen", END)
    else:
        graph.add_edge("polish_report", END)
    app = graph.compile()
    config = langfuse_config(
        run_name=f"zeromdash:restore-summary:{state['task_id']}",
        metadata={
            "target": state.get("target", ""),
            "common_focus": state.get("common_focus", ""),
            "task_id": state["task_id"],
            "workspace_path": str(Path(workspace_path).expanduser().resolve()),
            "agent_configs": json.dumps(agent_configs or {}, ensure_ascii=False, sort_keys=True),
            "max_concurrency": str(max_concurrency),
            "restore_mode": "start_from_summary",
        },
    )
    config = dict(config or {})
    config["max_concurrency"] = max_concurrency
    return app.invoke(state, config=config or None)


def run_pocs_from_workspace(
    workspace_path: str | Path,
    *,
    finding_id: str = "",
    backends: dict[str, str] | None = None,
    common_focus: str = "",
    agent_configs: nodes.AgentConfigs | None = None,
    agent_config_task_types: nodes.AgentConfigTaskTypes | None = None,
    max_concurrency: int = 8,
    poc_config: dict[str, Any] | None = None,
) -> ZeroMDASHState:
    """Run only PoC generation from a completed single-target workspace."""
    from zeromdash.poc_gen.config import normalize_poc_config

    state = _summary_state_from_workspace(
        workspace_path,
        common_focus=common_focus,
        agent_configs=agent_configs,
        agent_config_task_types=agent_config_task_types,
        require_findings=False,
    )
    state["poc_config"] = normalize_poc_config(poc_config, force_enabled=True)
    state["poc_finding_id"] = str(finding_id or "").strip()
    graph = StateGraph(ZeroMDASHState)
    graph.add_node("poc_gen", partial(nodes.poc_gen, backends=backends))
    graph.add_edge(START, "poc_gen")
    graph.add_edge("poc_gen", END)
    app = graph.compile()
    config = langfuse_config(
        run_name=f"zeromdash:only-poc:{state['task_id']}",
        metadata={
            "target": state.get("target", ""),
            "task_id": state["task_id"],
            "finding_id": state["poc_finding_id"],
            "workspace_path": str(Path(workspace_path).expanduser().resolve()),
        },
    )
    config = dict(config or {})
    config["max_concurrency"] = max_concurrency
    return app.invoke(state, config=config or None)


def run_polish_report_from_workspace(
    workspace_path: str | Path,
    common_focus: str = "",
    agent_configs: nodes.AgentConfigs | None = None,
    agent_config_task_types: nodes.AgentConfigTaskTypes | None = None,
    max_concurrency: int = 8,
    extra_state: dict[str, Any] | None = None,
) -> ZeroMDASHState:
    """Restore an existing workspace and run only the lightweight polish node."""
    state = _polish_report_state_from_workspace(
        workspace_path,
        common_focus=common_focus,
        agent_configs=agent_configs,
        agent_config_task_types=agent_config_task_types,
        extra_state=extra_state,
    )
    graph = StateGraph(ZeroMDASHState)
    graph.add_node("polish_report", nodes.polish_report)
    graph.add_edge(START, "polish_report")
    graph.add_edge("polish_report", END)
    app = graph.compile()
    config = langfuse_config(
        run_name=f"zeromdash:restore-polish-report:{state['task_id']}",
        metadata={
            "target": state.get("target", ""),
            "common_focus": state.get("common_focus", ""),
            "task_id": state["task_id"],
            "workspace_path": str(Path(workspace_path).expanduser().resolve()),
            "agent_configs": json.dumps(agent_configs or {}, ensure_ascii=False, sort_keys=True),
            "max_concurrency": str(max_concurrency),
            "restore_mode": "start_from_polish_report",
        },
    )
    config = dict(config or {})
    config["max_concurrency"] = max_concurrency
    return app.invoke(state, config=config or None)
