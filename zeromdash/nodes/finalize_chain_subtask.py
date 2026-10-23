"""Finalize one chain subtask after chain investigate/critic battle."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from zeromdash import prompts
from zeromdash.agents import normalize_agent_name
from zeromdash.cvss4 import CVSS4ValidationError, has_direct_impact, score_base_vector
from zeromdash.state import ZeroMDASHState

from .core.chain_qualification import (
    chain_investigation_json,
    close_chain_candidate,
    coerce_chain_review,
)
from .core.config import (
    _agent_configs_with_node_variant,
    agent_config_variants_for_node,
)
from .core.context import _node_focus, _ws
from .core.domain_registry import domain_registry_from_state, domain_registry_json
from .core.invocation import (
    _agent_errors,
    _make_agent,
    _run_agent_with_config,
    _selected_log_dir,
)
from .core.qualification import _direct_impact_metrics, _direct_impact_present
from .core.recovery import recover_runtime


FINALIZER_NODE = "chain_finalizer_subtask"


def _write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    os.replace(tmp, path)


def _dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return []


def _string(value: Any) -> str:
    return str(value or "").strip()


def _try_json_object(value: str) -> dict[str, Any]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _validate_finalizer_verdict(verdict: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if _string(verdict.get("decision")) not in {"accept", "reject"}:
        failures.append("finalizer decision must be accept or reject")
    for key in (
        "chain_is_valid",
        "deterministic_failures_are_contract_only",
        "all_primitives_confirmed",
        "bindings_valid",
        "global_constraints_satisfiable",
        "no_external_primitives_required",
    ):
        if not isinstance(verdict.get(key), bool):
            failures.append(f"finalizer {key} must be boolean")
    if not _string(verdict.get("reasoning")):
        failures.append("finalizer reasoning is empty")
    if not _string(verdict.get("title")):
        failures.append("finalizer title is empty")
    if not _string(verdict.get("detail")):
        failures.append("finalizer detail is empty")
    direct_impact = _dict(verdict.get("direct_security_impact"))
    if not _direct_impact_present(direct_impact):
        failures.append("finalizer direct_security_impact has no direct C/I/A impact")
    vector = _string(verdict.get("cvss4_vector"))
    try:
        score = score_base_vector(vector)
    except CVSS4ValidationError as exc:
        failures.append(f"finalizer invalid CVSS v4.0 Base vector: {exc}")
    else:
        declared = _direct_impact_metrics(direct_impact)
        if declared is not None and any(
            score.metrics[metric] != impact for metric, impact in declared.items()
        ):
            failures.append("finalizer direct_security_impact does not match CVSS impact metrics")
        if not has_direct_impact(score):
            failures.append("finalizer CVSS v4.0 vector has no direct impact")
    try:
        confidence = float(verdict.get("confidence"))
    except (TypeError, ValueError):
        failures.append("finalizer confidence must be numeric")
    else:
        if confidence < 0.0 or confidence > 1.0:
            failures.append("finalizer confidence must be between 0 and 1")
    if not isinstance(verdict.get("evidence"), dict):
        failures.append("finalizer evidence must be an object")
    return failures


@recover_runtime(node="chain_finalizer_subtask")
def _run_finalizer_agent(
    state: ZeroMDASHState,
    *,
    candidate: dict[str, Any],
    investigation: dict[str, Any],
    review: dict[str, Any],
    failures: list[str],
    backends=None,
) -> tuple[dict[str, Any] | None, list[str]]:
    ws = _ws(state)
    chain_id = _string(candidate.get("chain_id"))
    prompt = prompts.CHAIN_FINALIZER_SUBTASK.format(
        focus=_node_focus(state, "chain_finalizer_subtask_focus"),
        chain_candidate_json=json.dumps(candidate, ensure_ascii=False, indent=2),
        chain_pool_json=json.dumps(state.get("chain_pool") or [], ensure_ascii=False, indent=2),
        chain_investigation_json=json.dumps(investigation, ensure_ascii=False, indent=2),
        chain_review_json=json.dumps(review, ensure_ascii=False, indent=2),
        failure_reasons_json=json.dumps(failures, ensure_ascii=False, indent=2),
        domain_registry_json=domain_registry_json(state),
        repo_path=state["repo_path"],
        attack_surface=state.get("attack_surface", ""),
        spec_doc=state.get("spec_doc", ""),
        writeup_dir=str(ws.main_path("writeup")),
        patch_dir=str(ws.main_path("patch")),
        feature_docs=", ".join(state.get("feature_docs") or []),
    )
    selected_dir = _selected_log_dir(state)
    errors: list[str] = []
    variants = agent_config_variants_for_node(
        FINALIZER_NODE,
        backends,
        state.get("agent_configs"),
    )
    for variant_index, variant in enumerate(variants, start=1):
        backend_name = normalize_agent_name(variant["runtime"])
        variant_configs = _agent_configs_with_node_variant(
            state.get("agent_configs"),
            FINALIZER_NODE,
            variant,
        )
        sub_ws = ws.prepare_sub_workspace(
            node=FINALIZER_NODE,
            subtask_id=chain_id,
            backend=backend_name,
            extra_context={
                "chain_id": chain_id,
                "fallback_index": variant_index - 1,
                "fallback_count": len(variants) - 1,
            },
        )
        res = _run_agent_with_config(
            _make_agent(backend_name),
            FINALIZER_NODE,
            backend_name,
            prompt,
            sub_ws,
            None,
            variant_configs,
            state.get("agent_config_task_types"),
            selected_dir,
        )
        log = (
            selected_dir / "review_log" / f"{chain_id}.chain_finalizer.log"
            if selected_dir
            else ws.log_path("review_log") / f"{chain_id}.chain_finalizer.log"
        )
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open("a") as fp:
            fp.write(f"\n--- finalizer attempt {variant_index} ---\n{res.stdout}\n")
        runtime_errors = _agent_errors(res, FINALIZER_NODE, chain_id, log_path=log)
        parsed = _try_json_object(res.stdout)
        validation_errors = _validate_finalizer_verdict(parsed) if parsed else ["finalizer output is not a JSON object"]
        if not runtime_errors and not validation_errors:
            return parsed, []
        errors = runtime_errors + validation_errors
    return None, errors


def _finding_from_finalizer(
    *,
    candidate: dict[str, Any],
    investigation: dict[str, Any],
    review: dict[str, Any],
    verdict: dict[str, Any],
    failures: list[str],
) -> dict[str, Any]:
    score = score_base_vector(_string(verdict.get("cvss4_vector")))
    return {
        "schema_version": "2.0",
        "kind": "chain",
        "chain_id": _string(candidate.get("chain_id")),
        "subtask_id": _string(candidate.get("chain_id")),
        "title": _string(verdict.get("title")),
        "detail": _string(verdict.get("detail")),
        "evidence": _dict(verdict.get("evidence")),
        "severity": score.severity,
        "confidence": float(verdict.get("confidence", 0.0)),
        "review": {
            **review,
            "finalizer_verdict": verdict,
            "deterministic_gate_failures": list(failures),
        },
        "iterations": int(review.get("iterations") or investigation.get("iterations") or 0),
        "selected_skills": _list(review.get("selected_skills")),
        "disposition": "confirmed_vulnerability",
        "qualification_gate_passed": True,
        "cvss_applicable": True,
        "cvss4_vector": score.vector,
        "cvss4_score": score.score,
        "direct_security_impact": _dict(verdict.get("direct_security_impact")),
        "violated_security_property": _string(verdict.get("violated_security_property")),
        "documented_expected_behavior": False,
        "security_contract_violation": True,
        "standalone_security_impact": False,
        "required_external_primitives": [],
        "ordered_primitive_ids": _list(investigation.get("ordered_primitive_ids"))
        or _list(candidate.get("ordered_primitive_ids")),
        "source_primitive_ids": _list(investigation.get("ordered_primitive_ids"))
        or _list(candidate.get("ordered_primitive_ids")),
        "bindings": _list(investigation.get("bindings")) or _list(candidate.get("bindings")),
        "global_constraints": _dict(investigation.get("global_constraints"))
        or _dict(candidate.get("global_constraints")),
        "deterministic_advisories": _list(candidate.get("deterministic_advisories")),
        "attacker_entry": _dict(candidate.get("attacker_entry")),
        "attack_path": _list(investigation.get("attack_path")),
        "binding_claims": _list(investigation.get("binding_claims")),
        "emergent_transitions": _list(investigation.get("emergent_transitions")),
        "blocking_unmet_facts": _list(investigation.get("blocking_unmet_facts")),
        "validation_gaps": _list(investigation.get("validation_gaps")),
        "deployment_constraints": _list(investigation.get("deployment_constraints")),
        "impact_limits": _list(investigation.get("impact_limits")),
        "fact_verdicts": _list(review.get("fact_verdicts")),
        "closure_verdict": _string(review.get("closure_verdict")),
        "scope_verdict": _string(verdict.get("scope_verdict"))
        or _string(review.get("scope_verdict"))
        or "full_repository",
        "gate_decision": _string(verdict.get("gate_decision"))
        or _string(review.get("gate_decision"))
        or "ignore",
        "deterministic_gate_failures": list(failures),
    }


def _agent_finalizer_allowed(review: dict[str, Any], failures: list[str]) -> bool:
    if _string(review.get("verdict")).lower() != "confirm":
        return False
    if review.get("all_primitives_confirmed") is not True:
        return False
    if review.get("bindings_valid") is not True:
        return False
    if review.get("global_constraints_satisfiable") is not True:
        return False
    if _list(review.get("required_external_primitives")):
        return False
    if any(failure == "chain critic did not confirm" for failure in failures):
        return False
    if any(failure == "depends on unconfirmed external primitive" for failure in failures):
        return False
    return True


def finalize_chain_subtask(state: ZeroMDASHState, *, backends=None) -> dict:
    ws = _ws(state)
    candidate = state["chain_candidate"]
    chain_id = str(candidate.get("chain_id") or "")
    investigation = chain_investigation_json(state.get("chain_investigation", ""))
    review = coerce_chain_review(state.get("chain_review") or {})
    review["iterations"] = int(state.get("iteration", 0))

    finding, failed_candidate, failures = close_chain_candidate(
        candidate=candidate,
        investigation=investigation,
        review=review,
        chain_pool=list(state.get("chain_pool") or []),
        domain_registry=domain_registry_from_state(state),
    )
    selected_dir = _selected_log_dir(state)
    if finding is not None:
        out_dir = selected_dir / "chain_res" if selected_dir else ws.log_path("chain_res")
        out = out_dir / f"{chain_id}.json"
        payload = {
            "schema_version": "2.0",
            "outcome_type": "chain_finding",
            "chain_id": chain_id,
            "finding": finding,
            "review": review,
            "history": state.get("chain_review_history", []),
        }
        _write_json_atomic(out, payload)
        return {"chain_findings": [finding]}

    if _agent_finalizer_allowed(review, failures):
        finalizer_verdict, finalizer_errors = _run_finalizer_agent(
            state,
            candidate=dict(candidate),
            investigation=investigation,
            review=review,
            failures=list(failures),
            backends=backends,
        )
        if finalizer_verdict and _string(finalizer_verdict.get("decision")) == "accept":
            if (
                finalizer_verdict.get("chain_is_valid") is True
                and finalizer_verdict.get("deterministic_failures_are_contract_only") is True
                and finalizer_verdict.get("all_primitives_confirmed") is True
                and finalizer_verdict.get("bindings_valid") is True
                and finalizer_verdict.get("global_constraints_satisfiable") is True
                and finalizer_verdict.get("no_external_primitives_required") is True
            ):
                finding = _finding_from_finalizer(
                    candidate=dict(candidate),
                    investigation=investigation,
                    review=review,
                    verdict=finalizer_verdict,
                    failures=list(failures),
                )
                out_dir = selected_dir / "chain_res" if selected_dir else ws.log_path("chain_res")
                out = out_dir / f"{chain_id}.json"
                payload = {
                    "schema_version": "2.0",
                    "outcome_type": "chain_finding",
                    "chain_id": chain_id,
                    "finding": finding,
                    "review": review,
                    "finalizer": finalizer_verdict,
                    "history": state.get("chain_review_history", []),
                }
                _write_json_atomic(out, payload)
                return {"chain_findings": [finding]}
        if finalizer_errors:
            failures = sorted(set([*failures, *finalizer_errors]))

    failed = failed_candidate or {
        **dict(candidate),
        "status": "inconclusive",
        "failure_reasons": failures,
        "investigation": investigation,
        "review": review,
    }
    out_dir = selected_dir / "chain_candidates" if selected_dir else ws.log_path("chain_candidates")
    out = out_dir / f"{chain_id}.json"
    payload = {
        "schema_version": "2.0",
        "outcome_type": "chain_candidate",
        "chain_id": chain_id,
        "candidate": failed,
        "review": review,
        "history": state.get("chain_review_history", []),
    }
    _write_json_atomic(out, payload)
    return {"chain_candidates": [failed]}


__all__ = ["finalize_chain_subtask"]
