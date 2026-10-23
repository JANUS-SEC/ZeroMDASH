"""Unit tests for subtask dispatch, routing, and finalization flow."""

from __future__ import annotations

import json
import io
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from zeromdash import graph as graph_mod, nodes
from zeromdash.agents import AgentResult
from zeromdash.workspace import Workspace


_CVSS4_HIGH_VECTOR = (
    "CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/"
    "VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"
)


def _qualified_review(
    verdict: str = "confirm",
    *,
    confidence: float = 0.9,
    selected_skills: list[str] | None = None,
) -> dict:
    return {
        "verdict": verdict,
        "disposition": "confirmed_vulnerability",
        "documented_expected_behavior": False,
        "security_contract_violation": True,
        "violated_security_property": "untrusted input must not reach the privileged sink unsafely",
        "standalone_security_impact": True,
        "direct_security_impact": {
            "vulnerable_system": {
                "confidentiality": "high",
                "integrity": "high",
                "availability": "high",
            },
            "subsequent_system": {
                "confidentiality": "none",
                "integrity": "none",
                "availability": "none",
            },
        },
        "required_external_primitives": [],
        "cvss_applicable": True,
        "cvss4_vector": _CVSS4_HIGH_VECTOR,
        "cvss4_score": 8.5,
        "severity": "high",
        "qualification_gate_passed": True,
        "confidence": confidence,
        "selected_skills": list(selected_skills or []),
    }


def _workspace_state(ws: Workspace) -> dict:
    return {
        "target": "libfoo",
        "task_id": ws.task_id,
        "workspace_root": str(ws.root),
        "repo_path": str(ws.main_path("repo")),
    }


def _patch_manifest(
    ws: Workspace,
    *,
    target: str = "libfoo",
    repos: list[dict[str, str]] | None = None,
    coverage_ids: list[str] | None = None,
) -> dict:
    selected = repos or [
        {
            "repo_id": "main",
            "role": "main",
            "target": target,
            "repo_path": str(ws.main_path("repo")),
        }
    ]
    return {
        "schema_version": "1.0",
        "target": target,
        "mode": "multi_repo" if len(selected) > 1 else "single_repo",
        "repositories": [
            {
                **repo,
                "branch": "main",
                "head": "a" * 40,
                "describe": "v1.0-1-gaaaaaaa",
            }
            for repo in selected
        ],
        "coverage": [
            {
                "repo_id": repo_id,
                "status": "no_public_history",
                "sources_checked": ["https://example.test/advisories"],
                "notes": "No public history found.",
            }
            for repo_id in (coverage_ids or [repo["repo_id"] for repo in selected])
        ],
        "findings": [],
    }


def _valid_investigation(title: str = "ok") -> dict:
    return {
        "title": title,
        "detail": "validated detail",
        "evidence": {
            "code_locations": ["src/sample.c:2"],
            "call_path": ["entry -> sink"],
        },
        "status": "ok",
    }


def _hypothesis_package_subtask() -> dict:
    return {
        "id": "spec-028",
        "bucket": "spec",
        "objective": "audit SQPOLL setup paths",
        "hints": {},
        "coverage_obligations": [
            {"obligation_id": "spec-028:obl-cred", "statement": "check credential setup"},
            {"obligation_id": "spec-028:obl-cpu", "statement": "check no-SQ_AFF cpuset path"},
        ],
        "seed_hypotheses": [
            {"hypothesis_id": "spec-028:hyp-cred", "statement": "credential setup crosses an unsafe boundary", "obligation_ids": ["spec-028:obl-cred"]},
            {"hypothesis_id": "spec-028:hyp-cpu", "statement": "the no-SQ_AFF path escapes its cpuset", "obligation_ids": ["spec-028:obl-cpu"]},
        ],
    }


def _hypothesis_batch_investigation() -> dict:
    return {
        "schema_version": "1.0",
        "package_id": "spec-028",
        "manifest_revision": 1,
        "hypothesis_results": [
            {
                "hypothesis_id": "spec-028:hyp-cred",
                **_valid_investigation("credential path"),
            },
            {
                "hypothesis_id": "spec-028:hyp-cpu",
                **_valid_investigation("no-finding"),
                "status": "no-finding",
            },
        ],
        "newly_discovered_hypotheses": [],
        "coverage_matrix": [
            {"obligation_id": "spec-028:obl-cred", "hypothesis_ids": ["spec-028:hyp-cred"], "assessment": "traced"},
            {"obligation_id": "spec-028:obl-cpu", "hypothesis_ids": ["spec-028:hyp-cpu"], "assessment": "enumerated"},
        ],
        "counterexample_attempts": [
            {
                "dimension": "credential and CPU setup path",
                "cases": ["credential branch", "no-SQ_AFF branch"],
                "result": "both branches were traced to their terminal checks",
                "evidence": ["src/sample.c:2"],
            }
        ],
        "unresolved_cases": [],
        "proposed_coverage_closed": True,
    }


def _closed_hypothesis_review() -> dict:
    return {
        "package_id": "spec-028",
        "package_decision": "close",
        "verdict": "confirm",
        "reasoning": "both independent branches were adjudicated",
        "selected_skills": ["memory"],
        "skill_perspectives": {"memory": "both paths checked"},
        "hypothesis_verdicts": [
            {
                "hypothesis_id": "spec-028:hyp-cred",
                "reasoning": "direct impact is established",
                **_qualified_review(selected_skills=["memory"]),
            },
            {
                "hypothesis_id": "spec-028:hyp-cpu",
                "verdict": "reject",
                "outcome_type": "rejected",
                "reasoning": "all no-SQ_AFF paths preserve cpuset constraints",
                "disposition": "no_finding",
                "confidence": 0.9,
            },
        ],
        "new_hypothesis_decisions": [],
        "coverage_verdict": {
            "status": "closed",
            "reasoning": "each obligation has an independently verified result",
            "obligation_assessments": [
                {"obligation_id": "spec-028:obl-cred", "status": "satisfied", "hypothesis_ids": ["spec-028:hyp-cred"], "reasoning": "traced"},
                {"obligation_id": "spec-028:obl-cpu", "status": "satisfied", "hypothesis_ids": ["spec-028:hyp-cpu"], "reasoning": "enumerated"},
            ],
            "counterexample_attempts": [
                {
                    "dimension": "credential and CPU setup path",
                    "cases": ["credential branch", "no-SQ_AFF branch"],
                    "result": "independent review found no missing sibling",
                    "evidence": ["src/sample.c:2"],
                }
            ],
            "unresolved_cases": [],
        },
        "required_hypotheses": [],
        "feedback": {"gaps": [], "requested_evidence": [], "next_focus": ""},
    }


_SUMMARY_EN = """\
# Executive Summary

## Aggregation Method

Grouped by root cause and sink.

## Vulnerability Index

- VULN-001

## Vulnerability Details

### VULN-001: Example

#### Vulnerability Description

Example issue.

#### Threat Model

An attacker controls an untrusted input.

#### Trigger Conditions

The feature is enabled.

#### Data Flow

```mermaid
flowchart LR
    A[Input] --> B[Parser] --> C[Sink]
```

#### Attack Sequence

```mermaid
sequenceDiagram
    participant A as Attacker
    participant P as Parser
    participant S as Sink
    A->>P: Crafted input
    P->>S: Unsafe operation
```

#### Code Evidence

`src/parser.c:1`

```c
parse(input);
```

#### CVSS v4.0

8.5 — `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N`

#### Affected Versions

Confirmed affected: current checkout. Other bounds are not established.

#### Source Subtasks and Confidence

`spec-001`; high; 0.9.

## Recommended Next Steps

- Add a regression test.

## Sources

- spec-001
"""

_SUMMARY_ZH = """\
# 执行摘要

## 聚合方法

按根因和 sink 聚合。

## 漏洞索引

- VULN-001

## 漏洞详情

### VULN-001: 示例

#### 漏洞介绍

示例漏洞。

#### 威胁模型

攻击者控制不可信输入。

#### 触发条件

启用该 feature。

#### 数据流向图

```mermaid
flowchart LR
    A[输入] --> B[解析器] --> C[Sink]
```

#### 攻击时序图

```mermaid
sequenceDiagram
    participant A as 攻击者
    participant P as 解析器
    participant S as Sink
    A->>P: 构造输入
    P->>S: 不安全操作
```

#### 代码证据

`src/parser.c:1`

```c
parse(input);
```

#### CVSS v4.0

8.5 — `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N`

#### 版本影响范围

已确认当前 checkout 受影响，其他边界未确定。

#### 来源 Subtask 与置信度

`spec-001`；high；0.9。

## 建议的下一步

- 增加回归测试。

## 来源

- spec-001
"""


def _write_bilingual_summary(ws: Workspace) -> None:
    (ws.base / "summary.en.md").write_text(_SUMMARY_EN)
    (ws.base / "summary.zh_CN.md").write_text(_SUMMARY_ZH)


def _write_domain_registry(ws: Workspace) -> None:
    (ws.main_path("attack_surface") / "domain_invariant_registry.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "target": "libfoo",
                "status": "complete",
                "entities": [
                    {
                        "entity_id": "entity:request",
                        "kind": "attacker_input",
                        "name": "request",
                        "source_locations": ["src/parser.c:1"],
                    }
                ],
                "representations": [],
                "invariants": [],
                "transitions": [],
                "seams": [],
            }
        )
    )


class JsonExtractionTest(unittest.TestCase):
    def test_object_with_single_array_field_is_parsed_as_object(self):
        parsed = nodes._try_json('{"verdict": "reject", "selected_skills": ["memory"]}', fallback={})

        self.assertEqual(parsed["verdict"], "reject")
        self.assertEqual(parsed["selected_skills"], ["memory"])

    def test_array_of_objects_is_parsed_as_array(self):
        parsed = nodes._try_json('[{"id": "spec-001", "bucket": "spec"}]', fallback={})

        self.assertEqual(parsed, [{"id": "spec-001", "bucket": "spec"}])

    def test_summary_diagram_validator_requires_both_diagrams_per_vulnerability(self):
        complete = """
### VULN-001: First
```mermaid
flowchart LR
  A --> B
```
```mermaid
sequenceDiagram
  A->>B: first
```
### VULN-002: Second
```mermaid
flowchart LR
  C --> D
```
```mermaid
sequenceDiagram
  C->>D: second
```
"""
        missing_second_sequence = complete.rsplit("```mermaid", 1)[0]

        self.assertTrue(nodes._each_vulnerability_has_both_diagrams(complete))
        self.assertFalse(
            nodes._each_vulnerability_has_both_diagrams(missing_second_sequence)
        )
        mislabeled_single_block = """
### VULN-001: Broken
```mermaid
flowchart LR
  A[sequenceDiagram] --> B
```
"""
        self.assertFalse(
            nodes._each_vulnerability_has_both_diagrams(mislabeled_single_block)
        )

    def test_polish_report_invokes_agent_to_repair_common_mermaid_sequence_syntax(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="polish-mermaid")
        broken = """# Executive Summary

### VULN-001: Broken
```mermaid
flowchart LR
  A --> B
```
```mermaid
sequenceDiagram
participant Loop as io_loop_demangle_ctx
participant Create as io_create_region
Create->>Loop: first step; second step
Loop-->>Create: done
```
"""
        (ws.base / "summary.en.md").write_text(broken)
        (ws.base / "summary.zh_CN.md").write_text(broken)
        captured = {}

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                extra_context,
                timeout,
            )
            captured["node"] = node
            captured["prompt"] = prompt
            fixed = broken.replace("Loop", "LoopNode").replace("Create", "CreateNode").replace(";", ",")
            (ws.base / "summary.en.md").write_text(fixed)
            (ws.base / "summary.zh_CN.md").write_text(fixed)
            return AgentResult(stdout="polished", stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.polish_report(_workspace_state(ws), backends={"polish_report": "claude_code"})

        self.assertEqual(update["errors"], [])
        polished = (ws.base / "summary.en.md").read_text()
        self.assertIn("participant LoopNode as io_loop_demangle_ctx", polished)
        self.assertIn("participant CreateNode as io_create_region", polished)
        self.assertIn("CreateNode->>LoopNode: first step, second step", polished)
        self.assertEqual((ws.base / "summary.md").read_text(), polished)
        self.assertEqual(captured["node"], "polish_report")
        self.assertIn("suggested_deterministic_repairs", captured["prompt"])
        log = json.loads((ws.log_path("review_log") / "polish_report.log").read_text())
        self.assertEqual(log["reports"][0]["issues"], [])

    def test_run_polish_report_from_workspace_does_not_require_subtask_res_or_summary_node(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="polish-restore")
        (ws.base / "summary.en.md").write_text("# Executive Summary\n")
        (ws.base / "summary.zh_CN.md").write_text("# 执行摘要\n")

        def fake_invoke(*args, **kwargs):
            del args, kwargs
            return AgentResult(stdout="polished", stderr="", returncode=0, backend="claude_code")

        with patch.object(graph_mod.nodes, "summary") as summary, patch.object(
            nodes, "_invoke", side_effect=fake_invoke
        ):
            final = graph_mod.run_polish_report_from_workspace(str(ws.base))

        summary.assert_not_called()
        self.assertEqual(final["summary"], "# Executive Summary\n")
        self.assertEqual(final["summary_zh_CN"], "# 执行摘要\n")

    def test_polish_report_invokes_agent_for_non_mermaid_structure_issues(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="polish-agent")
        broken = """# Executive Summary

### VULN-001: Broken
```mermaid
sequenceDiagram
A->>B: missing flowchart
```
"""
        (ws.base / "summary.en.md").write_text(broken)
        (ws.base / "summary.zh_CN.md").write_text(broken)
        calls: list[str] = []

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                extra_context,
                timeout,
            )
            calls.append(node)
            fixed = """# Executive Summary

### VULN-001: Fixed
```mermaid
flowchart LR
  A --> B
```
```mermaid
sequenceDiagram
A->>B: fixed
```
"""
            (ws.base / "summary.en.md").write_text(fixed)
            (ws.base / "summary.zh_CN.md").write_text(fixed)
            return AgentResult(stdout="polished", stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.polish_report(_workspace_state(ws), backends={"polish_report": "claude_code"})

        self.assertEqual(calls, ["polish_report"])
        self.assertEqual(update["errors"], [])
        self.assertIn("flowchart LR", (ws.base / "summary.en.md").read_text())


class GraphConfigTest(unittest.TestCase):
    def test_deprecated_run_from_subagent_wrapper_translates_keyword_arguments(self):
        sentinel = {"summary": "done"}
        with patch.object(
            graph_mod,
            "run_from_subtask_workspace",
            return_value=sentinel,
        ) as run_subtasks:
            result = graph_mod.run_from_subagent_workspace(
                "/tmp/workspace",
                selected_subagent_ids=["vuln-001"],
                selected_subagent_log_dir="selected",
                run_summary=False,
            )

        self.assertIs(result, sentinel)
        self.assertEqual(
            run_subtasks.call_args.kwargs["selected_subtask_ids"],
            ["vuln-001"],
        )
        self.assertEqual(
            run_subtasks.call_args.kwargs["selected_subtask_log_dir"],
            "selected",
        )

    def test_native_subagent_nodes_accept_only_capable_primary_and_fallback_runtimes(self):
        for node in ("investigate_subtask", "critic_subtask", "summary"):
            variants = nodes.agent_config_variants_for_node(
                node,
                None,
                {
                    node: {
                        "runtime": "codex_cli",
                        "fallbacks": [
                            {"runtime": "trae-cli"},
                            {"runtime": "claude_code"},
                        ],
                    }
                },
            )
            self.assertEqual(
                [variant["runtime"] for variant in variants],
                ["codex", "traex", "claude_code"],
            )

    def test_native_subagent_nodes_reject_unsupported_primary_or_fallback(self):
        variants = nodes.agent_config_variants_for_node(
            "investigate_subtask",
            None,
            {"investigate_subtask": {"runtime": "dsh"}},
        )
        self.assertEqual([variant["runtime"] for variant in variants], ["dsh"])
        with self.assertRaisesRegex(ValueError, r"unsupported runtime\(s\): kimi"):
            nodes.agent_config_variants_for_node(
                "critic_subtask",
                None,
                {
                    "critic_subtask": {
                        "runtime": "codex",
                        "fallbacks": [{"runtime": "kimi"}],
                    }
                },
            )

    def test_native_subagent_gate_accepts_legacy_node_alias_and_inherited_fallback_runtime(self):
        variants = nodes.agent_config_variants_for_node(
            "investigate_subagent",
            None,
            {
                "investigate_subagent": {
                    "runtime": "codex",
                    "fallbacks": [{"model": "alternate-model"}],
                }
            },
        )
        self.assertEqual(
            [variant["runtime"] for variant in variants],
            ["codex", "codex"],
        )

    def test_legacy_critic_one_backend_override_maps_to_critic_subtask(self):
        variants = nodes.agent_config_variants_for_node(
            "critic_subtask",
            {"critic_one": "trae-cli"},
            {},
        )
        self.assertEqual([variant["runtime"] for variant in variants], ["traex"])

    def test_legacy_critic_one_function_alias_tracks_monkeypatches(self):
        sentinel = object()
        original = nodes.critic_subtask
        try:
            nodes.critic_one = sentinel
            self.assertIs(nodes.critic_subtask, sentinel)
        finally:
            nodes.critic_subtask = original
            nodes.critic_one = original

    def test_native_subagent_enable_flags_are_added_only_to_required_nodes(self):
        self.assertEqual(
            nodes.agent_extra_args_for_node("summary", "codex", {}),
            ["--enable", "multi_agent"],
        )
        self.assertEqual(
            nodes.agent_extra_args_for_node("critic_subtask", "traex", {}),
            ["--config", "features.multi_agent_v2.enabled=true"],
        )
        self.assertEqual(
            nodes.agent_extra_args_for_node("plan_by_spec", "codex", {}),
            [],
        )

    def test_run_rejects_multi_repo_diff_mode_for_programmatic_callers(self):
        with TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "full scan mode only"):
                graph_mod.run(
                    target="product",
                    workspace_root=tmp,
                    scan_mode="diff",
                    diff_file="change.patch",
                    target_repos=[
                        {"id": "core", "target": "https://example.com/core.git"}
                    ],
                )

    def test_run_sets_langgraph_max_concurrency(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        captured = {}

        class FakeGraph:
            def invoke(self, state, config=None):
                captured["state"] = state
                captured["config"] = config
                return {**state, "summary": "done"}

        with patch.object(graph_mod, "build_graph", return_value=FakeGraph()):
            final = graph_mod.run(
                target="libfoo",
                workspace_root=tmp.name,
                max_concurrency=3,
            )

        self.assertEqual(final["summary"], "done")
        self.assertEqual(captured["config"]["max_concurrency"], 3)

    def test_run_till_analyze_stops_after_attack_surface(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        seen = {"plan": 0, "summary": 0}

        def fetch(state, *, backends=None):
            del backends
            return {"repo_path": f"{state['workspace_root']}/{state['task_id']}/main/repo", "errors": []}

        def empty(*args, **kwargs):
            del args, kwargs
            return {"errors": []}

        def analyze(state, *, backends=None):
            del backends
            ws = Workspace.open(state["workspace_root"], state["task_id"])
            out = ws.main_path("attack_surface") / "attack_surface.md"
            out.write_text("attack surface")
            _write_domain_registry(ws)
            registry = ws.main_path("attack_surface") / "domain_invariant_registry.json"
            return {"attack_surface": str(out), "domain_registry_path": str(registry), "domain_registry": json.loads(registry.read_text()), "errors": []}

        def plan(state, *, backends=None):
            del state, backends
            seen["plan"] += 1
            return {"vuln_subtasks": [], "errors": []}

        def summary(state, *, backends=None):
            del state, backends
            seen["summary"] += 1
            return {"summary": "should not run"}

        with patch.object(graph_mod.nodes, "fetch_target_repo", side_effect=fetch), patch.object(
            graph_mod.nodes, "search_spec", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_fuzz_driver", side_effect=empty), patch.object(
            graph_mod.nodes, "search_similar_software", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_similar_history", side_effect=empty), patch.object(
            graph_mod.nodes, "search_target_history", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_new_feature", side_effect=empty), patch.object(
            graph_mod.nodes, "analyze_attack_surface", side_effect=analyze
        ), patch.object(
            graph_mod.nodes, "plan_by_vuln_similar", side_effect=plan
        ), patch.object(graph_mod.nodes, "summary", side_effect=summary):
            final = graph_mod.run(target="libfoo", workspace_root=tmp.name, till_node="analyze")

        self.assertEqual(final["stopped_at"], "analyze")
        self.assertEqual(seen, {"plan": 0, "summary": 0})
        self.assertNotIn("summary", final)
        self.assertEqual(final.get("errors") or [], [])

    def test_run_till_plan_stops_after_planners(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        seen = {"summary": 0}

        def fetch(state, *, backends=None):
            del backends
            return {"repo_path": f"{state['workspace_root']}/{state['task_id']}/main/repo", "errors": []}

        def empty(*args, **kwargs):
            del args, kwargs
            return {"errors": []}

        def analyze(state, *, backends=None):
            del backends
            ws = Workspace.open(state["workspace_root"], state["task_id"])
            out = ws.main_path("attack_surface") / "attack_surface.md"
            out.write_text("attack surface")
            return {"attack_surface": str(out), "errors": []}

        def plan_spec(state, *, backends=None):
            del backends
            ws = Workspace.open(state["workspace_root"], state["task_id"])
            out = ws.state_path("plan_by_spec.json")
            out.write_text(json.dumps([{"id": "spec-001", "bucket": "spec", "objective": "spec", "hints": {}}]))
            return {"spec_subtasks": [{"id": "spec-001", "bucket": "spec", "objective": "spec", "hints": {}}], "errors": []}

        def plan_vuln(state, *, backends=None):
            del backends
            ws = Workspace.open(state["workspace_root"], state["task_id"])
            out = ws.state_path("plan_by_vuln.json")
            out.write_text(json.dumps([{"id": "vuln-001", "bucket": "vuln", "objective": "vuln", "hints": {}}]))
            return {"vuln_subtasks": [{"id": "vuln-001", "bucket": "vuln", "objective": "vuln", "hints": {}}], "errors": []}

        def plan_patch(state, *, backends=None):
            del backends
            ws = Workspace.open(state["workspace_root"], state["task_id"])
            out = ws.state_path("plan_by_patch.json")
            out.write_text(json.dumps([{"id": "patch-001", "bucket": "patch_miss", "objective": "patch", "hints": {}}]))
            return {"patch_subtasks": [{"id": "patch-001", "bucket": "patch_miss", "objective": "patch", "hints": {}}], "errors": []}

        def plan_feature(state, *, backends=None):
            del backends
            ws = Workspace.open(state["workspace_root"], state["task_id"])
            out = ws.state_path("plan_by_feature.json")
            out.write_text(json.dumps([{"id": "feat-001", "bucket": "feature", "objective": "feature", "hints": {}}]))
            return {"feature_subtasks": [{"id": "feat-001", "bucket": "feature", "objective": "feature", "hints": {}}], "errors": []}

        def summary(state, *, backends=None):
            del state, backends
            seen["summary"] += 1
            return {"summary": "should not run"}

        with patch.object(graph_mod.nodes, "fetch_target_repo", side_effect=fetch), patch.object(
            graph_mod.nodes, "search_spec", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_fuzz_driver", side_effect=empty), patch.object(
            graph_mod.nodes, "search_similar_software", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_similar_history", side_effect=empty), patch.object(
            graph_mod.nodes, "search_target_history", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_new_feature", side_effect=empty
        ), patch.object(graph_mod.nodes, "analyze_attack_surface", side_effect=analyze), patch.object(
            graph_mod.nodes, "plan_by_spec", side_effect=plan_spec
        ), patch.object(graph_mod.nodes, "plan_by_vuln_similar", side_effect=plan_vuln), patch.object(
            graph_mod.nodes, "plan_by_vuln_patch", side_effect=plan_patch
        ), patch.object(graph_mod.nodes, "plan_by_new_feature", side_effect=plan_feature
        ), patch.object(graph_mod.nodes, "summary", side_effect=summary):
            final = graph_mod.run(target="libfoo", workspace_root=tmp.name, till_node="plan")

        self.assertEqual(final["stopped_at"], "plan")
        self.assertEqual(seen["summary"], 0)
        self.assertEqual(final.get("errors") or [], [])

    def test_run_from_subtask_workspace_loads_plan_json_and_summarizes(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="restore")
        (ws.main_path("repo") / "README.md").write_text("source")
        (ws.main_path("attack_surface") / "attack_surface.md").write_text("surface")
        (ws.main_path("spec") / "spec.md").write_text("spec")
        (ws.similar / "peer" / "writeup").mkdir(parents=True)
        (ws.similar / "peer" / "writeup" / "case.md").write_text("writeup")
        state_dir = ws.log_path("state")
        (state_dir / "plan_by_spec.json").write_text(
            json.dumps([{"id": "spec-001", "bucket": "spec", "objective": "spec", "hints": {}}])
        )
        (state_dir / "plan_by_vuln.json").write_text(
            json.dumps([{"id": "vuln-001", "bucket": "vuln", "objective": "vuln", "hints": {}}])
        )
        (state_dir / "plan_by_patch.json").write_text(
            json.dumps([{"id": "patch-001", "bucket": "patch_miss", "objective": "patch", "hints": {}}])
        )
        (state_dir / "plan_by_feature.json").write_text(
            json.dumps([{"id": "feat-001", "bucket": "feature", "objective": "feature", "hints": {}}])
        )
        seen = {"subtasks": [], "summary": 0}

        def fake_subtask(state):
            subtask = state["subtask"]
            seen["subtasks"].append(subtask["id"])
            if subtask["bucket"] == "spec":
                return {"spec_findings": [{"subtask_id": subtask["id"], "kind": "spec"}]}
            if subtask["bucket"] == "vuln":
                return {"vuln_candidates": [{"subtask_id": subtask["id"], "kind": "vuln"}]}
            if subtask["bucket"] == "feature":
                return {"feature_findings": [{"subtask_id": subtask["id"], "kind": "feature"}]}
            return {"patch_findings": [{"subtask_id": subtask["id"], "kind": "patch_miss"}]}

        def summary(state, *, backends=None):
            del backends
            seen["summary"] += 1
            return {
                "summary": (
                    f"spec={len(state.get('spec_findings', []))} "
                    f"vuln={len(state.get('vuln_candidates', []))} "
                    f"patch={len(state.get('patch_findings', []))} "
                    f"feature={len(state.get('feature_findings', []))}"
                )
            }

        with patch.object(graph_mod, "build_subtask_graph", return_value=fake_subtask), patch.object(
            graph_mod.nodes, "summary", side_effect=summary
        ):
            final = graph_mod.run_from_subtask_workspace(str(ws.base), backends={"investigate_subtask": "codex"})

        self.assertEqual(sorted(seen["subtasks"]), ["feat-001", "patch-001", "spec-001", "vuln-001"])
        self.assertEqual(seen["summary"], 1)
        self.assertEqual(final["summary"], "spec=1 vuln=1 patch=1 feature=1")
        self.assertEqual(final["repo_path"], str(ws.main_path("repo")))
        self.assertEqual(final["domain_registry"]["status"], "legacy_unavailable")

    def test_run_from_subtask_workspace_supports_legacy_review_res_and_plans(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="restore-skip")
        (ws.main_path("repo") / "README.md").write_text("source")
        (ws.main_path("attack_surface") / "attack_surface.md").write_text("surface")
        (ws.main_path("spec") / "spec.md").write_text("spec")
        review_log = ws.log_path("review_log")
        (review_log / "plan_by_spec.json").write_text(
            json.dumps([{"id": "spec-001", "bucket": "spec", "objective": "spec", "hints": {}}])
        )
        (review_log / "plan_by_vuln.json").write_text(
            json.dumps([{"id": "vuln-001", "bucket": "vuln", "objective": "vuln", "hints": {}}])
        )
        (review_log / "plan_by_patch.json").write_text(
            json.dumps([{"id": "patch-001", "bucket": "patch_miss", "objective": "patch", "hints": {}}])
        )
        (review_log / "plan_by_feature.json").write_text(
            json.dumps([{"id": "feat-001", "bucket": "feature", "objective": "feature", "hints": {}}])
        )
        review_res = ws.log_path("review_res")
        review_res.mkdir()
        (review_res / "spec-001.json").write_text(
            json.dumps({"finding": {"kind": "spec", "subtask_id": "spec-001", "title": "old spec"}})
        )
        (review_res / "stale-001.json").write_text(
            json.dumps({"finding": {"kind": "spec", "subtask_id": "stale-001", "title": "stale"}})
        )
        (review_res / "patch-001.json").write_text(
            json.dumps({"finding": {"kind": "patch_miss", "subtask_id": "patch-001", "title": "old patch"}})
        )
        seen = {"subtasks": []}

        def fake_subtask(state):
            subtask = state["subtask"]
            seen["subtasks"].append(subtask["id"])
            if subtask["bucket"] == "vuln":
                return {"vuln_candidates": [{"subtask_id": subtask["id"], "kind": "vuln"}]}
            return {"feature_findings": [{"subtask_id": subtask["id"], "kind": "feature"}]}

        def summary(state, *, backends=None):
            del backends
            return {
                "summary": (
                    f"spec={len(state.get('spec_findings', []))} "
                    f"vuln={len(state.get('vuln_candidates', []))} "
                    f"patch={len(state.get('patch_findings', []))} "
                    f"feature={len(state.get('feature_findings', []))}"
                )
            }

        with patch.object(graph_mod, "build_subtask_graph", return_value=fake_subtask), patch.object(
            graph_mod.nodes, "summary", side_effect=summary
        ):
            final = graph_mod.run_from_subtask_workspace(str(ws.base), backends={"investigate_subtask": "codex"})

        self.assertEqual(sorted(seen["subtasks"]), ["feat-001", "vuln-001"])
        self.assertEqual(final["summary"], "spec=1 vuln=1 patch=1 feature=1")
        self.assertEqual(final["completed_subtask_ids"], ["patch-001", "spec-001"])

    def test_subtask_res_overrides_same_named_legacy_review_res(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="result-overlay")
        legacy = ws.log_path("review_res")
        legacy.mkdir()
        (legacy / "vuln-001.json").write_text(
            json.dumps(
                {"finding": {"kind": "vuln", "subtask_id": "vuln-001", "title": "old"}}
            )
        )
        (ws.log_path("subtask_res") / "vuln-001.json").write_text(
            json.dumps(
                {"finding": {"kind": "vuln", "subtask_id": "vuln-001", "title": "new"}}
            )
        )

        payloads = graph_mod._subtask_res_payloads(ws, require_findings=True)

        self.assertEqual(len(payloads), 1)
        self.assertEqual(payloads[0][1]["finding"]["title"], "new")

    def test_batch_restore_tracks_parent_package_and_loads_atomic_findings(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="batch-restore")
        result_dir = ws.log_path("subtask_res")
        active_path = result_dir / "spec-028--hyp-cred.json"
        rejected_path = result_dir / "spec-028--hyp-cpu.json"
        (result_dir / "spec-028.json").write_text(
            json.dumps(
                {
                    "schema_version": "3.0",
                    "result_type": "hypothesis_package",
                    "package_id": "spec-028",
                    "closed": True,
                    "artifacts": [
                        {"hypothesis_id": "hyp-cred", "path": str(active_path)},
                        {"hypothesis_id": "hyp-cpu", "path": str(rejected_path)},
                    ],
                }
            )
        )
        active_path.write_text(
            json.dumps(
                {
                    "schema_version": "3.0",
                    "outcome_type": "standalone_finding",
                    "finding": {
                        "kind": "spec",
                        "subtask_id": "spec-028--hyp-cred",
                        "parent_subtask_id": "spec-028",
                        "hypothesis_id": "hyp-cred",
                        "title": "credential finding",
                        **_qualified_review(),
                    },
                }
            )
        )
        rejected_path.write_text(
            json.dumps(
                {
                    "schema_version": "3.0",
                    "outcome_type": "rejected",
                    "finding": {
                        "kind": "spec",
                        "subtask_id": "spec-028--hyp-cpu",
                        "parent_subtask_id": "spec-028",
                        "hypothesis_id": "hyp-cpu",
                        "title": "no finding",
                    },
                }
            )
        )

        self.assertEqual(
            graph_mod._completed_subtask_ids_from_subtask_res(ws),
            ["spec-028"],
        )
        spec, vuln, patch_findings, feature = graph_mod._finding_buckets_from_subtask_res(ws)
        self.assertEqual([item["hypothesis_id"] for item in spec], ["hyp-cred"])
        self.assertEqual(vuln, [])
        self.assertEqual(patch_findings, [])
        self.assertEqual(feature, [])
        self.assertEqual(
            graph_mod._filter_findings_by_subtask_ids(spec, {"spec-028"}),
            spec,
        )

    def test_batch_restore_ignores_atomic_artifact_dropped_by_latest_manifest(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="batch-stale")
        result_dir = ws.log_path("subtask_res")
        active_path = result_dir / "spec-028--active.json"
        stale_path = result_dir / "spec-028--stale.json"
        (result_dir / "spec-028.json").write_text(
            json.dumps(
                {
                    "schema_version": "3.0",
                    "result_type": "hypothesis_package",
                    "package_id": "spec-028",
                    "closed": True,
                    "artifacts": [
                        {
                            "hypothesis_id": "hyp-active",
                            # Deliberately use an old absolute root: restore
                            # should use the artifact basename after relocation.
                            "path": f"/old/workspace/log/subtask_res/{active_path.name}",
                        }
                    ],
                }
            )
        )
        for path, hypothesis_id, title in (
            (active_path, "hyp-active", "current"),
            (stale_path, "hyp-stale", "stale from an earlier rerun"),
        ):
            path.write_text(
                json.dumps(
                    {
                        "schema_version": "3.0",
                        "outcome_type": "standalone_finding",
                        "finding": {
                            "kind": "spec",
                            "subtask_id": f"spec-028--{hypothesis_id}",
                            "parent_subtask_id": "spec-028",
                            "hypothesis_id": hypothesis_id,
                            "title": title,
                            **_qualified_review(),
                        },
                    }
                )
            )

        spec, _, _, _ = graph_mod._finding_buckets_from_subtask_res(ws)

        self.assertEqual([item["hypothesis_id"] for item in spec], ["hyp-active"])
        self.assertEqual(
            [path.name for path in nodes.active_subtask_result_files(ws)],
            ["spec-028--active.json", "spec-028.json"],
        )

    def test_run_selected_subtasks_reruns_existing_result_without_summary(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="restore-selected")
        (ws.main_path("repo") / "README.md").write_text("source")
        (ws.main_path("attack_surface") / "attack_surface.md").write_text("surface")
        (ws.main_path("spec") / "spec.md").write_text("spec")
        state_dir = ws.log_path("state")
        (state_dir / "plan_by_spec.json").write_text(
            json.dumps(
                [{"id": "spec-012", "bucket": "spec", "objective": "spec", "hints": {}}]
            )
        )
        (state_dir / "plan_by_vuln.json").write_text(
            json.dumps(
                [{"id": "vuln-013", "bucket": "vuln", "objective": "vuln", "hints": {}}]
            )
        )
        (state_dir / "plan_by_patch.json").write_text(
            json.dumps(
                [{"id": "patch-008", "bucket": "patch_miss", "objective": "patch", "hints": {}}]
            )
        )
        canonical_result = ws.log_path("subtask_res") / "vuln-013.json"
        canonical_payload = {
            "finding": {
                "kind": "vuln",
                "subtask_id": "vuln-013",
                "title": "canonical result",
            },
            "history": [{"iteration": 1, "review": {"verdict": "confirm"}}],
        }
        canonical_result.write_text(json.dumps(canonical_payload))
        canonical_investigation_log = (
            ws.log_path("review_log") / "vuln-013.investigation.log"
        )
        canonical_investigation_log.write_text("canonical investigation log")
        canonical_command_log = ws.log / "agent_commands.jsonl"
        canonical_command_log.write_text('{"node":"old"}\n')
        seen: list[str] = []

        def fake_subtask(state):
            subtask = state["subtask"]
            seen.append(subtask["id"])
            selected_dir = Path(state["selected_subtask_log_dir"])
            payload = {
                "finding": {
                    "kind": subtask["bucket"],
                    "subtask_id": subtask["id"],
                    "title": f"rerun {subtask['id']}",
                    "severity": "high",
                    "iterations": 2,
                    "review": {"verdict": "confirm"},
                },
                "history": [
                    {"iteration": 1, "review": {"verdict": "revise"}},
                    {"iteration": 2, "review": {"verdict": "confirm"}},
                ],
            }
            (selected_dir / "results" / f"{subtask['id']}.json").write_text(
                json.dumps(payload)
            )
            return {}

        with patch.object(
            graph_mod,
            "build_subtask_graph",
            return_value=fake_subtask,
        ), patch.object(graph_mod.nodes, "summary") as summary:
            final = graph_mod.run_from_subtask_workspace(
                str(ws.base),
                selected_subtask_ids=["vuln013", "patch-008", "spec012"],
                selected_subtask_log_dir="selected-rerun",
                run_summary=False,
            )

        selected_dir = ws.base / "selected-rerun"
        self.assertEqual(sorted(seen), ["patch-008", "spec-012", "vuln-013"])
        summary.assert_not_called()
        self.assertEqual(final["stopped_at"], "selected_subtasks")
        self.assertEqual(
            [item["subtask_id"] for item in final["selected_subtask_statuses"]],
            ["vuln-013", "patch-008", "spec-012"],
        )
        self.assertEqual(
            final["selected_subagent_statuses"],
            final["selected_subtask_statuses"],
        )
        self.assertTrue(
            all(
                item["status"] == "completed"
                for item in final["selected_subtask_statuses"]
            )
        )
        self.assertEqual(json.loads(canonical_result.read_text()), canonical_payload)
        self.assertEqual(
            canonical_investigation_log.read_text(),
            "canonical investigation log",
        )
        self.assertEqual(canonical_command_log.read_text(), '{"node":"old"}\n')
        selected_payload = json.loads(
            (selected_dir / "results" / "vuln-013.json").read_text()
        )
        self.assertIn("finding", selected_payload)
        self.assertEqual(len(selected_payload["history"]), 2)
        self.assertTrue((selected_dir / "selected_subtask_statuses.json").is_file())
        self.assertTrue((selected_dir / "selected_subagent_statuses.json").is_file())

    def test_run_selected_subtasks_rejects_unknown_id_and_existing_output_dir(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="restore-selected-errors")
        (ws.main_path("repo") / "README.md").write_text("source")
        (ws.main_path("attack_surface") / "attack_surface.md").write_text("surface")
        state_dir = ws.log_path("state")
        (state_dir / "plan_by_spec.json").write_text("[]")
        (state_dir / "plan_by_vuln.json").write_text(
            json.dumps(
                [{"id": "vuln-013", "bucket": "vuln", "objective": "vuln", "hints": {}}]
            )
        )
        (state_dir / "plan_by_patch.json").write_text("[]")

        with self.assertRaisesRegex(ValueError, "not found in planner outputs"):
            graph_mod.run_from_subtask_workspace(
                str(ws.base),
                selected_subtask_ids=["vuln-999"],
                run_summary=False,
            )

        existing = ws.base / "selected-existing"
        existing.mkdir()
        with self.assertRaisesRegex(ValueError, "already exists"):
            graph_mod.run_from_subtask_workspace(
                str(ws.base),
                selected_subtask_ids=["vuln-013"],
                selected_subtask_log_dir=existing,
                run_summary=False,
            )

        with self.assertRaisesRegex(ValueError, "must stay inside the workspace"):
            graph_mod.run_from_subtask_workspace(
                str(ws.base),
                selected_subtask_ids=["vuln-013"],
                selected_subtask_log_dir="../escaped-selected-run",
                run_summary=False,
            )

    def test_selected_status_reads_hypothesis_package_manifest(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        selected_dir = Path(tmp.name) / "selected-batch"
        (selected_dir / "results").mkdir(parents=True)
        result_path = selected_dir / "results" / "spec-028.json"
        result_path.write_text(
            json.dumps(
                {
                    "schema_version": "3.0",
                    "result_type": "hypothesis_package",
                    "package_id": "spec-028",
                    "closed": True,
                    "review": {"package_decision": "close"},
                    "history": [{"iteration": 1}, {"iteration": 2}],
                    "artifacts": [],
                }
            )
        )

        update = nodes.collect_selected_subtask_statuses(
            {
                "selected_subtask_log_dir": str(selected_dir),
                "selected_subtask_ids": ["spec-028"],
                "errors": [],
            }
        )

        self.assertEqual(
            update["selected_subtask_statuses"],
            [
                {
                    "subtask_id": "spec-028",
                    "status": "completed",
                    "verdict": "close",
                    "severity": "",
                    "iterations": 2,
                    "result_path": str(result_path),
                    "errors": [],
                }
            ],
        )

    def test_run_summary_from_workspace_loads_subtask_res_findings(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="summary-restore")
        (ws.main_path("repo") / "README.md").write_text("source")
        (ws.main_path("attack_surface") / "attack_surface.md").write_text("surface")
        subtask_res = ws.log_path("subtask_res")
        (subtask_res / "spec-001.json").write_text(
            json.dumps({"finding": {"kind": "spec", "subtask_id": "spec-001", "title": "spec"}})
        )
        (subtask_res / "vuln-001.json").write_text(
            json.dumps({"finding": {"kind": "vuln", "subtask_id": "vuln-001", "title": "vuln"}})
        )
        (subtask_res / "patch-001.json").write_text(
            json.dumps({"finding": {"kind": "patch_miss", "subtask_id": "patch-001", "title": "patch"}})
        )
        (subtask_res / "feat-001.json").write_text(
            json.dumps({"finding": {"kind": "feature", "subtask_id": "feat-001", "title": "feature"}})
        )
        seen = {}

        def summary(state, *, backends=None):
            del backends
            seen["counts"] = (
                len(state.get("spec_findings", [])),
                len(state.get("vuln_candidates", [])),
                len(state.get("patch_findings", [])),
                len(state.get("feature_findings", [])),
            )
            return {"summary": f"counts={seen['counts']}"}

        with patch.object(graph_mod.nodes, "summary", side_effect=summary):
            final = graph_mod.run_summary_from_workspace(str(ws.base), backends={"summary": "claude_code"})

        self.assertEqual(seen["counts"], (1, 1, 1, 1))
        self.assertEqual(final["summary"], "counts=(1, 1, 1, 1)")
        self.assertEqual(final["repo_path"], str(ws.main_path("repo")))

    def test_run_summary_from_workspace_preserves_target_repos_manifest(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="product", task_id="summary-restore-multi")
        (ws.main_path("repo") / "core").mkdir(parents=True)
        (ws.main_path("repo") / "core" / "README.md").write_text("core")
        (ws.main_path("attack_surface") / "attack_surface.md").write_text("surface")
        (ws.main_path("scope") / "scope.json").write_text(json.dumps({"mode": "full", "repo_path": str(ws.main_path("repo"))}))
        (ws.main_path("repos") / "_manifest.json").write_text(
            json.dumps(
                {
                    "repos": [
                        {
                            "id": "core",
                            "target": "https://example.com/core.git",
                            "source_path": str(ws.main_path("repos") / "core"),
                            "aggregate_path": str(ws.main_path("repo") / "core"),
                        }
                    ]
                }
            )
        )
        final_state = ws.base / "final_state.json"
        final_state.write_text(
            json.dumps(
                {
                    "target": "product",
                    "target_repos": [{"id": "core", "target": "https://example.com/core.git"}],
                }
            )
        )
        subtask_res = ws.log_path("subtask_res")
        (subtask_res / "vuln-001.json").write_text(
            json.dumps({"finding": {"kind": "vuln", "subtask_id": "vuln-001", "title": "seed"}})
        )

        with patch.object(graph_mod.nodes, "summary", side_effect=lambda state, *, backends=None: {"summary": state["target_repos_path"]}):
            final = graph_mod.run_summary_from_workspace(str(ws.base), backends={"summary": "claude_code"})

        self.assertEqual(final["target_repos"], [{"id": "core", "target": "https://example.com/core.git"}])
        self.assertEqual(final["target_repos_path"], str(ws.main_path("repos") / "_manifest.json"))
        self.assertEqual(final["summary"], str(ws.main_path("repos") / "_manifest.json"))


class FetchTargetRepoTest(unittest.TestCase):
    def test_fetch_target_repo_copies_local_directory_without_agent_or_source_mutation(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        source = root / "source"
        source.mkdir()
        (source / "README.md").write_text("source tree")
        (source / "pkg").mkdir()
        (source / "pkg" / "code.py").write_text("print('ok')\n")
        (source / ".git").mkdir()
        (source / ".git" / "config").write_text("private git metadata")
        (source / ".zeromdash").mkdir()
        (source / ".zeromdash" / "old.txt").write_text("old workspace")

        ws = Workspace.create(root / "workspaces", target=str(source), task_id="fetch-local")

        with patch.object(nodes, "_invoke") as invoke:
            update = nodes.fetch_target_repo(
                {
                    "target": str(source),
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"fetch_target_repo": "claude_code"},
            )

        invoke.assert_not_called()
        self.assertEqual(update["errors"], [])
        self.assertEqual(update["repo_path"], str(ws.main_path("repo")))
        self.assertEqual((ws.main_path("repo") / "README.md").read_text(), "source tree")
        self.assertEqual((ws.main_path("repo") / "pkg" / "code.py").read_text(), "print('ok')\n")
        self.assertFalse((ws.main_path("repo") / ".git").exists())
        self.assertFalse((ws.main_path("repo") / ".zeromdash").exists())
        self.assertTrue((source / ".git" / "config").is_file())
        self.assertIn("deterministic local copy", (ws.log_path("review_log") / "fetch_target_repo.log").read_text())

    def test_fetch_target_repo_materializes_local_multi_repo_aggregate_view(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        core = root / "core"
        plugin = root / "plugin"
        core.mkdir()
        plugin.mkdir()
        (core / "core.go").write_text("package core\n")
        (plugin / "plugin.go").write_text("package plugin\n")
        (core / ".git").mkdir()
        (core / ".git" / "config").write_text("private")

        ws = Workspace.create(root / "workspaces", target="product", task_id="fetch-multi-local")

        with patch.object(nodes, "_invoke") as invoke:
            update = nodes.fetch_target_repo(
                {
                    "target": "product",
                    "target_repos": [
                        {"id": "core", "target": str(core), "role": "main"},
                        {"id": "plugin-auth", "target": str(plugin), "role": "plugin"},
                    ],
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"fetch_target_repo": "claude_code"},
            )

        invoke.assert_not_called()
        self.assertEqual(update["errors"], [])
        self.assertEqual(update["repo_path"], str(ws.main_path("repo")))
        self.assertEqual((ws.main_path("repos") / "core" / "core.go").read_text(), "package core\n")
        self.assertEqual((ws.main_path("repos") / "plugin-auth" / "plugin.go").read_text(), "package plugin\n")
        self.assertEqual((ws.main_path("repo") / "core" / "core.go").read_text(), "package core\n")
        self.assertEqual((ws.main_path("repo") / "plugin-auth" / "plugin.go").read_text(), "package plugin\n")
        self.assertTrue((ws.main_path("repo") / "core").is_symlink())
        self.assertTrue((ws.main_path("repo") / "plugin-auth").is_symlink())
        self.assertEqual(os.readlink(ws.main_path("repo") / "core"), "../repos/core")
        manifest = json.loads((ws.main_path("repos") / "_manifest.json").read_text())
        self.assertEqual([item["id"] for item in manifest["repos"]], ["core", "plugin-auth"])
        aggregate_manifest = json.loads((ws.main_path("repo") / "_target_repos.json").read_text())
        self.assertEqual([item["id"] for item in aggregate_manifest["repos"]], ["core", "plugin-auth"])
        self.assertEqual(update["target_repos_path"], str(ws.main_path("repos") / "_manifest.json"))

    def test_fetch_target_repo_invokes_claude_engine_and_records_repo_path(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="https://example.com/libfoo.git", task_id="fetch")
        captured = {}

        def fake_invoke(
            ws_arg, node, prompt, backends, agent_configs=None, agent_config_task_types=None, subtask_id=None, extra_context=None, timeout=None
        ):
            (ws.main_path("repo") / "README.md").write_text("source tree")
            captured.update(
                {
                    "ws": ws_arg,
                    "node": node,
                    "prompt": prompt,
                    "backends": backends,
                    "agent_configs": agent_configs,
                    "subtask_id": subtask_id,
                    "extra_context": extra_context,
                    "timeout": timeout,
                }
            )
            return AgentResult(
                stdout="fetched ok",
                stderr="",
                returncode=0,
                backend="claude_code",
                metadata={"resume_id": "sess-fetch"},
            )

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.fetch_target_repo(
                {
                    "target": "https://example.com/libfoo.git",
                    "diff_git": "v1.0..main",
                    "common_focus": "network reachable code",
                    "fetch_target_repo_focus": "HTTP parser module",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"fetch_target_repo": "claude_code"},
            )

        self.assertEqual(update["repo_path"], str(ws.main_path("repo")))
        self.assertEqual(update["errors"], [])
        self.assertEqual(captured["node"], "fetch_target_repo")
        self.assertEqual(captured["backends"], {"fetch_target_repo": "claude_code"})
        self.assertIsNone(captured["subtask_id"])
        self.assertIn("https://example.com/libfoo.git", captured["prompt"])
        self.assertIn("v1.0..main", captured["prompt"])
        self.assertIn('Global focus: "network reachable code"', captured["prompt"])
        self.assertIn('Stage-specific focus: "HTTP parser module"', captured["prompt"])
        self.assertIn('Global focus: "network reachable code"', captured["extra_context"]["focus"])
        self.assertIn('Stage-specific focus: "HTTP parser module"', captured["extra_context"]["focus"])
        self.assertIn(str(ws.main_path("repo")), captured["prompt"])
        self.assertIn("Verify Destination contains real source files", captured["prompt"])
        self.assertIn("not just an empty directory", captured["prompt"])
        self.assertIn("fetched ok", (ws.log_path("review_log") / "fetch_target_repo.log").read_text())

    def test_fetch_target_repo_invokes_agent_for_remote_multi_repo(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="product", task_id="fetch-multi-remote")
        captured = {}

        def fake_invoke(
            ws_arg, node, prompt, backends, agent_configs=None, agent_config_task_types=None, subtask_id=None, extra_context=None, timeout=None
        ):
            (ws.main_path("repos") / "core").mkdir(parents=True, exist_ok=True)
            (ws.main_path("repos") / "core" / "README.md").write_text("core")
            (ws.main_path("repos") / "plugin-auth").mkdir(parents=True, exist_ok=True)
            (ws.main_path("repos") / "plugin-auth" / "README.md").write_text("plugin")
            captured.update({"prompt": prompt, "node": node, "backends": backends})
            return AgentResult(stdout="fetched multi", stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.fetch_target_repo(
                {
                    "target": "product",
                    "target_repos": [
                        {"id": "core", "target": "https://example.com/core.git", "role": "main"},
                        {"id": "plugin-auth", "target": "https://example.com/plugin.git", "role": "plugin"},
                    ],
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"fetch_target_repo": "claude_code"},
            )

        self.assertEqual(update["errors"], [])
        self.assertEqual(captured["node"], "fetch_target_repo")
        self.assertIn('"id": "core"', captured["prompt"])
        self.assertIn('"destination":', captured["prompt"])
        self.assertIn(str(ws.main_path("repos") / "core"), captured["prompt"])
        self.assertEqual((ws.main_path("repo") / "core" / "README.md").read_text(), "core")
        self.assertEqual((ws.main_path("repo") / "plugin-auth" / "README.md").read_text(), "plugin")

    def test_invoke_records_agent_resume_metadata(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="invoke-meta")

        class FakeAgent:
            def run(self, prompt, cwd=None, timeout=None, extra_args=None, env=None):
                del prompt, timeout, extra_args, env
                return AgentResult(
                    stdout="ok",
                    stderr="",
                    returncode=0,
                    backend="claude_code",
                    cwd=str(cwd),
                    metadata={"resume_id": "sess-fetch", "command": ["claude", "-p", "--output-format", "json"]},
                )

        stderr = io.StringIO()
        with patch.dict("os.environ", {}, clear=True), patch.object(
            nodes, "_make_agent", return_value=FakeAgent()
        ), patch("sys.stderr", stderr):
            nodes._invoke(ws, "fetch_target_repo", "prompt", {"fetch_target_repo": "claude_code"})

        console = stderr.getvalue()
        self.assertIn("node fetch_target_repo: running runtime claude_code", console)
        self.assertIn("node fetch_target_repo: finished runtime claude_code ok=true rc=0", console)
        self.assertIn('command: ["claude", "-p", "--output-format", "json"]', console)
        self.assertIn("resume_id: sess-fetch", console)
        meta = json.loads((ws.sub_workspace_root / "node_fetch_target_repo" / "agent_invocation.json").read_text())
        self.assertEqual(meta["resume_id"], "sess-fetch")
        self.assertEqual(meta["backend"], "claude_code")
        log_records = [
            json.loads(line)
            for line in (ws.log / "agent_commands.jsonl").read_text().splitlines()
        ]
        self.assertEqual(len(log_records), 1)
        self.assertEqual(log_records[0]["node"], "fetch_target_repo")
        self.assertEqual(log_records[0]["backend"], "claude_code")
        self.assertEqual(log_records[0]["command"], ["claude", "-p", "--output-format", "json"])
        self.assertEqual(log_records[0]["resume_id"], "sess-fetch")
        self.assertTrue(log_records[0]["ok"])
        self.assertIn("node_fetch_target_repo", log_records[0]["sub_workspace"])

    def test_agent_extra_args_for_node_uses_task_type_and_backend(self):
        agent_configs = {
            "search_spec": {
                "runtime": "claude_code",
                "provider": "bedrock",
                "config": "/tmp/search-settings.json",
                "model": "claude-sonnet-test",
            },
            "plan_by_spec": {
                "runtime": "codex",
                "provider": "ark",
                "config": "volc_ark",
                "model": "gpt-test",
            },
            "summary": {
                "runtime": "opencode",
                "model": "provider/model",
            },
            "critic_subtask": {
                "runtime": "kimi",
                "model": "moonshot-cn/kimi-k3",
            },
            "investigate_subtask": {
                "runtime": "dsh",
                "provider": "deepseek-official",
                "config": "/tmp/dsh-extra.patch.yml",
                "model": "deepseek-v4-pro",
            },
        }

        self.assertEqual(
            nodes.agent_extra_args_for_node("search_spec", "claude", agent_configs),
            ["--settings", "/tmp/search-settings.json", "--model", "claude-sonnet-test"],
        )
        self.assertEqual(
            nodes.agent_extra_args_for_node("plan_by_spec", "codex", agent_configs),
            ["--profile", "volc_ark", "--model", "gpt-test"],
        )
        self.assertEqual(
            nodes.agent_extra_args_for_node("summary", "opencode", agent_configs),
            ["--model", "provider/model"],
        )
        self.assertEqual(
            nodes.agent_extra_args_for_node("critic_subtask", "kimi", agent_configs),
            ["--model", "moonshot-cn/kimi-k3"],
        )
        self.assertEqual(
            nodes.agent_extra_args_for_node(
                "investigate_subtask",
                "deepseek-harness",
                agent_configs,
            ),
            ["--patch", "/tmp/dsh-extra.patch.yml"],
        )
        self.assertEqual(
            nodes.agent_extra_args_for_node(
                "summary",
                "opencode",
                {"summary": {"runtime": "opencode", "model": ""}},
            ),
            [],
        )

    def test_agent_env_for_node_controls_claude_bedrock_environment(self):
        with patch.dict("os.environ", {"AWS_BEARER_TOKEN_BEDROCK": "token-1"}, clear=True):
            env = nodes.agent_env_for_node(
                "search_spec",
                "claude_code",
                {
                    "search_spec": {
                        "runtime": "claude_code",
                        "provider": "bedrock",
                        "config": "/tmp/settings.json",
                        "env": {"CUSTOM_ENV": "1"},
                    }
                },
            )
            self.assertEqual(env["CLAUDE_CODE_USE_BEDROCK"], "1")
            self.assertEqual(env["AWS_BEARER_TOKEN_BEDROCK"], "token-1")
            self.assertEqual(env["ZEROMDASH_CLAUDE_SETTINGS_PATH"], "/tmp/settings.json")
            self.assertEqual(env["CUSTOM_ENV"], "1")
            self.assertIsNone(env["ZEROMDASH_CLAUDE_MODEL"])
            self.assertIsNone(env["ANTHROPIC_MODEL"])
            self.assertIsNone(env["ANTHROPIC_BASE_URL"])

        self.assertEqual(
            nodes.agent_env_for_node(
                "search_spec",
                "claude_code",
                {
                    "search_spec": {
                        "runtime": "claude_code",
                        "provider": "anthropic",
                        "config": "/tmp/settings.json",
                    }
                },
            ),
            {"CLAUDE_CODE_USE_BEDROCK": None, "AWS_BEARER_TOKEN_BEDROCK": None},
        )

    def test_agent_env_for_node_clears_global_model_when_node_model_is_configured(self):
        self.assertEqual(
            nodes.agent_env_for_node(
                "plan_by_spec",
                "codex",
                {"plan_by_spec": {"runtime": "codex", "model": "gpt-test"}},
            ),
            {"ZEROMDASH_CODEX_MODEL": None},
        )
        self.assertEqual(
            nodes.agent_env_for_node(
                "summary",
                "opencode",
                {"summary": {"runtime": "opencode", "model": ""}},
            ),
            {"ZEROMDASH_OPENCODE_MODEL": None},
        )
        self.assertEqual(
            nodes.agent_env_for_node(
                "investigate_subtask",
                "dsh",
                {
                    "investigate_subtask": {
                        "runtime": "dsh",
                        "provider": "deepseek-official",
                        "model": "deepseek-v4-pro",
                    }
                },
            ),
            {
                "ZEROMDASH_DSH_PROVIDER": "deepseek-official",
                "ZEROMDASH_DSH_MODEL": "deepseek-v4-pro",
            },
        )
        self.assertEqual(
            nodes.agent_env_for_node(
                "summary",
                "opencode",
                {"summary": {"runtime": "opencode"}},
            ),
            {},
        )
        self.assertEqual(
            nodes.agent_env_for_node(
                "critic_subtask",
                "kimi",
                {"critic_subtask": {"runtime": "kimi", "model": "moonshot-cn/kimi-k3"}},
            ),
            {"ZEROMDASH_KIMI_MODEL": None},
        )

    def test_invoke_passes_agent_config_extra_args_to_agent_run(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="invoke-agent-config")
        captured = {}

        class FakeAgent:
            def run(self, prompt, cwd=None, timeout=None, extra_args=None, env=None):
                captured.update(
                    {
                        "prompt": prompt,
                        "cwd": cwd,
                        "timeout": timeout,
                        "extra_args": extra_args,
                        "env": env,
                    }
                )
                return AgentResult(
                    stdout="ok",
                    stderr="",
                    returncode=0,
                    backend="claude_code",
                    cwd=str(cwd),
                )

        with patch.dict("os.environ", {}, clear=True), patch.object(nodes, "_make_agent", return_value=FakeAgent()):
            nodes._invoke(
                ws,
                "search_spec",
                "prompt",
                {"search_spec": "claude_code"},
                agent_configs={
                    "search_spec": {
                        "runtime": "claude_code",
                        "provider": "bedrock",
                        "config": "/tmp/search-settings.json",
                    }
                },
                timeout=123,
            )

        self.assertEqual(captured["prompt"], "prompt")
        self.assertEqual(captured["timeout"], 123)
        self.assertEqual(captured["extra_args"], ["--settings", "/tmp/search-settings.json"])
        self.assertEqual(
            captured["env"],
            {
                "CLAUDE_CODE_USE_BEDROCK": "1",
                "ZEROMDASH_CLAUDE_MODEL": None,
                "ZEROMDASH_CLAUDE_SETTINGS_PATH": "/tmp/search-settings.json",
                "ANTHROPIC_AUTH_TOKEN": None,
                "ANTHROPIC_BASE_URL": None,
                "ANTHROPIC_MODEL": None,
                "ANTHROPIC_SMALL_FAST_MODEL": None,
                "ANTHROPIC_DEFAULT_HAIKU_MODEL": None,
                "ANTHROPIC_DEFAULT_SONNET_MODEL": None,
                "ANTHROPIC_DEFAULT_OPUS_MODEL": None,
                "CLAUDE_CODE_SUBAGENT_MODEL": None,
            },
        )
        self.assertIn("node_search_spec", str(captured["cwd"]))

    def test_invoke_falls_back_after_runtime_failure(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="invoke-runtime-fallback")
        calls = []

        class FakeAgent:
            def run(self, prompt, cwd=None, timeout=None, extra_args=None, env=None):
                del prompt, cwd, timeout, env
                args = list(extra_args or [])
                calls.append(args)
                if args == ["--settings", "/tmp/fallback-settings.json"]:
                    return AgentResult(
                        stdout="ok",
                        stderr="",
                        returncode=0,
                        backend="claude_code",
                        metadata={"command": ["claude", "--settings", "/tmp/fallback-settings.json"]},
                    )
                return AgentResult(
                    stdout="ExpiredToken",
                    stderr="",
                    returncode=1,
                    backend="claude_code",
                    metadata={"command": ["claude", "--settings", "/tmp/search-settings.json"]},
                )

        with patch.object(nodes, "_make_agent", return_value=FakeAgent()):
            res = nodes._invoke(
                ws,
                "search_spec",
                "prompt",
                {"search_spec": "claude_code"},
                agent_configs={
                    "search_spec": {
                        "runtime": "claude_code",
                        "provider": "bedrock",
                        "config": "/tmp/search-settings.json",
                        "fallbacks": [
                            {
                                "runtime": "claude_code",
                                "provider": "ark",
                                "config": "/tmp/fallback-settings.json",
                            }
                        ],
                    }
                },
            )

        self.assertTrue(res.ok)
        self.assertEqual(calls, [["--settings", "/tmp/search-settings.json"], ["--settings", "/tmp/fallback-settings.json"]])
        log_records = [
            json.loads(line)
            for line in (ws.log / "agent_commands.jsonl").read_text().splitlines()
        ]
        self.assertEqual(len(log_records), 2)
        self.assertFalse(log_records[0]["ok"])
        self.assertTrue(log_records[1]["ok"])
        self.assertEqual(log_records[1]["command"], ["claude", "--settings", "/tmp/fallback-settings.json"])

    def test_critic_revises_invalid_confirmed_primitive_shape(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="critic-primitive-gate")
        stdout = {
            "verdict": "confirm",
            "outcome_type": "confirmed_primitive",
            "reasoning": "mechanism exists but primitive JSON is incomplete",
            "selected_skills": [],
            "confidence": 0.7,
            "primitive": {
                "component": "parser",
                "root_cause_anchor": {"symbol": "parse", "locations": ["src/p.c:1"]},
            },
        }

        def fake_run_agent(*args, **kwargs):
            del args, kwargs
            return AgentResult(
                stdout=json.dumps(stdout),
                stderr="",
                returncode=0,
                backend="codex",
            )

        state = {
            **_workspace_state(ws),
            "subtask": {"id": "vuln-001", "bucket": "vuln", "objective": "probe", "hints": {}},
            "iteration": 1,
            "max_iterations": 3,
            "min_critic_skills": 0,
            "investigation": json.dumps(
                {
                    "title": "primitive",
                    "detail": "detail",
                    "evidence": {
                        "code_locations": ["src/p.c:1"],
                        "call_path": ["entry -> parse"],
                    },
                }
            ),
            "review_history": [],
            "agent_configs": {"critic_subtask": {"runtime": "codex"}},
        }

        with patch.object(nodes, "_run_agent_with_config", side_effect=fake_run_agent):
            update = nodes.critic_subtask(state, backends={"critic_subtask": "codex"})

        review = update["review"]
        self.assertEqual(review["original_verdict"], "confirm")
        self.assertEqual(review["verdict"], "revise")
        self.assertFalse(review["primitive_gate_ok"])
        self.assertIn("primitive requires at least one capabilities_gained item", review["primitive_gate_errors"])
        self.assertEqual(nodes.route_after_critic({**state, **update}), "investigate_subtask")

    def test_batch_critic_normalizes_each_hypothesis_and_closes_package(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="critic-batch")
        subtask = _hypothesis_package_subtask()
        stdout = _closed_hypothesis_review()

        def fake_run_agent(*args, **kwargs):
            del args, kwargs
            return AgentResult(
                stdout=json.dumps(stdout),
                stderr="",
                returncode=0,
                backend="codex",
            )

        state = {
            **_workspace_state(ws),
            "subtask": subtask,
            "iteration": 2,
            "max_iterations": 3,
            "min_critic_skills": 0,
            "investigation": json.dumps(_hypothesis_batch_investigation()),
            "hypothesis_manifest": nodes.initial_hypothesis_manifest(subtask),
            "review_history": [],
            "agent_configs": {"critic_subtask": {"runtime": "codex"}},
        }

        with patch.object(nodes, "_run_agent_with_config", side_effect=fake_run_agent):
            update = nodes.critic_subtask(state, backends={"critic_subtask": "codex"})

        self.assertEqual(update["review"]["verdict"], "confirm")
        self.assertTrue(update["review"]["hypothesis_verdicts"][0]["qualification_gate_passed"])
        self.assertEqual(update["review"]["hypothesis_verdicts"][1]["verdict"], "reject")
        self.assertEqual(update["hypothesis_manifest"]["revision"], 1)
        self.assertEqual(
            nodes.route_after_critic({**state, **update}),
            "finalize_subtask",
        )

    def test_batch_critic_prefers_fresh_review_artifact_over_valid_stdout(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="critic-artifact")
        subtask = _hypothesis_package_subtask()
        artifact_review = _closed_hypothesis_review()
        artifact_review["reasoning"] = "accepted artifact review"
        stdout_review = _closed_hypothesis_review()
        stdout_review["reasoning"] = "stdout review"

        def fake_run_agent(*args, **kwargs):
            del kwargs
            sub_ws = Path(args[4])
            (sub_ws / "review.json").write_text(json.dumps(artifact_review))
            return AgentResult(
                stdout=json.dumps(stdout_review),
                stderr="",
                returncode=0,
                backend="codex",
            )

        state = {
            **_workspace_state(ws),
            "subtask": subtask,
            "iteration": 2,
            "max_iterations": 3,
            "min_critic_skills": 0,
            "investigation": json.dumps(_hypothesis_batch_investigation()),
            "hypothesis_manifest": nodes.initial_hypothesis_manifest(subtask),
            "review_history": [],
            "agent_configs": {"critic_subtask": {"runtime": "codex"}},
        }

        with patch.object(nodes, "_run_agent_with_config", side_effect=fake_run_agent):
            update = nodes.critic_subtask(
                state, backends={"critic_subtask": "codex"}
            )

        self.assertEqual(update["review"]["reasoning"], "accepted artifact review")
        review_log = (
            ws.log_path("review_log") / f"{subtask['id']}.review.log"
        ).read_text()
        self.assertIn("source: artifact", review_log)

    def test_batch_critic_accepts_valid_stdout_without_review_artifact(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="critic-stdout")
        subtask = _hypothesis_package_subtask()
        stdout_review = _closed_hypothesis_review()
        stdout_review["reasoning"] = "accepted stdout review"
        critic_ws = ws.prepare_sub_workspace(
            node="critic_subtask",
            subtask_id=f"{subtask['id']}__critic",
            backend="codex",
        )
        stale_artifact = critic_ws / "review.json"
        stale_artifact.write_text(json.dumps(_closed_hypothesis_review()))

        def fake_run_agent(*args, **kwargs):
            del kwargs
            self.assertEqual(Path(args[4]), critic_ws)
            self.assertFalse(stale_artifact.exists())
            return AgentResult(
                stdout=json.dumps(stdout_review),
                stderr="",
                returncode=0,
                backend="codex",
            )

        state = {
            **_workspace_state(ws),
            "subtask": subtask,
            "iteration": 2,
            "max_iterations": 3,
            "min_critic_skills": 0,
            "investigation": json.dumps(_hypothesis_batch_investigation()),
            "hypothesis_manifest": nodes.initial_hypothesis_manifest(subtask),
            "review_history": [],
            "agent_configs": {"critic_subtask": {"runtime": "codex"}},
        }

        with patch.object(nodes, "_run_agent_with_config", side_effect=fake_run_agent):
            update = nodes.critic_subtask(
                state, backends={"critic_subtask": "codex"}
            )

        self.assertEqual(update["review"]["reasoning"], "accepted stdout review")
        review_log = (
            ws.log_path("review_log") / f"{subtask['id']}.review.log"
        ).read_text()
        self.assertIn("source: stdout", review_log)

    def test_batch_critic_reports_empty_stdout_without_fresh_artifact(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="critic-empty")
        subtask = _hypothesis_package_subtask()
        calls = 0

        def fake_run_agent(*args, **kwargs):
            nonlocal calls
            del args, kwargs
            calls += 1
            return AgentResult(
                stdout="",
                stderr="",
                returncode=0,
                backend="codex",
            )

        state = {
            **_workspace_state(ws),
            "subtask": subtask,
            "iteration": 2,
            "max_iterations": 3,
            "min_critic_skills": 0,
            "investigation": json.dumps(_hypothesis_batch_investigation()),
            "hypothesis_manifest": nodes.initial_hypothesis_manifest(subtask),
            "review_history": [],
            "agent_configs": {"critic_subtask": {"runtime": "codex"}},
        }

        with patch.object(nodes, "_run_agent_with_config", side_effect=fake_run_agent):
            update = nodes.critic_subtask(
                state, backends={"critic_subtask": "codex"}
            )

        self.assertEqual(calls, nodes.DEFAULT_NODE_OUTPUT_ATTEMPTS)
        failure = " ".join(update["review"]["batch_contract_errors"])
        self.assertIn("review.json: not created by this attempt", failure)
        self.assertIn("stdout: critic returned empty output", failure)
        self.assertNotIn("package_id does not match", failure)
        review_log = (
            ws.log_path("review_log") / f"{subtask['id']}.review.log"
        ).read_text()
        self.assertIn("source: invalid", review_log)
        self.assertIn("stdout: critic returned empty output", review_log)

    def test_batch_critic_repairs_schema_without_new_investigation_iteration(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="critic-repair")
        subtask = _hypothesis_package_subtask()
        invalid = _closed_hypothesis_review()
        invalid["new_hypothesis_decisions"] = [
            {
                "hypothesis_id": "spec-028:hyp-cred",
                "decision": "accept",
                "reasoning": "incorrectly re-decided a manifest hypothesis",
            }
        ]
        valid = _closed_hypothesis_review()
        outputs = [invalid, valid]
        prompts_seen = []

        def fake_run_agent(*args, **kwargs):
            del kwargs
            prompts_seen.append(args[3])
            return AgentResult(
                stdout=json.dumps(outputs[len(prompts_seen) - 1]),
                stderr="",
                returncode=0,
                backend="codex",
            )

        state = {
            **_workspace_state(ws),
            "subtask": subtask,
            "iteration": 2,
            "max_iterations": 3,
            "min_critic_skills": 0,
            "investigation": json.dumps(_hypothesis_batch_investigation()),
            "hypothesis_manifest": nodes.initial_hypothesis_manifest(subtask),
            "review_history": [],
            "agent_configs": {"critic_subtask": {"runtime": "codex"}},
        }

        with patch.object(nodes, "_run_agent_with_config", side_effect=fake_run_agent):
            update = nodes.critic_subtask(
                state, backends={"critic_subtask": "codex"}
            )

        self.assertEqual(len(prompts_seen), 2)
        self.assertIn("# Schema repair only", prompts_seen[1])
        self.assertIn("Current-iteration discovery IDs: []", prompts_seen[1])
        self.assertNotIn("batch_contract_errors", update["review"])
        self.assertEqual(update["review"]["verdict"], "confirm")
        self.assertEqual(state["iteration"], 2)
        self.assertEqual(
            nodes.route_after_critic({**state, **update}),
            "finalize_subtask",
        )

    def test_fetch_target_repo_retries_when_repo_is_empty(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="https://example.com/libfoo.git", task_id="fetch-retry")
        attempts = []

        def fake_invoke(
            ws_arg, node, prompt, backends, agent_configs=None, agent_config_task_types=None, subtask_id=None, extra_context=None, timeout=None
        ):
            del ws_arg, node, prompt, backends, agent_configs, subtask_id, timeout
            attempts.append(extra_context["attempt"])
            if extra_context["attempt"] == 2:
                (ws.main_path("repo") / "README.md").write_text("source tree")
            return AgentResult(stdout=f"attempt {extra_context['attempt']}", stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.fetch_target_repo(
                {
                    "target": "https://example.com/libfoo.git",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"fetch_target_repo": "claude_code"},
            )

        self.assertEqual(attempts, [1, 2])
        self.assertEqual(update["errors"], [])
        log_text = (ws.log_path("review_log") / "fetch_target_repo.log").read_text()
        self.assertIn("--- attempt 1/3", log_text)
        self.assertIn("--- attempt 2/3", log_text)

    def test_fetch_target_repo_reports_error_after_empty_repo_retries_exhausted(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="https://example.com/libfoo.git", task_id="fetch-empty")

        def fake_invoke(
            ws_arg, node, prompt, backends, agent_configs=None, agent_config_task_types=None, subtask_id=None, extra_context=None, timeout=None
        ):
            del ws_arg, node, prompt, backends, agent_configs, subtask_id, extra_context, timeout
            return AgentResult(stdout="claimed success", stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke) as invoke:
            update = nodes.fetch_target_repo(
                {
                    "target": "https://example.com/libfoo.git",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"fetch_target_repo": "claude_code"},
            )

        self.assertEqual(invoke.call_count, nodes.DEFAULT_FETCH_TARGET_REPO_ATTEMPTS)
        self.assertEqual(update["repo_path"], str(ws.main_path("repo")))
        self.assertEqual(
            update["errors"],
            [
                "[fetch_target_repo] materialized repo is empty after attempt "
                f"{nodes.DEFAULT_FETCH_TARGET_REPO_ATTEMPTS}/{nodes.DEFAULT_FETCH_TARGET_REPO_ATTEMPTS}: "
                f"{ws.main_path('repo')}"
            ],
        )

    def test_fetch_target_repo_retry_prompt_includes_empty_repo_failure(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="https://example.com/libfoo.git", task_id="fetch-retry-feedback")
        prompts_seen: list[str] = []

        def fake_invoke(
            ws_arg, node, prompt, backends, agent_configs=None, agent_config_task_types=None, subtask_id=None, extra_context=None, timeout=None
        ):
            del ws_arg, node, backends, agent_configs, agent_config_task_types, subtask_id, extra_context, timeout
            prompts_seen.append(prompt)
            return AgentResult(stdout="claimed success", stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.fetch_target_repo(
                {
                    "target": "https://example.com/libfoo.git",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"fetch_target_repo": "claude_code"},
            )

        self.assertEqual(len(prompts_seen), nodes.DEFAULT_FETCH_TARGET_REPO_ATTEMPTS)
        self.assertNotIn(nodes._RETRY_FEEDBACK_HEADER, prompts_seen[0])
        self.assertIn(nodes._RETRY_FEEDBACK_HEADER, prompts_seen[1])
        self.assertIn("materialized repo is empty after attempt 1/3", prompts_seen[1])
        self.assertIn(str(ws.main_path("repo")), prompts_seen[1])
        self.assertEqual(len(update["errors"]), 1)


class NodeOutputRetryTest(unittest.TestCase):
    def test_search_spec_retries_until_output_file_is_nonempty(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="search-spec-retry")
        attempts: list[int] = []

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                timeout,
            )
            attempts.append(extra_context["attempt"])
            stdout = "" if extra_context["attempt"] == 1 else "spec body"
            return AgentResult(stdout=stdout, stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.search_spec(
                {
                    "target": "libfoo",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"search_spec": "claude_code"},
            )

        self.assertEqual(attempts, [1, 2])
        self.assertEqual(update["errors"], [])
        self.assertEqual(Path(update["spec_doc"]).read_text(), "spec body")

    def test_retry_prompt_includes_previous_runtime_failure(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="search-spec-retry-feedback")
        prompts_seen: list[str] = []

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del ws_arg, node, backends, agent_configs, agent_config_task_types, subtask_id, timeout
            prompts_seen.append(prompt)
            if extra_context["attempt"] == 1:
                return AgentResult(stdout="", stderr="temporary failure", returncode=1, backend="claude_code")
            return AgentResult(stdout="spec body", stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.search_spec(
                {
                    "target": "libfoo",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"search_spec": "claude_code"},
            )

        self.assertEqual(update["errors"], [])
        self.assertEqual(len(prompts_seen), 2)
        self.assertNotIn(nodes._RETRY_FEEDBACK_HEADER, prompts_seen[0])
        self.assertIn(nodes._RETRY_FEEDBACK_HEADER, prompts_seen[1])
        self.assertIn("temporary failure", prompts_seen[1])
        self.assertIn(f"Required output: {ws.main_path('spec') / 'spec.md'}", prompts_seen[1])

    def test_retry_prompt_includes_previous_validation_failure(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="search-spec-validation-feedback")
        prompts_seen: list[str] = []

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del ws_arg, node, backends, agent_configs, agent_config_task_types, subtask_id, extra_context, timeout
            prompts_seen.append(prompt)
            return AgentResult(stdout="", stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.search_spec(
                {
                    "target": "libfoo",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"search_spec": "claude_code"},
            )

        self.assertEqual(len(prompts_seen), nodes.DEFAULT_NODE_OUTPUT_ATTEMPTS)
        self.assertNotIn(nodes._RETRY_FEEDBACK_HEADER, prompts_seen[0])
        self.assertIn(nodes._RETRY_FEEDBACK_HEADER, prompts_seen[1])
        self.assertIn("output validation failed after attempt 1/3", prompts_seen[1])
        self.assertIn("stdout_preview=(empty)", prompts_seen[1])
        self.assertIn(str(ws.main_path("spec") / "spec.md"), prompts_seen[1])
        self.assertEqual(len(update["errors"]), 1)

    def test_search_fuzz_driver_retries_after_nonzero_rc(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="fuzz-driver-retry")
        attempts: list[int] = []

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                timeout,
            )
            attempts.append(extra_context["attempt"])
            if extra_context["attempt"] == 1:
                return AgentResult(stdout="", stderr="temporary failure", returncode=1, backend="claude_code")
            return AgentResult(stdout="- fuzz/foo.cc", stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.search_fuzz_driver(
                {
                    **_workspace_state(ws),
                    "repo_path": str(ws.main_path("repo")),
                },
                backends={"search_fuzz_driver": "claude_code"},
            )

        self.assertEqual(attempts, [1, 2])
        self.assertEqual(update["errors"], [])
        self.assertEqual(update["fuzz_drivers"], ["fuzz/foo.cc"])

    def test_search_similar_software_retries_until_candidates_file_is_nonempty_json(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="similar-candidates-retry")
        attempts: list[int] = []

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                timeout,
            )
            attempts.append(extra_context["attempt"])
            if extra_context["attempt"] == 1:
                (ws.similar / "_candidates.json").write_text("")
                return AgentResult(stdout="", stderr="", returncode=0, backend="claude_code")
            payload = [
                {"name": "Peer One", "repo_url": "https://example.com/one.git"},
                {"name": "MongoDB server / mongod", "repo_url": "https://example.com/mongo.git"},
                {"name": "https://example.com/not-a-name", "repo_url": ""},
            ]
            return AgentResult(stdout=json.dumps(payload), stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.search_similar_software(
                {
                    "target": "libfoo",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"search_similar_software": "claude_code"},
            )

        self.assertEqual(attempts, [1, 2])
        self.assertEqual(update["errors"], [])
        self.assertEqual(update["similar_repos"], ["Peer One", "MongoDB server - mongod"])
        self.assertTrue((ws.similar / "peer_one" / "writeup").is_dir())
        self.assertTrue((ws.similar / "mongodb_server_-_mongod" / "writeup").is_dir())

    def test_search_target_history_retries_until_writeup_and_patch_dirs_are_nonempty(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="target-history-retry")
        attempts: list[int] = []

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                timeout,
            )
            attempts.append(extra_context["attempt"])
            if extra_context["attempt"] == 2:
                (ws.main_path("writeup") / "_index.md").write_text(
                    "# Target history\n\n## No public history\n"
                )
                (ws.main_path("patch") / "_patch_commits.json").write_text(
                    json.dumps(_patch_manifest(ws))
                )
            return AgentResult(stdout="writeup text", stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.search_target_history(
                {
                    "target": "libfoo",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"search_target_history": "claude_code"},
            )

        self.assertEqual(attempts, [1, 2])
        self.assertEqual(update["errors"], [])
        self.assertTrue((ws.main_path("writeup") / "_raw.md").is_file())
        self.assertEqual(
            update["target_patch_manifest"],
            str(ws.main_path("patch") / "_patch_commits.json"),
        )

    def test_search_target_history_multi_repo_requires_coverage_for_every_repo(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="bundle", task_id="target-history-multi")
        repos = [
            {
                "repo_id": "core",
                "role": "main",
                "target": "https://example.test/core.git",
                "repo_path": str(ws.main_path("repos") / "core"),
            },
            {
                "repo_id": "plugin",
                "role": "extension",
                "target": "https://example.test/plugin.git",
                "repo_path": str(ws.main_path("repos") / "plugin"),
            },
        ]
        attempts: list[int] = []

        def fake_invoke(
            ws_arg, node, prompt, backends, agent_configs=None,
            agent_config_task_types=None, subtask_id=None, extra_context=None, timeout=None,
        ):
            del ws_arg, node, prompt, backends, agent_configs, agent_config_task_types, subtask_id, timeout
            attempts.append(extra_context["attempt"])
            (ws.main_path("writeup") / "_index.md").write_text("# Target history\n")
            coverage = ["core"] if extra_context["attempt"] == 1 else ["core", "plugin"]
            (ws.main_path("patch") / "_patch_commits.json").write_text(
                json.dumps(_patch_manifest(ws, target="bundle", repos=repos, coverage_ids=coverage))
            )
            return AgentResult(stdout="done", stderr="", returncode=0, backend="claude_code")

        state = {
            "target": "bundle",
            "task_id": ws.task_id,
            "workspace_root": str(ws.root),
            "repo_path": str(ws.main_path("repo")),
            "target_repos": [
                {"id": "core", "role": "main", "target": repos[0]["target"]},
                {"id": "plugin", "role": "extension", "target": repos[1]["target"]},
            ],
        }
        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.search_target_history(
                state, backends={"search_target_history": "claude_code"}
            )

        self.assertEqual(attempts, [1, 2])
        self.assertEqual(update["errors"], [])

    def test_patch_manifest_rejects_target_specific_top_level_layout(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="patch-schema")
        path = ws.main_path("patch") / "_patch_commits.json"
        path.write_text(json.dumps({"head": {}, "postgresql_core": [], "extensions": []}))

        valid, detail = nodes._validate_patch_manifest(
            path,
            target="libfoo",
            repo_mode="single_repo",
            repo_registry=[
                {
                    "repo_id": "main",
                    "role": "main",
                    "target": "libfoo",
                    "repo_path": str(ws.main_path("repo")),
                }
            ],
        )

        self.assertFalse(valid)
        self.assertIn("top-level keys", detail)

    def test_patch_manifest_accepts_repository_qualified_finding(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="patch-finding-schema")
        payload = _patch_manifest(ws)
        payload["coverage"][0]["status"] = "researched"
        payload["findings"] = [
            {
                "record_id": "CVE-2026-0001",
                "repo_id": "main",
                "advisory_ids": ["CVE-2026-0001", "GHSA-xxxx-yyyy-zzzz"],
                "title": "Bounds check missing in parser",
                "root_cause_class": "integer overflow",
                "affected_locations": ["src/parser.c:42"],
                "sources": [
                    {"type": "advisory", "url": "https://example.test/CVE-2026-0001"},
                    {"type": "patch", "url": "https://example.test/commit/abc"},
                ],
                "applicability": "fixed",
                "patch": {
                    "status": "applied",
                    "upstream_commits": ["abc123"],
                    "equivalent_commits": [],
                    "verification": "ancestor",
                    "verified_against_head": "a" * 40,
                    "fixed_versions": ["1.2.3"],
                    "notes": "Verified with git merge-base --is-ancestor.",
                },
                "lesson": "Recheck sibling parser paths for the same overflow.",
                "notes": "",
            }
        ]
        path = ws.main_path("patch") / "_patch_commits.json"
        path.write_text(json.dumps(payload))

        valid, detail = nodes._validate_patch_manifest(
            path,
            target="libfoo",
            repo_mode="single_repo",
            repo_registry=[
                {
                    "repo_id": "main",
                    "role": "main",
                    "target": "libfoo",
                    "repo_path": str(ws.main_path("repo")),
                }
            ],
        )

        self.assertTrue(valid, detail)

    def test_search_new_feature_materializes_index_and_feature_docs(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="new-feature")
        attempts: list[int] = []

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                timeout,
            )
            attempts.append(extra_context["attempt"])
            feature_dir = ws.main_path("feature")
            payload = [
                {
                    "id": "feature-001",
                    "name": "new parser",
                    "untrusted_input_object": "file",
                    "trust_boundary": "file -> process",
                    "state_machine_family": "parser",
                    "expected_data_flow": ["open", "parse", "lookup"],
                    "coverage_status": {"spec": "none"},
                    "candidate_code_locations": ["src/parser.c:1"],
                    "priority_reason": "weak coverage",
                }
            ]
            if extra_context["attempt"] == 2:
                (feature_dir / "feature-001.md").write_text(
                    "# feature-001\n\n"
                    "## What Changed\n\n"
                    "## Security-Relevant Mode\n\n"
                    "## Untrusted Input Object\n\n"
                    "## Trust Boundary\n\n"
                    "## Involved State Machine Family\n\n"
                    "## Expected Data Flow\n\n"
                    "## Coverage Status\n\n"
                    "## Audit Seeds\n"
                )
            return AgentResult(stdout=json.dumps(payload), stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.search_new_feature(
                {
                    "target": "libfoo",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                    "repo_path": str(ws.main_path("repo")),
                },
                backends={"search_new_feature": "claude_code"},
            )

        self.assertEqual(attempts, [1, 2])
        self.assertEqual(update["errors"], [])
        self.assertTrue((ws.main_path("feature") / "_index.json").is_file())
        self.assertTrue((ws.main_path("feature") / "_index.md").is_file())
        self.assertIn(str(ws.main_path("feature") / "feature-001.md"), update["feature_docs"])

    def test_search_similar_history_reports_error_after_empty_dirs_are_exhausted(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="similar-history-empty")

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                extra_context,
                timeout,
            )
            return AgentResult(stdout="writeup only", stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke) as invoke:
            update = nodes.search_similar_history(
                {
                    "target": "libfoo",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                    "similar_software": "Peer One",
                },
                backends={"search_similar_history": "claude_code"},
            )

        self.assertEqual(invoke.call_count, nodes.DEFAULT_NODE_OUTPUT_ATTEMPTS)
        self.assertEqual(
            update["errors"],
            [
                "[search_similar_history/peer_one] output empty after attempt "
                f"{nodes.DEFAULT_NODE_OUTPUT_ATTEMPTS}/{nodes.DEFAULT_NODE_OUTPUT_ATTEMPTS}: "
                f"{ws.similar / 'peer_one' / 'writeup'} and {ws.similar / 'peer_one' / 'patch'}"
            ],
        )

    def test_search_similar_history_normalizes_slash_names(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="similar-history-safe-name")
        captured = {}

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del node, prompt, backends, agent_configs, agent_config_task_types, extra_context, timeout
            captured["subtask_id"] = subtask_id
            sw_dir = ws_arg.similar / "mongodb_server_-_mongod"
            (sw_dir / "patch" / "fix.patch").write_text("diff --git")
            return AgentResult(stdout="writeup text", stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.search_similar_history(
                {
                    "target": "libfoo",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                    "similar_software": "MongoDB server / mongod",
                },
                backends={"search_similar_history": "claude_code"},
            )

        self.assertEqual(update["errors"], [])
        self.assertEqual(captured["subtask_id"], "mongodb_server_-_mongod")
        self.assertEqual(update["similar_writeups"], [str(ws.similar / "mongodb_server_-_mongod" / "writeup")])
        self.assertEqual(update["similar_patches"], [str(ws.similar / "mongodb_server_-_mongod" / "patch")])

    def test_analyze_attack_surface_retries_until_report_file_is_nonempty(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="attack-surface-retry")
        attempts: list[int] = []

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                timeout,
            )
            attempts.append(extra_context["attempt"])
            stdout = "" if extra_context["attempt"] == 1 else "attack surface"
            if extra_context["attempt"] == 2:
                _write_domain_registry(ws)
            return AgentResult(stdout=stdout, stderr="", returncode=0, backend="codex")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.analyze_attack_surface(
                {
                    "target": "libfoo",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"analyze_attack_surface": "codex"},
            )

        self.assertEqual(attempts, [1, 2])
        self.assertEqual(update["errors"], [])
        self.assertEqual(Path(update["attack_surface"]).read_text(), "attack surface")
        self.assertEqual(update["domain_registry"]["schema_version"], "1.0")
        self.assertTrue(Path(update["domain_registry_path"]).is_file())

    def test_analyze_attack_surface_appends_to_preset_report(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="attack-surface-preset")
        preset = Path(tmp.name) / "preset_attack_surface.md"
        preset.write_text("# Existing attack surface\n\nSeeded entrypoint.\n")
        observed_seed = []

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                extra_context,
                timeout,
            )
            out = ws.main_path("attack_surface") / "attack_surface.md"
            observed_seed.append(out.read_text())
            self.assertIn("append your new findings", prompt)
            _write_domain_registry(ws)
            return AgentResult(stdout="## Appended analysis\nNew sink.", stderr="", returncode=0, backend="codex")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.analyze_attack_surface(
                {
                    "target": "libfoo",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                    "preset_attack_surface_path": str(preset),
                },
                backends={"analyze_attack_surface": "codex"},
            )

        text = Path(update["attack_surface"]).read_text()
        self.assertEqual(observed_seed, ["# Existing attack surface\n\nSeeded entrypoint.\n\n"])
        self.assertTrue(text.startswith("# Existing attack surface\n\nSeeded entrypoint."))
        self.assertIn("## Appended analysis\nNew sink.", text)
        self.assertEqual(update["errors"], [])
        self.assertEqual(update["domain_registry"]["status"], "complete")

    def test_diff_attack_surface_retries_until_risk_registry_exists(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="diff-risk-registry")
        attempts: list[int] = []

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                timeout,
            )
            attempts.append(extra_context["attempt"])
            if extra_context["attempt"] == 1:
                stdout = "# Attack Surface\n\n## Hypothesis list\n- changed parser"
            else:
                stdout = (
                    "# Attack Surface\n\n"
                    "## Diff Risk Surface Registry\n\n"
                    "### RS-001\n"
                    "- diff anchor: `src/parser.c:10`\n"
                    "- flow: input -> parser -> allocation sink\n"
                )
                _write_domain_registry(ws)
            return AgentResult(stdout=stdout, stderr="", returncode=0, backend="codex")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.analyze_attack_surface(
                {
                    "target": "libfoo",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                    "scan_scope": {
                        "mode": "diff",
                        "changed_files": ["src/parser.c"],
                    },
                },
                backends={"analyze_attack_surface": "codex"},
            )

        self.assertEqual(attempts, [1, 2])
        self.assertEqual(update["errors"], [])
        self.assertIn(
            "## Diff Risk Surface Registry",
            Path(update["attack_surface"]).read_text(),
        )
        self.assertEqual(update["domain_registry"]["status"], "complete")

    def test_summary_retries_after_nonzero_rc(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="summary-retry")
        attempts: list[int] = []

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                timeout,
            )
            attempts.append(extra_context["attempt"])
            if extra_context["attempt"] == 1:
                return AgentResult(stdout="", stderr="temporary failure", returncode=1, backend="claude_code")
            (ws.base / "summary.en.md").write_text("# Executive Summary")
            (ws.base / "summary.zh_CN.md").write_text("# 执行摘要")
            return AgentResult(stdout="done", stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.summary(
                {
                    "target": "libfoo",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"summary": "claude_code"},
            )

        self.assertEqual(attempts, [1, 2])
        self.assertEqual(update["errors"], [])
        self.assertEqual(update["summary"], "# Executive Summary")
        self.assertEqual(update["summary_en"], "# Executive Summary")
        self.assertEqual(update["summary_zh_CN"], "# 执行摘要")
        self.assertEqual((ws.base / "summary.md").read_text(), "# Executive Summary")

    def test_summary_prompt_uses_compact_confirm_then_revise_findings(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="summary-compact")
        captured = {}

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                extra_context,
                timeout,
            )
            captured["prompt"] = prompt
            _write_bilingual_summary(ws)
            return AgentResult(stdout="done", stderr="", returncode=0, backend="claude_code")

        state = {
            "target": "libfoo",
            "task_id": ws.task_id,
            "workspace_root": str(ws.root),
            "spec_findings": [
                {
                    "subtask_id": "spec-002",
                    "kind": "spec",
                    "title": "revise title",
                    "detail": "long revise detail",
                    "severity": "medium",
                    "confidence": 0.5,
                    "evidence": {"code_locations": ["b.py:2"], "call_path": ["b -> sink"], "notes": "keep"},
                    "review": _qualified_review("revise", confidence=0.5, selected_skills=["parser"]),
                    "disposition": "confirmed_vulnerability",
                    "qualification_gate_passed": True,
                    "cvss4_vector": _CVSS4_HIGH_VECTOR,
                    "cvss4_score": 8.5,
                    "selected_skills": ["parser"],
                },
                {
                    "subtask_id": "spec-001",
                    "kind": "spec",
                    "title": "confirm title",
                    "detail": "long confirm detail that must not be embedded",
                    "severity": "high",
                    "confidence": 0.9,
                    "evidence": {"code_locations": ["a.py:1"], "call_path": ["a -> sink"], "raw": "keep"},
                    "review": _qualified_review(selected_skills=["memory"]),
                    "disposition": "confirmed_vulnerability",
                    "qualification_gate_passed": True,
                    "cvss4_vector": _CVSS4_HIGH_VECTOR,
                    "cvss4_score": 8.5,
                    "selected_skills": ["memory"],
                },
                {
                    "subtask_id": "spec-003",
                    "kind": "spec",
                    "title": "reject title",
                    "detail": "rejected detail",
                    "severity": "critical",
                    "confidence": 1.0,
                    "evidence": {"code_locations": ["c.py:3"]},
                    "review": {"verdict": "reject"},
                },
            ],
            "vuln_candidates": [],
            "patch_findings": [],
        }

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.summary(state, backends={"summary": "claude_code"})

        self.assertEqual(update["errors"], [])
        prompt = captured["prompt"]
        self.assertIn('"id": "spec-001"', prompt)
        self.assertIn('"status": "confirm"', prompt)
        self.assertIn('"code_locations": [', prompt)
        self.assertIn('"call_path": [', prompt)
        self.assertIn('"call_flow": [', prompt)
        self.assertIn('"requires_call_path_summary": true', prompt)
        self.assertIn('"summary_format": "full"', prompt)
        self.assertIn('"skills": [', prompt)
        self.assertIn('"a -> sink"', prompt)
        self.assertIn('"raw": "keep"', prompt)
        self.assertIn('"notes": "keep"', prompt)
        self.assertNotIn("long confirm detail", prompt)
        self.assertNotIn("long revise detail", prompt)
        self.assertNotIn("reject title", prompt)
        self.assertLess(prompt.index('"id": "spec-001"'), prompt.index('"id": "spec-002"'))
        self.assertIn("ONE canonical vulnerability grouping", prompt)
        self.assertIn("VULN-001", prompt)
        self.assertIn("flowchart LR", prompt)
        self.assertIn("sequenceDiagram", prompt)
        self.assertIn("Code evidence at code-block granularity", prompt)
        self.assertIn("Affected version range", prompt)
        self.assertIn(str(ws.log_path("subtask_res")), prompt)
        self.assertEqual(update["summary_en"], _SUMMARY_EN)
        self.assertEqual(update["summary_zh_CN"], _SUMMARY_ZH)
        self.assertEqual((ws.base / "summary.md").read_text(), _SUMMARY_EN)
        self.assertEqual(update["gate_result"]["decision"], "pass")
        self.assertTrue((ws.base / "gate_result.json").is_file())

    def test_summary_prompt_and_validation_include_confirmed_primitives(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="summary-primitives")
        captured = {}
        en = """\
# Executive Summary

No standalone vulnerabilities passed the qualification gate.

## Confirmed Primitives

### prim_deadbeef: stale pointer primitive

Source subtasks: `spec-001:hyp-01`.
Capabilities gained: relative write into a freed page.
Missing next capabilities: deterministic page reuse.

## Recommended Next Steps

- Clear the stale pointer on teardown.
"""
        zh = """\
# 执行摘要

没有通过资格门禁的完整漏洞。

## 已确认原语

### prim_deadbeef: stale pointer primitive

来源 subtasks：`spec-001:hyp-01`。
获得的能力：对已释放页面的相对写。
缺失的下一跳能力：确定性页面复用。

## 建议的下一步

- 在 teardown 时清理 stale pointer。
"""

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                extra_context,
                timeout,
            )
            captured["prompt"] = prompt
            (ws.base / "summary.en.md").write_text(en)
            (ws.base / "summary.zh_CN.md").write_text(zh)
            return AgentResult(stdout="done", stderr="", returncode=0, backend="claude_code")

        state = {
            "target": "libfoo",
            "task_id": ws.task_id,
            "workspace_root": str(ws.root),
            "confirmed_primitives": [
                {
                    "primitive_id": "prim_deadbeef",
                    "source_subtask_ids": ["spec-001:hyp-01"],
                    "component": "core teardown",
                    "root_cause_anchor": {
                        "symbol": "teardown leaves stale pointer",
                        "locations": ["src/core.c:10"],
                    },
                    "capabilities_gained": [
                        {"kind": "relative_memory_write", "object_type": "freed page"}
                    ],
                    "missing_next_capabilities": [
                        {"kind": "custom", "object_type": "deterministic page reuse"}
                    ],
                    "terminal_impact": {"by_itself": "none"},
                    "evidence": {
                        "code_locations": ["src/core.c:10"],
                        "call_path": ["create -> fail -> teardown -> stale pointer"],
                    },
                }
            ],
        }

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.summary(state, backends={"summary": "claude_code"})

        self.assertEqual(update["errors"], [])
        self.assertIn("Confirmed primitive artifact directory", captured["prompt"])
        self.assertIn("- confirmed_primitives:", captured["prompt"])
        self.assertIn('"primitive_id": "prim_deadbeef"', captured["prompt"])
        self.assertIn("## Confirmed Primitives", captured["prompt"])
        self.assertIn("## 已确认原语", captured["prompt"])
        self.assertEqual(update["summary_en"], en)
        self.assertEqual(update["summary_zh_CN"], zh)
        self.assertEqual(
            update["gate_result"]["confirmed_primitives"][0]["primitive_id"],
            "prim_deadbeef",
        )

    def test_prepare_report_groups_uses_agent_adjudication_to_merge_semantic_duplicates(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="report-group-agent")
        finding_a = {
            "subtask_id": "spec-001",
            "kind": "spec",
            "title": "SETUP window reaches NULL ram_state",
            "detail": "detail",
            "severity": "medium",
            "confidence": 0.8,
            "evidence": {
                "code_locations": ["migration/ram.c:3046", "hw/virtio/virtio-balloon.c:557"],
                "call_path": ["guest kick -> qemu_guest_free_page_hint -> ram_state deref"],
            },
            "review": {
                **_qualified_review(confidence=0.8),
                "violated_security_property": "free-page hints must not run before RAMState exists",
            },
            "disposition": "confirmed_vulnerability",
            "qualification_gate_passed": True,
            "cvss4_vector": _CVSS4_HIGH_VECTOR,
            "cvss4_score": 8.5,
        }
        finding_b = {
            "subtask_id": "feat-001",
            "kind": "feature",
            "title": "Restored START crashes migration setup",
            "detail": "same bug with different wording",
            "severity": "medium",
            "confidence": 0.9,
            "evidence": {
                "code_locations": ["hw/virtio/virtio-balloon.c:837", "migration/ram.c:3046"],
                "call_path": ["VMState restore -> free_page_vq -> NULL ram_state"],
            },
            "review": {
                **_qualified_review(confidence=0.9),
                "violated_security_property": "restored free-page START must be quiesced before RAMState initialization",
            },
            "disposition": "confirmed_vulnerability",
            "qualification_gate_passed": True,
            "cvss4_vector": _CVSS4_HIGH_VECTOR,
            "cvss4_score": 8.5,
        }
        adjudication = {
            "merge_groups": [
                {
                    "source_group_ids": ["VULN-001", "VULN-002"],
                    "reasoning": "Both groups describe the same restored START / migration SETUP / qemu_guest_free_page_hint NULL ram_state root cause.",
                    "root_cause": "free-page START state can survive into migration SETUP before RAMState exists",
                    "shared_sink": "qemu_guest_free_page_hint ram_state dereference",
                    "trigger_equivalence": "different discovery buckets, same trigger window",
                    "variant_notes": ["spec and feature evidence retained"],
                }
            ],
            "notes": "merged semantic duplicate",
        }

        def fake_invoke(*args, **kwargs):
            del args, kwargs
            return AgentResult(
                stdout=json.dumps(adjudication),
                stderr="",
                returncode=0,
                backend="codex",
            )

        state = {
            **_workspace_state(ws),
            "spec_findings": [finding_a],
            "feature_findings": [finding_b],
            "vuln_candidates": [],
            "patch_findings": [],
            "chain_findings": [],
            "agent_configs": {"report_group_adjudicator": {"runtime": "codex"}},
        }

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.prepare_report_groups(
                state,
                backends={"report_group_adjudicator": "codex"},
            )

        self.assertEqual(len(update["report_groups"]), 1)
        group = update["report_groups"][0]
        self.assertEqual(group["group_id"], "VULN-001")
        self.assertEqual(group["source_subtasks"], ["feat-001", "spec-001"])
        self.assertEqual(group["absorbed_finding_ids"], ["spec-001"])
        self.assertEqual(group["primary_finding"]["subtask_id"], "feat-001")
        self.assertIn("dedup_adjudication", group)
        payload = json.loads((ws.log / "report_groups.json").read_text())
        self.assertEqual(payload["group_count"], 1)
        self.assertEqual(
            payload["adjudication"]["merge_groups"][0]["source_group_ids"],
            ["VULN-001", "VULN-002"],
        )

    def test_summary_accepts_file_output_when_stdout_is_empty(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="summary-file")

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                extra_context,
                timeout,
            )
            (ws.base / "summary.en.md").write_text("# File Summary")
            (ws.base / "summary.zh_CN.md").write_text("# 文件摘要")
            return AgentResult(stdout="", stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke) as invoke:
            update = nodes.summary(
                {
                    "target": "libfoo",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"summary": "claude_code"},
            )

        invoke.assert_called_once()
        self.assertEqual(update["errors"], [])
        self.assertEqual(update["summary"], "# File Summary")
        self.assertEqual(update["summary_en"], "# File Summary")
        self.assertEqual(update["summary_zh_CN"], "# 文件摘要")
        self.assertEqual((ws.base / "summary.md").read_text(), "# File Summary")

    def test_summary_retries_when_bilingual_group_ids_diverge(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="summary-group-retry")
        attempts: list[int] = []

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                timeout,
            )
            attempts.append(extra_context["attempt"])
            (ws.base / "summary.en.md").write_text(_SUMMARY_EN)
            zh = _SUMMARY_ZH
            if extra_context["attempt"] == 1:
                zh = zh.replace("VULN-001", "VULN-002")
            (ws.base / "summary.zh_CN.md").write_text(zh)
            return AgentResult(stdout="done", stderr="", returncode=0, backend="claude_code")

        state = {
            "target": "libfoo",
            "task_id": ws.task_id,
            "workspace_root": str(ws.root),
            "spec_findings": [
                {
                    "subtask_id": "spec-001",
                    "title": "example",
                    "severity": "high",
                    "confidence": 0.9,
                    "evidence": {"code_locations": ["src/parser.c:1"]},
                    "review": _qualified_review(),
                    "disposition": "confirmed_vulnerability",
                    "qualification_gate_passed": True,
                    "cvss4_vector": _CVSS4_HIGH_VECTOR,
                    "cvss4_score": 8.5,
                }
            ],
        }

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.summary(state, backends={"summary": "claude_code"})

        self.assertEqual(attempts, [1, 2])
        self.assertEqual(update["errors"], [])
        self.assertEqual(update["summary_en"], _SUMMARY_EN)
        self.assertEqual(update["summary_zh_CN"], _SUMMARY_ZH)

    def test_summary_accepts_known_cve_patch_gap_without_full_vulnerability_sections(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="summary-patch-gap")
        captured = {}
        en = """\
# Executive Summary

## Aggregation Method

Known CVE patch gaps are reported without full exploit writeups.

## Vulnerability Index

- CVE-2024-1234

## Known CVE Patch Gaps

#### CVE-2024-1234: parser length check fix not applied

Patch status: not applied
Upstream fix: `abc123`
Current checkout evidence: `src/parser.c:10` still lacks the upstream length check.
Action: backport `abc123` and add a regression test.
Source subtasks: `patch-001`; confidence 0.9.

## Recommended Next Steps

- Backport `abc123`.

## Sources

- patch-001
"""
        zh = """\
# 执行摘要

## 聚合方法

已知 CVE 补丁缺口不展开为完整漏洞报告。

## 漏洞索引

- CVE-2024-1234

## 已知 CVE 补丁缺口

#### CVE-2024-1234: parser length check fix not applied

补丁状态：未应用
上游修复：`abc123`
当前 checkout 证据：`src/parser.c:10` 仍缺少上游长度检查。
动作：backport `abc123` 并添加回归测试。
来源 Subtask 与置信度：`patch-001`；置信度 0.9。

## 建议的下一步

- backport `abc123`。

## 来源

- patch-001
"""

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                extra_context,
                timeout,
            )
            captured["prompt"] = prompt
            (ws.base / "summary.en.md").write_text(en)
            (ws.base / "summary.zh_CN.md").write_text(zh)
            return AgentResult(stdout="done", stderr="", returncode=0, backend="claude_code")

        state = {
            "target": "libfoo",
            "task_id": ws.task_id,
            "workspace_root": str(ws.root),
            "patch_findings": [
                {
                    "subtask_id": "patch-001",
                    "kind": "patch_miss",
                    "title": "CVE-2024-1234 parser length check fix not applied",
                    "detail": "Upstream fix abc123 is missing from the current checkout.",
                    "severity": "none",
                    "confidence": 0.9,
                    "evidence": {
                        "code_locations": ["src/parser.c:10"],
                        "patch_refs": ["abc123"],
                    },
                    "patch_status": "not_applied",
                    "disposition": "known_cve_patch_gap",
                    "qualification_gate_passed": False,
                    "review": {
                        "verdict": "confirm",
                        "disposition": "known_cve_patch_gap",
                        "qualification_gate_passed": False,
                        "cvss_applicable": False,
                    },
                }
            ],
        }

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.summary(state, backends={"summary": "claude_code"})

        self.assertEqual(update["errors"], [])
        self.assertIn('"summary_format": "patch_gap"', captured["prompt"])
        self.assertIn('"patch_status": "not_applied"', captured["prompt"])
        self.assertIn('"cve_ids"', captured["prompt"])
        self.assertIn('"CVE-2024-1234"', captured["prompt"])
        self.assertIn("Known CVE Patch Gaps", captured["prompt"])
        self.assertEqual(update["summary_en"], en)
        self.assertEqual(update["summary_zh_CN"], zh)
        self.assertEqual((ws.base / "summary.md").read_text(), en)

    def test_patch_bypass_and_incomplete_fix_are_not_collapsed_to_patch_gap(self):
        base = {
            "subtask_id": "patch-001",
            "kind": "patch_miss",
            "severity": "high",
            "confidence": 0.9,
            "evidence": {"code_locations": ["src/parser.c:10"], "patch_refs": ["abc123"]},
            "review": _qualified_review(),
            "disposition": "confirmed_vulnerability",
            "qualification_gate_passed": True,
            "cvss4_vector": _CVSS4_HIGH_VECTOR,
            "cvss4_score": 8.5,
        }
        not_applied = {
            **base,
            "title": "CVE-2024-1234 fix not applied",
            "detail": "The upstream fix is absent from this checkout.",
        }
        bypass = {
            **base,
            "title": "CVE-2024-1234 patch bypass",
            "detail": "The applied guard can be bypassed through the sibling path.",
        }
        incomplete = {
            **base,
            "title": "CVE-2024-1234 incomplete fix",
            "detail": "补丁残缺：只覆盖了参考路径，fast path 仍可触发。",
        }
        structured_not_applied = {
            **base,
            "title": "CVE-2024-1234 patch state",
            "detail": "See upstream fix abc123.",
            "patch_status": "not_applied",
        }
        structured_bypass = {
            **base,
            "title": "CVE-2024-1234 patch state",
            "detail": "The guard differs on the sibling path.",
            "patch_status": "bypass",
        }
        structured_applied = {
            **base,
            "title": "CVE-2024-1234 patch state",
            "detail": "The guard is present on all audited paths.",
            "patch_status": "applied",
        }
        structured_applied["qualification_gate_passed"] = False
        structured_applied["review"] = {
            "verdict": "confirm",
            "disposition": "no_finding",
            "qualification_gate_passed": False,
        }

        self.assertEqual(nodes._compact_summary_finding(not_applied, "patch")["summary_format"], "full")
        self.assertEqual(nodes._compact_summary_finding(bypass, "patch")["summary_format"], "full")
        self.assertEqual(nodes._compact_summary_finding(incomplete, "patch")["summary_format"], "full")
        self.assertEqual(nodes._compact_summary_finding(structured_not_applied, "patch")["summary_format"], "full")
        self.assertEqual(nodes._compact_summary_finding(structured_bypass, "patch")["summary_format"], "full")
        self.assertIsNone(nodes._compact_summary_finding(structured_applied, "patch"))
        self.assertEqual(nodes._compact_summary_finding(bypass, "patch")["cve_ids"], [])
        self.assertEqual(nodes._compact_summary_finding(incomplete, "patch")["cve_ids"], [])
        self.assertEqual(nodes._compact_summary_finding(structured_not_applied, "patch")["patch_status"], "not_applied")
        self.assertEqual(nodes._compact_summary_finding(structured_bypass, "patch")["patch_status"], "bypass")

    def test_summary_failure_writes_full_attempt_log(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="summary-stderr")
        long_stderr = "summary failed: " + "x" * 800

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                ws_arg,
                node,
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                timeout,
            )
            return AgentResult(
                stdout="",
                stderr=f"{long_stderr} attempt={extra_context['attempt']}",
                returncode=1,
                backend="codex",
                metadata={"resume_id": f"sess-{extra_context['attempt']}", "command": ["codex", "exec", "-"]},
            )

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.summary(
                {
                    "target": "libfoo",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"summary": "codex"},
            )

        self.assertEqual(update["summary"], "")
        self.assertEqual(update["summary_en"], "")
        self.assertEqual(update["summary_zh_CN"], "")
        self.assertEqual(len(update["errors"]), 1)
        self.assertIn("full log:", update["errors"][0])
        log_path = ws.log_path("review_log") / "summary.attempt-3.log"
        self.assertTrue(log_path.is_file())
        log_text = log_path.read_text()
        self.assertIn(long_stderr, log_text)
        self.assertIn('command: ["codex", "exec", "-"]', log_text)
        self.assertIn("resume_id: sess-3", log_text)


class FocusRoutingTest(unittest.TestCase):
    def test_node_focus_composes_common_before_stage_specific_focus(self):
        state = {
            "common_focus": "network reachable code",
            "search_fuzz_driver_focus": "HTTP parser harnesses",
        }

        focus = nodes._node_focus(state, "search_fuzz_driver_focus")

        self.assertEqual(
            focus,
            'Global focus: "network reachable code"\n'
            'Stage-specific focus: "HTTP parser harnesses"\n'
            'Apply the global focus first, and additionally prioritize the '
            'stage-specific focus in this step.',
        )
        self.assertEqual(
            nodes._node_focus({"common_focus": "network reachable code"}, "summary_focus"),
            'Global focus: "network reachable code"\nApply the global focus in this step.',
        )
        self.assertEqual(
            nodes._node_focus({"summary_focus": "actionable triage"}, "summary_focus"),
            'Stage-specific focus: "actionable triage"\nPrioritize the stage-specific focus in this step.',
        )
        self.assertEqual(
            nodes._node_focus(
                {
                    "common_focus": "network reachable code",
                    "agent_configs": {"search_fuzz_driver": {"focus": "configured harness focus"}},
                },
                "search_fuzz_driver_focus",
            ),
            'Global focus: "network reachable code"\n'
            'Stage-specific focus: "configured harness focus"\n'
            'Apply the global focus first, and additionally prioritize the '
            'stage-specific focus in this step.',
        )
        self.assertEqual(
            nodes._node_focus(
                {
                    "search_fuzz_driver_focus": "CLI override focus",
                    "agent_configs": {"search_fuzz_driver": {"focus": "configured harness focus"}},
                },
                "search_fuzz_driver_focus",
            ),
            'Stage-specific focus: "CLI override focus"\nPrioritize the stage-specific focus in this step.',
        )
        self.assertEqual(nodes._node_focus({}, "summary_focus"), "")

    def test_focus_aware_nodes_receive_their_stage_focus(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="focus-routing")
        prompts_by_node = {}

        def fake_invoke(
            ws_arg, node, prompt, backends, agent_configs=None, agent_config_task_types=None, subtask_id=None, extra_context=None, timeout=None
        ):
            del ws_arg, backends, agent_configs, subtask_id, extra_context, timeout
            prompts_by_node[node] = prompt
            if node == "search_similar_software":
                (ws.similar / "_candidates.json").write_text(json.dumps([{"name": "Peer One"}]))
            if node == "search_similar_history":
                sw_dir = ws.similar_for("Peer One")
                (sw_dir / "patch" / "fix.patch").write_text("diff --git")
            if node == "analyze_attack_surface":
                _write_domain_registry(ws)
            return AgentResult(stdout="ok", stderr="", returncode=0, backend="claude_code")

        state = {
            **_workspace_state(ws),
            "common_focus": "network reachable code",
            "search_fuzz_driver_focus": "HTTP parser harnesses",
            "search_similar_software_focus": "state-machine peers",
            "search_target_history_focus": "parser CVEs",
            "search_new_feature_focus": "new parser surfaces",
            "analyze_attack_surface_focus": "trust boundaries",
            "summary_focus": "actionable triage",
            "similar_writeups": ["similar/peer/writeup", "similar/peer2/writeup"],
            "feature_docs": ["main/feature/_index.json"],
        }

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            nodes.search_spec(state, backends={"search_spec": "claude_code"})
            nodes.search_fuzz_driver(state, backends={"search_fuzz_driver": "claude_code"})
            nodes.search_similar_software(state, backends={"search_similar_software": "claude_code"})
            nodes.search_similar_history(
                {**state, "similar_software": "Peer One"},
                backends={"search_similar_history": "claude_code"},
            )
            nodes.search_target_history(state, backends={"search_target_history": "claude_code"})
            nodes.search_new_feature(state, backends={"search_new_feature": "claude_code"})
            nodes.analyze_attack_surface(state, backends={"analyze_attack_surface": "claude_code"})
            nodes.summary(state, backends={"summary": "claude_code"})

        self.assertIn('Global focus: "network reachable code"', prompts_by_node["search_spec"])
        self.assertIn('Global focus: "network reachable code"', prompts_by_node["search_fuzz_driver"])
        self.assertIn('Stage-specific focus: "HTTP parser harnesses"', prompts_by_node["search_fuzz_driver"])
        self.assertIn('Stage-specific focus: "state-machine peers"', prompts_by_node["search_similar_software"])
        self.assertIn('Global focus: "network reachable code"', prompts_by_node["search_similar_history"])
        self.assertIn('Stage-specific focus: "parser CVEs"', prompts_by_node["search_target_history"])
        self.assertIn('Stage-specific focus: "new parser surfaces"', prompts_by_node["search_new_feature"])
        self.assertIn('Stage-specific focus: "trust boundaries"', prompts_by_node["analyze_attack_surface"])
        self.assertIn('Stage-specific focus: "actionable triage"', prompts_by_node["summary"])
        self.assertIn(str(ws.main_path("attack_surface") / "fuzz_drivers.md"), prompts_by_node["search_fuzz_driver"])
        self.assertIn(f"target writeups: {ws.main_path('writeup')}", prompts_by_node["analyze_attack_surface"])
        self.assertIn("similar-software writeups: ['similar/peer/writeup', 'similar/peer2/writeup']", prompts_by_node["analyze_attack_surface"])
        self.assertIn(f"new / weakly-covered feature surfaces: {ws.main_path('feature')}", prompts_by_node["analyze_attack_surface"])
        self.assertIn("feature_findings", prompts_by_node["summary"])
        self.assertIn(str(ws.base / "summary.en.md"), prompts_by_node["summary"])
        self.assertIn(str(ws.base / "summary.zh_CN.md"), prompts_by_node["summary"])


class DispatchTest(unittest.TestCase):
    def test_search_similar_software_parses_materialized_candidates_file(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="similar-file")

        def fake_invoke(
            ws_arg, node, prompt, backends, agent_configs=None, agent_config_task_types=None, subtask_id=None, extra_context=None, timeout=None
        ):
            del node, prompt, backends, agent_configs, subtask_id, extra_context, timeout
            (ws_arg.similar / "_candidates.json").write_text(
                json.dumps(
                    [
                        {"name": "Peer One", "repo_url": "https://example.com/one.git"},
                            {"name": "Peer Two / parser", "repo_url": "https://example.com/two.git"},
                        ]
                    )
                )
            return AgentResult(stdout="saved candidates to disk", stderr="", returncode=0, backend="claude_code")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.search_similar_software(
                {
                    "target": "libfoo",
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                },
                backends={"search_similar_software": "claude_code"},
            )

        self.assertEqual(update["similar_repos"], ["Peer One", "Peer Two - parser"])
        self.assertTrue((ws.similar / "peer_one" / "writeup").is_dir())
        self.assertTrue((ws.similar / "peer_two_-_parser" / "patch").is_dir())

    def test_dispatch_similar_history_fans_out_one_send_per_software(self):
        state = {
            "task_id": "task-1",
            "workspace_root": "/tmp/ws",
            "target": "libfoo",
            "common_focus": "parser",
            "similar_repos": [
                "Peer One",
                "MongoDB server / mongod",
                "/tmp/ws/similar/_candidates.json",
                "https://example.com/not-a-name",
            ],
        }

        sends = nodes.dispatch_similar_history(state)

        self.assertEqual([s.node for s in sends], ["search_similar_history", "search_similar_history"])
        self.assertEqual([s.arg["similar_software"] for s in sends], ["Peer One", "MongoDB server - mongod"])
        self.assertEqual(sends[0].arg["common_focus"], "parser")
        self.assertNotIn("focus", sends[0].arg)
        self.assertEqual(nodes.dispatch_similar_history({**state, "similar_repos": []}), "search_similar_history")

    def test_dispatch_creates_one_send_per_subtask_with_child_state(self):
        subtasks = [
            {"id": "spec-001", "bucket": "spec", "objective": "first", "hints": {}},
            {"id": "spec-002", "bucket": "spec", "objective": "second", "hints": {}},
        ]
        state = {
            "task_id": "task-1",
            "workspace_root": "/tmp/ws",
            "target": "libfoo",
            "repo_path": "/tmp/ws/main/repo",
            "max_iterations": 5,
        }

        sends = nodes._dispatch(subtasks, state)

        self.assertEqual(len(sends), 2)
        self.assertEqual([s.node for s in sends], ["subtask", "subtask"])
        self.assertEqual(sends[0].arg["subtask"], subtasks[0])
        self.assertEqual(sends[0].arg["iteration"], 0)
        self.assertEqual(sends[0].arg["review_history"], [])
        self.assertEqual(sends[0].arg["max_iterations"], 5)
        self.assertEqual(sends[0].arg["min_critic_skills"], nodes.DEFAULT_MIN_CRITIC_SKILLS)
        self.assertEqual(sends[0].arg["repo_path"], "/tmp/ws/main/repo")

    def test_dispatch_wrappers_pick_their_bucket_lists(self):
        state = {
            "task_id": "task-1",
            "workspace_root": "/tmp/ws",
            "target": "libfoo",
            "repo_path": "/tmp/ws/main/repo",
            "spec_subtasks": [{"id": "s", "bucket": "spec"}],
            "vuln_subtasks": [{"id": "v", "bucket": "vuln"}],
            "patch_subtasks": [{"id": "p", "bucket": "patch_miss"}],
        }

        self.assertEqual(nodes.dispatch_spec(state)[0].arg["subtask"]["id"], "s")
        self.assertEqual(nodes.dispatch_vuln(state)[0].arg["subtask"]["id"], "v")
        self.assertEqual(nodes.dispatch_patch(state)[0].arg["subtask"]["id"], "p")

    def test_dispatch_all_fans_out_all_buckets_or_routes_to_summary(self):
        state = {
            "task_id": "task-1",
            "workspace_root": "/tmp/ws",
            "target": "libfoo",
            "repo_path": "/tmp/ws/main/repo",
            "spec_subtasks": [{"id": "s", "bucket": "spec"}],
            "vuln_subtasks": [{"id": "v", "bucket": "vuln"}],
            "patch_subtasks": [{"id": "p", "bucket": "patch_miss"}],
        }

        sends = nodes.dispatch_all(state)

        self.assertEqual([s.arg["subtask"]["id"] for s in sends], ["s", "v", "p"])
        self.assertEqual([s.node for s in sends], ["subtask", "subtask", "subtask"])
        self.assertEqual(nodes.dispatch_all({**state, "spec_subtasks": [], "vuln_subtasks": [], "patch_subtasks": []}), "summary")

    def test_dispatch_all_applies_top_k_limits_per_bucket(self):
        state = {
            "task_id": "task-1",
            "workspace_root": "/tmp/ws",
            "target": "libfoo",
            "repo_path": "/tmp/ws/main/repo",
            "common_focus": "guest host escape stage2 mmu",
            "attack_surface": "guest ioctl reaches stage2 mmu path arch/arm64/kvm/mmu.c",
            "top_K": {"spec": 1, "patch": 1},
            "spec_subtasks": [
                {"id": "s1", "bucket": "spec", "objective": "check logging clause", "hints": {}},
                {
                    "id": "s2",
                    "bucket": "spec",
                    "objective": "check guest host escape stage2 mmu validation",
                    "hints": {"candidate_code_locations": ["arch/arm64/kvm/mmu.c:42"]},
                },
            ],
            "vuln_subtasks": [{"id": "v1", "bucket": "vuln"}, {"id": "v2", "bucket": "vuln"}],
            "patch_subtasks": [
                {"id": "p1", "bucket": "patch_miss", "objective": "audit unrelated cleanup", "hints": {}},
                {
                    "id": "p2",
                    "bucket": "patch_miss",
                    "objective": "audit stage2 mmu host escape fix",
                    "hints": {"candidate_code_locations": ["arch/arm64/kvm/mmu.c:88"]},
                },
            ],
        }

        sends = nodes.dispatch_all(state)

        self.assertEqual([s.arg["subtask"]["id"] for s in sends], ["s2", "v1", "v2", "p2"])

    def test_dispatch_all_skips_completed_subtasks_without_top_k_backfill(self):
        state = {
            "task_id": "task-1",
            "workspace_root": "/tmp/ws",
            "target": "libfoo",
            "repo_path": "/tmp/ws/main/repo",
            "top_K": {"spec": 1},
            "completed_subtask_ids": ["s1"],
            "spec_subtasks": [
                {"id": "s1", "bucket": "spec", "objective": "first", "hints": {}},
                {"id": "s2", "bucket": "spec", "objective": "second", "hints": {}},
            ],
            "vuln_subtasks": [{"id": "v1", "bucket": "vuln"}],
            "patch_subtasks": [],
        }

        sends = nodes.dispatch_all(state)

        self.assertEqual([s.arg["subtask"]["id"] for s in sends], ["v1"])

    def test_dispatch_all_diff_mode_converges_risk_surfaces_without_default_cap(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="diff-dispatch")
        state = {
            "task_id": ws.task_id,
            "workspace_root": str(ws.root),
            "target": "libfoo",
            "repo_path": str(ws.main_path("repo")),
            "scan_scope": {
                "mode": "diff",
                "repo_path": str(ws.main_path("repo")),
                "changed_files": ["src/changed.c"],
            },
            "spec_subtasks": [
                {
                    "id": "s1",
                    "bucket": "spec",
                    "objective": "validate length before allocation",
                    "hints": {
                        "risk_surface_ids": ["RS-001"],
                        "blocking_eligible": True,
                        "diff_anchor": ["main/repo/src/changed.c:10"],
                        "change_to_sink_path": ["parser", "allocator"],
                        "spec_clause": "Clause 1",
                    },
                },
                {
                    "id": "s2",
                    "bucket": "spec",
                    "objective": "validate the same length before allocation",
                    "hints": {
                        "risk_surface_ids": ["RS-001"],
                        "blocking_eligible": True,
                        "diff_anchor": ["src/changed.c:20"],
                        "change_to_sink_path": ["parser", "allocator"],
                        "spec_clause": "Clause 2",
                    },
                },
                {
                    "id": "s3",
                    "bucket": "spec",
                    "objective": "authorize state transition",
                    "hints": {
                        "risk_surface_ids": ["RS-002"],
                        "blocking_eligible": True,
                        "diff_anchor": ["src/changed.c:30"],
                        "change_to_sink_path": ["dispatcher", "privileged state"],
                    },
                },
                {
                    "id": "s4",
                    "bucket": "spec",
                    "objective": "context only",
                    "hints": {
                        "blocking_eligible": False,
                        "candidate_code_locations": ["src/context.c:40"],
                    },
                },
            ],
            "vuln_subtasks": [],
            "patch_subtasks": [],
            "feature_subtasks": [],
        }

        sends = nodes.dispatch_all(state)

        self.assertEqual([send.arg["subtask"]["id"] for send in sends], ["s1", "s3"])
        merged = sends[0].arg["subtask"]["hints"]
        self.assertEqual(merged["merged_subtasks"][0]["id"], "s2")
        self.assertEqual(merged["spec_refs"], ["Clause 1", "Clause 2"])
        report = json.loads(
            ws.state_path("dispatch_plan.json").read_text()
        )
        self.assertEqual(report["scan_mode"], "diff")
        self.assertEqual(report["totals"], {"candidates": 4, "selected": 2})
        self.assertEqual(report["buckets"]["spec"]["diff_attributable_count"], 3)
        self.assertEqual(report["buckets"]["spec"]["independent_risk_count"], 2)
        self.assertIsNone(report["buckets"]["spec"]["effective_limit"])
        self.assertEqual(
            [item["id"] for item in report["buckets"]["spec"]["selected"]],
            ["s1", "s3"],
        )
        self.assertEqual(
            {
                item["id"]: item["reason"]
                for item in report["buckets"]["spec"]["omitted"]
            },
            {"s2": "same_bucket_duplicate", "s4": "not_diff_attributable"},
        )

    def test_dispatch_all_diff_mode_does_not_dispatch_context_without_diff_path(self):
        state = {
            "task_id": "task-1",
            "workspace_root": "/tmp/ws",
            "target": "libfoo",
            "repo_path": "/tmp/ws/main/repo",
            "scan_scope": {"mode": "diff", "changed_files": ["src/changed.c"]},
            "spec_subtasks": [],
            "vuln_subtasks": [],
            "patch_subtasks": [],
            "feature_subtasks": [
                {
                    "id": "f1",
                    "bucket": "feature",
                    "hints": {
                        "risk_surface_ids": ["RS-001"],
                        "blocking_eligible": True,
                        "diff_anchor": ["src/changed.c:10"],
                    },
                },
                {
                    "id": "f2",
                    "bucket": "feature",
                    "hints": {"blocking_eligible": False},
                },
                {
                    "id": "f3",
                    "bucket": "feature",
                    "hints": {"blocking_eligible": False},
                },
            ],
        }

        sends = nodes.dispatch_all(state)

        self.assertEqual([send.arg["subtask"]["id"] for send in sends], ["f1"])

    def test_dispatch_all_diff_mode_merges_same_risk_surface_across_buckets(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="cross-bucket")
        common_hints = {
            "risk_surface_ids": ["RS-007"],
            "blocking_eligible": True,
            "diff_anchor": ["src/changed.c:10"],
            "change_to_sink_path": ["changed parser", "state machine", "sink"],
        }
        state = {
            "task_id": ws.task_id,
            "workspace_root": str(ws.root),
            "target": "libfoo",
            "repo_path": str(ws.main_path("repo")),
            "scan_scope": {
                "mode": "diff",
                "changed_files": ["src/changed.c"],
            },
            "spec_subtasks": [
                {
                    "id": "s1",
                    "bucket": "spec",
                    "objective": "verify parser clause",
                    "hints": {**common_hints, "spec_clause": "Clause 7"},
                }
            ],
            "vuln_subtasks": [
                {
                    "id": "v1",
                    "bucket": "vuln",
                    "objective": "probe parser CVE analogue",
                    "hints": {**common_hints, "cve": "CVE-2026-0001"},
                }
            ],
            "patch_subtasks": [
                {
                    "id": "p1",
                    "bucket": "patch_miss",
                    "objective": "verify parser patch invariant",
                    "hints": {**common_hints, "patch_commit": "abc123"},
                }
            ],
            "feature_subtasks": [],
        }

        sends = nodes.dispatch_all(state)

        self.assertEqual([send.arg["subtask"]["id"] for send in sends], ["p1"])
        representative = sends[0].arg["subtask"]
        self.assertEqual(
            [item["id"] for item in representative["hints"]["merged_subtasks"]],
            ["v1", "s1"],
        )
        self.assertEqual(representative["hints"]["cve_refs"], ["CVE-2026-0001"])
        self.assertEqual(representative["hints"]["spec_refs"], ["Clause 7"])
        report = json.loads(
            ws.state_path("dispatch_plan.json").read_text()
        )
        self.assertEqual(
            report["buckets"]["vuln"]["omitted"][-1],
            {
                "id": "v1",
                "reason": "cross_bucket_duplicate",
                "duplicate_of": "p1",
            },
        )
        self.assertEqual(
            report["buckets"]["spec"]["omitted"][-1],
            {
                "id": "s1",
                "reason": "cross_bucket_duplicate",
                "duplicate_of": "p1",
            },
        )

    def test_dispatch_all_diff_mode_round_robins_buckets(self):
        def task(task_id: str, bucket: str, risk_id: str) -> dict:
            return {
                "id": task_id,
                "bucket": bucket,
                "objective": task_id,
                "hints": {
                    "risk_surface_id": risk_id,
                    "diff_anchor": ["src/changed.c:10"],
                    "blocking_eligible": True,
                },
            }

        state = {
            "task_id": "task-1",
            "workspace_root": "/tmp/ws",
            "target": "libfoo",
            "repo_path": "/tmp/ws/main/repo",
            "scan_scope": {
                "mode": "diff",
                "changed_files": ["src/changed.c"],
            },
            "spec_subtasks": [
                task("s1", "spec", "RS-001"),
                task("s2", "spec", "RS-005"),
            ],
            "vuln_subtasks": [
                task("v1", "vuln", "RS-002"),
                task("v2", "vuln", "RS-006"),
            ],
            "patch_subtasks": [
                task("p1", "patch_miss", "RS-003"),
                task("p2", "patch_miss", "RS-007"),
            ],
            "feature_subtasks": [
                task("f1", "feature", "RS-004"),
                task("f2", "feature", "RS-008"),
            ],
        }

        sends = nodes.dispatch_all(state)

        self.assertEqual(
            [send.arg["subtask"]["id"] for send in sends],
            ["s1", "v1", "p1", "f1", "s2", "v2", "p2", "f2"],
        )

    def test_diff_convergence_does_not_merge_distinct_canonical_risk_ids(self):
        state = {
            "repo_path": "/tmp/ws/main/repo",
            "scan_scope": {
                "mode": "diff",
                "changed_files": ["src/changed.c"],
            },
        }
        tasks = [
            {
                "id": "s1",
                "bucket": "spec",
                "objective": "first invariant",
                "hints": {
                    "risk_surface_id": "RS-001",
                    "diff_anchor": ["src/changed.c:10"],
                    "blocking_eligible": True,
                    "priority_reason": "attack surface hypothesis #1",
                },
            },
            {
                "id": "s2",
                "bucket": "spec",
                "objective": "second invariant",
                "hints": {
                    "risk_surface_id": "RS-002",
                    "diff_anchor": ["src/changed.c:20"],
                    "blocking_eligible": True,
                    "priority_reason": "attack surface hypothesis #1",
                },
            },
        ]

        selected, omitted = nodes._converge_diff_planner_subtasks(tasks, state)

        self.assertEqual([task["id"] for task in selected], ["s1", "s2"])
        self.assertEqual(omitted, [])

    def test_full_mode_preserves_existing_fanout_without_diff_convergence(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="full-dispatch")
        state = {
            "task_id": ws.task_id,
            "workspace_root": str(ws.root),
            "target": "libfoo",
            "repo_path": str(ws.main_path("repo")),
            "scan_scope": {"mode": "full"},
            "common_focus": "critical parser escape",
            "spec_subtasks": [
                {"id": "s1", "bucket": "spec", "objective": "low priority", "hints": {}},
                {
                    "id": "s2",
                    "bucket": "spec",
                    "objective": "critical parser escape",
                    "hints": {},
                },
                {"id": "s3", "bucket": "spec", "objective": "medium priority", "hints": {}},
            ],
            "vuln_subtasks": [],
            "patch_subtasks": [],
            "feature_subtasks": [],
        }

        sends = nodes.dispatch_all(state)

        self.assertEqual(
            [send.arg["subtask"]["id"] for send in sends],
            ["s1", "s2", "s3"],
        )
        self.assertFalse(
            ws.state_path("dispatch_plan.json").exists()
        )

    def test_dispatch_wrappers_apply_top_k_limits(self):
        state = {
            "task_id": "task-1",
            "workspace_root": "/tmp/ws",
            "target": "libfoo",
            "repo_path": "/tmp/ws/main/repo",
            "common_focus": "ioctl host escape",
            "attack_surface": "ioctl path in virt/kvm/kvm_main.c is reachable by guest",
            "top_K": {"spec": 1, "vuln": 1},
            "spec_subtasks": [
                {"id": "s1", "bucket": "spec", "objective": "check docs", "hints": {}},
                {
                    "id": "s2",
                    "bucket": "spec",
                    "objective": "check ioctl host escape guard",
                    "hints": {"candidate_code_locations": ["virt/kvm/kvm_main.c:10"]},
                },
            ],
            "vuln_subtasks": [
                {"id": "v1", "bucket": "vuln", "objective": "low value", "hints": {}},
                {
                    "id": "v2",
                    "bucket": "vuln",
                    "objective": "guest ioctl host escape analogue",
                    "hints": {"candidate_code_locations": ["virt/kvm/kvm_main.c:20"]},
                },
            ],
            "patch_subtasks": [{"id": "p1", "bucket": "patch_miss"}, {"id": "p2", "bucket": "patch_miss"}],
        }

        self.assertEqual([s.arg["subtask"]["id"] for s in nodes.dispatch_spec(state)], ["s2"])
        self.assertEqual([s.arg["subtask"]["id"] for s in nodes.dispatch_vuln(state)], ["v2"])
        self.assertEqual([s.arg["subtask"]["id"] for s in nodes.dispatch_patch(state)], ["p1", "p2"])

    def test_dispatch_propagates_upstream_context_into_child_state(self):
        # The investigator must receive the fused attack-surface model +
        # threat model, not just repo_path + subtask, so it can frame its
        # work top-down instead of bottom-up only.
        subtasks = [{"id": "spec-001", "bucket": "spec", "objective": "o", "hints": {}}]
        state = {
            "task_id": "task-1",
            "workspace_root": "/tmp/ws",
            "target": "libfoo",
            "repo_path": "/tmp/ws/main/repo",
            "common_focus": "guest-to-host escape",
            "attack_surface": "/tmp/ws/main/attack_surface/attack_surface.md",
            "spec_doc": "/tmp/ws/main/spec/spec.md",
            "similar_writeups": ["similar/peer/writeup"],
            "feature_docs": ["main/feature/_index.json"],
        }

        sends = nodes._dispatch(subtasks, state)

        child = sends[0].arg
        self.assertEqual(child["common_focus"], "guest-to-host escape")
        self.assertEqual(child["attack_surface"], "/tmp/ws/main/attack_surface/attack_surface.md")
        self.assertEqual(child["spec_doc"], "/tmp/ws/main/spec/spec.md")
        self.assertEqual(child["similar_writeups"], ["similar/peer/writeup"])
        self.assertEqual(child["feature_docs"], ["main/feature/_index.json"])


class RouteAfterCriticTest(unittest.TestCase):
    def test_hypothesis_package_routes_only_after_critic_closes_coverage(self):
        subtask = _hypothesis_package_subtask()
        open_review = _closed_hypothesis_review()
        open_review["package_decision"] = "revise"
        open_review["verdict"] = "revise"
        open_review["coverage_verdict"]["status"] = "open"
        open_review["coverage_verdict"]["obligation_assessments"][1]["status"] = "open"

        self.assertEqual(
            nodes.route_after_critic(
                {
                    "subtask": subtask,
                    "review": open_review,
                    "iteration": 1,
                    "max_iterations": 3,
                }
            ),
            "investigate_subtask",
        )
        self.assertEqual(
            nodes.route_after_critic(
                {
                    "subtask": subtask,
                    "review": _closed_hypothesis_review(),
                    "iteration": 2,
                    "max_iterations": 3,
                }
            ),
            "finalize_subtask",
        )

    def test_hypothesis_package_without_counterexample_does_not_close(self):
        review = _closed_hypothesis_review()
        review["coverage_verdict"]["counterexample_attempts"] = []

        self.assertFalse(nodes.hypothesis_package_closed(review))
        self.assertEqual(
            nodes.route_after_critic(
                {
                    "subtask": _hypothesis_package_subtask(),
                    "review": review,
                    "iteration": 1,
                    "max_iterations": 3,
                }
            ),
            "investigate_subtask",
        )

    def test_hypothesis_package_exhaustion_finalizes_without_claiming_closure(self):
        review = _closed_hypothesis_review()
        review["package_decision"] = "revise"
        review["verdict"] = "revise"
        review["coverage_verdict"]["status"] = "open"

        self.assertEqual(
            nodes.route_after_critic(
                {
                    "subtask": _hypothesis_package_subtask(),
                    "review": review,
                    "iteration": 3,
                    "max_iterations": 3,
                }
            ),
            "finalize_subtask",
        )

    def test_hypothesis_package_contract_error_does_not_consume_investigation_iteration(self):
        review = _closed_hypothesis_review()
        review["package_decision"] = "revise"
        review["verdict"] = "revise"
        review["batch_contract_errors"] = [
            "new_hypothesis_decisions included a manifest hypothesis"
        ]

        self.assertEqual(
            nodes.route_after_critic(
                {
                    "subtask": _hypothesis_package_subtask(),
                    "review": review,
                    "iteration": 1,
                    "max_iterations": 3,
                }
            ),
            "finalize_subtask",
        )

    def test_route_after_fetch_stops_on_errors_or_fans_out_on_success(self):
        self.assertEqual(nodes.route_after_fetch_target_repo({"errors": ["empty repo"]}), "__end__")
        self.assertEqual(nodes.route_after_fetch_target_repo({"errors": []}), "prepare_scan_scope")
        self.assertEqual(
            nodes.route_after_prepare_scan_scope({"errors": []}),
            [
                "search_spec",
                "search_fuzz_driver",
                "search_similar_software",
                "search_target_history",
            ],
        )

    def test_route_after_fetch_filters_disabled_gather_nodes(self):
        self.assertEqual(
            nodes.route_after_prepare_scan_scope({"disabled_nodes": ["search_spec"]}),
            ["search_fuzz_driver", "search_similar_software", "search_target_history"],
        )
        self.assertEqual(
            nodes.route_after_prepare_scan_scope({"disabled_nodes": ["search_target_history"]}),
            ["search_spec", "search_fuzz_driver", "search_similar_software"],
        )
        self.assertEqual(
            nodes.route_after_prepare_scan_scope({}),
            ["search_spec", "search_fuzz_driver", "search_similar_software", "search_target_history"],
        )
        self.assertEqual(
            nodes.route_after_fetch_target_repo({"errors": ["x"], "disabled_nodes": ["search_spec"]}),
            "__end__",
        )
        self.assertEqual(nodes.route_after_prepare_scan_scope({"errors": ["bad diff"]}), "__end__")


class PrepareScanScopeNodeTest(unittest.TestCase):
    def test_full_mode_materializes_scope_without_restricting_repository(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="scope-full")
        (ws.main_path("repo") / "README.md").write_text("source")

        update = nodes.prepare_scan_scope(
            {
                "task_id": ws.task_id,
                "workspace_root": str(ws.root),
                "repo_path": str(ws.main_path("repo")),
                "scan_mode": "full",
            }
        )

        self.assertEqual(update["errors"], [])
        self.assertEqual(update["scan_scope"]["mode"], "full")
        self.assertFalse(update["scan_scope"]["policy"]["finding_must_intersect_diff"])
        self.assertTrue(Path(update["scope_path"]).is_file())

    def test_diff_mode_rejects_repo_that_does_not_contain_patched_path(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="scope-diff-bad")
        (ws.main_path("repo") / "README.md").write_text("source")
        diff = Path(tmp.name) / "change.patch"
        diff.write_text(
            "diff --git a/src/new.c b/src/new.c\n"
            "new file mode 100644\n"
            "--- /dev/null\n"
            "+++ b/src/new.c\n"
            "@@ -0,0 +1 @@\n"
            "+new();\n"
        )

        update = nodes.prepare_scan_scope(
            {
                "task_id": ws.task_id,
                "workspace_root": str(ws.root),
                "repo_path": str(ws.main_path("repo")),
                "scan_mode": "diff",
                "diff_file": str(diff),
            }
        )

        self.assertEqual(len(update["errors"]), 1)
        self.assertIn("patched repository does not contain", update["errors"][0])

    def test_confirm_and_reject_finalize(self):
        self.assertEqual(
            nodes.route_after_critic({"review": {"verdict": "confirm"}, "iteration": 1, "max_iterations": 3}),
            "finalize_subtask",
        )
        self.assertEqual(
            nodes.route_after_critic({"review": {"verdict": "Reject"}, "iteration": 1, "max_iterations": 3}),
            "finalize_subtask",
        )

    def test_first_iteration_no_finding_terminal_verdict_routes_to_revise(self):
        state = {
            "investigation": json.dumps(
                {
                    "title": "no-finding",
                    "status": "no-finding",
                    "detail": "reference path applies the guard",
                    "evidence": {},
                }
            ),
            "iteration": 1,
            "max_iterations": 3,
        }

        self.assertEqual(
            nodes.route_after_critic({**state, "review": {"verdict": "reject"}}),
            "investigate_subtask",
        )
        self.assertEqual(
            nodes.route_after_critic({**state, "review": {"verdict": "confirm"}}),
            "investigate_subtask",
        )

    def test_first_iteration_no_finding_forces_revise_even_when_max_exhausted(self):
        state = {
            "review": {"verdict": "reject"},
            "investigation": json.dumps({"title": "no-finding", "status": "no-finding"}),
            "iteration": 1,
            "max_iterations": 1,
        }

        self.assertEqual(nodes.route_after_critic(state), "investigate_subtask")

    def test_revise_loops_until_max_iterations(self):
        self.assertEqual(
            nodes.route_after_critic({"review": {"verdict": "revise"}, "iteration": 1, "max_iterations": 3}),
            "investigate_subtask",
        )
        self.assertEqual(
            nodes.route_after_critic({"review": {"verdict": "revise"}, "iteration": 3, "max_iterations": 3}),
            "finalize_subtask",
        )

    def test_missing_verdict_defaults_to_revise(self):
        self.assertEqual(
            nodes.route_after_critic({"review": {}, "iteration": 0, "max_iterations": 1}),
            "investigate_subtask",
        )

    def test_non_object_review_defaults_to_revise(self):
        self.assertEqual(
            nodes.route_after_critic({"review": [{"verdict": "confirm"}], "iteration": 1, "max_iterations": 3}),
            "investigate_subtask",
        )

    def test_invalid_confirmed_primitive_review_routes_back_for_one_repair(self):
        state = {
            "review": {
                "verdict": "revise",
                "original_verdict": "confirm",
                "outcome_type": "confirmed_primitive",
                "primitive_gate_ok": False,
            },
            "iteration": 1,
            "max_iterations": 3,
            "review_history": [],
        }
        self.assertEqual(nodes.route_after_critic(state), "investigate_subtask")

    def test_repeated_invalid_confirmed_primitive_can_finalize_at_iteration_limit(self):
        state = {
            "review": {
                "verdict": "revise",
                "original_verdict": "confirm",
                "outcome_type": "confirmed_primitive",
                "primitive_gate_ok": False,
            },
            "iteration": 3,
            "max_iterations": 3,
            "review_history": [
                {"iteration": 2, "review": {"primitive_gate_ok": False}},
            ],
        }
        self.assertEqual(nodes.route_after_critic(state), "finalize_subtask")


class FinalizeSubtaskTest(unittest.TestCase):
    def _finalize(
        self,
        bucket: str,
        verdict: str = "confirm",
        investigation_extra: dict | None = None,
        review_extra: dict | None = None,
    ) -> tuple[dict, Workspace]:
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id=f"finalize-{bucket}")
        investigation = {
            "title": "confirmed title",
            "detail": "finding detail",
            "evidence": {
                "code_locations": ["a.py:1"],
                "call_path": ["entry -> sink"],
            },
            "severity": "low",
            "confidence": 0.2,
            **(investigation_extra or {}),
        }
        review = {
            **_qualified_review(verdict, selected_skills=["memory"]),
            **(review_extra or {}),
        }
        state = {
            **_workspace_state(ws),
            "subtask": {"id": f"{bucket}-001", "bucket": bucket, "objective": "fallback title"},
            "iteration": 2,
            "investigation": json.dumps(investigation),
            "review": review,
            "review_history": [{"iteration": 2, "review": {"verdict": verdict}}],
        }
        return nodes.finalize_subtask(state), ws

    def test_spec_bucket_merges_to_spec_findings(self):
        update, _ = self._finalize("spec")

        self.assertIn("spec_findings", update)
        finding = update["spec_findings"][0]
        self.assertEqual(finding["kind"], "spec")
        self.assertEqual(finding["title"], "confirmed title")
        self.assertEqual(finding["severity"], "high")
        self.assertEqual(finding["confidence"], 0.9)
        self.assertEqual(finding["selected_skills"], ["memory"])

    def test_vuln_bucket_merges_to_vuln_candidates(self):
        update, _ = self._finalize("vuln")

        self.assertIn("vuln_candidates", update)
        self.assertEqual(update["vuln_candidates"][0]["kind"], "vuln")

    def test_patch_miss_bucket_merges_to_patch_findings(self):
        update, ws = self._finalize("patch_miss")

        self.assertIn("patch_findings", update)
        self.assertEqual(update["patch_findings"][0]["kind"], "patch_miss")
        self.assertTrue((ws.log_path("subtask_res") / "patch_miss-001.json").is_file())

    def test_patch_status_is_persisted_to_finding(self):
        update, ws = self._finalize(
            "patch_miss",
            investigation_extra={"patch_status": "bypass"},
        )

        finding = update["patch_findings"][0]
        self.assertEqual(finding["patch_status"], "bypass")
        payload = json.loads((ws.log_path("subtask_res") / "patch_miss-001.json").read_text())
        self.assertEqual(payload["finding"]["patch_status"], "bypass")

    def test_known_cve_patch_gap_is_not_promoted_to_vulnerability(self):
        update, ws = self._finalize(
            "patch_miss",
            investigation_extra={
                "title": "CVE-2025-1234 fix not applied",
                "detail": "The named upstream fix is absent.",
                "patch_status": "not_applied",
            },
            review_extra={
                "disposition": "known_cve_patch_gap",
                "documented_expected_behavior": False,
                "security_contract_violation": False,
                "violated_security_property": "",
                "standalone_security_impact": False,
                "direct_security_impact": {
                    "vulnerable_system": {
                        "confidentiality": "none",
                        "integrity": "none",
                        "availability": "none",
                    },
                    "subsequent_system": {
                        "confidentiality": "none",
                        "integrity": "none",
                        "availability": "none",
                    },
                },
                "required_external_primitives": [],
                "cvss_applicable": False,
                "cvss4_vector": "",
            },
        )

        self.assertIn("patch_findings", update)
        self.assertIn("observations", update)
        finding = update["patch_findings"][0]
        self.assertEqual(finding["disposition"], "known_cve_patch_gap")
        self.assertFalse(finding["qualification_gate_passed"])
        self.assertFalse(finding["cvss_applicable"])
        self.assertEqual(finding["severity"], "none")
        self.assertNotIn("cvss4_score", finding)
        payload = json.loads((ws.log_path("subtask_res") / "patch_miss-001.json").read_text())
        self.assertEqual(payload["finding"]["patch_status"], "not_applied")

    def test_review_patch_status_overrides_investigation_value(self):
        update, _ = self._finalize(
            "patch_miss",
            investigation_extra={"patch_status": "not_applied"},
            review_extra={"patch_status": "incomplete"},
        )

        self.assertEqual(update["patch_findings"][0]["patch_status"], "incomplete")

    def test_rejected_subtask_writes_result_but_returns_no_finding(self):
        update, ws = self._finalize("patch_miss", verdict="reject")

        self.assertEqual(update, {})
        self.assertTrue((ws.log_path("subtask_res") / "patch_miss-001.json").is_file())

    def test_selected_run_writes_finding_and_history_only_to_isolated_results(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="selected-finalize")
        selected_dir = ws.base / "selected-run"
        (selected_dir / "results").mkdir(parents=True)
        canonical = ws.log_path("subtask_res") / "vuln-001.json"
        canonical.write_text('{"canonical": true}')
        history = [
            {"iteration": 1, "review": {"verdict": "revise"}},
            {"iteration": 2, "review": {"verdict": "confirm"}},
        ]
        state = {
            **_workspace_state(ws),
            "selected_subtask_log_dir": str(selected_dir),
            "subtask": {
                "id": "vuln-001",
                "bucket": "vuln",
                "objective": "rerun finding",
            },
            "iteration": 2,
            "investigation": json.dumps(_valid_investigation("rerun finding")),
            "review": {
                **_qualified_review(selected_skills=["memory"]),
            },
            "review_history": history,
        }

        update = nodes.finalize_subtask(state)

        self.assertIn("vuln_candidates", update)
        self.assertEqual(canonical.read_text(), '{"canonical": true}')
        isolated = json.loads(
            (selected_dir / "results" / "vuln-001.json").read_text()
        )
        self.assertEqual(isolated["finding"]["title"], "rerun finding")
        self.assertEqual(isolated["history"], history)

    def test_invalid_investigation_json_is_not_persisted(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="invalid-json")
        state = {
            **_workspace_state(ws),
            "subtask": {"id": "patch-001", "bucket": "patch_miss", "objective": "fallback objective"},
            "iteration": 1,
            "investigation": "not json",
            "review": {"verdict": "confirm"},
        }

        update = nodes.finalize_subtask(state)

        self.assertNotIn("patch_findings", update)
        self.assertIn("refusing to persist invalid investigation", update["errors"][0])
        self.assertFalse((ws.log_path("subtask_res") / "patch-001.json").exists())

    def test_batch_finalization_persists_atomic_results_and_parent_manifest(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="batch-finalize")
        subtask = _hypothesis_package_subtask()
        state = {
            **_workspace_state(ws),
            "subtask": subtask,
            "iteration": 2,
            "max_iterations": 3,
            "hypothesis_manifest": nodes.initial_hypothesis_manifest(subtask),
            "investigation": json.dumps(_hypothesis_batch_investigation()),
            "review": _closed_hypothesis_review(),
            "review_history": [],
        }

        update = nodes.finalize_subtask(state)

        self.assertEqual(len(update["spec_findings"]), 1)
        finding = update["spec_findings"][0]
        self.assertEqual(finding["parent_subtask_id"], "spec-028")
        self.assertEqual(finding["hypothesis_id"], "spec-028:hyp-cred")
        self.assertEqual(finding["subtask_id"], "spec-028--spec-028:hyp-cred")
        manifest = json.loads(
            (ws.log_path("subtask_res") / "spec-028.json").read_text()
        )
        self.assertTrue(manifest["closed"])
        self.assertEqual(len(manifest["artifacts"]), 2)
        for artifact in manifest["artifacts"]:
            self.assertTrue(Path(artifact["path"]).is_file())

    def test_exhausted_open_batch_is_materialized_as_inconclusive(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="batch-exhausted")
        subtask = _hypothesis_package_subtask()
        review = _closed_hypothesis_review()
        review["package_decision"] = "revise"
        review["verdict"] = "revise"
        review["coverage_verdict"]["status"] = "open"
        review["hypothesis_verdicts"][1]["verdict"] = "revise"
        state = {
            **_workspace_state(ws),
            "subtask": subtask,
            "iteration": 3,
            "max_iterations": 3,
            "hypothesis_manifest": nodes.initial_hypothesis_manifest(subtask),
            "investigation": json.dumps(_hypothesis_batch_investigation()),
            "review": review,
            "review_history": [],
        }

        update = nodes.finalize_subtask(state)

        self.assertIn("observations", update)
        self.assertEqual(len(update["spec_findings"]), 1)
        self.assertEqual(
            update["spec_findings"][0]["hypothesis_id"],
            "spec-028:hyp-cred",
        )
        self.assertTrue(any(item["outcome_type"] == "inconclusive" for item in update["observations"]))
        self.assertIn("exhausted before critic confirmed coverage closure", update["errors"][0])
        manifest = json.loads(
            (ws.log_path("subtask_res") / "spec-028.json").read_text()
        )
        self.assertFalse(manifest["closed"])
        self.assertTrue(manifest["exhausted"])

    def test_package_contract_error_preserves_terminal_atomic_finding(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="batch-contract-error")
        subtask = _hypothesis_package_subtask()
        review = _closed_hypothesis_review()
        review["package_decision"] = "revise"
        review["verdict"] = "revise"
        review["coverage_verdict"]["status"] = "open"
        review["batch_contract_errors"] = [
            "new_hypothesis_decisions included a manifest hypothesis"
        ]
        state = {
            **_workspace_state(ws),
            "subtask": subtask,
            "iteration": 2,
            "max_iterations": 3,
            "hypothesis_manifest": nodes.initial_hypothesis_manifest(subtask),
            "investigation": json.dumps(_hypothesis_batch_investigation()),
            "review": review,
            "review_history": [],
        }

        update = nodes.finalize_subtask(state)

        self.assertEqual(len(update["spec_findings"]), 1)
        finding = update["spec_findings"][0]
        self.assertEqual(finding["hypothesis_id"], "spec-028:hyp-cred")
        self.assertEqual(finding["package_status"], "incomplete")
        self.assertEqual(
            finding["package_contract_errors"],
            review["batch_contract_errors"],
        )
        package = json.loads(
            (ws.log_path("subtask_res") / "spec-028.json").read_text()
        )
        self.assertFalse(package["closed"])
        self.assertEqual(package["status"], "incomplete")

    def test_package_contract_error_preserves_terminal_discovered_sibling(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="batch-discovery-salvage")
        subtask = _hypothesis_package_subtask()
        investigation = _hypothesis_batch_investigation()
        discovery = {
            "hypothesis_id": "spec-028:hyp-teardown",
            "statement": "teardown races with credential release",
            "obligation_ids": ["spec-028:obl-cred"],
        }
        investigation["newly_discovered_hypotheses"] = [discovery]
        investigation["hypothesis_results"].append(
            {
                "hypothesis_id": discovery["hypothesis_id"],
                **_valid_investigation("teardown race"),
            }
        )
        investigation["coverage_matrix"][0]["hypothesis_ids"].append(
            discovery["hypothesis_id"]
        )
        review = _closed_hypothesis_review()
        review["package_decision"] = "revise"
        review["verdict"] = "revise"
        review["coverage_verdict"]["status"] = "open"
        review["coverage_verdict"]["obligation_assessments"][0]["status"] = "open"
        review["hypothesis_verdicts"].append(
            {
                "hypothesis_id": discovery["hypothesis_id"],
                "reasoning": "the teardown race independently violates the lifetime contract",
                **_qualified_review(),
            }
        )
        review["batch_contract_errors"] = [
            "new_hypothesis_decisions must account for exactly this iteration's "
            "newly_discovered_hypotheses"
        ]
        state = {
            **_workspace_state(ws),
            "subtask": subtask,
            "iteration": 2,
            "max_iterations": 3,
            # The package contract failed before the discovery could advance
            # the monotonic manifest.  Its terminal atomic verdict must still
            # survive finalization.
            "hypothesis_manifest": nodes.initial_hypothesis_manifest(subtask),
            "investigation": json.dumps(investigation),
            "review": review,
            "review_history": [],
        }

        update = nodes.finalize_subtask(state)

        self.assertEqual(
            {item["hypothesis_id"] for item in update["spec_findings"]},
            {"spec-028:hyp-cred", "spec-028:hyp-teardown"},
        )
        package = json.loads(
            (ws.log_path("subtask_res") / "spec-028.json").read_text()
        )
        self.assertFalse(package["closed"])
        self.assertEqual(
            {item["hypothesis_id"] for item in package["artifacts"]},
            {
                "spec-028:hyp-cred",
                "spec-028:hyp-cpu",
                "spec-028:hyp-teardown",
            },
        )

    def test_incomplete_batch_restore_does_not_promote_inconclusive_sibling(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="batch-restore-open")
        subtask = _hypothesis_package_subtask()
        review = _closed_hypothesis_review()
        review["package_decision"] = "revise"
        review["verdict"] = "revise"
        review["coverage_verdict"]["status"] = "open"
        review["hypothesis_verdicts"][1]["verdict"] = "revise"
        state = {
            **_workspace_state(ws),
            "subtask": subtask,
            "iteration": 3,
            "max_iterations": 3,
            "hypothesis_manifest": nodes.initial_hypothesis_manifest(subtask),
            "investigation": json.dumps(_hypothesis_batch_investigation()),
            "review": review,
            "review_history": [],
        }

        live_update = nodes.finalize_subtask(state)
        spec, vuln, patch_findings, feature = graph_mod._finding_buckets_from_subtask_res(ws)

        self.assertEqual(
            [item["hypothesis_id"] for item in spec],
            [item["hypothesis_id"] for item in live_update["spec_findings"]],
        )
        self.assertEqual(vuln, [])
        self.assertEqual(patch_findings, [])
        self.assertEqual(feature, [])

    def test_summary_restore_recovers_primitive_and_inconclusive_siblings_as_observations(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="batch-restore-observations")
        (ws.main_path("repo") / "README.md").write_text("source")
        (ws.main_path("attack_surface") / "attack_surface.md").write_text("surface")
        subtask = _hypothesis_package_subtask()
        review = _closed_hypothesis_review()
        review["package_decision"] = "revise"
        review["verdict"] = "revise"
        review["coverage_verdict"]["status"] = "open"
        review["hypothesis_verdicts"][0] = {
            "hypothesis_id": "spec-028:hyp-cred",
            "verdict": "confirm",
            "outcome_type": "confirmed_primitive",
            "reasoning": "the credential reference primitive is established",
            "confidence": 0.8,
            "cvss_applicable": False,
            "primitive": {
                "component": "credential",
                "root_cause_anchor": {
                    "symbol": "setup_cred",
                    "locations": ["src/sample.c:2"],
                },
                "capabilities_gained": [
                    {
                        "kind": "credential_access",
                        "object_type": "credential",
                        "principal": "worker",
                    }
                ],
            },
        }
        review["hypothesis_verdicts"][1]["verdict"] = "revise"
        state = {
            **_workspace_state(ws),
            "subtask": subtask,
            "iteration": 3,
            "max_iterations": 3,
            "hypothesis_manifest": nodes.initial_hypothesis_manifest(subtask),
            "investigation": json.dumps(_hypothesis_batch_investigation()),
            "review": review,
            "review_history": [],
        }

        live_update = nodes.finalize_subtask(state)
        restored = graph_mod._summary_state_from_workspace(ws.base)
        restored_again = graph_mod._summary_state_from_workspace(ws.base)

        self.assertEqual(restored["spec_findings"], [])
        self.assertEqual(
            [item["primitive_id"] for item in restored["confirmed_primitives"]],
            [item["primitive_id"] for item in live_update["confirmed_primitives"]],
        )
        self.assertEqual(
            {
                (
                    item["hypothesis_id"],
                    item["outcome_type"],
                    item.get("primitive_gate_passed"),
                )
                for item in restored["observations"]
            },
            {
                (
                    item["hypothesis_id"],
                    item["outcome_type"],
                    item.get("primitive_gate_passed"),
                )
                for item in live_update["observations"]
            },
        )
        self.assertIn(
            ("spec-028:hyp-cred", "confirmed_primitive", True),
            {
                (
                    item["hypothesis_id"],
                    item["outcome_type"],
                    item.get("primitive_gate_passed"),
                )
                for item in restored["observations"]
            },
        )
        self.assertEqual(restored_again["confirmed_primitives"], restored["confirmed_primitives"])
        self.assertEqual(restored_again["observations"], restored["observations"])

    def test_exhausted_batch_materializes_critic_required_hypothesis_as_inconclusive(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="batch-required")
        subtask = _hypothesis_package_subtask()
        required = {
            "hypothesis_id": "spec-028:hyp-teardown",
            "statement": "teardown may race with credential release",
            "obligation_ids": ["spec-028:obl-cred"],
        }
        review = _closed_hypothesis_review()
        review["package_decision"] = "revise"
        review["verdict"] = "revise"
        review["coverage_verdict"]["status"] = "open"
        review["coverage_verdict"]["obligation_assessments"][0]["status"] = "open"
        review["required_hypotheses"] = [required]
        manifest = nodes.advance_hypothesis_manifest(
            subtask,
            nodes.initial_hypothesis_manifest(subtask),
            _hypothesis_batch_investigation(),
            review,
        )
        state = {
            **_workspace_state(ws),
            "subtask": subtask,
            "iteration": 3,
            "max_iterations": 3,
            "hypothesis_manifest": manifest,
            "investigation": json.dumps(_hypothesis_batch_investigation()),
            "review": review,
            "review_history": [],
        }

        update = nodes.finalize_subtask(state)

        required_observation = next(
            item
            for item in update["observations"]
            if item.get("hypothesis_id") == "spec-028:hyp-teardown"
        )
        self.assertEqual(required_observation["outcome_type"], "inconclusive")
        self.assertEqual(required_observation["evidence"]["code_locations"], [])
        manifest_payload = json.loads(
            (ws.log_path("subtask_res") / "spec-028.json").read_text()
        )
        self.assertEqual(len(manifest_payload["artifacts"]), 3)


class InvestigateSubtaskTest(unittest.TestCase):
    def test_batch_investigation_rejects_dropped_seed_hypothesis(self):
        subtask = _hypothesis_package_subtask()
        investigation = _hypothesis_batch_investigation()
        investigation["hypothesis_results"] = investigation["hypothesis_results"][:1]
        investigation["coverage_matrix"][1]["hypothesis_ids"] = ["spec-028:hyp-cred"]

        parsed, detail = nodes.validate_hypothesis_investigation(
            investigation,
            subtask=subtask,
            prior_manifest=nodes.initial_hypothesis_manifest(subtask),
        )

        self.assertIsNone(parsed)
        self.assertIn("dropped known hypothesis", detail)

    def test_batch_review_requires_one_verdict_per_hypothesis(self):
        review = _closed_hypothesis_review()
        review["hypothesis_verdicts"] = review["hypothesis_verdicts"][:1]

        parsed, detail = nodes.validate_hypothesis_review(
            review,
            subtask=_hypothesis_package_subtask(),
            investigation=_hypothesis_batch_investigation(),
        )

        self.assertIsNone(parsed)
        self.assertIn("exactly one verdict", detail)

    def test_second_iteration_does_not_redecide_manifest_hypothesis(self):
        subtask = _hypothesis_package_subtask()
        manifest = nodes.initial_hypothesis_manifest(subtask)
        manifest["revision"] = 1
        manifest["hypotheses"].append(
            {
                "hypothesis_id": "spec-028:hyp-teardown",
                "statement": "teardown races with credential release",
                "obligation_ids": ["spec-028:obl-cred"],
            }
        )
        investigation = _hypothesis_batch_investigation()
        investigation["manifest_revision"] = 2
        investigation["hypothesis_results"].append(
            {
                "hypothesis_id": "spec-028:hyp-teardown",
                **_valid_investigation("teardown race"),
            }
        )
        investigation["coverage_matrix"][0]["hypothesis_ids"].append(
            "spec-028:hyp-teardown"
        )
        investigation["newly_discovered_hypotheses"] = []

        parsed_investigation, detail = nodes.validate_hypothesis_investigation(
            investigation,
            subtask=subtask,
            prior_manifest=manifest,
        )
        self.assertIsNotNone(parsed_investigation, detail)

        review = _closed_hypothesis_review()
        review["hypothesis_verdicts"].append(
            {
                "hypothesis_id": "spec-028:hyp-teardown",
                "verdict": "reject",
                "outcome_type": "rejected",
                "reasoning": "teardown holds the required reference",
                "disposition": "no_finding",
            }
        )
        review["coverage_verdict"]["obligation_assessments"][0][
            "hypothesis_ids"
        ].append("spec-028:hyp-teardown")
        review["new_hypothesis_decisions"] = []

        parsed_review, detail = nodes.validate_hypothesis_review(
            review,
            subtask=subtask,
            investigation=parsed_investigation,
        )
        self.assertIsNotNone(parsed_review, detail)
        self.assertEqual(parsed_review["new_hypothesis_decisions"], [])

    def test_package_closure_requires_counterexample_attempt(self):
        review = _closed_hypothesis_review()
        review["coverage_verdict"]["counterexample_attempts"] = []

        parsed, detail = nodes.validate_hypothesis_review(
            review,
            subtask=_hypothesis_package_subtask(),
            investigation=_hypothesis_batch_investigation(),
        )

        self.assertIsNone(parsed)
        self.assertIn("cannot claim closure without a counterexample attempt", detail)

    def test_investigator_cannot_propose_closure_without_counterexample_attempt(self):
        investigation = _hypothesis_batch_investigation()
        investigation["counterexample_attempts"] = []

        parsed, detail = nodes.validate_hypothesis_investigation(
            investigation,
            subtask=_hypothesis_package_subtask(),
            prior_manifest=nodes.initial_hypothesis_manifest(
                _hypothesis_package_subtask()
            ),
        )

        self.assertIsNone(parsed)
        self.assertIn("cannot claim closure without a counterexample attempt", detail)

    def test_critic_accepted_discovery_extends_manifest_without_new_graph_subtask(self):
        subtask = _hypothesis_package_subtask()
        investigation = _hypothesis_batch_investigation()
        discovery = {
            "hypothesis_id": "hyp-teardown",
            "statement": "teardown races with worker credential release",
            "obligation_ids": ["spec-028:obl-cred"],
        }
        investigation["newly_discovered_hypotheses"] = [discovery]
        investigation["hypothesis_results"].append(
            {"hypothesis_id": "hyp-teardown", **_valid_investigation("teardown race")}
        )
        investigation["coverage_matrix"][0]["hypothesis_ids"].append("hyp-teardown")
        review = _closed_hypothesis_review()
        review["package_decision"] = "revise"
        review["verdict"] = "revise"
        review["coverage_verdict"]["status"] = "open"
        review["coverage_verdict"]["obligation_assessments"][0]["status"] = "open"
        review["hypothesis_verdicts"].append(
            {
                "hypothesis_id": "hyp-teardown",
                "verdict": "revise",
                "reasoning": "needs lifetime proof",
            }
        )
        review["new_hypothesis_decisions"] = [
            {
                "hypothesis_id": "hyp-teardown",
                "decision": "accept",
                "reasoning": "independent lifecycle branch",
            }
        ]

        parsed, detail = nodes.validate_hypothesis_review(
            review,
            subtask=subtask,
            investigation=investigation,
        )
        self.assertIsNotNone(parsed, detail)
        manifest = nodes.advance_hypothesis_manifest(
            subtask,
            nodes.initial_hypothesis_manifest(subtask),
            investigation,
            parsed,
        )
        self.assertEqual(
            [item["hypothesis_id"] for item in manifest["hypotheses"]],
            ["spec-028:hyp-cred", "spec-028:hyp-cpu", "hyp-teardown"],
        )
        self.assertEqual(manifest["revision"], 1)

    def test_fresh_finding_artifact_avoids_stdout_format_retry(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="fresh-artifact")
        calls = 0

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            nonlocal calls
            del (
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                extra_context,
                timeout,
            )
            calls += 1
            sub_ws = ws_arg.prepare_sub_workspace(
                node=node,
                subtask_id=subtask_id,
                backend="codex",
            )
            (sub_ws / "finding.json").write_text(
                json.dumps(_valid_investigation("artifact result"))
            )
            return AgentResult(
                stdout="wrote finding.json",
                stderr="",
                returncode=0,
                backend="codex",
                cwd=str(sub_ws),
            )

        state = {
            **_workspace_state(ws),
            "subtask": {
                "id": "vuln-013",
                "bucket": "vuln",
                "objective": "validate artifact fallback",
            },
            "iteration": 0,
            "max_iterations": 3,
        }

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.investigate_subtask(
                state,
                backends={"investigate_subtask": "codex"},
            )

        self.assertEqual(calls, 1)
        self.assertTrue(update["investigation_valid"])
        self.assertEqual(
            json.loads(update["investigation"])["title"],
            "artifact result",
        )
        attempt_log = (
            ws.log_path("review_log")
            / "vuln-013.iter-1.investigate_subtask.attempt-1.log"
        ).read_text()
        self.assertIn("output_source: artifact", attempt_log)
        self.assertIn("artifact_path:", attempt_log)

    def test_dsh_timeout_recovery_still_uses_structured_artifact_validation(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="dsh-timeout-artifact")

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
            **kwargs,
        ):
            del (
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                extra_context,
                timeout,
                kwargs,
            )
            sub_ws = ws_arg.prepare_sub_workspace(
                node=node,
                subtask_id=subtask_id,
                backend="dsh",
            )
            artifact = sub_ws / "finding.json"
            stdout = json.dumps(_valid_investigation("timeout artifact result"))
            artifact.write_text(stdout)
            return AgentResult(
                stdout=stdout,
                stderr="DSH timed out; recovering fresh finding.json",
                returncode=0,
                backend="dsh",
                cwd=str(sub_ws),
                metadata={
                    "timeout_recovered_from_artifact": True,
                    "timeout_seconds": 120,
                    "timeout_artifact_path": str(artifact),
                },
            ), []

        state = {
            **_workspace_state(ws),
            "subtask": {
                "id": "vuln-016",
                "bucket": "vuln",
                "objective": "recover timeout artifact",
            },
            "iteration": 0,
            "max_iterations": 3,
        }

        def fake_invoke_with_validation(*args, **kwargs):
            res, errors = fake_invoke(*args, **kwargs)
            validate = kwargs.get("validate")
            if validate:
                validate(res)
            return res, errors

        with patch("zeromdash.nodes.investigate_subtask._invoke_with_output_retry", fake_invoke_with_validation):
            result = nodes.investigate_subtask(
                state,
                backends={"investigate_subtask": "dsh"},
            )

        self.assertTrue(result["investigation_valid"])
        investigation = json.loads(result["investigation"])
        self.assertEqual(investigation["title"], "timeout artifact result")
        attempt_log = ws.log_path("review_log") / "vuln-016.investigation.log"
        self.assertTrue(attempt_log.is_file())

    def test_structured_stdout_takes_precedence_over_fresh_artifact(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="stdout-first")

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            del (
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                extra_context,
                timeout,
            )
            sub_ws = ws_arg.prepare_sub_workspace(
                node=node,
                subtask_id=subtask_id,
                backend="codex",
            )
            (sub_ws / "finding.json").write_text(
                json.dumps(_valid_investigation("artifact result"))
            )
            return AgentResult(
                stdout=json.dumps(_valid_investigation("stdout result")),
                stderr="",
                returncode=0,
                backend="codex",
                cwd=str(sub_ws),
            )

        state = {
            **_workspace_state(ws),
            "subtask": {
                "id": "vuln-014",
                "bucket": "vuln",
                "objective": "prefer stdout",
            },
            "iteration": 0,
            "max_iterations": 3,
        }

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.investigate_subtask(
                state,
                backends={"investigate_subtask": "codex"},
            )

        self.assertEqual(
            json.loads(update["investigation"])["title"],
            "stdout result",
        )
        attempt_log = (
            ws.log_path("review_log")
            / "vuln-014.iter-1.investigate_subtask.attempt-1.log"
        ).read_text()
        self.assertIn("output_source: stdout", attempt_log)
        self.assertNotIn("output_source: artifact", attempt_log)

    def test_stale_finding_artifact_is_not_reused(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="stale-artifact")
        sub_ws = ws.prepare_sub_workspace(
            node="investigate_subtask",
            subtask_id="vuln-015",
            backend="codex",
        )
        stale = sub_ws / "finding.json"
        stale.write_text(json.dumps(_valid_investigation("stale result")))
        calls = 0

        def fake_invoke(
            ws_arg,
            node,
            prompt,
            backends,
            agent_configs=None,
            agent_config_task_types=None,
            subtask_id=None,
            extra_context=None,
            timeout=None,
        ):
            nonlocal calls
            del (
                ws_arg,
                node,
                prompt,
                backends,
                agent_configs,
                agent_config_task_types,
                subtask_id,
                extra_context,
                timeout,
            )
            calls += 1
            self.assertFalse(stale.exists())
            return AgentResult(
                stdout="not json",
                stderr="",
                returncode=0,
                backend="codex",
                cwd=str(sub_ws),
            )

        state = {
            **_workspace_state(ws),
            "subtask": {
                "id": "vuln-015",
                "bucket": "vuln",
                "objective": "reject stale artifact",
            },
            "iteration": 0,
            "max_iterations": 3,
        }

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.investigate_subtask(
                state,
                backends={"investigate_subtask": "codex"},
            )

        self.assertEqual(calls, nodes.DEFAULT_NODE_OUTPUT_ATTEMPTS)
        self.assertFalse(update["investigation_valid"])
        self.assertFalse(stale.exists())
        attempt_log = (
            ws.log_path("review_log")
            / "vuln-015.iter-1.investigate_subtask.attempt-3.log"
        ).read_text()
        self.assertIn(
            "artifact_validation_failure: finding.json: not created by this attempt",
            attempt_log,
        )

    def test_selected_run_writes_attempt_and_command_logs_to_isolated_dir(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="selected-logs")
        selected_dir = ws.base / "selected-run"
        for subdir in ("attempts", "investigations", "critic_reviews", "results"):
            (selected_dir / subdir).mkdir(parents=True, exist_ok=True)
        canonical_command_log = ws.log / "agent_commands.jsonl"
        canonical_command_log.write_text('{"node":"canonical"}\n')

        class FakeAgent:
            def run(self, prompt, cwd=None, timeout=None, extra_args=None, env=None):
                del prompt, timeout, extra_args, env
                return AgentResult(
                    stdout=json.dumps(_valid_investigation("selected result")),
                    stderr="",
                    returncode=0,
                    backend="codex",
                    cwd=str(cwd),
                    metadata={"command": ["codex", "exec", "-"]},
                )

        state = {
            **_workspace_state(ws),
            "selected_subtask_log_dir": str(selected_dir),
            "subtask": {
                "id": "vuln-016",
                "bucket": "vuln",
                "objective": "verify isolated logs",
            },
            "iteration": 0,
            "max_iterations": 3,
            "agent_configs": {
                "investigate_subtask": {"runtime": "codex"},
            },
        }

        with patch.object(nodes, "_make_agent", return_value=FakeAgent()):
            update = nodes.investigate_subtask(
                state,
                backends={"investigate_subtask": "codex"},
            )

        self.assertTrue(update["investigation_valid"])
        self.assertEqual(
            canonical_command_log.read_text(),
            '{"node":"canonical"}\n',
        )
        selected_commands = (
            selected_dir / "agent_commands.jsonl"
        ).read_text()
        self.assertIn('"node": "investigate_subtask"', selected_commands)
        self.assertTrue(
            (
                selected_dir
                / "attempts"
                / "vuln-016.iter-1.investigate_subtask.attempt-1.log"
            ).is_file()
        )
        self.assertTrue(
            (
                selected_dir
                / "investigations"
                / "vuln-016.investigation.log"
            ).is_file()
        )
        self.assertFalse(
            (ws.log_path("review_log") / "vuln-016.investigation.log").exists()
        )

    def test_feedback_from_previous_review_is_included_in_prompt_and_logged(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="investigate")
        captured = {}

        def fake_invoke(
            ws_arg, node, prompt, backends, agent_configs=None, agent_config_task_types=None, subtask_id=None, extra_context=None, timeout=None
        ):
            captured.update(
                {
                    "ws": ws_arg,
                    "node": node,
                    "prompt": prompt,
                    "backends": backends,
                    "agent_configs": agent_configs,
                    "subtask_id": subtask_id,
                    "extra_context": extra_context,
                    "timeout": timeout,
                }
            )
            return AgentResult(
                stdout=json.dumps(
                    {
                        "title": "ok",
                        "detail": "validated detail",
                        "evidence": {
                            "code_locations": ["src/a.c:10"],
                            "call_path": ["entry -> sink"],
                        },
                    }
                ),
                stderr="",
                returncode=0,
                backend="codex",
            )

        state = {
            **_workspace_state(ws),
            "subtask": {"id": "patch-001", "bucket": "patch_miss", "objective": "re-check patch"},
            "iteration": 0,
            "max_iterations": 3,
            "review": {
                "verdict": "revise",
                "feedback": {
                    "gaps": ["missing call path"],
                    "requested_evidence": ["show sanitizer edge"],
                },
            },
        }

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.investigate_subtask(state, backends={"investigate_subtask": "codex"})

        self.assertEqual(update["iteration"], 1)
        self.assertEqual(json.loads(update["investigation"])["title"], "ok")
        self.assertEqual(update["errors"], [])
        self.assertEqual(captured["node"], "investigate_subtask")
        self.assertEqual(captured["subtask_id"], "patch-001")
        self.assertEqual(captured["extra_context"]["iteration"], 1)
        self.assertEqual(captured["extra_context"]["bucket"], "patch_miss")
        self.assertIn("Previous critic feedback", captured["prompt"])
        self.assertIn("missing call path", captured["prompt"])
        self.assertIn("show sanitizer edge", captured["prompt"])
        log_text = (ws.log_path("review_log") / "patch-001.investigation.log").read_text()
        self.assertIn("--- iteration 1 ---", log_text)

    def test_investigate_prompt_includes_upstream_context_and_threat_model(self):
        # The investigator must receive the attack-surface report, spec,
        # writeup/patch dirs, similar-software writeups, and the threat
        # model — so it frames its work top-down, not code-by-code only.
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="investigate-ctx")
        captured = {}

        def fake_invoke(
            ws_arg, node, prompt, backends, agent_configs=None, agent_config_task_types=None, subtask_id=None, extra_context=None, timeout=None
        ):
            captured["prompt"] = prompt
            return AgentResult(
                stdout=json.dumps(_valid_investigation()),
                stderr="",
                returncode=0,
                backend="codex",
            )

        attack_surface = str(ws.main_path("attack_surface") / "attack_surface.md")
        spec_doc = str(ws.main_path("spec") / "spec.md")
        state = {
            **_workspace_state(ws),
            "subtask": {"id": "spec-001", "bucket": "spec", "objective": "verify ID-register scheme"},
            "iteration": 0,
            "max_iterations": 3,
            "common_focus": "guest-to-host escape threat model",
            "attack_surface": attack_surface,
            "spec_doc": spec_doc,
            "similar_writeups": ["similar/peer/writeup", "similar/peer2/writeup"],
        }

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            nodes.investigate_subtask(state, backends={"investigate_subtask": "codex"})

        prompt = captured["prompt"]
        self.assertIn(attack_surface, prompt)
        self.assertIn(spec_doc, prompt)
        self.assertIn(str(ws.main_path("writeup")), prompt)
        self.assertIn(str(ws.main_path("patch")), prompt)
        self.assertIn("similar/peer/writeup", prompt)
        self.assertIn("similar/peer2/writeup", prompt)
        self.assertIn('Global focus: "guest-to-host escape threat model"', prompt)
        self.assertIn("Upstream context", prompt)
        self.assertIn("top-down", prompt)

    def test_investigate_prompt_includes_completeness_disciplines(self):
        # A no-finding that rests on a completeness claim ("every path to the
        # sink is safe", "sole consumer", "value clean at the sink") must be
        # justified via sink-anchored enumeration, sibling parity, and
        # sanitize liveness — not assumed from a gate on the reference path.
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="investigate-disc")
        captured = {}

        def fake_invoke(
            ws_arg, node, prompt, backends, agent_configs=None, agent_config_task_types=None, subtask_id=None, extra_context=None, timeout=None
        ):
            captured["prompt"] = prompt
            return AgentResult(
                stdout=json.dumps(_valid_investigation()),
                stderr="",
                returncode=0,
                backend="codex",
            )

        state = {
            **_workspace_state(ws),
            "subtask": {"id": "vuln-001", "bucket": "vuln", "objective": "probe sink invariant"},
            "iteration": 0,
            "max_iterations": 3,
        }

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            nodes.investigate_subtask(state, backends={"investigate_subtask": "codex"})

        prompt = captured["prompt"]
        self.assertIn("completeness claim", prompt)
        self.assertIn("Sink-anchored enumeration", prompt)
        self.assertIn("Sibling parity", prompt)
        self.assertIn("Sanitize liveness", prompt)
        self.assertIn("first-iteration no-finding", prompt)
        self.assertIn("plausible paths", prompt)


class GraphFanoutIsolationTest(unittest.TestCase):
    def test_fetch_failure_stops_workflow_before_search_nodes(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        counts = {"search_spec": 0, "summary": 0}

        def fetch(state, *, backends=None):
            del backends
            return {
                "repo_path": f"{state['workspace_root']}/{state['task_id']}/main/repo",
                "errors": ["[fetch_target_repo] materialized repo is empty after attempt 3/3"],
            }

        def search_spec(state, *, backends=None):
            del state, backends
            counts["search_spec"] += 1
            return {"errors": []}

        def summary(state, *, backends=None):
            del state, backends
            counts["summary"] += 1
            return {"summary": "should not run"}

        with patch.object(graph_mod.nodes, "fetch_target_repo", side_effect=fetch), patch.object(
            graph_mod.nodes, "search_spec", side_effect=search_spec
        ), patch.object(graph_mod.nodes, "summary", side_effect=summary):
            final = graph_mod.run(target="libfoo", workspace_root=tmp.name)

        self.assertEqual(final["errors"], ["[fetch_target_repo] materialized repo is empty after attempt 3/3"])
        self.assertNotIn("summary", final)
        self.assertEqual(counts["search_spec"], 0)
        self.assertEqual(counts["summary"], 0)

    def test_graph_fans_out_similar_history_before_attack_surface_barrier(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        seen_similars: list[str] = []
        analyze_inputs = {}
        counts = {"analyze": 0, "summary": 0}

        def fetch(state, *, backends=None):
            del backends
            return {"repo_path": f"{state['workspace_root']}/{state['task_id']}/main/repo", "errors": []}

        def empty(*args, **kwargs):
            del args, kwargs
            return {"errors": []}

        def search_similar_software(state, *, backends=None):
            del state, backends
            return {"similar_repos": ["Peer One", "Peer Two"], "errors": []}

        def search_similar_history(state, *, backends=None):
            del backends
            sw = state["similar_software"]
            seen_similars.append(sw)
            return {
                "similar_writeups": [f"similar/{sw}/writeup"],
                "similar_patches": [f"similar/{sw}/patch"],
                "errors": [],
            }

        def analyze(state, *, backends=None):
            del backends
            counts["analyze"] += 1
            analyze_inputs["similar_writeups"] = state.get("similar_writeups", [])
            analyze_inputs["similar_patches"] = state.get("similar_patches", [])
            return {"attack_surface": "surface", "errors": []}

        def plan_spec(state, *, backends=None):
            del state, backends
            return {"spec_subtasks": [], "errors": []}

        def plan_vuln(state, *, backends=None):
            del state, backends
            return {"vuln_subtasks": [], "errors": []}

        def plan_patch(state, *, backends=None):
            del state, backends
            return {"patch_subtasks": [], "errors": []}

        def plan_feature(state, *, backends=None):
            del state, backends
            return {"feature_subtasks": [], "errors": []}

        def summary(state, *, backends=None):
            del state, backends
            counts["summary"] += 1
            return {"summary": "done"}

        with patch.object(graph_mod.nodes, "fetch_target_repo", side_effect=fetch), patch.object(
            graph_mod.nodes, "search_spec", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_fuzz_driver", side_effect=empty), patch.object(
            graph_mod.nodes, "search_similar_software", side_effect=search_similar_software
        ), patch.object(graph_mod.nodes, "search_similar_history", side_effect=search_similar_history), patch.object(
            graph_mod.nodes, "search_target_history", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_new_feature", side_effect=empty
        ), patch.object(graph_mod.nodes, "analyze_attack_surface", side_effect=analyze), patch.object(
            graph_mod.nodes, "plan_by_spec", side_effect=plan_spec
        ), patch.object(graph_mod.nodes, "plan_by_vuln_similar", side_effect=plan_vuln), patch.object(
            graph_mod.nodes, "plan_by_vuln_patch", side_effect=plan_patch
        ), patch.object(graph_mod.nodes, "plan_by_new_feature", side_effect=plan_feature
        ), patch.object(graph_mod.nodes, "summary", side_effect=summary):
            final = graph_mod.run(target="libfoo", workspace_root=tmp.name)

        self.assertEqual(final["summary"], "done")
        self.assertCountEqual(seen_similars, ["Peer One", "Peer Two"])
        self.assertEqual(counts["analyze"], 1)
        self.assertEqual(counts["summary"], 1)
        self.assertCountEqual(
            analyze_inputs["similar_writeups"],
            ["similar/Peer One/writeup", "similar/Peer Two/writeup"],
        )
        self.assertCountEqual(
            analyze_inputs["similar_patches"],
            ["similar/Peer One/patch", "similar/Peer Two/patch"],
        )

    def test_parallel_subtasks_do_not_concurrently_merge_scratch_state(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)

        def fetch(state, *, backends=None):
            del backends
            return {"repo_path": f"{state['workspace_root']}/{state['task_id']}/main/repo"}

        def empty(*args, **kwargs):
            del args, kwargs
            return {"errors": []}

        def plan_two(state, *, backends=None):
            del state, backends
            return {
                "spec_subtasks": [
                    {"id": "spec-001", "bucket": "spec", "objective": "one", "hints": {}},
                    {"id": "spec-002", "bucket": "spec", "objective": "two", "hints": {}},
                ],
                "errors": [],
            }

        def plan_no_vuln(state, *, backends=None):
            del state, backends
            return {"vuln_subtasks": [], "errors": []}

        def plan_no_patch(state, *, backends=None):
            del state, backends
            return {"patch_subtasks": [], "errors": []}

        def plan_no_feature(state, *, backends=None):
            del state, backends
            return {"feature_subtasks": [], "errors": []}

        def investigate(state, *, backends=None):
            del backends
            iteration = int(state.get("iteration", 0)) + 1
            return {
                "iteration": iteration,
                "investigation": json.dumps(
                    _valid_investigation(state["subtask"]["id"])
                ),
            }

        def critic(state, *, backends=None):
            del backends
            return {"review": _qualified_review(), "review_history": []}

        def summary(state, *, backends=None):
            del backends
            return {"summary": f"findings={len(state.get('spec_findings', []))}"}

        with patch.object(graph_mod.nodes, "fetch_target_repo", side_effect=fetch), patch.object(
            graph_mod.nodes, "search_spec", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_fuzz_driver", side_effect=empty), patch.object(
            graph_mod.nodes, "search_similar_software", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_similar_history", side_effect=empty), patch.object(
            graph_mod.nodes, "search_target_history", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_new_feature", side_effect=empty
        ), patch.object(graph_mod.nodes, "analyze_attack_surface", side_effect=empty), patch.object(
            graph_mod.nodes, "plan_by_spec", side_effect=plan_two
        ), patch.object(graph_mod.nodes, "plan_by_vuln_similar", side_effect=plan_no_vuln), patch.object(
            graph_mod.nodes, "plan_by_vuln_patch", side_effect=plan_no_patch
        ), patch.object(graph_mod.nodes, "plan_by_new_feature", side_effect=plan_no_feature
        ), patch.object(graph_mod.nodes, "investigate_subtask", side_effect=investigate), patch.object(
            graph_mod.nodes, "critic_subtask", side_effect=critic
        ), patch.object(graph_mod.nodes, "summary", side_effect=summary):
            final = graph_mod.run(target="libfoo", workspace_root=tmp.name)

        self.assertEqual(final["summary"], "findings=2")
        for scratch_key in ("subtask", "iteration", "investigation", "review", "review_history"):
            self.assertNotIn(scratch_key, final)

    def test_subtask_graph_input_schema_preserves_agent_config(self):
        captured = {}

        def investigate(state, *, backends=None):
            del backends
            captured["agent_configs"] = state.get("agent_configs")
            captured["agent_config_task_types"] = state.get("agent_config_task_types")
            return {"iteration": 1, "investigation": json.dumps({"title": "ok"})}

        def critic(state, *, backends=None):
            del state, backends
            return {"review": {"verdict": "reject", "confidence": 0.0}, "review_history": []}

        def finalize(state, *, backends=None):
            del state, backends
            return {}

        agent_configs = {
            "investigate_subtask": {
                "runtime": "codex",
                "config": "foundry",
                "model": "gpt-5.5",
            }
        }
        agent_config_task_types = {"investigate_subtask": "legacy-type"}

        with patch.object(graph_mod.nodes, "investigate_subtask", side_effect=investigate), patch.object(
            graph_mod.nodes, "critic_subtask", side_effect=critic
        ), patch.object(graph_mod.nodes, "finalize_subtask", side_effect=finalize):
            subgraph = graph_mod.build_subtask_graph()
            subgraph.invoke(
                {
                    "task_id": "task-1",
                    "workspace_root": "/tmp/ws",
                    "target": "libfoo",
                    "repo_path": "/tmp/ws/main/repo",
                    "subtask": {"id": "vuln-006", "bucket": "vuln", "objective": "probe", "hints": {}},
                    "iteration": 0,
                    "max_iterations": 3,
                    "min_critic_skills": 2,
                    "agent_configs": agent_configs,
                    "agent_config_task_types": agent_config_task_types,
                    "review_history": [],
                }
            )

        self.assertEqual(captured["agent_configs"], agent_configs)
        self.assertEqual(captured["agent_config_task_types"], agent_config_task_types)

    def test_subtask_graph_passes_codex_config_to_investigator_agent_run(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="subtask-config")
        captured = {}

        class FakeAgent:
            def run(self, prompt, cwd=None, timeout=None, extra_args=None, env=None):
                captured.update(
                    {
                        "prompt": prompt,
                        "cwd": cwd,
                        "timeout": timeout,
                        "extra_args": extra_args,
                        "env": env,
                    }
                )
                return AgentResult(
                    stdout=json.dumps(_valid_investigation()),
                    stderr="",
                    returncode=0,
                    backend="codex",
                    cwd=str(cwd),
                )

        def critic(state, *, backends=None):
            del state, backends
            return {"review": {"verdict": "reject", "confidence": 0.0}, "review_history": []}

        agent_configs = {
            "investigate_subtask": {
                "runtime": "codex_cli",
                "config": "foundry",
                "model": "gpt-5.5",
            }
        }

        with patch.dict("os.environ", {"ZEROMDASH_CODEX_MODEL": "global-default"}, clear=True), patch.object(
            nodes, "_make_agent", return_value=FakeAgent()
        ) as make_agent, patch.object(graph_mod.nodes, "critic_subtask", side_effect=critic):
            subgraph = graph_mod.build_subtask_graph()
            subgraph.invoke(
                {
                    "task_id": ws.task_id,
                    "workspace_root": str(ws.root),
                    "target": "libfoo",
                    "repo_path": str(ws.main_path("repo")),
                    "subtask": {"id": "vuln-010", "bucket": "vuln", "objective": "probe", "hints": {}},
                    "iteration": 0,
                    "max_iterations": 3,
                    "min_critic_skills": 2,
                    "agent_configs": agent_configs,
                    "agent_config_task_types": {},
                    "review_history": [],
                }
            )

        make_agent.assert_called_once_with("codex")
        self.assertEqual(
            captured["extra_args"],
            ["--enable", "multi_agent", "--profile", "foundry", "--model", "gpt-5.5"],
        )
        self.assertEqual(captured["env"], {"ZEROMDASH_CODEX_MODEL": None})
        self.assertIsNone(captured["timeout"])
        self.assertIn("vuln-010", captured["prompt"])
        self.assertIn("node_investigate_subtask", str(captured["cwd"]))

    def test_zero_subtasks_still_runs_summary_once(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        counts = {"summary": 0, "polish": 0}

        def fetch(state, *, backends=None):
            del backends
            return {"repo_path": f"{state['workspace_root']}/{state['task_id']}/main/repo"}

        def empty(*args, **kwargs):
            del args, kwargs
            return {"errors": []}

        def analyze(state, *, backends=None):
            del state, backends
            return {"attack_surface": "surface", "errors": []}

        def plan_spec(state, *, backends=None):
            del state, backends
            return {"spec_subtasks": [], "errors": []}

        def plan_vuln(state, *, backends=None):
            del state, backends
            return {"vuln_subtasks": [], "errors": []}

        def plan_patch(state, *, backends=None):
            del state, backends
            return {"patch_subtasks": [], "errors": []}

        def summary(state, *, backends=None):
            del state, backends
            counts["summary"] += 1
            return {"summary": "no findings"}

        def polish_report(state, *, backends=None):
            del backends
            counts["polish"] += 1
            return {"summary": state.get("summary", "")}

        with patch.object(graph_mod.nodes, "fetch_target_repo", side_effect=fetch), patch.object(
            graph_mod.nodes, "search_spec", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_fuzz_driver", side_effect=empty), patch.object(
            graph_mod.nodes, "search_similar_software", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_similar_history", side_effect=empty), patch.object(
            graph_mod.nodes, "search_target_history", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_new_feature", side_effect=empty
        ), patch.object(graph_mod.nodes, "analyze_attack_surface", side_effect=analyze), patch.object(
            graph_mod.nodes, "plan_by_spec", side_effect=plan_spec
        ), patch.object(graph_mod.nodes, "plan_by_vuln_similar", side_effect=plan_vuln), patch.object(
            graph_mod.nodes, "plan_by_vuln_patch", side_effect=plan_patch
        ), patch.object(graph_mod.nodes, "plan_by_new_feature", side_effect=empty
        ), patch.object(graph_mod.nodes, "summary", side_effect=summary), patch.object(
            graph_mod.nodes, "polish_report", side_effect=polish_report
        ):
            final = graph_mod.run(target="libfoo", workspace_root=tmp.name)

        self.assertEqual(final["summary"], "no findings")
        self.assertEqual(counts["summary"], 1)
        self.assertEqual(counts["polish"], 1)

    def test_run_persists_role_lang_in_workspace_metadata(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)

        def fetch(state, *, backends=None):
            del backends
            return {"repo_path": f"{state['workspace_root']}/{state['task_id']}/main/repo", "errors": ["stop"]}

        with patch.object(graph_mod.nodes, "fetch_target_repo", side_effect=fetch):
            final = graph_mod.run(target="libfoo", workspace_root=tmp.name, role_lang="zh_CN")

        self.assertEqual(final["role_lang"], "zh_CN")
        meta = json.loads((Path(tmp.name) / final["task_id"] / "workspace.json").read_text())
        self.assertEqual(meta["role_lang"], "zh_CN")

    def test_disable_spec_skips_search_spec_and_plan_by_spec_nodes(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        seen = {"search_spec": 0, "plan_by_spec": 0, "analyze": 0, "summary": 0}

        def fetch(state, *, backends=None):
            del backends
            return {"repo_path": f"{state['workspace_root']}/{state['task_id']}/main/repo", "errors": []}

        def empty(*args, **kwargs):
            del args, kwargs
            return {"errors": []}

        def search_spec(state, *, backends=None):
            del state, backends
            seen["search_spec"] += 1
            return {"errors": []}

        def plan_spec(state, *, backends=None):
            del state, backends
            seen["plan_by_spec"] += 1
            return {"spec_subtasks": [], "errors": []}

        def analyze(state, *, backends=None):
            del state, backends
            seen["analyze"] += 1
            return {"attack_surface": "surface", "errors": []}

        def summary(state, *, backends=None):
            del state, backends
            seen["summary"] += 1
            return {"summary": "done"}

        with patch.object(graph_mod.nodes, "fetch_target_repo", side_effect=fetch), patch.object(
            graph_mod.nodes, "search_spec", side_effect=search_spec
        ), patch.object(graph_mod.nodes, "search_fuzz_driver", side_effect=empty), patch.object(
            graph_mod.nodes, "search_similar_software", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_similar_history", side_effect=empty), patch.object(
            graph_mod.nodes, "search_target_history", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_new_feature", side_effect=empty
        ), patch.object(graph_mod.nodes, "analyze_attack_surface", side_effect=analyze), patch.object(
            graph_mod.nodes, "plan_by_spec", side_effect=plan_spec
        ), patch.object(graph_mod.nodes, "plan_by_vuln_similar", side_effect=empty), patch.object(
            graph_mod.nodes, "plan_by_vuln_patch", side_effect=empty
        ), patch.object(graph_mod.nodes, "plan_by_new_feature", side_effect=empty
        ), patch.object(graph_mod.nodes, "summary", side_effect=summary):
            final = graph_mod.run(
                target="libfoo",
                workspace_root=tmp.name,
                top_K={"spec": 99},
                disabled_nodes={"search_spec", "plan_by_spec"},
            )

        self.assertEqual(seen["search_spec"], 0)
        self.assertEqual(seen["plan_by_spec"], 0)
        self.assertEqual(seen["analyze"], 1)
        self.assertEqual(seen["summary"], 1)
        self.assertEqual(final["summary"], "done")

    def test_disable_target_history_skips_search_target_history_and_patch_planner(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        seen = {"search_target_history": 0, "plan_by_vuln_patch": 0, "analyze": 0, "summary": 0}

        def fetch(state, *, backends=None):
            del backends
            return {"repo_path": f"{state['workspace_root']}/{state['task_id']}/main/repo", "errors": []}

        def empty(*args, **kwargs):
            del args, kwargs
            return {"errors": []}

        def search_target_history(state, *, backends=None):
            del state, backends
            seen["search_target_history"] += 1
            return {"target_writeups": ["should-not-run"], "target_patches": ["should-not-run"], "errors": []}

        def plan_patch(state, *, backends=None):
            del state, backends
            seen["plan_by_vuln_patch"] += 1
            return {"patch_subtasks": [{"id": "patch-001", "bucket": "patch_miss"}], "errors": []}

        def analyze(state, *, backends=None):
            del state, backends
            seen["analyze"] += 1
            return {"attack_surface": "surface", "errors": []}

        def plan_no_spec(state, *, backends=None):
            del state, backends
            return {"spec_subtasks": [], "errors": []}

        def plan_no_vuln(state, *, backends=None):
            del state, backends
            return {"vuln_subtasks": [], "errors": []}

        def summary(state, *, backends=None):
            del state, backends
            seen["summary"] += 1
            return {"summary": "done"}

        with patch.object(graph_mod.nodes, "fetch_target_repo", side_effect=fetch), patch.object(
            graph_mod.nodes, "search_spec", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_fuzz_driver", side_effect=empty), patch.object(
            graph_mod.nodes, "search_similar_software", side_effect=empty
        ), patch.object(graph_mod.nodes, "search_similar_history", side_effect=empty), patch.object(
            graph_mod.nodes, "search_target_history", side_effect=search_target_history
        ), patch.object(graph_mod.nodes, "search_new_feature", side_effect=empty
        ), patch.object(graph_mod.nodes, "analyze_attack_surface", side_effect=analyze), patch.object(
            graph_mod.nodes, "plan_by_spec", side_effect=plan_no_spec
        ), patch.object(graph_mod.nodes, "plan_by_vuln_similar", side_effect=plan_no_vuln), patch.object(
            graph_mod.nodes, "plan_by_vuln_patch", side_effect=plan_patch
        ), patch.object(graph_mod.nodes, "plan_by_new_feature", side_effect=empty
        ), patch.object(graph_mod.nodes, "summary", side_effect=summary):
            final = graph_mod.run(
                target="libfoo",
                workspace_root=tmp.name,
                disabled_nodes={"search_target_history", "plan_by_vuln_patch"},
            )

        self.assertEqual(seen["search_target_history"], 0)
        self.assertEqual(seen["plan_by_vuln_patch"], 0)
        self.assertEqual(seen["analyze"], 1)
        self.assertEqual(seen["summary"], 1)
        self.assertEqual(final["summary"], "done")


if __name__ == "__main__":
    unittest.main()
