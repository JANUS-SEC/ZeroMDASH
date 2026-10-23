"""Agent-native attack-chain planner with deterministic prefiltering."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from zeromdash import prompts
from zeromdash.agents import AgentResult
from zeromdash.state import ChainCandidate, Primitive, ZeroMDASHState

from .core.chain_compatibility import (
    CHAIN_SCHEMA_VERSION,
    bind_requirements,
    capability_compatible,
    merge_global_constraints,
    primitive_gains,
    primitive_has_terminal_impact,
    primitive_requirements,
    rank_chain_candidate,
    stable_chain_id,
    stable_edge_id,
)
from .core.context import _node_focus, _ws
from .core.domain_registry import domain_registry_json
from .core.invocation import _invoke_with_output_retry
from .core.io import _planner_fallback_json, _try_json
from .core.primitive_qualification import capability_signature, normalize_capabilities


def _int_config(config: dict[str, Any], key: str, default: int) -> int:
    value = config.get(key, default)
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default


def _chain_config(state: ZeroMDASHState) -> dict[str, Any]:
    config = {
        "enabled": True,
        "max_length": 4,
        "max_successors_per_capability": 4,
        "beam_width": 64,
        "max_candidates_before_top_k": 200,
        "max_battle_rounds": 2,
        "attacker_entry_capabilities": [],
    }
    raw = state.get("chain_config")
    if isinstance(raw, dict):
        config.update(raw)
    return config


def _write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    os.replace(tmp, path)


def _append_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as fp:
        for record in records:
            fp.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def _attacker_entry(config: dict[str, Any]) -> dict[str, Any]:
    return {
        "capabilities": normalize_capabilities(config.get("attacker_entry_capabilities"))
    }


def _provider_capabilities(path: list[Primitive], attacker_entry: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    available: list[dict[str, Any]] = [
        cap for cap in (attacker_entry or {}).get("capabilities", []) if isinstance(cap, dict)
    ]
    for primitive in path:
        primitive_id = str(primitive.get("primitive_id") or "")
        for gained in primitive_gains(primitive):
            available.append({**gained, "provider_primitive_id": primitive_id})
    return available


def _candidate_from_path(
    path: list[Primitive],
    bindings: list[dict[str, Any]],
    global_constraints: dict[str, Any],
    primitives_by_id: dict[str, Primitive],
    attacker_entry: dict[str, Any],
) -> ChainCandidate:
    primitive_ids = [str(primitive.get("primitive_id") or "") for primitive in path]
    for index, binding in enumerate(bindings):
        binding.setdefault("edge_id", stable_edge_id(binding, index))
        binding["deterministic_advisory"] = _binding_advisory(
            binding,
            primitives_by_id=primitives_by_id,
        )
    candidate: ChainCandidate = {
        "schema_version": CHAIN_SCHEMA_VERSION,
        "ordered_primitive_ids": primitive_ids,
        "attacker_entry": attacker_entry,
        "bindings": bindings,
        "available_capabilities": _provider_capabilities(path, attacker_entry),
        "global_constraints": global_constraints,
        "expected_terminal_impact": path[-1].get("terminal_impact") if path else {},
        "status": "prefiltered",
        "pruning_context": {"source": "deterministic_prefilter"},
        "deterministic_advisories": [
            binding["deterministic_advisory"] for binding in bindings
        ],
    }
    candidate["chain_id"] = stable_chain_id(primitive_ids, bindings)
    candidate["rank_score"] = rank_chain_candidate(candidate, primitives_by_id)
    return candidate


def _direct_impact_present(impact: Any) -> bool:
    if not isinstance(impact, dict):
        return False
    for key in ("vulnerable_system", "subsequent_system"):
        system = impact.get(key)
        if isinstance(system, dict) and any(str(value).lower() in {"low", "high"} for value in system.values()):
            return True
    return False


def _initial_states(
    primitives: list[Primitive],
    primitives_by_id: dict[str, Primitive],
    pruning: list[dict[str, Any]],
    attacker_entry: dict[str, Any],
) -> list[tuple[list[Primitive], list[dict[str, Any]], dict[str, Any]]]:
    states: list[tuple[list[Primitive], list[dict[str, Any]], dict[str, Any]]] = []
    for primitive in primitives:
        primitive_id = str(primitive.get("primitive_id") or "")
        ok, bindings, failures = bind_requirements(
            primitive,
            _provider_capabilities([], attacker_entry),
            primitives_by_id=primitives_by_id,
        )
        if not ok:
            pruning.append(
                {
                    "primitive_id": primitive_id,
                    "reason": sorted(set(failures))[0] if failures else "missing_required_capability",
                    "stage": "initial",
                }
            )
            continue
        constraints, failures = merge_global_constraints([primitive])
        if failures:
            for failure in failures:
                pruning.append({"primitive_id": primitive_id, "reason": failure, "stage": "initial"})
            continue
        states.append(([primitive], bindings, constraints))
    return states


def _prefilter_chain_candidates(
    *,
    primitives: list[Primitive],
    primitives_by_id: dict[str, Primitive],
    config: dict[str, Any],
    max_candidates: int,
) -> tuple[list[ChainCandidate], list[dict[str, Any]]]:
    pruning: list[dict[str, Any]] = []
    max_length = _int_config(config, "max_length", 4)
    max_successors = _int_config(config, "max_successors_per_capability", 4)
    beam_width = _int_config(config, "beam_width", 64)
    attacker_entry = _attacker_entry(config)
    candidates_by_id: dict[str, ChainCandidate] = {}
    frontier = _initial_states(primitives, primitives_by_id, pruning, attacker_entry)
    while frontier and len(candidates_by_id) < max_candidates:
        next_frontier: list[tuple[list[Primitive], list[dict[str, Any]], dict[str, Any]]] = []
        for path, path_bindings, _constraints in frontier:
            if len(path) >= max_length:
                pruning.append(
                    {
                        "path": [primitive.get("primitive_id") for primitive in path],
                        "reason": "max_length",
                    }
                )
                continue
            available = _provider_capabilities(path, attacker_entry)
            successor_count = 0
            used = {str(primitive.get("primitive_id") or "") for primitive in path}
            for successor in primitives:
                successor_id = str(successor.get("primitive_id") or "")
                if not primitive_requirements(successor):
                    pruning.append(
                        {
                            "path": [primitive.get("primitive_id") for primitive in path],
                            "primitive_id": successor_id,
                            "reason": "missing_required_capability",
                            "detail": "successor has no requirement to bind to the existing capability closure",
                        }
                    )
                    continue
                if successor_id in used:
                    pruning.append(
                        {
                            "path": sorted(used),
                            "primitive_id": successor_id,
                            "reason": "cycle",
                        }
                    )
                    continue
                ok, bindings, bind_failures = bind_requirements(
                    successor,
                    available,
                    primitives_by_id=primitives_by_id,
                )
                if not ok:
                    for reason in bind_failures:
                        pruning.append(
                            {
                                "path": [primitive.get("primitive_id") for primitive in path],
                                "primitive_id": successor_id,
                                "reason": reason,
                            }
                        )
                    continue
                new_path = [*path, successor]
                constraints, constraint_failures = merge_global_constraints(new_path)
                if constraint_failures:
                    for reason in constraint_failures:
                        pruning.append(
                            {
                                "path": [primitive.get("primitive_id") for primitive in new_path],
                                "reason": reason,
                            }
                        )
                    continue
                successor_count += 1
                if successor_count > max_successors:
                    pruning.append(
                        {
                            "path": [primitive.get("primitive_id") for primitive in path],
                            "primitive_id": successor_id,
                            "reason": "successor_cap",
                        }
                    )
                    continue
                merged_bindings = [*path_bindings, *bindings]
                if primitive_has_terminal_impact(successor):
                    candidate = _candidate_from_path(
                        new_path,
                        merged_bindings,
                        constraints,
                        primitives_by_id,
                        attacker_entry,
                    )
                    candidates_by_id.setdefault(str(candidate["chain_id"]), candidate)
                next_frontier.append((new_path, merged_bindings, constraints))
        next_frontier.sort(
            key=lambda item: (
                -sum(
                    float((primitive.get("confirmation") or {}).get("confidence") or 0.0)
                    for primitive in item[0]
                    if isinstance(primitive.get("confirmation"), dict)
                ),
                len(item[0]),
            )
        )
        if len(next_frontier) > beam_width:
            for dropped_path, _, _ in next_frontier[beam_width:]:
                pruning.append(
                    {
                        "path": [primitive.get("primitive_id") for primitive in dropped_path],
                        "reason": "beam_width",
                    }
                )
        frontier = next_frontier[:beam_width]

    return sorted(
        candidates_by_id.values(),
        key=lambda item: (-float(item.get("rank_score") or 0.0), str(item.get("chain_id") or "")),
    ), pruning


def _binding_error(
    binding: Any,
    ordered_ids: list[str],
    primitives_by_id: dict[str, Primitive],
    attacker_entry: dict[str, Any],
) -> str:
    if not isinstance(binding, dict):
        return "binding is not an object"
    consumer_id = str(binding.get("consumer_primitive_id") or "")
    if consumer_id not in primitives_by_id:
        return f"binding references unknown consumer primitive: {consumer_id}"
    if consumer_id not in ordered_ids:
        return f"binding consumer is not in ordered_primitive_ids: {consumer_id}"
    provider = binding.get("provider")
    if not isinstance(provider, dict):
        return f"binding for {consumer_id} has no provider object"
    evidence = binding.get("evidence")
    if not isinstance(evidence, list) or not any(str(item or "").strip() for item in evidence):
        return f"binding for {consumer_id} has no evidence"
    provider_type = str(provider.get("type") or "")
    required_signature = capability_signature(binding.get("required_capability") or {})
    known_requirements = {
        capability_signature(item)
        for item in primitive_requirements(primitives_by_id[consumer_id])
    }
    if required_signature not in known_requirements:
        return f"binding for {consumer_id} references an unknown confirmed requirement"
    provider_signature = capability_signature(provider.get("capability") or {})
    if provider_type == "attacker_entry":
        entry_capabilities = {
            capability_signature(item)
            for item in normalize_capabilities(attacker_entry.get("capabilities"))
        }
        return "" if provider_signature in entry_capabilities else (
            f"binding for {consumer_id} invents an attacker-entry capability"
        )
    if provider_type != "primitive":
        return f"binding for {consumer_id} has invalid provider type: {provider_type}"
    provider_id = str(provider.get("primitive_id") or "")
    if provider_id not in primitives_by_id:
        return f"binding for {consumer_id} references unknown provider primitive: {provider_id}"
    if provider_id not in ordered_ids:
        return f"binding provider is not in ordered_primitive_ids: {provider_id}"
    if ordered_ids.index(provider_id) >= ordered_ids.index(consumer_id):
        return f"binding provider {provider_id} does not precede consumer {consumer_id}"
    known_gains = {
        capability_signature(item)
        for item in primitive_gains(primitives_by_id[provider_id])
    }
    if provider_signature not in known_gains:
        return f"binding for {consumer_id} invents a capability not gained by {provider_id}"
    return ""


def _binding_advisory(
    binding: dict[str, Any],
    *,
    primitives_by_id: dict[str, Primitive],
) -> dict[str, Any]:
    provider = binding.get("provider") if isinstance(binding.get("provider"), dict) else {}
    provider_id = str(provider.get("primitive_id") or "")
    consumer_id = str(binding.get("consumer_primitive_id") or "")
    compatible, reasons = capability_compatible(
        provider.get("capability") if isinstance(provider.get("capability"), dict) else {},
        binding.get("required_capability") if isinstance(binding.get("required_capability"), dict) else {},
        provider_primitive=primitives_by_id.get(provider_id),
        consumer_primitive=primitives_by_id.get(consumer_id),
    )
    return {
        "kind": "capability_compatibility",
        "edge_id": str(binding.get("edge_id") or ""),
        "compatible": compatible,
        "reasons": reasons,
        "authority": "advisory",
    }


def _requirement_binding_errors(
    raw: dict[str, Any],
    ordered_ids: list[str],
    primitives_by_id: dict[str, Primitive],
) -> list[str]:
    bindings = [item for item in raw.get("bindings") or [] if isinstance(item, dict)]
    errors: list[str] = []
    for primitive_id in ordered_ids:
        required_signatures = sorted(
            capability_signature(item)
            for item in primitive_requirements(primitives_by_id[primitive_id])
        )
        bound_signatures = sorted(
            capability_signature(binding.get("required_capability") or {})
            for binding in bindings
            if str(binding.get("consumer_primitive_id") or "") == primitive_id
        )
        if bound_signatures != required_signatures:
            errors.append(
                f"primitive {primitive_id} bindings do not cover its confirmed "
                "requirements exactly once"
            )
    return errors


def _normalize_agent_plan_payload(
    payload: Any,
    *,
    primitives_by_id: dict[str, Primitive],
    default_attacker_entry: dict[str, Any],
) -> tuple[list[ChainCandidate], list[str]]:
    if isinstance(payload, list):
        raw_chains = payload
    elif isinstance(payload, dict) and isinstance(payload.get("chains"), list):
        raw_chains = payload["chains"]
    else:
        return [], ["chain plan must be a JSON object with chains[] or a JSON array"]

    primitive_ids = set(primitives_by_id)
    chains: list[ChainCandidate] = []
    errors: list[str] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_chains):
        if not isinstance(raw, dict):
            errors.append(f"chains[{index}] is not an object")
            continue
        ordered_ids = [str(item) for item in raw.get("ordered_primitive_ids") or [] if str(item or "")]
        if len(ordered_ids) < 2:
            errors.append(f"chains[{index}] requires at least two ordered_primitive_ids")
            continue
        unknown = [primitive_id for primitive_id in ordered_ids if primitive_id not in primitive_ids]
        if unknown:
            errors.append(f"chains[{index}] references unknown primitive id(s): {', '.join(unknown)}")
            continue
        if len(set(ordered_ids)) != len(ordered_ids):
            errors.append(f"chains[{index}] repeats a primitive id")
            continue
        bindings = [dict(item) for item in raw.get("bindings") or [] if isinstance(item, dict)]
        if not bindings:
            errors.append(f"chains[{index}] requires at least one binding")
            continue
        for binding_index, binding in enumerate(bindings):
            binding.setdefault("edge_id", stable_edge_id(binding, binding_index))
            binding["deterministic_advisory"] = _binding_advisory(
                binding,
                primitives_by_id=primitives_by_id,
            )
        candidate_attacker_entry = (
            raw.get("attacker_entry")
            if isinstance(raw.get("attacker_entry"), dict)
            else default_attacker_entry
        )
        binding_errors = [
            err
            for err in (
                _binding_error(
                    binding,
                    ordered_ids,
                    primitives_by_id,
                    candidate_attacker_entry,
                )
                for binding in bindings
            )
            if err
        ]
        if binding_errors:
            errors.append(f"chains[{index}] invalid bindings: {'; '.join(binding_errors)}")
            continue
        coverage_errors = _requirement_binding_errors(raw, ordered_ids, primitives_by_id)
        if coverage_errors:
            errors.append(f"chains[{index}] incomplete bindings: {'; '.join(coverage_errors)}")
            continue
        expected_impact = raw.get("expected_terminal_impact")
        if not isinstance(expected_impact, dict):
            expected_impact = primitives_by_id[ordered_ids[-1]].get("terminal_impact") or {}
        candidate: ChainCandidate = {
            "schema_version": CHAIN_SCHEMA_VERSION,
            "ordered_primitive_ids": ordered_ids,
            "attacker_entry": candidate_attacker_entry,
            "bindings": bindings,
            "available_capabilities": raw.get("available_capabilities")
            if isinstance(raw.get("available_capabilities"), list)
            else _provider_capabilities([primitives_by_id[item] for item in ordered_ids], default_attacker_entry),
            "global_constraints": raw.get("global_constraints") if isinstance(raw.get("global_constraints"), dict) else {},
            "expected_terminal_impact": expected_impact,
            "emergent_impact_hypothesis": raw.get("emergent_impact_hypothesis")
            if isinstance(raw.get("emergent_impact_hypothesis"), dict)
            else {},
            "status": str(raw.get("status") or "planned"),
            "pruning_context": raw.get("pruning_context") if isinstance(raw.get("pruning_context"), dict) else {},
            "deterministic_advisories": [
                *([item for item in raw.get("deterministic_advisories") or [] if isinstance(item, dict)]),
                *[binding["deterministic_advisory"] for binding in bindings],
            ],
        }
        if raw.get("rank_score") is not None:
            try:
                candidate["rank_score"] = float(raw.get("rank_score"))
            except (TypeError, ValueError):
                candidate["rank_score"] = rank_chain_candidate(candidate, primitives_by_id)
        else:
            candidate["rank_score"] = rank_chain_candidate(candidate, primitives_by_id)
        candidate["chain_id"] = stable_chain_id(ordered_ids, bindings)
        chain_id = str(candidate["chain_id"])
        if chain_id in seen:
            continue
        seen.add(chain_id)
        chains.append(candidate)
    return chains, errors


def _agent_plan_payload(res: AgentResult) -> Any:
    payload = _try_json(res.stdout, fallback=None)
    if payload is not None:
        return payload
    return _planner_fallback_json(res)


def plan_chains(state: ZeroMDASHState, *, backends=None) -> dict:
    ws = _ws(state)
    config = _chain_config(state)
    disabled = set(state.get("disabled_nodes") or [])
    top_k = int((state.get("top_K") or {}).get("chain") or 16)
    plan_path = ws.state_path("chain_plan.json")
    prefilter_path = ws.log_path("review_log") / "chain_prefilter.json"
    pruning_path = ws.log_path("review_log") / "chain_pruning.jsonl"
    if config.get("enabled") is False or "plan_chains" in disabled or "chain_investigate_subtask" in disabled:
        payload = {"schema_version": CHAIN_SCHEMA_VERSION, "chains": [], "disabled": True}
        _write_json_atomic(plan_path, payload)
        _write_json_atomic(prefilter_path, payload)
        _append_jsonl(pruning_path, [])
        return {"chain_plan": [], "chain_plan_path": str(plan_path)}

    primitives = [primitive for primitive in state.get("chain_pool", []) if isinstance(primitive, dict)]
    primitives_by_id = {
        str(primitive.get("primitive_id") or ""): primitive
        for primitive in primitives
        if str(primitive.get("primitive_id") or "")
    }
    if len(primitives) < 2:
        payload = {
            "schema_version": CHAIN_SCHEMA_VERSION,
            "chains": [],
            "reason": "fewer_than_two_primitives",
        }
        _write_json_atomic(plan_path, payload)
        _write_json_atomic(prefilter_path, payload)
        _append_jsonl(pruning_path, [])
        return {"chain_plan": [], "chain_plan_path": str(plan_path)}

    max_candidates = _int_config(config, "max_candidates_before_top_k", 200)
    attacker_entry = _attacker_entry(config)
    prefilter_candidates, pruning = _prefilter_chain_candidates(
        primitives=primitives,
        primitives_by_id=primitives_by_id,
        config=config,
        max_candidates=max_candidates,
    )
    _write_json_atomic(
        prefilter_path,
        {
            "schema_version": CHAIN_SCHEMA_VERSION,
            "chain_count": len(prefilter_candidates),
            "config": config,
            "chains": prefilter_candidates,
        },
    )
    _append_jsonl(pruning_path, pruning)

    focus = _node_focus(state, "plan_chains_focus")
    selected: list[ChainCandidate] = []
    validation_errors: list[str] = []

    def validate(res: AgentResult) -> tuple[bool, str]:
        nonlocal selected, validation_errors
        payload = _agent_plan_payload(res)
        selected, validation_errors = _normalize_agent_plan_payload(
            payload,
            primitives_by_id=primitives_by_id,
            default_attacker_entry=attacker_entry,
        )
        if validation_errors:
            return False, "; ".join(validation_errors[:5])
        if len(selected) > top_k:
            validation_errors = [f"agent returned {len(selected)} chains, exceeding top_K.chain={top_k}"]
            selected = []
            return False, validation_errors[0]
        return True, ""

    prompt = prompts.PLAN_CHAINS.format(
        target=state.get("target", ""),
        repo_path=state.get("repo_path", ""),
        focus=focus or "(none)",
        top_k=top_k,
        chain_pool_json=json.dumps(primitives, ensure_ascii=False, indent=2),
        domain_registry_json=domain_registry_json(state),
        prefilter_json=json.dumps(
            {
                "schema_version": CHAIN_SCHEMA_VERSION,
                "chain_count": len(prefilter_candidates),
                "chains": prefilter_candidates,
                "pruning_log": str(pruning_path),
            },
            ensure_ascii=False,
            indent=2,
        ),
    )
    _, errors = _invoke_with_output_retry(
        ws,
        "plan_chains",
        prompt,
        backends,
        state,
        output_desc=f"agent-produced chain plan JSON at {plan_path}",
        validate=validate,
        artifact_filenames=("chain_plan.json", "plan.json"),
        focus=focus,
    )
    if errors:
        _write_json_atomic(
            plan_path,
            {
                "schema_version": CHAIN_SCHEMA_VERSION,
                "chain_count": 0,
                "total_prefilter_candidates": len(prefilter_candidates),
                "config": config,
                "chains": [],
                "agent_errors": errors,
                "validation_errors": validation_errors,
                "prefilter_path": str(prefilter_path),
            },
        )
        return {"chain_plan": [], "chain_plan_path": str(plan_path), "errors": errors}

    ordered = sorted(
        selected,
        key=lambda item: (-float(item.get("rank_score") or 0.0), str(item.get("chain_id") or "")),
    )[:top_k]
    _write_json_atomic(
        plan_path,
        {
            "schema_version": CHAIN_SCHEMA_VERSION,
            "chain_count": len(ordered),
            "total_prefilter_candidates": len(prefilter_candidates),
            "config": config,
            "chains": ordered,
            "prefilter_path": str(prefilter_path),
            "planned_by": "agent",
        },
    )
    return {
        "chain_plan": ordered,
        "chain_plan_path": str(plan_path),
    }


__all__ = ["plan_chains"]
