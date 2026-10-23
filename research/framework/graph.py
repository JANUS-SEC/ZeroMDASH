"""LangGraph state machine for one research subject.

Evidence remains in versioned files for auditability. Graph state carries paths,
the current verdict, and revision-loop control data.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Annotated, Any, TypedDict

from langgraph.graph import END, START, StateGraph

from research.framework.runner import (
    DIMENSIONS,
    ClaudeRunner,
    atomic_json,
    atomic_text,
    collect_evidence,
    cached_result,
    merge_evidence,
    evidence_gate,
    person_dir,
    read_json,
    render_person_report,
    render_template,
    run_dimension,
)


def _merge_dicts(left: dict[str, str], right: dict[str, str]) -> dict[str, str]:
    return {**left, **right}


def _task_material(value: Any) -> Any:
    """Omit invocation telemetry from facts supplied to another agent."""
    if isinstance(value, dict):
        return {key: _task_material(item) for key, item in value.items() if key != "_run"}
    if isinstance(value, list):
        return [_task_material(item) for item in value]
    return value


def _editorial_structure(value: dict[str, Any]) -> dict[str, Any]:
    """Fields an editorial rewrite must preserve exactly, apart from prose."""
    return {
        "person": value.get("person"),
        "expertise_count": len(value.get("expertise", [])),
        "stages": [
            {key: stage.get(key) for key in ("period", "evidence_ids", "confidence")}
            for stage in value.get("stages", [])
        ],
        "mechanisms": [
            {
                **{key: mechanism.get(key) for key in ("evidence_ids", "validation_tests", "confidence")},
                "observed_outcomes_count": len(mechanism.get("observed_outcomes", [])),
            }
            for mechanism in value.get("mechanisms", [])
        ],
        "list_counts": {
            key: len(value.get(key, []))
            for key in ("tensions", "transferable_practices", "non_transferable_conditions", "open_questions")
        },
    }


def _is_editorial_path(parts: list[str]) -> bool:
    top_level_lists = {
        "expertise", "tensions", "transferable_practices",
        "non_transferable_conditions", "open_questions",
    }
    stage_fields = {"stage", "capability_change"}
    mechanism_fields = {
        "name", "starting_conditions", "repeated_practice", "feedback",
        "intermediate_capability", "alternative_explanation",
    }
    return (
        (len(parts) == 2 and parts[0] in top_level_lists and parts[1].isdigit())
        or (len(parts) == 3 and parts[0] == "stages" and parts[1].isdigit() and parts[2] in stage_fields)
        or (len(parts) == 3 and parts[0] == "mechanisms" and parts[1].isdigit() and parts[2] in mechanism_fields)
        or (len(parts) == 4 and parts[0] == "mechanisms" and parts[1].isdigit()
            and parts[2] == "observed_outcomes" and parts[3].isdigit())
    )


def apply_editorial_edits(original: dict[str, Any], edits: list[dict[str, str]]) -> dict[str, Any]:
    """Apply exact prose replacements without granting the editor structural writes."""
    if not edits:
        raise ValueError("文字修订没有提供替换项")
    result = copy.deepcopy(original)
    seen: set[str] = set()
    for edit in edits:
        path = edit["path"]
        parts = path.split("/")[1:] if path.startswith("/") else []
        if not _is_editorial_path(parts) or path in seen:
            raise ValueError(f"文字修订路径不允许或重复：{path}")
        seen.add(path)
        target: Any = result
        try:
            for part in parts[:-1]:
                target = target[int(part)] if isinstance(target, list) else target[part]
            key: str | int = int(parts[-1]) if isinstance(target, list) else parts[-1]
            current = target[key]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ValueError(f"文字修订路径不存在：{path}") from exc
        if not isinstance(current, str) or current != edit["before"] or not edit["after"].strip() or current == edit["after"]:
            raise ValueError(f"文字修订原文不匹配或替换无效：{path}")
        target[key] = edit["after"]
    if _editorial_structure(original) != _editorial_structure(result):
        raise ValueError("文字修订改变了事实性结构")
    return result


class ResearchState(TypedDict, total=False):
    person_name: str
    evidence_paths: Annotated[dict[str, str], _merge_dicts]
    synthesis_path: str
    review_path: str
    targeted_research_paths: list[str]
    revision_round: int
    editorial_round: int
    editorial_revisions: list[str]
    max_revisions: int
    verdict: str
    status: str


def build_research_graph(
    runner: ClaudeRunner,
    person: dict[str, str],
    *,
    force: bool,
    max_revisions: int,
):
    """Build a fan-out, review-loop graph for a single researcher."""
    graph = StateGraph(ResearchState)
    base = person_dir(runner.config, person)

    def effective_evidence(state: ResearchState) -> dict[str, Any]:
        revisions = [read_json(Path(p)) for p in state.get("targeted_research_paths", [])]
        evidence = merge_evidence(collect_evidence(runner.config, person), revisions)
        atomic_json(base / "evidence_merged" / f"v{int(state.get('revision_round', 0)) + 1}.json", evidence)
        return evidence

    def evidence_node(slug: str):
        def node(_state: ResearchState) -> dict[str, Any]:
            print(f"[start] {person['name_or_handle']} evidence:{slug}", flush=True)
            path = run_dimension(runner, person, slug, force)
            print(f"[done]  {person['name_or_handle']} evidence:{slug}", flush=True)
            return {"evidence_paths": {slug: str(path)}}

        return node

    def synthesis_node(state: ResearchState) -> dict[str, Any]:
        revision_round = int(state.get("revision_round", 0))
        version = revision_round + 1
        versioned = base / "synthesis" / (f"v{version}.json" if version == 1 else f"v{version}-p2.json")
        print(f"[start] {person['name_or_handle']} synthesis:v{version}", flush=True)
        canonical = base / "synthesis.json"
        if versioned.exists() and not force:
            result = cached_result(versioned)
        else:
            evidence = effective_evidence(state)
            targeted = [read_json(Path(path)) for path in state.get("targeted_research_paths", [])]
            revision_context = [
                {key: item.get(key, []) for key in ("synthesis_instructions", "unresolved")}
                for item in targeted
            ]
            prompt = render_template(
                "synthesis.md",
                {
                    "PERSON_JSON": json.dumps(person, ensure_ascii=False, indent=2),
                    "EVIDENCE_JSON": json.dumps(_task_material(evidence), ensure_ascii=False),
                    "REVISION_CONTEXT": json.dumps(revision_context, ensure_ascii=False),
                },
            )
            result = runner.call(prompt, "synthesis.json", f"{person['name_or_handle']}:synthesis:v{version}")
            atomic_json(versioned, result)
        atomic_json(canonical, result)
        print(f"[done]  {person['name_or_handle']} synthesis:v{version}", flush=True)
        return {"synthesis_path": str(versioned), "status": "reviewing"}

    def review_node(state: ResearchState) -> dict[str, Any]:
        revision_round = int(state.get("revision_round", 0))
        version = revision_round + 1
        editorial_round = int(state.get("editorial_round", 0))
        suffix = f"-edit-{editorial_round}" if editorial_round else ""
        versioned = base / "reviews" / f"v{version}{suffix}-p2.json"
        print(f"[start] {person['name_or_handle']} review:v{version}{suffix}", flush=True)
        canonical = base / "review.json"
        if versioned.exists() and not force:
            result = cached_result(versioned)
        else:
            evidence = effective_evidence(state)
            synthesis = read_json(Path(state["synthesis_path"]))
            prompt = render_template(
                "review.md",
                {
                    "PERSON_JSON": json.dumps(person, ensure_ascii=False, indent=2),
                    "EVIDENCE_JSON": json.dumps(_task_material(evidence), ensure_ascii=False),
                    "SYNTHESIS_JSON": json.dumps(_task_material(synthesis), ensure_ascii=False),
                },
            )
            result = runner.call(prompt, "review.json", f"{person['name_or_handle']}:review:v{version}{suffix}:p2")
            atomic_json(versioned, result)
        issues = evidence_gate(effective_evidence(state), read_json(Path(state["synthesis_path"])))
        if issues:
            result["verdict"] = "revise"
            result["required_revisions"] = list(dict.fromkeys(result.get("required_revisions", []) + issues))
        if result.get("required_revisions"):
            result["verdict"] = "revise"
        result.setdefault("editorial_revisions", [])
        atomic_json(versioned, result)
        atomic_json(canonical, result)
        print(f"[done]  {person['name_or_handle']} review:v{version}{suffix} verdict={result['verdict']}", flush=True)
        return {
            "review_path": str(versioned),
            "verdict": result["verdict"],
            "editorial_revisions": result["editorial_revisions"],
            "status": "passed" if result["verdict"] == "pass" else "revising",
        }

    def route_after_review(state: ResearchState) -> str:
        if state.get("verdict") == "pass":
            if state.get("editorial_revisions"):
                if int(state.get("editorial_round", 0)) < runner.config.max_editorial_revisions:
                    return "editorial_rewrite"
                return "revision_exhausted"
            return "finalize"
        if int(state.get("revision_round", 0)) < int(state.get("max_revisions", max_revisions)):
            return "targeted_research"
        return "revision_exhausted"

    def editorial_rewrite_node(state: ResearchState) -> dict[str, Any]:
        version = int(state.get("revision_round", 0)) + 1
        editorial_round = int(state.get("editorial_round", 0)) + 1
        output = base / "synthesis" / f"v{version}-edit-{editorial_round}-p2.json"
        print(f"[start] {person['name_or_handle']} editorial:v{version}:{editorial_round}", flush=True)
        original = read_json(Path(state["synthesis_path"]))
        if output.exists() and not force:
            result = cached_result(output)
        else:
            prompt = render_template(
                "editorial_rewrite.md",
                {
                    "PERSON_JSON": json.dumps(person, ensure_ascii=False),
                    "SYNTHESIS_JSON": json.dumps(_task_material(original), ensure_ascii=False),
                    "EDITORIAL_JSON": json.dumps(state["editorial_revisions"], ensure_ascii=False),
                },
            )
            edits_result = runner.call(
                prompt, "editorial_edits.json",
                f"{person['name_or_handle']}:editorial:v{version}:round-{editorial_round}",
            )
            result = apply_editorial_edits(original, edits_result["edits"])
            result.setdefault("_run", {})["editorial_edits_run"] = edits_result.get("_run", {})
        if _editorial_structure(original) != _editorial_structure(result):
            raise RuntimeError(f"{person['name_or_handle']} 文字修订改变了事实性结构，已拒绝采用")
        if not output.exists() or force:
            atomic_json(output, result)
        atomic_json(base / "synthesis.json", result)
        print(f"[done]  {person['name_or_handle']} editorial:v{version}:{editorial_round}", flush=True)
        return {"synthesis_path": str(output), "editorial_round": editorial_round, "status": "reviewing"}

    def targeted_research_node(state: ResearchState) -> dict[str, Any]:
        next_round = int(state.get("revision_round", 0)) + 1
        output = base / "revisions" / f"round-{next_round}-p2.json"
        print(f"[start] {person['name_or_handle']} targeted-research:round-{next_round}", flush=True)
        if output.exists() and not force:
            result = cached_result(output)
        else:
            evidence = effective_evidence(state)
            synthesis = read_json(Path(state["synthesis_path"]))
            review = read_json(Path(state["review_path"]))
            prompt = render_template(
                "targeted_research.md",
                {
                    "PERSON_JSON": json.dumps(person, ensure_ascii=False, indent=2),
                    "EVIDENCE_JSON": json.dumps(_task_material(evidence), ensure_ascii=False),
                    "SYNTHESIS_JSON": json.dumps(_task_material(synthesis), ensure_ascii=False),
                    "REVIEW_JSON": json.dumps(_task_material(review), ensure_ascii=False),
                    "REVISION_ROUND": str(next_round),
                },
            )
            result = runner.call(
                prompt,
                "targeted_research.json",
                f"{person['name_or_handle']}:targeted-research:round-{next_round}",
            )
            atomic_json(output, result)
        print(f"[done]  {person['name_or_handle']} targeted-research:round-{next_round}", flush=True)
        paths = list(state.get("targeted_research_paths", []))
        if str(output) not in paths:
            paths.append(str(output))
        return {
            "targeted_research_paths": paths,
            "revision_round": next_round,
            "editorial_round": 0,
            "editorial_revisions": [],
            "status": "resynthesizing",
        }

    def finalize_node(state: ResearchState) -> dict[str, Any]:
        synthesis = read_json(Path(state["synthesis_path"]))
        review = read_json(Path(state["review_path"]))
        report = render_person_report(person, synthesis, review)
        atomic_text(base / "FINAL.md", report)
        final_state = {**state, "status": "complete", "verdict": "pass"}
        atomic_json(base / "state.json", _serializable_state(final_state))
        return {"status": "complete"}

    def revision_exhausted_node(state: ResearchState) -> dict[str, Any]:
        synthesis = read_json(Path(state["synthesis_path"]))
        review = read_json(Path(state["review_path"]))
        draft = render_person_report(person, synthesis, review)
        editorial_exhausted = state.get("verdict") == "pass" and bool(state.get("editorial_revisions"))
        reason = (
            f"已达到最大文字修订次数 {runner.config.max_editorial_revisions}"
            if editorial_exhausted else f"已达到最大事实性修订次数 {state.get('max_revisions', max_revisions)}"
        )
        banner = f"# 未通过定稿检查\n\n{reason}；本文件是审计草稿，不得进入跨人物比较。\n\n"
        atomic_text(base / "DRAFT.md", banner + draft)
        status = "editorial_exhausted" if editorial_exhausted else "revision_exhausted"
        exhausted_state = {**state, "status": status, "verdict": "revise"}
        atomic_json(base / "state.json", _serializable_state(exhausted_state))
        return {"status": status, "verdict": "revise"}

    evidence_nodes = []
    for slug in DIMENSIONS:
        node_name = f"evidence_{slug}"
        evidence_nodes.append(node_name)
        graph.add_node(node_name, evidence_node(slug))
        graph.add_edge(START, node_name)

    graph.add_node("synthesis", synthesis_node)
    graph.add_node("review", review_node)
    graph.add_node("editorial_rewrite", editorial_rewrite_node)
    graph.add_node("targeted_research", targeted_research_node)
    graph.add_node("finalize", finalize_node)
    graph.add_node("revision_exhausted", revision_exhausted_node)

    graph.add_edge(evidence_nodes, "synthesis")
    graph.add_edge("synthesis", "review")
    graph.add_conditional_edges(
        "review",
        route_after_review,
        {
            "finalize": "finalize",
            "editorial_rewrite": "editorial_rewrite",
            "targeted_research": "targeted_research",
            "revision_exhausted": "revision_exhausted",
        },
    )
    graph.add_edge("targeted_research", "synthesis")
    graph.add_edge("editorial_rewrite", "review")
    graph.add_edge("finalize", END)
    graph.add_edge("revision_exhausted", END)
    return graph.compile()


def _serializable_state(state: ResearchState) -> dict[str, Any]:
    return {
        "person_name": state.get("person_name"),
        "evidence_paths": state.get("evidence_paths", {}),
        "synthesis_path": state.get("synthesis_path"),
        "review_path": state.get("review_path"),
        "targeted_research_paths": state.get("targeted_research_paths", []),
        "revision_round": state.get("revision_round", 0),
        "editorial_round": state.get("editorial_round", 0),
        "editorial_revisions": state.get("editorial_revisions", []),
        "max_revisions": state.get("max_revisions", 3),
        "verdict": state.get("verdict"),
        "status": state.get("status"),
    }


def run_research_graph(
    runner: ClaudeRunner,
    person: dict[str, str],
    *,
    force: bool = False,
    max_revisions: int = 3,
) -> ResearchState:
    if max_revisions < 0:
        raise ValueError("max_revisions 不能小于 0")
    graph = build_research_graph(runner, person, force=force, max_revisions=max_revisions)
    initial: ResearchState = {
        "person_name": person["name_or_handle"],
        "evidence_paths": {},
        "targeted_research_paths": [],
        "revision_round": 0,
        "editorial_round": 0,
        "editorial_revisions": [],
        "max_revisions": max_revisions,
        "verdict": "",
        "status": "collecting_evidence",
    }
    return graph.invoke(initial, config={
        "max_concurrency": runner.config.max_concurrency,
        "recursion_limit": (
            12 + (max_revisions + 1) * (2 + 2 * runner.config.max_editorial_revisions)
            + max_revisions
        ),
    })
