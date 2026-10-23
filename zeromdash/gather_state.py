"""State and artifact types for cross-workspace gather scans."""

from __future__ import annotations

import operator
from typing import Annotated, Any, TypedDict


class GatherTarget(TypedDict, total=False):
    target_id: str
    name: str
    role: str
    workspace_path: str
    agent_config_path: str
    source_scan_mode: str
    source_revision: dict[str, Any]
    source_common_focus: str
    source_roots: list[str]
    original_source_roots: dict[str, str]
    snapshot_root: str
    artifact_hashes: dict[str, str]


class SourceRef(TypedDict, total=False):
    target_id: str
    workspace_id: str
    artifact_kind: str
    artifact_path: str
    artifact_sha256: str
    json_pointer: str
    local_id: str
    repo_id: str
    revision: str
    code_locations: list[str]
    legacy_activity_unverified: bool


class GatherEvidenceUnit(TypedDict, total=False):
    unit_id: str
    local_id: str
    unit_kind: str
    target_id: str
    component: str
    entry_conditions: dict[str, Any]
    required_capabilities: list[dict[str, Any]]
    attacker_controls: list[dict[str, Any]]
    capabilities_gained: list[dict[str, Any]]
    handoff_objects: list[dict[str, Any]]
    required_entity_states: list[dict[str, Any]]
    resulting_entity_states: list[dict[str, Any]]
    terminal_impact: dict[str, Any]
    constraints: dict[str, Any]
    constituent_unit_ids: list[str]
    source_refs: list[SourceRef]
    source_payload: dict[str, Any]


class GatherChainCandidate(TypedDict, total=False):
    schema_version: str
    chain_id: str
    target_sequence: list[str]
    ordered_unit_ids: list[str]
    attacker_entry: dict[str, Any]
    bindings: list[dict[str, Any]]
    global_constraints: dict[str, Any]
    expected_terminal_impact: dict[str, Any]
    emergent_impact_hypothesis: dict[str, Any]
    rank_score: float
    agent_reasoning: str
    deterministic_advisories: list[dict[str, Any]]
    status: str
    failure_reasons: list[str]
    investigation: dict[str, Any]
    review: dict[str, Any]


class GatherReviewTurn(TypedDict, total=False):
    iteration: int
    investigation: dict[str, Any]
    review: dict[str, Any]


class GatherState(TypedDict, total=False):
    scan_mode: str
    target: str
    scenario_name: str
    scenario: str
    manifest_path: str
    manifest_hash: str
    task_id: str
    workspace_root: str
    role_lang: str
    gather_targets: list[GatherTarget]
    source_read_roots: list[str]
    input_lock_path: str
    input_lock_hash: str
    agent_configs: dict[str, dict[str, Any]]
    agent_config_task_types: dict[str, str]
    common_focus: str
    gather_analyze_attack_surface_focus: str
    gather_plan_chains_focus: str
    gather_chain_investigate_subtask_focus: str
    gather_chain_critic_subtask_focus: str
    gather_chain_finalizer_subtask_focus: str
    gather_report_group_adjudicator_focus: str
    summary_focus: str
    min_critic_skills: int
    top_K: dict[str, int]
    gather_config: dict[str, Any]
    gather_attack_surface: str
    cross_target_registry_path: str
    cross_target_registry: dict[str, Any]
    cross_target_flow_count: int
    gather_evidence_pool: list[GatherEvidenceUnit]
    gather_evidence_count: int
    gather_evidence_pool_path: str
    gather_chain_plan: list[GatherChainCandidate]
    gather_chain_plan_path: str
    gather_chain_candidates: Annotated[list[dict[str, Any]], operator.add]
    gather_chain_findings: Annotated[list[dict[str, Any]], operator.add]
    gather_report_groups: list[dict[str, Any]]
    gather_report_groups_path: str
    summary: str
    summary_en: str
    summary_zh_CN: str
    gate_result: dict[str, Any]
    gate_result_path: str
    errors: Annotated[list[str], operator.add]


class GatherChainSubtaskInputState(TypedDict, total=False):
    task_id: str
    workspace_root: str
    target: str
    scenario_name: str
    scenario: str
    manifest_hash: str
    input_lock_path: str
    input_lock_hash: str
    gather_targets: list[GatherTarget]
    source_read_roots: list[str]
    gather_chain_candidate: GatherChainCandidate
    gather_evidence_pool: list[GatherEvidenceUnit]
    gather_evidence_pool_path: str
    gather_attack_surface: str
    cross_target_registry_path: str
    cross_target_registry: dict[str, Any]
    cross_target_flow_count: int
    iteration: int
    max_chain_iterations: int
    min_critic_skills: int
    agent_configs: dict[str, dict[str, Any]]
    agent_config_task_types: dict[str, str]
    common_focus: str
    gather_review_history: Annotated[list[GatherReviewTurn], operator.add]


class GatherChainSubtaskState(GatherChainSubtaskInputState, total=False):
    gather_chain_investigation: dict[str, Any]
    gather_chain_investigation_valid: bool
    gather_chain_review: dict[str, Any]
    gather_chain_candidates: Annotated[list[dict[str, Any]], operator.add]
    gather_chain_findings: Annotated[list[dict[str, Any]], operator.add]
    errors: Annotated[list[str], operator.add]


class GatherChainSubtaskOutputState(TypedDict, total=False):
    gather_chain_candidates: list[dict[str, Any]]
    gather_chain_findings: list[dict[str, Any]]
    errors: list[str]


__all__ = [
    "GatherChainCandidate",
    "GatherChainSubtaskInputState",
    "GatherChainSubtaskOutputState",
    "GatherChainSubtaskState",
    "GatherEvidenceUnit",
    "GatherReviewTurn",
    "GatherState",
    "GatherTarget",
    "SourceRef",
]
