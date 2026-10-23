"""Shared state, focus, and scan-scope context helpers."""

from __future__ import annotations

import re
from pathlib import Path

from zeromdash.state import ZeroMDASHState
from zeromdash.workspace import Workspace

from .config import agent_config_for_node
from .io import _read_text_lossy

def _node_from_focus_key(node_focus_key: str) -> str:
    return node_focus_key[:-6] if node_focus_key.endswith("_focus") else node_focus_key

def _node_focus(state: ZeroMDASHState, node_focus_key: str) -> str:
    """Compose common focus and one stage-specific focus for a prompt.

    Both pieces are optional. Keep the text as an explicit instruction block so
    every focus-aware node receives the shared steer first, then its local steer.
    """
    common = str(state.get("common_focus") or state.get("focus") or "").strip()
    node = _node_from_focus_key(node_focus_key)
    config_focus = agent_config_for_node(node, state.get("agent_configs")).get("focus", "")
    # CLI/state focus is kept as an explicit override for backward-compatible
    # programmatic callers, but the preferred source is agent-config YAML.
    stage = str(state.get(node_focus_key) or config_focus or "").strip()
    if common and stage:
        focus = (
            f'Global focus: "{common}"\n'
            f'Stage-specific focus: "{stage}"\n'
            "Apply the global focus first, and additionally prioritize the "
            "stage-specific focus in this step."
        )
    elif common:
        focus = f'Global focus: "{common}"\nApply the global focus in this step.'
    elif stage:
        focus = f'Stage-specific focus: "{stage}"\nPrioritize the stage-specific focus in this step.'
    else:
        focus = ""
    scope = _scope_context(state, node)
    return "\n\n".join(part for part in (focus, scope) if part)

def _scope_context(state: ZeroMDASHState, node: str = "") -> str:
    scope = state.get("scan_scope")
    if not isinstance(scope, dict) or not scope:
        return ""
    mode = str(scope.get("mode") or "full")
    scope_path = str(state.get("scope_path") or "")
    if mode != "diff":
        return (
            "Scan scope: full repository.\n"
            f"Scope artifact: {scope_path}\n"
            "The complete repository is in scope. Preserve the existing repository-wide "
            "analysis behavior."
        )

    changed_files = [str(path) for path in scope.get("changed_files") or []]
    shown = changed_files[:40]
    suffix = f"\n- ... and {len(changed_files) - len(shown)} more" if len(changed_files) > len(shown) else ""
    changed_list = "\n".join(f"- {path}" for path in shown) + suffix
    common = (
        "Scan scope: diff-highlighted analysis over the complete patched repository.\n"
        f"Scope artifact: {scope_path}\n"
        f"Diff artifact: {Path(scope_path).with_name('changes.diff') if scope_path else ''}\n"
        "The repository already contains the patched code. Read any repository file needed "
        "for call graphs, types, configuration, sibling paths, and security invariants. "
        "Do not restrict code reading to changed files.\n"
        "The diff defines attribution and priority: a blocking finding must prove that the "
        "change introduced, enabled, or regressed the vulnerable path. A pre-existing or "
        "unrelated issue may be reported as non-blocking context.\n"
    )
    if node.startswith("search_") or node == "analyze_attack_surface":
        node_contract = (
            "Use changed files/symbols to prioritize domain research and attack-surface "
            "modeling, while retaining relevant repository-wide context."
        )
    elif node.startswith("plan_by_"):
        node_contract = (
            "Planner outputs must add one hints.risk_surface_id, hints.diff_anchor, "
            "hints.change_to_sink_path, hints.scope_relation, hints.changed_locations, "
            "hints.context_locations, hints.change_hypothesis, and hints.blocking_eligible. "
            "Use RS-EXT-<slug> plus a complete hints.risk_surface_definition only when "
            "the canonical registry missed a genuinely independent diff-to-sink risk."
        )
    elif node == "investigate_subtask":
        node_contract = (
            "Investigation output must include scope_relation and evidence.diff_evidence "
            "with changed/context locations, change_to_sink_path, and causal_explanation."
        )
    elif node == "critic_subtask":
        node_contract = (
            "Review output must independently verify attribution and include scope_verdict "
            "plus gate_decision. Pre-existing/unrelated issues are non-blocking."
        )
    elif node == "summary":
        node_contract = (
            "Separate blocking introduced/enabled/regressed findings from non-blocking "
            "pre-existing/unrelated findings in both reports."
        )
    else:
        node_contract = ""
    return common + node_contract + f"\nChanged files:\n{changed_list or '- (none)'}"

def _attack_surface_text(state: ZeroMDASHState) -> str:
    raw = str(state.get("attack_surface") or "")
    if not raw:
        return ""
    path = Path(raw)
    return _read_text_lossy(path) if path.is_file() else raw

def _attack_surface_has_risk_registry(state: ZeroMDASHState) -> bool:
    text = _attack_surface_text(state)
    return "## Diff Risk Surface Registry" in text

def _risk_registry_section(text: str) -> str:
    marker = "## Diff Risk Surface Registry"
    if marker not in text:
        return ""
    section = text.split(marker, 1)[1]
    next_h2 = re.search(r"(?m)^## (?!#)", section)
    return section[: next_h2.start()] if next_h2 else section

def _attack_surface_risk_ids(state: ZeroMDASHState) -> set[str]:
    if not _attack_surface_has_risk_registry(state):
        return set()
    return {
        match.upper()
        for match in re.findall(
            r"(?m)^###\s+(RS-\d{3,})\b",
            _risk_registry_section(_attack_surface_text(state)),
            re.IGNORECASE,
        )
    }

def _diff_attack_surface_registry_ready(path: Path, state: ZeroMDASHState) -> bool:
    scope = state.get("scan_scope")
    if not isinstance(scope, dict) or scope.get("mode") != "diff":
        return True
    text = _read_text_lossy(path)
    if "## Diff Risk Surface Registry" not in text:
        return False
    section = _risk_registry_section(text)
    ids = [
        match.upper()
        for match in re.findall(
            r"(?m)^###\s+(RS-\d{3,})\b",
            section,
            re.IGNORECASE,
        )
    ]
    return (bool(ids) and len(ids) == len(set(ids))) or (
        "no diff-attributable security risk surfaces identified" in text.lower()
    )

def _ws(state: ZeroMDASHState) -> Workspace:
    return Workspace.open(state["workspace_root"], state["task_id"])

__all__ = ["_node_from_focus_key","_node_focus","_scope_context","_attack_surface_text","_attack_surface_has_risk_registry","_risk_registry_section","_attack_surface_risk_ids","_diff_attack_surface_registry_ready","_ws"]

