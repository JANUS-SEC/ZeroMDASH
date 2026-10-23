"""Build a scenario-level attack-surface model from source workspace snapshots."""

from __future__ import annotations

import json
from typing import Any

from zeromdash import prompts
from zeromdash.agents import AgentResult
from zeromdash.gather_state import GatherState

from .core.context import _node_focus, _ws
from .core.gather_qualification import validate_cross_target_registry
from .core.invocation import _invoke_with_output_retry
from .core.io import _file_has_text, _reset_file_output, _try_json
from .materialize_chain_pool import _write_json_atomic


def gather_analyze_attack_surface(state: GatherState, *, backends=None) -> dict:
    ws = _ws(state)
    out = ws.main_path("attack_surface") / "gather_attack_surface.md"
    registry_out = ws.main_path("attack_surface") / "cross_target_registry.json"
    targets = list(state.get("gather_targets") or [])
    target_ids = {str(item.get("target_id") or "") for item in targets}
    focus = _node_focus(state, "gather_analyze_attack_surface_focus")
    parsed: dict[str, Any] | None = None
    validation_failure = ""
    prompt = prompts.GATHER_ANALYZE_ATTACK_SURFACE.format(
        scenario_name=state.get("scenario_name", "gather"),
        scenario=state.get("scenario", ""),
        targets_json=json.dumps(targets, ensure_ascii=False, indent=2),
        max_pair_passes=int((state.get("gather_config") or {}).get("max_pair_passes") or 12),
        out_path=out,
        registry_path=registry_out,
        focus=focus,
    )

    def reset() -> None:
        _reset_file_output(out)
        _reset_file_output(registry_out)

    def materialize(res: AgentResult) -> None:
        payload = _try_json(res.stdout, fallback=None)
        if isinstance(payload, dict) and not registry_out.is_file():
            _write_json_atomic(registry_out, payload)

    def validate(res: AgentResult) -> tuple[bool, str]:
        nonlocal parsed, validation_failure
        payload = _try_json(res.stdout, fallback=None)
        if registry_out.is_file():
            try:
                payload = json.loads(registry_out.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                payload = None
        parsed, validation_failure = validate_cross_target_registry(
            payload,
            target_ids=target_ids,
        )
        if parsed is None:
            return False, validation_failure
        if not _file_has_text(out):
            return False, "gather attack-surface Markdown was not written"
        return True, ""

    _, errors = _invoke_with_output_retry(
        ws,
        "gather_analyze_attack_surface",
        prompt,
        backends,
        state,
        output_desc=f"{out} and {registry_out}",
        validate=validate,
        materialize=materialize,
        reset=reset,
        artifact_filenames=("cross_target_registry.json", "output.json"),
        focus=focus,
        additional_read_roots=list(state.get("source_read_roots") or []),
    )
    if parsed is None:
        parsed = {
            "schema_version": "1.0",
            "scenario": state.get("scenario", ""),
            "targets": targets,
            "interfaces": [],
            "data_flows": [],
            "cross_target_invariants": [],
            "deployment_assumptions": [],
            "unresolved_gaps": [validation_failure or "analysis failed"],
        }
    _write_json_atomic(registry_out, parsed)
    return {
        "gather_attack_surface": str(out),
        "cross_target_registry_path": str(registry_out),
        "cross_target_registry": parsed,
        "errors": errors,
    }


__all__ = ["gather_analyze_attack_surface"]
