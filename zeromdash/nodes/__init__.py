"""Public facade for ZeroMDASH LangGraph nodes.

Node implementations live in focused modules.  This facade intentionally
preserves the historical ``zeromdash.nodes`` API, including private helpers
used by integrations and tests during the staged refactor.
"""

from __future__ import annotations

import sys
import types
from importlib import import_module
from types import ModuleType
from typing import Any

from .core import CORE_MODULES
from . import polish_report as _polish_report_module
from . import summary as _summary_module
from zeromdash.poc_gen import node as _poc_gen_module


_IMPLEMENTATION_MODULES: list[ModuleType] = []


def _export_module(module: ModuleType) -> None:
    if module not in _IMPLEMENTATION_MODULES:
        _IMPLEMENTATION_MODULES.append(module)
    for name, value in vars(module).items():
        if name.startswith("__"):
            continue
        globals()[name] = value


for _core_module in CORE_MODULES:
    _export_module(_core_module)
_export_module(_polish_report_module)
_export_module(_summary_module)
_export_module(_poc_gen_module)

_NODE_MODULE_NAMES = (
    "fetch_target_repo",
    "prepare_scan_scope",
    "search_spec",
    "search_fuzz_driver",
    "search_similar_software",
    "search_similar_history",
    "search_target_history",
    "search_new_feature",
    "analyze_attack_surface",
    "plan_by_spec",
    "plan_by_vuln_similar",
    "plan_by_vuln_patch",
    "plan_by_new_feature",
    "dispatch_subtasks",
    "investigate_subtask",
    "critic_subtask",
    "finalize_subtask",
    "materialize_chain_pool",
    "plan_chains",
    "dispatch_chains",
    "chain_investigate_subtask",
    "chain_critic_subtask",
    "finalize_chain_subtask",
    "prepare_report_groups",
    "gather_analyze_attack_surface",
    "gather_plan_chains",
    "dispatch_gather_chains",
    "gather_chain_investigate_subtask",
    "gather_chain_critic_subtask",
    "gather_finalize_chain_subtask",
    "gather_prepare_report_groups",
    "gather_summary",
)
for _module_name in _NODE_MODULE_NAMES:
    _export_module(import_module(f"{__name__}.{_module_name}"))

# Deprecated public aliases.
dispatch_subagents = dispatch_subtasks
collect_selected_subagent_statuses = collect_selected_subtask_statuses
investigate_subagent = investigate_subtask
critic_one = critic_subtask
finalize_subagent = finalize_subtask
_PUBLIC_ALIASES = {
    "investigate_subagent": "investigate_subtask",
    "critic_one": "critic_subtask",
}


class _NodesFacade(types.ModuleType):
    """Mirror monkeypatches onto implementation modules.

    Existing tests and callers patch helpers such as ``nodes._invoke``.  Node
    implementations may now live in another module, so assignments on the
    facade are propagated to every implementation module that defines the same
    symbol.
    """

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        canonical = _PUBLIC_ALIASES.get(name, name)
        if canonical != name:
            super().__setattr__(canonical, value)
        for module in tuple(_IMPLEMENTATION_MODULES):
            for target in {name, canonical}:
                if hasattr(module, target):
                    setattr(module, target, value)


sys.modules[__name__].__class__ = _NodesFacade


def _register_module(module: ModuleType) -> None:
    """Register and export one focused implementation module."""
    _export_module(module)
