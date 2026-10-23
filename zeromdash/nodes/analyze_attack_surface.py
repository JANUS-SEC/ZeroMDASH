"""LangGraph node implementation: analyze_attack_surface."""

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

from .core.context import (
    _diff_attack_surface_registry_ready,
    _node_focus,
    _ws,
)
from .core.domain_registry import read_domain_registry, validate_domain_registry
from .core.invocation import (
    _invoke_with_output_retry,
    _read_preset_attack_surface,
    _seeded_attack_surface_has_append,
)
from .core.io import (
    _file_has_text,
    _reset_file_output,
    _write_stdout_fallback_file,
)

def analyze_attack_surface(state: ZeroMDASHState, *, backends=None) -> dict:
    ws = _ws(state)
    out = ws.main_path("attack_surface") / "attack_surface.md"
    registry_out = ws.main_path("attack_surface") / "domain_invariant_registry.json"
    focus = _node_focus(state, "analyze_attack_surface_focus")
    preset_text, preset_errors = _read_preset_attack_surface(state)
    prompt = prompts.ATTACK_SURFACE.format(
        target=state["target"],
        focus=focus,
        target_writeups_dir=ws.main_path("writeup"),
        similar_writeup_dirs=state.get("similar_writeups", []),
        spec_dir=ws.main_path("spec"),
        fuzz_drivers=state.get("fuzz_drivers", []),
        feature_dir=ws.main_path("feature"),
        out_path=out,
        domain_registry_path=registry_out,
    )

    def reset_output() -> None:
        _reset_file_output(out)
        _reset_file_output(registry_out)
        if preset_text:
            out.write_text(preset_text.rstrip() + "\n\n")

    def materialize(res: AgentResult) -> None:
        if preset_text:
            if not _seeded_attack_surface_has_append(out, preset_text) and res.stdout.strip():
                with out.open("a") as fp:
                    fp.write(res.stdout.strip() + "\n")
            return
        _write_stdout_fallback_file(out, res.stdout)

    def validate(res: AgentResult) -> bool:
        del res
        try:
            registry_payload = json.loads(registry_out.read_text())
        except (OSError, json.JSONDecodeError):
            return False
        registry, _ = validate_domain_registry(registry_payload)
        if registry is None or registry.get("status") == "legacy_unavailable":
            return False
        if preset_text:
            return (
                _seeded_attack_surface_has_append(out, preset_text)
                and _diff_attack_surface_registry_ready(out, state)
            )
        return _file_has_text(out) and _diff_attack_surface_registry_ready(out, state)

    _, errors = _invoke_with_output_retry(
        ws,
        "analyze_attack_surface",
        prompt,
        backends,
        state,
        output_desc=f"{out} and {registry_out}",
        reset=reset_output,
        materialize=materialize,
        validate=validate,
        focus=focus,
    )
    registry_payload = read_domain_registry(
        registry_out,
        target=str(state.get("target") or ""),
    )
    return {
        "attack_surface": str(out),
        "domain_registry_path": str(registry_out),
        "domain_registry": registry_payload,
        "errors": preset_errors + errors,
    }

__all__ = ["analyze_attack_surface"]

