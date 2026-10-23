"""Constants shared by ZeroMDASH node implementations."""

from __future__ import annotations

import re

DEFAULT_BACKENDS = {
    "fetch_target_repo":         "claude_code",
    "search_spec":               "claude_code",
    "search_fuzz_driver":        "claude_code",
    "search_similar_software":   "claude_code",
    "search_similar_history":    "claude_code",
    "search_target_history":     "claude_code",
    "search_new_feature":        "claude_code",
    "analyze_attack_surface":    "codex",

    "plan_by_spec":              "codex",
    "plan_by_vuln_similar":      "codex",
    "plan_by_vuln_patch":        "codex",
    "plan_by_new_feature":       "codex",

    "investigate_subtask":      "codex",
    "critic_subtask":                "codex",

    "plan_chains":              "codex",
    "chain_investigate_subtask":      "codex",
    "chain_critic_subtask":           "codex",
    "chain_finalizer_subtask":         "codex",
    "report_group_adjudicator":        "codex",

    "gather_analyze_attack_surface":   "codex",
    "gather_plan_chains":              "codex",
    "gather_chain_investigate_subtask": "codex",
    "gather_chain_critic_subtask":     "codex",
    "gather_chain_finalizer_subtask":  "codex",
    "gather_report_group_adjudicator": "codex",

    "summary":                   "claude_code",
    "polish_report":             "claude_code",
}

NATIVE_SUBAGENT_REQUIRED_NODES = frozenset(
    {
        "investigate_subtask",
        "critic_subtask",
        "plan_chains",
        "chain_investigate_subtask",
        "chain_critic_subtask",
        "chain_finalizer_subtask",
        "report_group_adjudicator",
        "gather_analyze_attack_surface",
        "gather_plan_chains",
        "gather_chain_investigate_subtask",
        "gather_chain_critic_subtask",
        "gather_chain_finalizer_subtask",
        "gather_report_group_adjudicator",
        "summary",
    }
)
NODE_NAME_ALIASES = {
    "investigate_subagent": "investigate_subtask",
    "critic_one": "critic_subtask",
}

DEFAULT_MAX_ITERATIONS = 3
DEFAULT_MIN_CRITIC_SKILLS = 2
DEFAULT_FETCH_TARGET_REPO_ATTEMPTS = 3
DEFAULT_NODE_OUTPUT_ATTEMPTS = 3
_IGNORED_OUTPUT_FILENAMES = {".DS_Store", ".gitkeep"}
_PRIORITY_REASON_FALLBACK = (
    "Ranked by common_focus alignment and attack-surface reachability; "
    "planner did not provide a specific priority_reason."
)
_PRIORITY_STOP_WORDS = {
    "and",
    "are",
    "for",
    "from",
    "into",
    "not",
    "the",
    "that",
    "this",
    "with",
    "without",
    "是否",
    "以及",
    "或者",
    "一个",
    "需要",
}

_FIRST_NO_FINDING_REVISE_GAP = (
    "first-iteration no-finding cannot terminate the subtask; it must first "
    "test whether this vulnerability pattern is eliminated on all plausible "
    "paths to the relevant sink"
)
_FIRST_NO_FINDING_REQUESTED_EVIDENCE = [
    "Enumerate attacker-influenced entrypoints and sibling paths that can reach the relevant sink, including paths not listed in the subtask hints.",
    "For each path, show the exact check/transform that eliminates this vulnerability pattern, or show why the path cannot reach the sink.",
    "Account for writers or rewriters between any sanitizer/check and the point of use.",
]
_FIRST_NO_FINDING_NEXT_FOCUS = (
    "Divergently enumerate all plausible paths for this vulnerability pattern "
    "before concluding no-finding."
)
_RETRY_FEEDBACK_HEADER = "# Orchestrator retry feedback"
_SUMMARY_STATUS_RANK = {
    "confirm": 0,
    "revise": 1,
    "reject": 2,
}
_DISPOSITIONS = {
    "confirmed_vulnerability",
    "configuration_vulnerability",
    "known_cve_patch_gap",
    "hardening_recommendation",
    "expected_behavior",
    "insufficient_evidence",
    "no_finding",
}
_VULNERABILITY_DISPOSITIONS = {
    "confirmed_vulnerability",
    "configuration_vulnerability",
}
_NON_VULNERABILITY_DISPOSITIONS = _DISPOSITIONS - _VULNERABILITY_DISPOSITIONS
_QUALIFICATION_GATE_VERSION = "cvss4-v1"
_SUMMARY_EVIDENCE_DROP_KEYS = {
    "code_locations",
    "call_flow",
    "call_path",
    "call_paths",
    "data_flow",
    "data_flows",
}
_SUMMARY_FORMAT_FULL = "full"
_SUMMARY_FORMAT_PATCH_GAP = "patch_gap"
_CVE_ID_RE = re.compile(r"\bCVE-\d{4}-\d{4,7}\b", re.IGNORECASE)
_PATCH_STATUSES = {"not_applied", "bypass", "incomplete", "applied"}
_PATCH_GAP_NOT_APPLIED_MARKERS = (
    "not applied",
    "not apply",
    "missing patch",
    "patch missing",
    "fix is absent",
    "fix not present",
    "unpatched",
    "not backported",
    "backport required",
    "apply patch",
    "尚未应用",
    "未应用",
    "缺少补丁",
    "补丁缺失",
    "需要回填",
)
_PATCH_GAP_FULL_VULN_MARKERS = (
    "bypass",
    "bypassable",
    "circumvent",
    "incomplete",
    "insufficient",
    "partial fix",
    "partially fixed",
    "regression",
    "绕过",
    "残缺",
    "不完整",
    "修复不足",
    "补丁不全",
)

_PATCH_MANIFEST_SCHEMA_VERSION = "1.0"
_PATCH_COVERAGE_STATUSES = {"researched", "no_public_history", "unavailable"}
_PATCH_APPLICABILITY = {"affected", "fixed", "unaffected", "historical_class", "unknown"}
_PATCH_MANIFEST_STATUSES = {"applied", "not_applied", "partial", "not_applicable", "unknown", "unavailable"}
_PATCH_VERIFICATIONS = {"ancestor", "content_equivalent", "absent", "not_checked", "not_in_git", "not_isolatable"}
_PATCH_SOURCE_TYPES = {"advisory", "writeup", "patch", "issue", "release_note", "other"}
_PATCH_MANIFEST_KEYS = {"schema_version", "target", "mode", "repositories", "coverage", "findings"}
_PATCH_REPOSITORY_KEYS = {"repo_id", "role", "target", "repo_path", "branch", "head", "describe"}
_PATCH_COVERAGE_KEYS = {"repo_id", "status", "sources_checked", "notes"}
_PATCH_FINDING_KEYS = {"record_id", "repo_id", "advisory_ids", "title", "root_cause_class", "affected_locations", "sources", "applicability", "patch", "lesson", "notes"}
_PATCH_SOURCE_KEYS = {"type", "url"}
_PATCH_OBJECT_KEYS = {"status", "upstream_commits", "equivalent_commits", "verification", "verified_against_head", "fixed_versions", "notes"}

__all__ = ["DEFAULT_BACKENDS","NATIVE_SUBAGENT_REQUIRED_NODES","NODE_NAME_ALIASES","DEFAULT_MAX_ITERATIONS","DEFAULT_MIN_CRITIC_SKILLS","DEFAULT_FETCH_TARGET_REPO_ATTEMPTS","DEFAULT_NODE_OUTPUT_ATTEMPTS","_IGNORED_OUTPUT_FILENAMES","_PRIORITY_REASON_FALLBACK","_PRIORITY_STOP_WORDS","_FIRST_NO_FINDING_REVISE_GAP","_FIRST_NO_FINDING_REQUESTED_EVIDENCE","_FIRST_NO_FINDING_NEXT_FOCUS","_RETRY_FEEDBACK_HEADER","_SUMMARY_STATUS_RANK","_DISPOSITIONS","_VULNERABILITY_DISPOSITIONS","_NON_VULNERABILITY_DISPOSITIONS","_QUALIFICATION_GATE_VERSION","_SUMMARY_EVIDENCE_DROP_KEYS","_SUMMARY_FORMAT_FULL","_SUMMARY_FORMAT_PATCH_GAP","_CVE_ID_RE","_PATCH_STATUSES","_PATCH_GAP_NOT_APPLIED_MARKERS","_PATCH_GAP_FULL_VULN_MARKERS","_PATCH_MANIFEST_SCHEMA_VERSION","_PATCH_COVERAGE_STATUSES","_PATCH_APPLICABILITY","_PATCH_MANIFEST_STATUSES","_PATCH_VERIFICATIONS","_PATCH_SOURCE_TYPES","_PATCH_MANIFEST_KEYS","_PATCH_REPOSITORY_KEYS","_PATCH_COVERAGE_KEYS","_PATCH_FINDING_KEYS","_PATCH_SOURCE_KEYS","_PATCH_OBJECT_KEYS"]
