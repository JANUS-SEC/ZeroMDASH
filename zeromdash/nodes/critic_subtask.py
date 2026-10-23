"""LangGraph node implementation: critic_subtask."""

from __future__ import annotations

import copy
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any

from langgraph.constants import Send

from zeromdash import presets, prompts, skills as skills_mod
from zeromdash.agents import AgentResult, normalize_agent_name
from zeromdash.scope import materialize_scan_scope
from zeromdash.state import Finding, ReviewTurn, Subtask, ZeroMDASHState
from zeromdash.workspace import Workspace, slugify

from .core.config import (
    _agent_configs_with_node_variant,
    agent_config_variants_for_node,
)
from .core.constants import (
    DEFAULT_MAX_ITERATIONS,
    DEFAULT_MIN_CRITIC_SKILLS,
    DEFAULT_NODE_OUTPUT_ATTEMPTS,
)
from .core.context import (
    _node_focus,
    _ws,
)
from .core.domain_registry import domain_registry_from_state, domain_registry_json
from .core.invocation import (
    _agent_errors,
    _emit_node_fallback,
    _make_agent,
    _run_agent_with_config,
    _selected_log_dir,
)
from .core.io import _reset_file_output
from .core.recovery import node_runtime_failure, recover_runtime
from .core.hypothesis_batch import (
    advance_hypothesis_manifest,
    hypothesis_package_closed,
    is_hypothesis_batch,
    is_hypothesis_package,
    validate_hypothesis_review,
)
from .core.primitive_qualification import build_confirmed_primitive, review_outcome_type
from .core.qualification import (
    _coerce_review_dict,
    _first_no_finding_needs_revise,
    _force_first_no_finding_revise,
    _investigation_json,
    _normalize_qualification_review,
    _normalize_scope_review,
    _try_json,
)


_REVIEW_ARTIFACT_NAME = "review.json"


def _read_review_artifact(path: Path) -> tuple[dict[str, Any] | None, str]:
    if not path.is_file():
        return None, f"{path.name}: not created by this attempt"
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"{path.name}: invalid JSON ({exc})"
    if not isinstance(value, dict) or not value:
        return None, f"{path.name}: review must be a non-empty JSON object"
    return value, ""


def _stdout_review(stdout: str) -> tuple[dict[str, Any] | None, str]:
    if not str(stdout or "").strip():
        return None, "stdout: critic returned empty output"
    value = _try_json(
        stdout,
        fallback={"verdict": "revise", "raw": stdout},
    )
    return _coerce_review_dict(value, raw=stdout), ""


def _review_contract_error(*failures: str) -> str:
    return "; ".join(failure for failure in failures if failure)


@recover_runtime(node="critic_subtask", failure=node_runtime_failure)
def critic_subtask(state: ZeroMDASHState, *, backends=None) -> dict:
    """Critic-review ONE subtask's latest investigation.

    Skills 选择是 *运行时* 行为：我们扫描 bundled `presets/skills/` 与本次
    sub_workspace 下的 `./skills/`，把 `name — summary` 目录注入 prompt，
    强制 critic 自己根据内容挑 ≥ N 个相关 skill 并在 JSON 里回传。绝不在
    prompt 里写死「scenario X -> skill Y」。
    """
    ws = _ws(state)
    subtask = state["subtask"]
    history = state.get("review_history", [])
    investigation = _investigation_json(state.get("investigation", ""))
    batch_mode = is_hypothesis_package(subtask) and is_hypothesis_batch(investigation)

    sub_id = f"{subtask['id']}__critic"
    variants = agent_config_variants_for_node("critic_subtask", backends, state.get("agent_configs"))
    res: AgentResult | None = None
    available_names: list[str] = []
    prompt_text = ""
    review: dict[str, Any] = {}
    validated_batch_review: dict[str, Any] | None = None
    contract_error = ""
    output_source = ""
    for variant_index, variant in enumerate(variants, start=1):
        backend_name = normalize_agent_name(variant["runtime"])
        variant_configs = _agent_configs_with_node_variant(state.get("agent_configs"), "critic_subtask", variant)
        sub_ws = ws.prepare_sub_workspace(
            node="critic_subtask",
            subtask_id=sub_id,
            backend=backend_name,
            extra_context={
                "iteration": int(state.get("iteration", 0)),
                "bucket": subtask.get("bucket", ""),
                "fallback_index": variant_index - 1,
                "fallback_count": len(variants) - 1,
            },
        )

        # 运行时枚举可用 skill (bundled + 本 sub_workspace 自定义), 后者优先
        skills_catalog_dirs = [
            presets.default_presets_dir() / "skills",
            sub_ws / "skills",
        ]
        skill_list = skills_mod.discover_skills(skills_catalog_dirs)
        catalog_md = skills_mod.render_catalog(skill_list)
        available_names = skills_mod.names(skill_list)
        min_required = int(state.get("min_critic_skills", DEFAULT_MIN_CRITIC_SKILLS))
        # 若可用 skill 数量本身少于阈值, 至少要求 critic 把现有的全选上
        effective_min = min(min_required, len(skill_list)) if skill_list else 0

        # 把目录信息也落到 sub_workspace 方便 agent 翻看
        (sub_ws / "skills_catalog.md").write_text(catalog_md)

        prompt_text = prompts.CRITIC_SUBTASK.format(
            subtask_json=json.dumps(subtask, ensure_ascii=False, indent=2),
            investigation_json=state.get("investigation", ""),
            history_json=json.dumps(history, ensure_ascii=False, indent=2),
            repo_path=state["repo_path"],
            attack_surface=state.get("attack_surface", ""),
            domain_registry=domain_registry_json(state),
            writeup_dir=str(ws.main_path("writeup")),
            patch_dir=str(ws.main_path("patch")),
            feature_docs=", ".join(state.get("feature_docs") or []),
            skills_catalog=catalog_md,
            min_skills=effective_min,
            focus=_node_focus(state, "critic_subtask_focus"),
        )
        repair_prompt = prompt_text
        for repair_attempt in range(1, DEFAULT_NODE_OUTPUT_ATTEMPTS + 1):
            artifact_path = sub_ws / _REVIEW_ARTIFACT_NAME
            _reset_file_output(artifact_path)
            res = _run_agent_with_config(
                _make_agent(backend_name),
                "critic_subtask",
                backend_name,
                repair_prompt,
                sub_ws,
                None,
                variant_configs,
                state.get("agent_config_task_types"),
                _selected_log_dir(state),
            )
            artifact_review, artifact_failure = _read_review_artifact(artifact_path)
            stdout_review, stdout_failure = _stdout_review(res.stdout)
            output_source = ""

            if not batch_mode:
                if artifact_review is not None:
                    review = _coerce_review_dict(artifact_review)
                    output_source = "artifact"
                elif stdout_review is not None:
                    review = stdout_review
                    output_source = "stdout"
                else:
                    contract_error = _review_contract_error(
                        artifact_failure,
                        stdout_failure,
                    )
                    review = _coerce_review_dict(
                        {
                            "verdict": "revise",
                            "raw": res.stdout,
                            "output_validation_error": contract_error,
                        },
                        raw=res.stdout,
                    )
                break

            candidate_failures: list[str] = []
            review = {}
            validated_batch_review = None
            for source, candidate, source_failure in (
                ("artifact", artifact_review, artifact_failure),
                ("stdout", stdout_review, stdout_failure),
            ):
                if candidate is None:
                    candidate_failures.append(source_failure)
                    continue
                parsed, validation_failure = validate_hypothesis_review(
                    candidate,
                    subtask=subtask,
                    investigation=investigation,
                )
                if parsed is not None:
                    review = parsed
                    validated_batch_review = parsed
                    output_source = source
                    contract_error = ""
                    break
                review = candidate
                candidate_failures.append(
                    f"{source}: {validation_failure or 'review contract validation failed'}"
                )

            if validated_batch_review is not None:
                break
            contract_error = _review_contract_error(*candidate_failures)
            if not review:
                review = _coerce_review_dict(
                    {
                        "verdict": "revise",
                        "raw": res.stdout,
                        "output_validation_error": contract_error,
                    },
                    raw=res.stdout,
                )
            if not res.ok:
                break
            if repair_attempt < DEFAULT_NODE_OUTPUT_ATTEMPTS:
                current_discovery_ids = [
                    str(item.get("hypothesis_id") or "")
                    for item in (
                        investigation.get("newly_discovered_hypotheses")
                        or investigation.get("discovered_hypotheses")
                        or []
                    )
                    if isinstance(item, dict)
                ]
                repair_prompt = (
                    prompt_text
                    + "\n\n# Schema repair only\n"
                    + f"Your previous JSON failed the batch contract: {contract_error}\n"
                    + "Return the complete corrected Review JSON only. Preserve valid "
                    + "source-grounded verdicts, evidence, and qualification fields; do not "
                    + "invent evidence or restart the investigation. Correct the structural "
                    + "or accounting error. If the existing evidence cannot support closure, "
                    + "keep coverage open and add a concrete required hypothesis. "
                    + "new_hypothesis_decisions must contain decisions only for hypotheses "
                    + "newly discovered in this investigation pass.\n"
                    + "Current-iteration discovery IDs: "
                    + json.dumps(current_discovery_ids, ensure_ascii=False)
                    + "\nPrevious invalid JSON:\n"
                    + json.dumps(review, ensure_ascii=False, indent=2)
                )
        legacy_failure = node_runtime_failure({"review": review}) if not batch_mode else ""
        if res.ok and (validated_batch_review is not None or (not batch_mode and not legacy_failure)):
            break
        if variant_index < len(variants):
            _emit_node_fallback("critic_subtask", res, variants[variant_index])

    if res is None:
        res = AgentResult("", "critic_subtask did not run", 1, "critic_subtask")

    if not review:
        review = _coerce_review_dict(
            _try_json(res.stdout, fallback={"verdict": "revise", "raw": res.stdout}),
            raw=res.stdout,
        )

    # 5) 后处理: 校验 selected_skills, 不达标时记入 review.feedback.gaps
    if isinstance(review, dict):
        selected = review.get("selected_skills") or []
        if isinstance(selected, list):
            kept = [s for s in selected if isinstance(s, str) and s in available_names]
            review["selected_skills"] = kept
            review["available_skills"] = available_names
            if effective_min and len(kept) < effective_min:
                fb = review.setdefault("feedback", {})
                gaps = list(fb.get("gaps") or [])
                gaps.append(
                    f"critic selected {len(kept)} skill(s); required >= {effective_min}"
                )
                fb["gaps"] = gaps
                review["skill_selection_ok"] = False
            else:
                review["skill_selection_ok"] = True
        else:
            review["selected_skills"] = []
            review["available_skills"] = available_names
            review["skill_selection_ok"] = False

    next_manifest = state.get("hypothesis_manifest")
    if batch_mode:
        parsed_review = validated_batch_review
        if parsed_review is None:
            if not contract_error:
                _, contract_error = validate_hypothesis_review(
                    review,
                    subtask=subtask,
                    investigation=investigation,
                )
            contract_error = contract_error or "critic did not return a valid batch review"
            review["package_decision"] = "revise"
            review["verdict"] = "revise"
            review["batch_contract_errors"] = [contract_error]
            feedback = review.setdefault("feedback", {})
            if not isinstance(feedback, dict):
                feedback = {}
                review["feedback"] = feedback
            gaps = list(feedback.get("gaps") or [])
            gaps.append(f"hypothesis batch contract invalid: {contract_error}")
            feedback["gaps"] = gaps
        else:
            review = parsed_review
            result_by_id = {
                str(item.get("hypothesis_id") or ""): item
                for item in investigation.get("hypothesis_results", [])
                if isinstance(item, dict)
            }
            normalized_verdicts: list[dict[str, Any]] = []
            for item_review in review.get("hypothesis_verdicts", []):
                hypothesis_id = str(item_review.get("hypothesis_id") or "")
                inv_item = result_by_id[hypothesis_id]
                normalized = dict(item_review)
                normalized["selected_skills"] = list(review.get("selected_skills") or [])
                normalized["skill_perspectives"] = dict(review.get("skill_perspectives") or {})
                normalized = _force_first_no_finding_revise(
                    {**state, "investigation": inv_item},
                    normalized,
                )
                normalized = _normalize_qualification_review(normalized)
                normalized = _normalize_scope_review(state, inv_item, normalized)
                if (
                    str(normalized.get("verdict") or "").lower() == "confirm"
                    and review_outcome_type(normalized) == "confirmed_primitive"
                ):
                    primitive, primitive_errors = build_confirmed_primitive(
                        subtask={
                            **subtask,
                            "id": f"{subtask.get('id')}--{hypothesis_id}",
                        },
                        investigation=inv_item,
                        review=normalized,
                        domain_registry=domain_registry_from_state(state),
                    )
                    if primitive_errors:
                        normalized["original_verdict"] = "confirm"
                        normalized["verdict"] = "revise"
                        normalized["primitive_gate_ok"] = False
                        normalized["primitive_gate_errors"] = primitive_errors
                        feedback = normalized.setdefault("feedback", {})
                        gaps = list(feedback.get("gaps") or [])
                        gaps.append(
                            "confirmed_primitive output does not satisfy primitive schema: "
                            + "; ".join(primitive_errors)
                        )
                        feedback["gaps"] = gaps
                    else:
                        normalized["primitive_gate_ok"] = True
                        normalized["primitive_id_preview"] = (
                            primitive.get("primitive_id") if primitive else ""
                        )
                normalized_verdicts.append(normalized)
            review["hypothesis_verdicts"] = normalized_verdicts
            revised_ids = {
                str(item.get("hypothesis_id") or "")
                for item in normalized_verdicts
                if str(item.get("verdict") or "").lower() == "revise"
            }
            if revised_ids:
                review["package_decision"] = "revise"
                review["verdict"] = "revise"
                coverage = review.get("coverage_verdict")
                if isinstance(coverage, dict):
                    coverage["status"] = "open"
                    for assessment in coverage.get("obligation_assessments", []) or []:
                        if not isinstance(assessment, dict):
                            continue
                        mapped_ids = {
                            str(item)
                            for item in assessment.get("hypothesis_ids", []) or []
                        }
                        if mapped_ids & revised_ids:
                            assessment["status"] = "open"
                package_feedback = review.setdefault("feedback", {})
                if not isinstance(package_feedback, dict):
                    package_feedback = {}
                    review["feedback"] = package_feedback
                package_gaps = list(package_feedback.get("gaps") or [])
                package_requested = list(
                    package_feedback.get("requested_evidence") or []
                )
                for item in normalized_verdicts:
                    hypothesis_id = str(item.get("hypothesis_id") or "")
                    if hypothesis_id not in revised_ids:
                        continue
                    item_feedback = item.get("feedback")
                    if not isinstance(item_feedback, dict):
                        continue
                    for gap in item_feedback.get("gaps", []) or []:
                        message = f"{hypothesis_id}: {gap}"
                        if message not in package_gaps:
                            package_gaps.append(message)
                    for request in item_feedback.get("requested_evidence", []) or []:
                        message = f"{hypothesis_id}: {request}"
                        if message not in package_requested:
                            package_requested.append(message)
                package_feedback["gaps"] = package_gaps
                package_feedback["requested_evidence"] = package_requested
                package_feedback["next_focus"] = (
                    package_feedback.get("next_focus")
                    or "Re-investigate non-terminal hypotheses: "
                    + ", ".join(sorted(revised_ids))
                )
            else:
                review["verdict"] = (
                    "confirm" if hypothesis_package_closed(review) else "revise"
                )
            next_manifest = advance_hypothesis_manifest(
                subtask,
                state.get("hypothesis_manifest"),
                investigation,
                review,
            )
    else:
        review = _force_first_no_finding_revise(state, review)
        review = _normalize_qualification_review(review)
        review = _normalize_scope_review(state, investigation, review)
        if (
            str(review.get("verdict") or "").lower() == "confirm"
            and review_outcome_type(review) == "confirmed_primitive"
        ):
            primitive, primitive_errors = build_confirmed_primitive(
                subtask=subtask,
                investigation=investigation,
                review=review,
                domain_registry=domain_registry_from_state(state),
            )
            if primitive_errors:
                review["original_verdict"] = "confirm"
                review["verdict"] = "revise"
                review["primitive_gate_ok"] = False
                review["primitive_gate_errors"] = primitive_errors
                feedback = review.setdefault("feedback", {})
                gaps = list(feedback.get("gaps") or [])
                gap = "confirmed_primitive output does not satisfy primitive schema: " + "; ".join(primitive_errors)
                if gap not in gaps:
                    gaps.append(gap)
                requested = list(feedback.get("requested_evidence") or [])
                requested.append(
                    "Return outcome_type=confirmed_primitive only with primitive.root_cause_anchor, "
                    "primitive.capabilities_gained, evidence.code_locations, evidence.call_path, "
                    "and required_capabilities when direct impact still needs another primitive."
                )
                feedback["gaps"] = gaps
                feedback["requested_evidence"] = requested
            else:
                review["primitive_gate_ok"] = True
                review["primitive_id_preview"] = primitive.get("primitive_id") if primitive else ""

    selected_dir = _selected_log_dir(state)
    log = (
        selected_dir / "critic_reviews" / f"{subtask['id']}.review.log"
        if selected_dir
        else ws.log_path("review_log") / f"{subtask['id']}.review.log"
    )
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a") as fp:
        fp.write(
            f"\n--- iteration {state['iteration']} (skills: "
            f"{review.get('selected_skills') if isinstance(review, dict) else '?'}, "
            f"source: {output_source or 'invalid'}) ---\n"
            f"{res.stdout if output_source == 'stdout' else json.dumps(review, ensure_ascii=False)}\n"
        )

    turn = ReviewTurn(
        iteration=state["iteration"],
        investigation=state.get("investigation", ""),
        review=review,
    )
    return {
        "review": review,
        "review_history": [turn],
        **({"hypothesis_manifest": next_manifest} if batch_mode and isinstance(next_manifest, dict) else {}),
        "errors": _agent_errors(res, "critic_subtask", subtask["id"]),
    }

def route_after_critic(state: ZeroMDASHState) -> str:
    review = _coerce_review_dict(state.get("review") or {})
    iteration = int(state.get("iteration", 0))
    max_iter = int(state.get("max_iterations", DEFAULT_MAX_ITERATIONS))
    if is_hypothesis_package(state.get("subtask")):
        if (
            hypothesis_package_closed(review)
            or review.get("batch_contract_errors")
            or iteration >= max_iter
        ):
            return "finalize_subtask"
        return "investigate_subtask"
    if _first_no_finding_needs_revise(state):
        return "investigate_subtask"
    if review.get("primitive_gate_ok") is False:
        history = state.get("review_history") or []
        already_retried = any(
            isinstance(turn, dict)
            and isinstance(turn.get("review"), dict)
            and turn["review"].get("primitive_gate_ok") is False
            for turn in history
        )
        if not already_retried:
            return "investigate_subtask"
    verdict = str(review.get("verdict", "revise")).lower()
    if verdict in {"confirm", "reject"} or iteration >= max_iter:
        return "finalize_subtask"
    return "investigate_subtask"

__all__ = ["critic_subtask","route_after_critic"]

