"""LangGraph state schema for ZeroMDASH.

The state is a TypedDict so LangGraph can merge updates from each node.
Qualified vulnerabilities flow through the per-bucket finding lists. Expected
behavior, hardening recommendations, patch-state notes, and inconclusive cases
flow through `observations` so the summary can preserve evidence without
promoting those records to `VULN-XXX`.

Per-bucket fan-out
------------------
The `fanout_by_*` step does NOT directly emit findings. Instead it runs a
**planner** that produces a *dynamic* list of `Subtask` items (the count
depends on the actual target / writeups / spec content). The graph then
    fans out one nested **subtask graph** per `Subtask` via
    `langgraph.constants.Send`.

Each subtask graph runs an Agent-Native `investigate -> critic` loop. New
planner outputs are bounded work packages with coverage obligations and a
monotonic hypothesis ledger; old single-outcome subtasks remain readable:
    investigate_subtask -> critic_subtask --(loop, with feedback)--> investigate_subtask
                                       --(done: confirm/reject/exhausted)--> END
First-iteration `no-finding` hypothesis results are forced through one feedback
loop before they can terminate. A package closes only after the critic has
issued a terminal verdict for every retained hypothesis and independently
accepted coverage closure.
The feedback edge carries the critic's reasoning back into the investigator
for the next iteration.
"""

from __future__ import annotations

import operator
from typing import Annotated, Any, TypedDict


# --------------------------------------------------------------------- types
class Subtask(TypedDict, total=False):
    """One unit of work spawned by a `fanout_by_*` planner.

    `bucket` selects which output channel the final finding is written to:
        "spec"       -> spec_findings
        "vuln"       -> vuln_candidates
        "patch_miss" -> patch_findings
        "feature"    -> feature_findings
    """
    id: str
    bucket: str
    objective: str           # 自然语言任务描述（喂给 investigator）
    hints: dict[str, Any]    # 行号/标准条款/CVE 等线索
    coverage_obligations: list[dict[str, Any]]  # agent-defined package coverage contract
    seed_hypotheses: list[dict[str, Any]]       # initial atomic hypotheses; investigator may append


class ReviewTurn(TypedDict, total=False):
    iteration: int
    investigation: str
    review: dict[str, Any]


class Finding(TypedDict, total=False):
    kind: str                    # "spec" | "vuln" | "patch_miss" | "feature"
    subtask_id: str
    parent_subtask_id: str
    hypothesis_id: str
    title: str
    detail: str
    evidence: dict[str, Any]
    review: dict[str, Any]       # 终态 critic 结论
    severity: str
    confidence: float
    iterations: int              # 走了多少轮 investigate<->critic
    selected_skills: list[str]   # critic 终态选中的专家 skill
    scope_relation: str          # introduced/enabled/regressed/pre_existing/...
    patch_status: str            # patch audit: not_applied/bypass/incomplete/applied
    diff_evidence: dict[str, Any]
    scope_verdict: str
    gate_decision: str
    disposition: str             # vulnerability/configuration/hardening/non-finding taxonomy
    qualification_gate_passed: bool
    cvss_applicable: bool
    cvss4_vector: str
    cvss4_score: float
    direct_security_impact: dict[str, Any]
    violated_security_property: str
    documented_expected_behavior: bool
    security_contract_violation: bool
    standalone_security_impact: bool
    required_external_primitives: list[str]
    capability_view: dict[str, Any]
    source_primitive_ids: list[str]
    attack_path: list[dict[str, Any]]


class Primitive(TypedDict, total=False):
    schema_version: str
    primitive_id: str
    source_subtask_ids: list[str]
    source_finding_ids: list[str]
    repo_id: str
    revision: str
    component: str
    root_cause_anchor: dict[str, Any]
    entry_conditions: dict[str, Any]
    required_capabilities: list[dict[str, Any]]
    attacker_controls: list[dict[str, Any]]
    capabilities_gained: list[dict[str, Any]]
    handoff_objects: list[dict[str, Any]]
    reliability: dict[str, Any]
    evidence: dict[str, Any]
    terminal_impact: dict[str, Any]
    missing_next_capabilities: list[dict[str, Any]]
    confirmation: dict[str, Any]
    domain_refs: dict[str, list[str]]
    required_entity_states: list[dict[str, Any]]
    resulting_entity_states: list[dict[str, Any]]
    violated_invariant_ids: list[str]


class ChainCandidate(TypedDict, total=False):
    schema_version: str
    chain_id: str
    ordered_primitive_ids: list[str]
    attacker_entry: dict[str, Any]
    bindings: list[dict[str, Any]]
    available_capabilities: list[dict[str, Any]]
    global_constraints: dict[str, Any]
    expected_terminal_impact: dict[str, Any]
    rank_score: float
    status: str
    pruning_context: dict[str, Any]
    failure_reasons: list[str]
    review: dict[str, Any]
    investigation: dict[str, Any]
    deterministic_advisories: list[dict[str, Any]]


class ChainFinding(Finding, total=False):
    schema_version: str
    chain_id: str
    ordered_primitive_ids: list[str]
    bindings: list[dict[str, Any]]
    global_constraints: dict[str, Any]
    attacker_entry: dict[str, Any]
    binding_claims: list[dict[str, Any]]
    emergent_transitions: list[dict[str, Any]]
    deterministic_advisories: list[dict[str, Any]]
    blocking_unmet_facts: list[dict[str, Any]]
    validation_gaps: list[dict[str, Any]]
    deployment_constraints: list[dict[str, Any]]
    impact_limits: list[dict[str, Any]]
    closure_facts: list[dict[str, Any]]
    fact_verdicts: list[dict[str, Any]]
    closure_verdict: str


class ReportGroup(TypedDict, total=False):
    schema_version: str
    group_id: str
    group_key: str
    title: str
    status: str
    summary_format: str
    primary_finding: dict[str, Any]
    findings: list[dict[str, Any]]
    source_subtasks: list[str]
    source_chains: list[str]
    source_primitive_ids: list[str]
    absorbed_finding_ids: list[str]
    cvss4_vector: str
    cvss4_score: float
    severity: str
    confidence: float


# --------------------------------------------------------------------- state
class ZeroMDASHState(TypedDict, total=False):
    # ------------------------- inputs -------------------------
    target: str                  # 目标软件描述 / 路径 / URL
    target_repos: list[dict[str, Any]]  # optional multi-repo target registry
    scan_mode: str               # "full" | "diff"; diff only highlights changes
    diff_file: str               # optional unified diff against patched repo
    diff_git: str                # optional <before>..<after> refs for remote git targets
    common_focus: str            # 可选全局分析重点；会作为各阶段 focus 的前缀
    fetch_target_repo_focus: str
    search_spec_focus: str
    search_fuzz_driver_focus: str
    search_similar_software_focus: str
    search_similar_history_focus: str
    search_target_history_focus: str
    search_new_feature_focus: str
    analyze_attack_surface_focus: str
    chain_finalizer_subtask_focus: str
    report_group_adjudicator_focus: str
    summary_focus: str
    role_lang: str               # role card language, e.g. "en" or "zh_CN"
    task_id: str
    workspace_root: str
    max_iterations: int          # 单个 subtask 的最大 critic 反馈轮数
    min_critic_skills: int       # critic 每次必须选择的最少专家 skill 数
    agent_configs: dict[str, dict[str, Any]]  # node -> {runtime, provider, config, env, focus}
    agent_config_task_types: dict[str, str]  # legacy; retained for old programmatic callers
    preset_attack_surface_path: str  # optional seed file appended by analyze_attack_surface
    top_K: dict[str, int]  # optional positive per-bucket subtask fan-out caps: spec/vuln/patch/feature
    chain_config: dict[str, Any]
    poc_config: dict[str, Any]  # optional post-summary PoC generation settings
    poc_finding_id: str  # optional report-group/subtask/chain selector for only-gen-poc
    disabled_nodes: list[str]  # node names to skip (e.g. ["search_spec", "plan_by_spec"] for --disable-spec)
    completed_subtask_ids: list[str]  # restore-only: subtask ids materialized under log/subtask_res (or legacy review_res)
    selected_subtask_ids: list[str]
    selected_subtask_log_dir: str
    selected_subtask_statuses: list[dict[str, Any]]
    selected_chain_ids: list[str]
    selected_chain_log_dir: str
    selected_chain_statuses: list[dict[str, Any]]
    # Deprecated restore-state aliases, read-only compatibility.
    selected_subagent_ids: list[str]
    selected_subagent_log_dir: str
    selected_subagent_statuses: list[dict[str, Any]]

    # --------------------- left half: gather -------------------
    repo_path: str               # workspace[main]/repo
    target_repos_path: str       # workspace[main]/repos/_manifest.json
    scope_path: str              # workspace[main]/scope/scope.json
    scan_scope: dict[str, Any]   # parsed full/diff scope metadata
    spec_doc: str                # workspace[main]/spec
    fuzz_drivers: list[str]
    similar_repos: list[str]     # workspace[similar]/repo (if oss)
    similar_software: str        # per-Send scratch key for one similar-history branch
    similar_writeups: Annotated[list[str], operator.add]  # workspace[similar]/writeup
    similar_patches: Annotated[list[str], operator.add]   # workspace[similar]/patch
    target_writeups: list[str]   # workspace[main]/writeup
    target_patches: list[str]    # workspace[main]/patch
    target_patch_manifest: str   # workspace[main]/patch/_patch_commits.json
    feature_docs: list[str]      # workspace[main]/feature

    # ----------------------- middle: fuse ----------------------
    attack_surface: str          # workspace[main]/attack_surface
    domain_registry_path: str    # workspace[main]/attack_surface/domain_invariant_registry.json
    domain_registry: dict[str, Any]

    # ------------- planner outputs (dynamic subtask lists) ------
    spec_subtasks: list[Subtask]
    vuln_subtasks: list[Subtask]
    patch_subtasks: list[Subtask]
    feature_subtasks: list[Subtask]

    # --------- aggregated findings (subtask -> parent merge) ----
    spec_findings: Annotated[list[Finding], operator.add]
    vuln_candidates: Annotated[list[Finding], operator.add]
    patch_findings: Annotated[list[Finding], operator.add]
    feature_findings: Annotated[list[Finding], operator.add]
    observations: Annotated[list[Finding], operator.add]
    confirmed_primitives: Annotated[list[Primitive], operator.add]
    chain_candidates: Annotated[list[ChainCandidate], operator.add]
    chain_findings: Annotated[list[ChainFinding], operator.add]
    chain_pool: list[Primitive]
    chain_pool_path: str
    chain_plan: list[ChainCandidate]
    chain_plan_path: str
    report_groups: list[ReportGroup]
    report_groups_path: str

    # ----------------------- output ----------------------------
    summary: str
    summary_en: str
    summary_zh_CN: str
    gate_result: dict[str, Any]
    gate_result_path: str
    poc_results: list[dict[str, Any]]
    stopped_at: str
    errors: Annotated[list[str], operator.add]


class SubtaskInputState(TypedDict, total=False):
    task_id: str
    workspace_root: str
    target: str
    repo_path: str
    scope_path: str
    scan_scope: dict[str, Any]
    subtask: Subtask
    iteration: int
    max_iterations: int
    min_critic_skills: int
    agent_configs: dict[str, dict[str, Any]]
    agent_config_task_types: dict[str, str]
    # Upstream context propagated from the parent graph via _dispatch so the
    # investigator can frame its work within the attack-surface model + threat
    # model instead of doing bottom-up code reading only.
    common_focus: str
    attack_surface: str
    domain_registry_path: str
    domain_registry: dict[str, Any]
    spec_doc: str
    similar_writeups: list[str]
    feature_docs: list[str]
    review_history: Annotated[list[ReviewTurn], operator.add]
    selected_subtask_log_dir: str


class SubtaskState(SubtaskInputState, total=False):
    investigation: str           # 本轮 investigator 产出的调查内容
    investigation_valid: bool    # structured output passed evidence validation
    review: dict[str, Any]       # 本轮 critic 结论
    hypothesis_manifest: dict[str, Any]  # monotonic agent-owned hypothesis ledger
    spec_findings: Annotated[list[Finding], operator.add]
    vuln_candidates: Annotated[list[Finding], operator.add]
    patch_findings: Annotated[list[Finding], operator.add]
    feature_findings: Annotated[list[Finding], operator.add]
    observations: Annotated[list[Finding], operator.add]
    confirmed_primitives: Annotated[list[Primitive], operator.add]
    errors: Annotated[list[str], operator.add]


class SubtaskOutputState(TypedDict, total=False):
    # Plain lists here: the nested graph emits one completed subtask's
    # aggregate output. The parent ZeroMDASHState owns the operator.add
    # reducers that merge outputs from multiple concurrent subgraphs.
    spec_findings: list[Finding]
    vuln_candidates: list[Finding]
    patch_findings: list[Finding]
    feature_findings: list[Finding]
    observations: list[Finding]
    confirmed_primitives: list[Primitive]
    errors: list[str]


class ChainSubtaskInputState(TypedDict, total=False):
    task_id: str
    workspace_root: str
    target: str
    repo_path: str
    scope_path: str
    scan_scope: dict[str, Any]
    chain_candidate: ChainCandidate
    chain_pool: list[Primitive]
    iteration: int
    max_chain_iterations: int
    min_critic_skills: int
    agent_configs: dict[str, dict[str, Any]]
    agent_config_task_types: dict[str, str]
    common_focus: str
    attack_surface: str
    domain_registry_path: str
    domain_registry: dict[str, Any]
    spec_doc: str
    similar_writeups: list[str]
    feature_docs: list[str]
    chain_review_history: Annotated[list[ReviewTurn], operator.add]
    selected_chain_log_dir: str


class ChainSubtaskState(ChainSubtaskInputState, total=False):
    chain_investigation: str
    chain_investigation_valid: bool
    chain_review: dict[str, Any]
    chain_candidates: Annotated[list[ChainCandidate], operator.add]
    chain_findings: Annotated[list[ChainFinding], operator.add]
    errors: Annotated[list[str], operator.add]


class ChainSubtaskOutputState(TypedDict, total=False):
    chain_candidates: list[ChainCandidate]
    chain_findings: list[ChainFinding]
    errors: list[str]


# Deprecated Python API aliases for callers that imported the old state names.
SubagentInputState = SubtaskInputState
SubagentState = SubtaskState
SubagentOutputState = SubtaskOutputState
