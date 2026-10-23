"""Tests for cross-workspace gather mode."""

from __future__ import annotations

import json
import importlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from click.testing import CliRunner

from zeromdash.agents import AgentHealth, AgentResult, additional_read_root_args
from zeromdash.cli import main
from zeromdash.cli import _parse_agent_config_file, _pop_gather_config_from_agent_config
from zeromdash import gather_graph as gather_graph_mod
from zeromdash.gather import load_gather_manifest, prepare_gather_state, source_drift_errors
from zeromdash.gather_graph import build_gather_graph
from zeromdash.nodes.core.gather_qualification import (
    close_gather_chain,
    normalize_gather_chain_plan,
    validate_cross_target_registry,
)
from zeromdash.workspace import Workspace


_CVSS4_C_HIGH_VECTOR = (
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/"
    "VC:H/VI:N/VA:N/SC:N/SI:N/SA:N"
)


def _primitive(primitive_id: str, component: str) -> dict:
    return {
        "schema_version": "2.0",
        "primitive_id": primitive_id,
        "repo_id": "main",
        "component": component,
        "source_subtask_ids": ["vuln-001"],
        "entry_conditions": {},
        "required_capabilities": [],
        "attacker_controls": [{"kind": "request"}],
        "capabilities_gained": [{"kind": "controlled_object", "object_type": "job"}],
        "handoff_objects": [{"object_type": "job"}],
        "required_entity_states": [],
        "resulting_entity_states": [],
        "terminal_impact": {},
        "root_cause_anchor": {"locations": [f"src/{component}.c:10"]},
        "evidence": {"code_locations": [f"src/{component}.c:10"]},
        "confirmation": {"critic_verdict": "confirm", "confidence": 0.9},
    }


def _source_workspace(root: Path, name: str) -> tuple[Workspace, Path]:
    ws = Workspace.create(root / "sources", target=name)
    (ws.main_path("repo") / "src").mkdir(parents=True)
    (ws.main_path("repo") / "src" / f"{name}.c").write_text("int main(void) { return 0; }\n")
    (ws.main_path("attack_surface") / "attack_surface.md").write_text(f"# {name} surface\n")
    (ws.main_path("attack_surface") / "domain_invariant_registry.json").write_text(
        json.dumps({"schema_version": "1.0", "target": name, "status": "available"})
    )
    (ws.log_path("primitive_res") / "shared.json").write_text(
        json.dumps(_primitive("PRIM-001", name))
    )
    config = root / f"{name}.yaml"
    config.write_text(
        "common_focus: target boundary\n"
        "node:\n"
        "  investigate_subtask:\n"
        "    focus: target-specific invariant\n"
        "    env:\n"
        "      SECRET_TOKEN: must-not-leak\n"
    )
    return ws, config


class GatherManifestTest(unittest.TestCase):
    def test_additional_read_roots_are_explicit_and_deduplicated(self):
        with TemporaryDirectory() as tmp:
            expected = str(Path(tmp).resolve())
            self.assertEqual(
                additional_read_root_args("codex", [tmp, tmp]),
                ["--add-dir", expected],
            )
            with self.assertRaisesRegex(ValueError, "does not support"):
                additional_read_root_args("opencode", [tmp])

    def test_gather_agent_config_is_parsed_separately(self):
        with TemporaryDirectory() as tmp:
            config = Path(tmp) / "gather.yaml"
            config.write_text(
                "gather:\n"
                "  max_pair_passes: 8\n"
                "  max_chain_length: 5\n"
                "  max_candidates_before_top_k: 40\n"
                "  max_battle_rounds: 2\n"
                "  require_cross_target: true\n"
                "node:\n"
                "  gather_plan_chains:\n"
                "    runtime: codex\n"
            )
            parsed = _parse_agent_config_file(str(config))
        self.assertEqual(
            _pop_gather_config_from_agent_config(parsed),
            {
                "max_pair_passes": 8,
                "max_chain_length": 5,
                "max_candidates_before_top_k": 40,
                "max_battle_rounds": 2,
                "require_cross_target": True,
            },
        )
        self.assertEqual(parsed["gather_plan_chains"]["runtime"], "codex")

    def test_manifest_resolves_paths_and_rejects_namespace_collisions(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            first, first_config = _source_workspace(root, "api")
            second, second_config = _source_workspace(root, "worker")
            manifest = root / "multi.yaml"
            manifest.write_text(
                "schema_version: '1.0'\n"
                "scenario: api forwards jobs to worker\n"
                "targets:\n"
                f"  - name: api\n    agent_config: {first_config.name}\n    workspace: {first.base}\n"
                f"  - name: worker\n    agent_config: {second_config.name}\n    workspace: {second.base}\n"
            )
            loaded = load_gather_manifest(manifest)
            self.assertEqual([item["target_id"] for item in loaded["targets"]], ["api", "worker"])
            self.assertEqual(loaded["targets"][0]["agent_config"], str(first_config.resolve()))

            manifest.write_text(
                "schema_version: '1.0'\nscenario: collision\ntargets:\n"
                f"  - name: A B\n    agent_config: {first_config}\n    workspace: {first.base}\n"
                f"  - name: A_B\n    agent_config: {second_config}\n    workspace: {second.base}\n"
            )
            with self.assertRaisesRegex(ValueError, "namespace collision"):
                load_gather_manifest(manifest)

    def test_prepare_state_snapshots_and_namespaces_evidence_without_secrets(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            first, first_config = _source_workspace(root, "api")
            second, second_config = _source_workspace(root, "worker")
            manifest_path = root / "multi.yaml"
            manifest_path.write_text(
                "schema_version: '1.0'\nname: stack\nscenario: api forwards jobs to worker\ntargets:\n"
                f"  - name: api\n    agent_config: {first_config}\n    workspace: {first.base}\n"
                f"  - name: worker\n    agent_config: {second_config}\n    workspace: {second.base}\n"
            )
            source_before = (first.main_path("repo") / "src" / "api.c").read_text()
            state = prepare_gather_state(
                load_gather_manifest(manifest_path),
                workspace_root=root / "output",
            )
            ids = [item["unit_id"] for item in state["gather_evidence_pool"]]
            self.assertEqual(ids, ["api::PRIM-001", "worker::PRIM-001"])
            self.assertTrue(Path(state["input_lock_path"]).is_file())
            self.assertTrue(Path(state["gather_evidence_pool_path"]).is_file())
            self.assertEqual((first.main_path("repo") / "src" / "api.c").read_text(), source_before)
            snapshot_text = "\n".join(
                path.read_text(errors="ignore")
                for path in (Path(state["workspace_root"]) / state["task_id"] / "inputs").rglob("*")
                if path.is_file()
            )
            self.assertNotIn("must-not-leak", snapshot_text)
            self.assertTrue(all(Path(path).is_dir() for path in state["source_read_roots"]))
            (first.main_path("repo") / "src" / "api.c").write_text("changed after snapshot\n")
            self.assertTrue(any(item.startswith("source_drift:api:") for item in source_drift_errors(state)))


class GatherQualificationTest(unittest.TestCase):
    def setUp(self):
        self.units = {
            "api::PRIM-001": {
                "unit_id": "api::PRIM-001",
                "target_id": "api",
                "unit_kind": "primitive",
                "source_refs": [{"target_id": "api", "artifact_path": "api.json", "artifact_sha256": "a"}],
            },
            "worker::PRIM-001": {
                "unit_id": "worker::PRIM-001",
                "target_id": "worker",
                "unit_kind": "primitive",
                "source_refs": [{"target_id": "worker", "artifact_path": "worker.json", "artifact_sha256": "b"}],
            },
        }
        self.registry = {
            "schema_version": "1.0",
            "scenario": "api forwards jobs",
            "targets": [{"target_id": "api"}, {"target_id": "worker"}],
            "interfaces": [],
            "data_flows": [
                {
                    "flow_id": "FLOW-001",
                    "producer_target_id": "api",
                    "consumer_target_id": "worker",
                    "data_object": "job",
                    "status": "confirmed",
                    "source_refs": [
                        {"target_id": "api", "artifact_path": "api.json", "artifact_sha256": "a"},
                        {"target_id": "worker", "artifact_path": "worker.json", "artifact_sha256": "b"},
                    ],
                }
            ],
            "cross_target_invariants": [],
            "deployment_assumptions": [],
            "unresolved_gaps": [],
        }

    def test_registry_and_plan_require_real_cross_target_references(self):
        registry, failure = validate_cross_target_registry(self.registry, target_ids={"api", "worker"})
        self.assertEqual(failure, "")
        payload = {
            "chains": [
                {
                    "target_sequence": ["api", "worker"],
                    "ordered_unit_ids": ["api::PRIM-001", "worker::PRIM-001"],
                    "bindings": [
                        {
                            "provider_unit_id": "api::PRIM-001",
                            "consumer_unit_id": "worker::PRIM-001",
                            "flow_id": "FLOW-001",
                            "compatibility_reason": "same job object",
                            "source_refs": [],
                        }
                    ],
                    "rank_score": 0.9,
                    "agent_reasoning": "the job crosses a trust boundary",
                }
            ]
        }
        chains, errors = normalize_gather_chain_plan(
            payload,
            evidence_by_id=self.units,
            registry=registry or {},
            top_k=4,
        )
        self.assertEqual(errors, [])
        self.assertEqual(len(chains), 1)
        self.assertTrue(chains[0]["chain_id"].startswith("gchain_"))

    def test_closed_chain_requires_bilateral_confirmed_edge(self):
        candidate = {
            "chain_id": "gchain_test",
            "target_sequence": ["api", "worker"],
            "ordered_unit_ids": ["api::PRIM-001", "worker::PRIM-001"],
            "bindings": [],
        }
        fact = {"fact_id": "fact-1", "statement": "deployment exists", "evidence": ["deploy.yaml:1"]}
        investigation = {
            "title": "cross-target authorization bypass",
            "detail": "api-controlled job reaches privileged worker sink",
            "ordered_unit_ids": candidate["ordered_unit_ids"],
            "bindings": [],
            "binding_claims": [
                {
                    "edge_id": "edge-1",
                    "provider_unit_id": "api::PRIM-001",
                    "consumer_unit_id": "worker::PRIM-001",
                    "flow_id": "FLOW-001",
                    "flow_status": "confirmed",
                    "source_refs": [
                        {"target_id": "api", "artifact_path": "api.json", "artifact_sha256": "a"},
                        {"target_id": "worker", "artifact_path": "worker.json", "artifact_sha256": "b"},
                    ],
                }
            ],
            "attack_path": [],
            "global_constraints": {},
            "evidence": {"code_locations": ["api.c:10", "worker.c:10"]},
            "direct_security_impact": {
                "vulnerable_system": {"confidentiality": "high", "integrity": "none", "availability": "none"},
                "subsequent_system": {"confidentiality": "none", "integrity": "none", "availability": "none"},
            },
            "closure_facts": [fact],
        }
        review = {
            "verdict": "confirm",
            "all_units_confirmed": True,
            "bindings_valid": True,
            "global_constraints_satisfiable": True,
            "required_external_primitives": [],
            "closure_verdict": "closed",
            "edge_verdicts": [
                {
                    "edge_id": "edge-1",
                    "verdict": "confirm",
                    "reasoning": "producer and consumer evidence agree",
                    "evidence": ["api.c:10", "worker.c:10"],
                }
            ],
            "fact_verdicts": [
                {
                    "fact_id": "fact-1",
                    "classification": "deployment_constraint",
                    "blocking": False,
                    "resolved": True,
                    "reasoning": "deployment manifest confirms the flow",
                    "evidence": ["deploy.yaml:1"],
                }
            ],
            "direct_security_impact": investigation["direct_security_impact"],
            "cvss4_vector": _CVSS4_C_HIGH_VECTOR,
            "confidence": 0.9,
            "violated_security_property": "worker authorization",
            "gate_decision": "block",
        }
        finding, failures = close_gather_chain(
            candidate=candidate,
            investigation=investigation,
            review=review,
            evidence_by_id=self.units,
            registry=self.registry,
            drift_errors=[],
        )
        self.assertEqual(failures, [])
        self.assertEqual(finding["kind"], "gather_chain")

        investigation["binding_claims"][0]["source_refs"] = [
            {"target_id": "api", "artifact_path": "api.json", "artifact_sha256": "a"}
        ]
        finding, failures = close_gather_chain(
            candidate=candidate,
            investigation=investigation,
            review=review,
            evidence_by_id=self.units,
            registry=self.registry,
            drift_errors=[],
        )
        self.assertIsNone(finding)
        self.assertTrue(any("bilateral" in item for item in failures))

    def test_gather_graph_compiles(self):
        graph = build_gather_graph({})
        names = set(graph.get_graph().nodes)
        self.assertIn("gather_analyze_attack_surface", names)
        self.assertIn("gather_chain_subtask", names)
        self.assertIn("gather_prepare_report_groups", names)

    def test_empty_plan_routes_once_to_report_and_summary(self):
        calls: list[str] = []

        def analyze(state, *, backends=None):
            del state, backends
            calls.append("analyze")
            return {"cross_target_registry": {"data_flows": []}}

        def plan(state, *, backends=None):
            del state, backends
            calls.append("plan")
            return {"gather_chain_plan": []}

        def groups(state, *, backends=None):
            del state, backends
            calls.append("groups")
            return {"gather_report_groups": []}

        def summary(state, *, backends=None):
            del state, backends
            calls.append("summary")
            return {"summary": "done", "summary_en": "done", "summary_zh_CN": "完成"}

        def polish(state, *, backends=None):
            del backends
            calls.append("polish")
            return {"summary": state.get("summary", "")}

        with patch.object(gather_graph_mod, "gather_analyze_attack_surface", side_effect=analyze), patch.object(
            gather_graph_mod, "gather_plan_chains", side_effect=plan
        ), patch.object(gather_graph_mod, "gather_prepare_report_groups", side_effect=groups), patch.object(
            gather_graph_mod, "gather_summary", side_effect=summary
        ), patch.object(gather_graph_mod, "polish_report", side_effect=polish):
            final = gather_graph_mod.build_gather_graph({}).invoke(
                {
                    "scan_mode": "gather",
                    "target": "gather:test",
                    "scenario_name": "test",
                    "scenario": "a calls b",
                    "task_id": "workspace_for_gather-test",
                    "workspace_root": "/tmp",
                    "gather_targets": [],
                    "gather_evidence_pool": [],
                    "gather_chain_candidates": [],
                    "gather_chain_findings": [],
                    "errors": [],
                }
            )
        self.assertEqual(calls, ["analyze", "plan", "groups", "summary", "polish"])
        self.assertEqual(final["summary"], "done")

    def test_candidate_fans_out_through_nested_battle(self):
        calls: list[str] = []
        candidate = {"chain_id": "gchain_test", "ordered_unit_ids": ["a::p", "b::p"]}

        def mark(name, result):
            def call(state, *, backends=None):
                del state, backends
                calls.append(name)
                return result
            return call

        def investigate(state, *, backends=None):
            del backends
            calls.append("investigate")
            return {
                "iteration": 1,
                "gather_chain_investigation_valid": True,
                "gather_chain_investigation": {"title": "candidate"},
            }

        def critic(state, *, backends=None):
            del state, backends
            calls.append("critic")
            return {"gather_chain_review": {"verdict": "confirm"}}

        with patch.object(
            gather_graph_mod,
            "gather_analyze_attack_surface",
            side_effect=mark("analyze", {"cross_target_registry": {"data_flows": []}}),
        ), patch.object(
            gather_graph_mod,
            "gather_plan_chains",
            side_effect=mark("plan", {"gather_chain_plan": [candidate]}),
        ), patch.object(
            gather_graph_mod,
            "gather_chain_investigate_subtask",
            side_effect=investigate,
        ), patch.object(
            gather_graph_mod,
            "gather_chain_critic_subtask",
            side_effect=critic,
        ), patch.object(
            gather_graph_mod,
            "route_after_gather_chain_critic",
            return_value="gather_finalize_chain_subtask",
        ), patch.object(
            gather_graph_mod,
            "gather_finalize_chain_subtask",
            side_effect=mark("finalize", {"gather_chain_findings": [{"chain_id": "gchain_test"}]}),
        ), patch.object(
            gather_graph_mod,
            "gather_prepare_report_groups",
            side_effect=mark("groups", {"gather_report_groups": []}),
        ), patch.object(
            gather_graph_mod,
            "gather_summary",
            side_effect=mark("summary", {"summary": "done"}),
        ), patch.object(
            gather_graph_mod,
            "polish_report",
            side_effect=mark("polish", {"summary": "done"}),
        ):
            final = gather_graph_mod.build_gather_graph({}).invoke(
                {
                    "scan_mode": "gather",
                    "target": "gather:test",
                    "scenario_name": "test",
                    "scenario": "a calls b",
                    "task_id": "workspace_for_gather-test",
                    "workspace_root": "/tmp",
                    "gather_targets": [],
                    "gather_evidence_pool": [],
                    "gather_chain_candidates": [],
                    "gather_chain_findings": [],
                    "errors": [],
                }
            )
        self.assertEqual(
            calls,
            ["analyze", "plan", "investigate", "critic", "finalize", "groups", "summary", "polish"],
        )
        self.assertEqual(final["gather_chain_findings"], [{"chain_id": "gchain_test"}])


class GatherNodeTest(unittest.TestCase):
    def test_analyze_and_plan_materialize_canonical_artifacts(self):
        analyze_mod = importlib.import_module("zeromdash.nodes.gather_analyze_attack_surface")
        plan_mod = importlib.import_module("zeromdash.nodes.gather_plan_chains")
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="gather-stack")
            targets = [
                {"target_id": "api", "source_roots": []},
                {"target_id": "worker", "source_roots": []},
            ]
            registry = {
                "schema_version": "1.0",
                "scenario": "api calls worker",
                "targets": targets,
                "interfaces": [],
                "data_flows": [
                    {
                        "flow_id": "FLOW-001",
                        "producer_target_id": "api",
                        "consumer_target_id": "worker",
                        "data_object": "job",
                        "status": "confirmed",
                        "source_refs": [{"target_id": "api"}, {"target_id": "worker"}],
                    }
                ],
                "cross_target_invariants": [],
                "deployment_assumptions": [],
                "unresolved_gaps": [],
            }
            state = {
                "target": "gather:stack",
                "scenario_name": "stack",
                "scenario": "api calls worker",
                "task_id": ws.task_id,
                "workspace_root": str(ws.root),
                "gather_targets": targets,
                "source_read_roots": [],
                "agent_configs": {},
                "gather_config": {},
                "errors": [],
            }

            def fake_analyze_invoke(_ws, _node, _prompt, _backends, _state, **kwargs):
                kwargs["reset"]()
                (ws.main_path("attack_surface") / "gather_attack_surface.md").write_text("# topology\n")
                result = AgentResult(json.dumps(registry), "", 0, "codex")
                kwargs["materialize"](result)
                self.assertTrue(kwargs["validate"](result)[0])
                return result, []

            with patch.object(analyze_mod, "_invoke_with_output_retry", side_effect=fake_analyze_invoke):
                analyzed = analyze_mod.gather_analyze_attack_surface(state, backends={})
            self.assertEqual(analyzed["cross_target_registry"], registry)
            self.assertTrue(Path(analyzed["cross_target_registry_path"]).is_file())

            units = [
                {"unit_id": "api::PRIM-001", "target_id": "api", "unit_kind": "primitive"},
                {"unit_id": "worker::PRIM-001", "target_id": "worker", "unit_kind": "primitive"},
            ]
            evidence_path = ws.state_path("gather_evidence_pool.json")
            evidence_path.write_text(json.dumps({"units": units}))
            planned_state = {
                **state,
                **analyzed,
                "gather_evidence_pool": units,
                "gather_evidence_pool_path": str(evidence_path),
                "top_K": {"chain": 4},
            }
            plan_payload = {
                "chains": [
                    {
                        "target_sequence": ["api", "worker"],
                        "ordered_unit_ids": ["api::PRIM-001", "worker::PRIM-001"],
                        "bindings": [
                            {
                                "provider_unit_id": "api::PRIM-001",
                                "consumer_unit_id": "worker::PRIM-001",
                                "flow_id": "FLOW-001",
                                "compatibility_reason": "same serialized job",
                                "source_refs": [],
                            }
                        ],
                        "rank_score": 1.0,
                        "agent_reasoning": "candidate crosses the worker boundary",
                    }
                ]
            }

            def fake_plan_invoke(_ws, _node, _prompt, _backends, _state, **kwargs):
                result = AgentResult(json.dumps(plan_payload), "", 0, "codex")
                self.assertTrue(kwargs["validate"](result)[0])
                return result, []

            with patch.object(plan_mod, "_invoke_with_output_retry", side_effect=fake_plan_invoke):
                planned = plan_mod.gather_plan_chains(planned_state, backends={})
            self.assertEqual(len(planned["gather_chain_plan"]), 1)
            self.assertTrue(Path(planned["gather_chain_plan_path"]).is_file())

    def test_report_groups_and_empty_summary(self):
        groups_mod = importlib.import_module("zeromdash.nodes.gather_prepare_report_groups")
        summary_mod = importlib.import_module("zeromdash.nodes.gather_summary")
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="gather-stack")
            state = {
                "target": "gather:stack",
                "scenario_name": "stack",
                "scenario": "api calls worker",
                "task_id": ws.task_id,
                "workspace_root": str(ws.root),
                "gather_targets": [],
                "gather_chain_findings": [],
                "gather_chain_candidates": [],
                "agent_configs": {},
                "errors": [],
            }
            grouped = groups_mod.gather_prepare_report_groups(state, backends={})
            self.assertEqual(grouped["gather_report_groups"], [])
            self.assertTrue(Path(grouped["gather_report_groups_path"]).is_file())

            def fake_summary_invoke(_ws, _node, _prompt, _backends, _state, **kwargs):
                kwargs["reset"]()
                (ws.base / "summary.en.md").write_text("# Executive Summary\nNo confirmed chain.\n")
                (ws.base / "summary.zh_CN.md").write_text("# 执行摘要\n未确认跨目标攻击链。\n")
                result = AgentResult("done", "", 0, "claude_code")
                kwargs["materialize"](result)
                self.assertTrue(kwargs["validate"](result)[0])
                return result, []

            with patch.object(summary_mod, "_invoke_with_output_retry", side_effect=fake_summary_invoke):
                result = summary_mod.gather_summary({**state, **grouped}, backends={})
            self.assertEqual(result["gate_result"]["scan_mode"], "gather")
            self.assertEqual(result["gate_result"]["decision"], "pass")
            self.assertTrue((ws.base / "summary.md").is_file())


class GatherCliTest(unittest.TestCase):
    def test_help_lists_gather_mode(self):
        result = CliRunner().invoke(main, ["--help"])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("full|diff|gather", result.output)
        self.assertIn("--gather-workspace-to-chain", result.output)

    def test_gather_requires_manifest_and_non_gather_rejects_it(self):
        runner = CliRunner()
        missing = runner.invoke(main, ["--scan-mode", "gather"])
        self.assertNotEqual(missing.exit_code, 0)
        self.assertIn("requires --gather-workspace-to-chain", missing.output)
        with TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "targets.yaml"
            manifest.write_text("schema_version: '1.0'\nscenario: x\ntargets: []\n")
            wrong_mode = runner.invoke(main, ["--target", "x", "--gather-workspace-to-chain", str(manifest)])
        self.assertNotEqual(wrong_mode.exit_code, 0)
        self.assertIn("requires --scan-mode gather", wrong_mode.output)

    def test_gather_cli_dispatches_to_run_gather(self):
        runner = CliRunner()
        manifest = {
            "schema_version": "1.0",
            "name": "stack",
            "scenario": "a calls b",
            "targets": [{"target_id": "a"}, {"target_id": "b"}],
            "manifest_path": "/tmp/targets.yaml",
        }
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "targets.yaml"
            path.write_text("placeholder\n")
            output = Path(tmp) / "out"
            task = output / "workspace_for_gather-stack"
            task.mkdir(parents=True)
            final = {
                "summary": "done",
                "task_id": task.name,
                "workspace_root": str(output),
                "errors": [],
                "gate_result": {"decision": "pass"},
            }
            healthy = AgentHealth(name="codex", ok=True, binary="codex", message="ok")
            with patch("zeromdash.cli.load_gather_manifest", return_value=manifest), patch(
                "zeromdash.cli.check_agent_health", return_value=healthy
            ), patch("zeromdash.cli.run_gather", return_value=final) as run:
                result = runner.invoke(
                    main,
                    [
                        "--scan-mode",
                        "gather",
                        "--gather-workspace-to-chain",
                        str(path),
                        "--workspace-root",
                        str(output),
                    ],
                )
        self.assertEqual(result.exit_code, 0, result.output)
        run.assert_called_once()
        self.assertEqual(run.call_args.kwargs["manifest"], manifest)


if __name__ == "__main__":
    unittest.main()
