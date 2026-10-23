"""Unit tests for planner nodes in zeromdash.nodes."""

from __future__ import annotations

import json
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from zeromdash import nodes
from zeromdash.agents import AgentResult
from zeromdash.workspace import Workspace


def _state_for_workspace(ws: Workspace) -> dict:
    return {
        "target": "libfoo",
        "task_id": ws.task_id,
        "workspace_root": str(ws.root),
        "repo_path": str(ws.main_path("repo")),
        "attack_surface": str(ws.main_path("attack_surface") / "attack_surface.md"),
        "spec_doc": str(ws.main_path("spec") / "spec.md"),
    }


class NormalizeSubtasksTest(unittest.TestCase):
    def test_normalizes_valid_items_and_skips_non_dict_items(self):
        subtasks = nodes._normalize_subtasks(
            [
                {"id": "given-id", "objective": "check clause", "hints": {"line": 7}},
                "not-a-dict",
                {"objective": "missing id", "hints": None},
            ],
            bucket="spec",
            prefix="spec",
        )

        self.assertEqual(len(subtasks), 2)
        self.assertEqual(subtasks[0]["id"], "given-id")
        self.assertEqual(subtasks[0]["bucket"], "spec")
        self.assertEqual(subtasks[0]["objective"], "check clause")
        self.assertEqual(subtasks[0]["hints"]["line"], 7)
        self.assertIn("priority_reason", subtasks[0]["hints"])

        self.assertRegex(subtasks[1]["id"], r"^spec-002-[0-9a-f]{6}$")
        self.assertEqual(subtasks[1]["bucket"], "spec")
        self.assertEqual(subtasks[1]["objective"], "missing id")
        self.assertIn("priority_reason", subtasks[1]["hints"])

    def test_stringifies_objective_when_missing_or_non_string(self):
        subtasks = nodes._normalize_subtasks(
            [{"id": "x", "objective": 123, "hints": {}}],
            bucket="vuln",
            prefix="vuln",
        )

        self.assertEqual(subtasks[0]["objective"], "123")

    def test_diff_scope_adds_attribution_hints_without_fencing_context(self):
        subtasks = nodes._normalize_subtasks(
            [
                {
                    "id": "vuln-001",
                    "objective": "trace changed parser to old sink",
                    "hints": {
                        "candidate_code_locations": [
                            "src/parser.c:12",
                            "src/common.c:88",
                        ]
                    },
                }
            ],
            bucket="vuln",
            prefix="vuln",
        )

        scoped = nodes._apply_scan_scope_to_subtasks(
            subtasks,
            {
                "scan_scope": {
                    "mode": "diff",
                    "changed_files": ["src/parser.c"],
                }
            },
        )

        hints = scoped[0]["hints"]
        self.assertEqual(hints["changed_locations"], ["src/parser.c:12"])
        self.assertEqual(hints["context_locations"], ["src/common.c:88"])
        self.assertTrue(hints["blocking_eligible"])
        self.assertEqual(hints["scope_relation"], "unknown")

    def test_diff_scope_normalizes_workspace_repo_prefixes(self):
        subtasks = nodes._normalize_subtasks(
            [
                {
                    "id": "vuln-001",
                    "objective": "trace changed parser",
                    "hints": {
                        "candidate_code_locations": [
                            "main/repo/source/parser.c:12",
                            "/tmp/ws/main/repo/source/helper.c:88",
                        ]
                    },
                }
            ],
            bucket="vuln",
            prefix="vuln",
        )
        state = {
            "repo_path": "/tmp/ws/main/repo",
            "scan_scope": {
                "mode": "diff",
                "repo_path": "/tmp/ws/main/repo",
                "changed_files": ["source/parser.c", "source/helper.c"],
            },
        }

        scoped = nodes._apply_scan_scope_to_subtasks(subtasks, state)

        self.assertEqual(
            scoped[0]["hints"]["changed_locations"],
            [
                "main/repo/source/parser.c:12",
                "/tmp/ws/main/repo/source/helper.c:88",
            ],
        )
        self.assertTrue(scoped[0]["hints"]["blocking_eligible"])

    def test_domain_ref_validator_rejects_unknown_ids_and_non_array_collections(self):
        registry = {
            "schema_version": "1.0",
            "status": "complete",
            "entities": [{"entity_id": "entity:known", "kind": "state", "name": "Known", "source_locations": []}],
            "representations": [],
            "invariants": [],
            "transitions": [],
            "seams": [],
        }
        unknown = nodes._normalize_subtasks(
            [{"id": "spec-001", "objective": "probe", "hints": {"domain_refs": {"entity_ids": ["entity:missing"]}}}],
            bucket="spec",
            prefix="spec",
        )
        ok, detail = nodes._validate_domain_refs(unknown, {"domain_registry": registry})
        self.assertFalse(ok)
        self.assertIn("entity:missing", detail)

        invalid_shape = nodes._normalize_subtasks(
            [{"id": "spec-002", "objective": "probe", "hints": {"domain_refs": {"entity_ids": "entity:known"}}}],
            bucket="spec",
            prefix="spec",
        )
        ok, detail = nodes._validate_domain_refs(invalid_shape, {"domain_registry": registry})
        self.assertFalse(ok)
        self.assertIn("must be arrays", detail)

        missing = nodes._normalize_subtasks(
            [{"id": "spec-003", "objective": "probe", "hints": {}}],
            bucket="spec",
            prefix="spec",
        )
        ok, detail = nodes._validate_domain_refs(missing, {"domain_registry": registry})
        self.assertFalse(ok)
        self.assertIn("domain_refs is required", detail)

    def test_registry_aware_plans_require_complete_hypothesis_packages(self):
        registry = {
            "schema_version": "1.0",
            "status": "complete",
            "entities": [],
            "representations": [],
            "invariants": [],
            "transitions": [],
            "seams": [],
        }
        legacy = nodes._normalize_subtasks(
            [{"id": "spec-001", "objective": "probe", "hints": {"domain_refs": {}}}],
            bucket="spec",
            prefix="spec",
        )
        ok, detail = nodes._validate_hypothesis_packages(legacy, {"domain_registry": registry})
        self.assertFalse(ok)
        self.assertIn("coverage_obligations", detail)

        packaged = nodes._normalize_subtasks(
            [
                {
                    "id": "spec-001",
                    "objective": "probe both paths",
                    "hints": {"domain_refs": {}},
                    "coverage_obligations": [
                        {"obligation_id": "spec-001:obl-01", "statement": "check path A"},
                        {"obligation_id": "spec-001:obl-02", "statement": "check path B"},
                    ],
                    "seed_hypotheses": [
                        {"hypothesis_id": "spec-001:hyp-01", "statement": "path A bypasses the guard", "obligation_ids": ["spec-001:obl-01"]},
                        {"hypothesis_id": "spec-001:hyp-02", "statement": "path B bypasses the guard", "obligation_ids": ["spec-001:obl-02"]},
                    ],
                }
            ],
            bucket="spec",
            prefix="spec",
        )
        ok, detail = nodes._validate_hypothesis_packages(packaged, {"domain_registry": registry})
        self.assertTrue(ok, detail)
        self.assertEqual(len(packaged[0]["seed_hypotheses"]), 2)

    def test_legacy_registry_allows_old_single_outcome_plan(self):
        subtasks = nodes._normalize_subtasks(
            [{"id": "spec-001", "objective": "legacy probe", "hints": {}}],
            bucket="spec",
            prefix="spec",
        )
        ok, detail = nodes._validate_hypothesis_packages(
            subtasks,
            {"target": "legacy"},
        )
        self.assertTrue(ok, detail)


class PlannerNodesTest(unittest.TestCase):
    def _run_planner(self, planner, stdout: str, state_overrides: dict | None = None) -> tuple[dict, Workspace, str]:
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="planner")
        result = AgentResult(stdout=stdout, stderr="", returncode=0, backend="codex")
        captured_prompt = ""

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
            nonlocal captured_prompt
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
            captured_prompt = prompt
            return result

        state = {**_state_for_workspace(ws), **(state_overrides or {})}
        with patch.object(nodes, "_invoke", side_effect=fake_invoke) as invoke:
            update = planner(state, backends={"any": "override"})

        invoke.assert_called_once()
        return update, ws, captured_prompt

    def test_plan_by_spec_returns_spec_subtasks_and_writes_log(self):
        update, ws, _ = self._run_planner(
            nodes.plan_by_spec,
            json.dumps([
                {
                    "id": "spec-001",
                    "objective": "verify RFC clause",
                    "hints": {"spec": "1.2", "priority_reason": "matches focus and reachable parser"},
                }
            ]),
        )

        self.assertEqual(update["errors"], [])
        self.assertEqual(len(update["spec_subtasks"]), 1)
        self.assertEqual(update["spec_subtasks"][0]["bucket"], "spec")
        self.assertEqual(update["spec_subtasks"][0]["objective"], "verify RFC clause")
        self.assertEqual(update["spec_subtasks"][0]["hints"]["priority_reason"], "matches focus and reachable parser")
        self.assertTrue(ws.state_path("plan_by_spec.json").is_file())

    def test_plan_by_vuln_similar_returns_vuln_subtasks_and_writes_log(self):
        update, ws, _ = self._run_planner(
            nodes.plan_by_vuln_similar,
            json.dumps([
                {
                    "id": "vuln-001",
                    "objective": "probe CVE analogue",
                    "hints": {"cve": "CVE-1", "priority_reason": "focus match and reachable analogue path"},
                }
            ]),
        )

        self.assertEqual(update["errors"], [])
        self.assertEqual(len(update["vuln_subtasks"]), 1)
        self.assertEqual(update["vuln_subtasks"][0]["bucket"], "vuln")
        self.assertEqual(update["vuln_subtasks"][0]["hints"]["cve"], "CVE-1")
        self.assertEqual(update["vuln_subtasks"][0]["hints"]["priority_reason"], "focus match and reachable analogue path")
        self.assertTrue(ws.state_path("plan_by_vuln.json").is_file())

    def test_planner_accepts_subworkspace_plan_json_when_stdout_is_prose(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="planner-file-fallback")
        plan = [
            {
                "id": "vuln-001",
                "objective": "probe CVE analogue",
                "hints": {
                    "cve": "CVE-1",
                    "priority_reason": "focus match and reachable analogue path",
                },
            }
        ]

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
                subtask_id,
                extra_context,
                timeout,
            )
            sub_ws = ws_arg.sub_workspace_root / f"node_{node}"
            sub_ws.mkdir(parents=True, exist_ok=True)
            (sub_ws / "plan.json").write_text(json.dumps(plan))
            return AgentResult(
                stdout="The plan is persisted at ./plan.json.\n\n## Summary\nDone.",
                stderr="",
                returncode=0,
                backend="claude_code",
                cwd=str(sub_ws),
            )

        with patch.object(nodes, "_invoke", side_effect=fake_invoke) as invoke:
            update = nodes.plan_by_vuln_similar(
                _state_for_workspace(ws),
                backends={"plan_by_vuln_similar": "claude_code"},
            )

        invoke.assert_called_once()
        self.assertEqual(update["errors"], [])
        self.assertEqual(len(update["vuln_subtasks"]), 1)
        self.assertEqual(update["vuln_subtasks"][0]["bucket"], "vuln")
        self.assertEqual(update["vuln_subtasks"][0]["hints"]["cve"], "CVE-1")
        self.assertEqual(
            json.loads(ws.state_path("plan_by_vuln.json").read_text())[0]["id"],
            "vuln-001",
        )

    def test_planner_returns_canonical_artifact_when_stdout_is_status_receipt(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="planner-artifact-state")
        out = ws.state_path("plan_by_spec.json")
        plan = [
            {
                "id": "spec-001",
                "objective": "verify the persisted plan",
                "hints": {
                    "priority_reason": "canonical artifact covers the target",
                    "domain_refs": {},
                },
                "coverage_obligations": [
                    {
                        "obligation_id": "spec-001:obl-01",
                        "statement": "cover the first persisted package",
                    }
                ],
                "seed_hypotheses": [
                    {
                        "hypothesis_id": "spec-001:hyp-01",
                        "statement": "the first persisted package may fail",
                        "obligation_ids": ["spec-001:obl-01"],
                    }
                ],
            },
            {
                "id": "spec-002",
                "objective": "verify the second persisted package",
                "hints": {
                    "priority_reason": "canonical artifact has two packages",
                    "domain_refs": {},
                },
                "coverage_obligations": [
                    {
                        "obligation_id": "spec-002:obl-01",
                        "statement": "cover the second persisted package",
                    }
                ],
                "seed_hypotheses": [
                    {
                        "hypothesis_id": "spec-002:hyp-01",
                        "statement": "the second persisted package may fail",
                        "obligation_ids": ["spec-002:obl-01"],
                    }
                ],
            },
        ]
        domain_registry = {
            "schema_version": "1.0",
            "status": "complete",
            "entities": [],
            "representations": [],
            "invariants": [],
            "transitions": [],
            "seams": [],
        }

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
            out.write_text(json.dumps(plan))
            return AgentResult(
                stdout=json.dumps(
                    [
                        {
                            "status": "ok",
                            "artifact": str(out),
                            "subtasks": 2,
                            "validation": "schema ok",
                        }
                    ]
                ),
                stderr="",
                returncode=0,
                backend="traex",
            )

        with patch.object(nodes, "_invoke", side_effect=fake_invoke) as invoke:
            update = nodes.plan_by_spec(
                {**_state_for_workspace(ws), "domain_registry": domain_registry},
                backends={"plan_by_spec": "traex"},
            )

        invoke.assert_called_once()
        persisted = json.loads(out.read_text())
        self.assertEqual(update["errors"], [])
        self.assertEqual(update["spec_subtasks"], persisted)
        self.assertEqual(
            [item["id"] for item in update["spec_subtasks"]],
            ["spec-001", "spec-002"],
        )
        self.assertNotIn("status", update["spec_subtasks"][0])

    def test_planner_rejects_status_receipt_without_artifact(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="planner-receipt-only")
        attempts = []

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
            return AgentResult(
                stdout=json.dumps(
                    [{"status": "ok", "subtasks": 30, "validation": "schema ok"}]
                ),
                stderr="",
                returncode=0,
                backend="traex",
            )

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.plan_by_spec(
                _state_for_workspace(ws),
                backends={"plan_by_spec": "traex"},
            )

        self.assertEqual(attempts, [1, 2, 3])
        self.assertEqual(update["spec_subtasks"], [])
        self.assertEqual(json.loads(ws.state_path("plan_by_spec.json").read_text()), [])
        self.assertIn("output empty after attempt 3/3", update["errors"][0])

    def test_output_retry_falls_back_only_after_attempts_exhausted(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="planner-runtime-fallback")
        out = ws.state_path("plan_by_vuln.json")
        calls = []
        plan = [
            {
                "id": "vuln-001",
                "objective": "probe fallback analogue",
                "hints": {"priority_reason": "focus match and reachable analogue path"},
            }
        ]

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
            del ws_arg, prompt, agent_config_task_types, subtask_id, timeout
            backend = backends[node]
            calls.append((backend, extra_context["attempt"], agent_configs[node].get("config")))
            if backend == "codex":
                return AgentResult(stdout="", stderr="blocked", returncode=1, backend="codex")
            return AgentResult(stdout=json.dumps(plan), stderr="", returncode=0, backend="claude_code")

        state = {
            **_state_for_workspace(ws),
            "agent_configs": {
                "plan_by_vuln_similar": {
                    "runtime": "codex",
                    "config": "primary",
                    "fallbacks": [
                        {"runtime": "claude_code", "config": "/tmp/fallback-settings.json"}
                    ],
                }
            },
        }

        subtasks = []

        def materialize(res):
            nonlocal subtasks
            subtasks = nodes._normalize_subtasks(json.loads(res.stdout), "vuln", "vuln")
            out.write_text(json.dumps(subtasks))

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            res, errors = nodes._invoke_with_output_retry(
                ws,
                "plan_by_vuln_similar",
                "prompt",
                {},
                state,
                output_desc=str(out),
                reset=lambda: out.unlink() if out.exists() else None,
                materialize=materialize,
                validate=lambda _res: out.is_file(),
                attempts=2,
            )

        self.assertEqual(errors, [])
        self.assertTrue(res.ok)
        self.assertEqual(
            calls,
            [
                ("codex", 1, "primary"),
                ("codex", 2, "primary"),
                ("claude_code", 1, "/tmp/fallback-settings.json"),
            ],
        )
        self.assertEqual(json.loads(out.read_text())[0]["bucket"], "vuln")
        self.assertTrue((ws.log_path("review_log") / "plan_by_vuln_similar.attempt-3.log").is_file())

    def test_plan_by_vuln_patch_returns_patch_miss_subtasks_and_writes_log(self):
        update, ws, prompt = self._run_planner(
            nodes.plan_by_vuln_patch,
            json.dumps([
                {
                    "id": "patch-001",
                    "objective": "verify missing backport",
                    "hints": {
                        "type": "missing",
                        "patch_commit": "abc123",
                        "priority_reason": "host escape focus and reachable fixed path",
                    },
                }
            ]),
        )

        self.assertEqual(update["errors"], [])
        self.assertEqual(len(update["patch_subtasks"]), 1)
        self.assertEqual(update["patch_subtasks"][0]["bucket"], "patch_miss")
        self.assertEqual(update["patch_subtasks"][0]["objective"], "verify missing backport")
        self.assertEqual(update["patch_subtasks"][0]["hints"]["patch_commit"], "abc123")
        self.assertTrue(ws.state_path("plan_by_patch.json").is_file())
        self.assertIn("reachability evidence and validation steps", prompt)
        self.assertIn(str(ws.main_path("patch") / "_patch_commits.json"), prompt)
        self.assertIn("preserve each record's `repo_id`", prompt)
        self.assertNotIn("PoC sketch", prompt)

    def test_plan_by_new_feature_returns_feature_subtasks_and_writes_log(self):
        update, ws, prompt = self._run_planner(
            nodes.plan_by_new_feature,
            json.dumps([
                {
                    "id": "feat-001",
                    "objective": "audit new parser",
                    "hints": {
                        "feature_ref": "main/feature/feature-001.md",
                        "priority_reason": "weak coverage and reachable file parser",
                    },
                }
            ]),
            state_overrides={"top_K": {"feature": 5}},
        )

        self.assertEqual(update["errors"], [])
        self.assertEqual(len(update["feature_subtasks"]), 1)
        self.assertEqual(update["feature_subtasks"][0]["bucket"], "feature")
        self.assertEqual(update["feature_subtasks"][0]["id"], "feat-001")
        self.assertIn("top_K.feature=5", prompt)
        self.assertIn("Feature surface directory", prompt)
        self.assertTrue(ws.state_path("plan_by_feature.json").is_file())

    def test_planner_prompt_includes_focus_top_k_and_priority_contract(self):
        update, _, prompt = self._run_planner(
            nodes.plan_by_spec,
            "[]",
            state_overrides={
                "common_focus": "guest-to-host escape in parser",
                "top_K": {"spec": 3},
            },
        )

        self.assertEqual(update["spec_subtasks"], [])
        self.assertIn("Global focus", prompt)
        self.assertIn("guest-to-host escape in parser", prompt)
        self.assertIn("top_K.spec=3", prompt)
        self.assertIn("priority_reason", prompt)

    def test_diff_planner_prompt_requires_risk_surface_convergence_without_default_cap(self):
        update, _, prompt = self._run_planner(
            nodes.plan_by_spec,
            "[]",
            state_overrides={
                "scan_scope": {
                    "mode": "diff",
                    "changed_files": ["src/parser.c"],
                },
            },
        )

        self.assertEqual(update["spec_subtasks"], [])
        self.assertIn("there is no numeric dispatch cap", prompt)
        self.assertIn("risk_surface_id", prompt)
        self.assertIn("diff_anchor", prompt)
        self.assertIn("change_to_sink_path", prompt)

    def test_diff_planner_writes_raw_candidates_and_converged_plan(self):
        stdout = json.dumps(
            [
                {
                    "id": "spec-001",
                    "objective": "check clause one",
                    "hints": {
                        "risk_surface_ids": ["RS-001"],
                        "diff_anchor": ["src/parser.c:10"],
                        "change_to_sink_path": ["parser", "sink"],
                        "spec_clause": "Clause 1",
                        "candidate_code_locations": ["src/parser.c:10"],
                        "blocking_eligible": True,
                        "priority_reason": "direct diff path",
                    },
                },
                {
                    "id": "spec-002",
                    "objective": "check clause two",
                    "hints": {
                        "risk_surface_ids": ["RS-001"],
                        "diff_anchor": ["src/parser.c:20"],
                        "change_to_sink_path": ["parser", "sink"],
                        "spec_clause": "Clause 2",
                        "candidate_code_locations": ["src/parser.c:20"],
                        "blocking_eligible": True,
                        "priority_reason": "same diff path",
                    },
                },
                {
                    "id": "spec-003",
                    "objective": "check unrelated context",
                    "hints": {
                        "candidate_code_locations": ["src/old.c:30"],
                        "blocking_eligible": False,
                        "priority_reason": "pre-existing context",
                    },
                },
            ]
        )

        update, ws, _ = self._run_planner(
            nodes.plan_by_spec,
            stdout,
            state_overrides={
                "scan_scope": {
                    "mode": "diff",
                    "changed_files": ["src/parser.c"],
                }
            },
        )

        self.assertEqual([task["id"] for task in update["spec_subtasks"]], ["spec-001"])
        self.assertEqual(
            update["spec_subtasks"][0]["hints"]["merged_subtasks"][0]["id"],
            "spec-002",
        )
        state_dir = ws.log_path("state")
        self.assertEqual(
            len(json.loads((state_dir / "plan_by_spec.candidates.json").read_text())),
            3,
        )
        self.assertEqual(
            len(json.loads((state_dir / "plan_by_spec.json").read_text())),
            1,
        )
        convergence = json.loads(
            (state_dir / "plan_by_spec.convergence.json").read_text()
        )
        self.assertEqual(convergence["raw_candidate_count"], 3)
        self.assertEqual(convergence["diff_attributable_count"], 2)
        self.assertEqual(convergence["independent_risk_count"], 1)

    def test_diff_planner_registry_rejects_unknown_risk_surface_then_retries(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="planner-registry")
        attack_surface = ws.main_path("attack_surface") / "attack_surface.md"
        attack_surface.write_text(
            "# Attack Surface\n\n"
            "## Diff Risk Surface Registry\n\n"
            "### RS-001\n"
            "- diff anchor: `src/parser.c:10`\n"
            "- flow: input -> parser -> allocation sink\n"
        )
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
            risk_surface_id = "RS-999" if extra_context["attempt"] == 1 else "RS-001"
            return AgentResult(
                stdout=json.dumps(
                    [
                        {
                            "id": "spec-001",
                            "objective": "check parser invariant",
                            "hints": {
                                "risk_surface_id": risk_surface_id,
                                "diff_anchor": ["src/parser.c:10"],
                                "change_to_sink_path": ["parser", "allocation sink"],
                                "blocking_eligible": True,
                                "priority_reason": "direct diff path",
                            },
                        }
                    ]
                ),
                stderr="",
                returncode=0,
                backend="codex",
            )

        state = {
            **_state_for_workspace(ws),
            "scan_scope": {
                "mode": "diff",
                "changed_files": ["src/parser.c"],
            },
        }
        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.plan_by_spec(state, backends={"plan_by_spec": "codex"})

        self.assertEqual(attempts, [1, 2])
        self.assertEqual(update["errors"], [])
        self.assertEqual(update["spec_subtasks"][0]["hints"]["risk_surface_id"], "RS-001")

    def test_diff_planner_registry_accepts_complete_extended_risk_surface(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="planner-extension")
        attack_surface = ws.main_path("attack_surface") / "attack_surface.md"
        attack_surface.write_text(
            "# Attack Surface\n\n"
            "## Diff Risk Surface Registry\n\n"
            "### RS-001\n"
            "- diff anchor: `src/parser.c:10`\n"
            "- flow: input -> parser -> allocation sink\n"
        )
        extension = {
            "root_cause": "changed length normalization reaches an unchecked sink",
            "untrusted_input_object": "wire length field",
            "trust_boundary": "network client to privileged parser",
            "state_machine_family": "length-prefixed parser",
            "sink": "allocation size",
            "security_invariant": "normalized length must bound allocation",
        }
        stdout = json.dumps(
            [
                {
                    "id": "spec-001",
                    "objective": "check newly discovered parser risk",
                    "hints": {
                        "risk_surface_id": "RS-EXT-length-allocation",
                        "risk_surface_definition": extension,
                        "diff_anchor": ["src/parser.c:10"],
                        "change_to_sink_path": ["normalize length", "allocate buffer"],
                        "blocking_eligible": True,
                        "priority_reason": "independent diff path",
                    },
                }
            ]
        )

        update, _, _ = self._run_planner(
            nodes.plan_by_spec,
            stdout,
            state_overrides={
                "attack_surface": str(attack_surface),
                "scan_scope": {
                    "mode": "diff",
                    "changed_files": ["src/parser.c"],
                },
            },
        )

        self.assertEqual(update["errors"], [])
        self.assertEqual(
            update["spec_subtasks"][0]["hints"]["risk_surface_id"],
            "RS-EXT-length-allocation",
        )

    def test_full_planner_ignores_risk_registry_contract(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="planner-full-registry")
        attack_surface = ws.main_path("attack_surface") / "attack_surface.md"
        attack_surface.write_text(
            "# Attack Surface\n\n"
            "## Diff Risk Surface Registry\n\n"
            "### RS-001\n"
            "- historical text retained in a full-mode report\n"
        )
        stdout = json.dumps(
            [
                {
                    "id": "spec-001",
                    "objective": "full repository clause check",
                    "hints": {
                        "candidate_code_locations": ["src/parser.c:10"],
                        "priority_reason": "reachable full repository path",
                    },
                }
            ]
        )

        update, _, _ = self._run_planner(
            nodes.plan_by_spec,
            stdout,
            state_overrides={
                "attack_surface": str(attack_surface),
                "scan_scope": {"mode": "full", "changed_files": []},
            },
        )

        self.assertEqual(update["errors"], [])
        self.assertEqual([task["id"] for task in update["spec_subtasks"]], ["spec-001"])

    def test_planner_retries_and_reports_error_when_stdout_is_not_json_array(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="planner-invalid")

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
            self.assertIn(extra_context["attempt"], [1, 2, 3])
            return AgentResult(stdout="not json", stderr="", returncode=0, backend="codex")

        with patch.object(nodes, "_invoke", side_effect=fake_invoke) as invoke:
            update = nodes.plan_by_vuln_patch(
                _state_for_workspace(ws),
                backends={"plan_by_vuln_patch": "codex"},
            )

        self.assertEqual(invoke.call_count, nodes.DEFAULT_NODE_OUTPUT_ATTEMPTS)
        self.assertEqual(update["patch_subtasks"], [])
        self.assertEqual(
            update["errors"],
            [
                "[plan_by_vuln_patch] output empty after attempt "
                f"{nodes.DEFAULT_NODE_OUTPUT_ATTEMPTS}/{nodes.DEFAULT_NODE_OUTPUT_ATTEMPTS}: "
                f"{ws.state_path('plan_by_patch.json')}"
            ],
        )
        self.assertTrue(ws.state_path("plan_by_patch.json").is_file())

    def test_planner_retries_after_nonzero_rc_then_writes_valid_log(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ws = Workspace.create(tmp.name, target="libfoo", task_id="planner-rc")
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
                return AgentResult(stdout="", stderr="temporary failure", returncode=1, backend="codex")
            return AgentResult(
                stdout=json.dumps([{"id": "spec-001", "objective": "check", "hints": {}}]),
                stderr="",
                returncode=0,
                backend="codex",
            )

        with patch.object(nodes, "_invoke", side_effect=fake_invoke):
            update = nodes.plan_by_spec(
                _state_for_workspace(ws),
                backends={"plan_by_spec": "codex"},
            )

        self.assertEqual(attempts, [1, 2])
        self.assertEqual(update["errors"], [])
        self.assertEqual(update["spec_subtasks"][0]["id"], "spec-001")
        self.assertTrue(ws.state_path("plan_by_spec.json").is_file())

    def test_planner_accepts_empty_json_array_as_non_empty_output(self):
        update, ws, _ = self._run_planner(nodes.plan_by_spec, "[]")

        self.assertEqual(update["errors"], [])
        self.assertEqual(update["spec_subtasks"], [])
        self.assertEqual(
            ws.state_path("plan_by_spec.json").read_text().strip(),
            "[]",
        )


if __name__ == "__main__":
    unittest.main()
