"""Unit tests for primitive and chain analysis flow."""

from __future__ import annotations

import json
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from zeromdash import graph as graph_mod, nodes
from zeromdash.agents import AgentResult
from zeromdash.workspace import Workspace


_CVSS4_C_HIGH_VECTOR = (
    "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/"
    "VC:H/VI:N/VA:N/SC:N/SI:N/SA:N"
)


def _workspace_state(ws: Workspace) -> dict:
    return {
        "target": "libfoo",
        "task_id": ws.task_id,
        "workspace_root": str(ws.root),
        "repo_path": str(ws.main_path("repo")),
    }




def _nonblocking_fact(fact_id: str, statement: str, evidence: list[str] | None = None) -> dict:
    return {"fact_id": fact_id, "statement": statement, "evidence": list(evidence or [])}


def _fact_verdict(fact: dict, classification: str, *, blocking: bool = False, resolved: bool = True) -> dict:
    return {
        "fact_id": fact["fact_id"],
        "classification": classification,
        "blocking": blocking,
        "resolved": resolved,
        "reasoning": "critic classified this fact",
        "evidence": list(fact.get("evidence") or []),
    }


def _closed_fact_contract(facts: list[dict] | None = None) -> dict:
    facts = list(facts or [])
    return {
        "closure_verdict": "closed",
        "fact_verdicts": [
            _fact_verdict(
                fact,
                str(fact.get("proposed_classification") or "validation_gap"),
                blocking=str(fact.get("proposed_classification")) == "blocking_unmet_fact",
                resolved=True,
            )
            for fact in facts
        ],
    }


def _primitive_a() -> dict:
    return {
        "schema_version": "2.0",
        "primitive_id": "prim_a",
        "source_subtask_ids": ["vuln-001"],
        "repo_id": "main",
        "component": "session",
        "root_cause_anchor": {"symbol": "accept_sid", "locations": ["src/a.c:10"]},
        "entry_conditions": {},
        "required_capabilities": [
            {
                "kind": "controlled_request",
                "object_type": "*",
                "scope": "*",
                "principal": "attacker",
                "tenant": "*",
                "address_space": "*",
            }
        ],
        "attacker_controls": [],
        "capabilities_gained": [
            {
                "kind": "object_reference",
                "object_type": "session",
                "scope": "same-service",
                "principal": "victim",
                "tenant": "same-tenant",
                "address_space": "server-process",
            }
        ],
        "handoff_objects": [],
        "reliability": {"level": "high"},
        "evidence": {"code_locations": ["src/a.c:10"], "call_path": ["entry -> accept_sid"]},
        "terminal_impact": {},
        "confirmation": {"critic_verdict": "confirm", "confidence": 0.9},
    }


def _primitive_b() -> dict:
    return {
        "schema_version": "2.0",
        "primitive_id": "prim_b",
        "source_subtask_ids": ["vuln-002"],
        "repo_id": "main",
        "component": "profile",
        "root_cause_anchor": {"symbol": "read_profile", "locations": ["src/b.c:20"]},
        "entry_conditions": {},
        "required_capabilities": [
            {
                "kind": "object_reference",
                "object_type": "session",
                "scope": "same-service",
                "principal": "victim",
                "tenant": "same-tenant",
                "address_space": "server-process",
            }
        ],
        "attacker_controls": [],
        "capabilities_gained": [
            {
                "kind": "arbitrary_file_read",
                "object_type": "profile",
                "scope": "same-service",
                "principal": "victim",
                "tenant": "same-tenant",
                "address_space": "server-process",
            }
        ],
        "handoff_objects": [],
        "reliability": {"level": "high"},
        "evidence": {"code_locations": ["src/b.c:20"], "call_path": ["read_profile -> leak"]},
        "terminal_impact": {
            "vulnerable_system": {
                "confidentiality": "high",
                "integrity": "none",
                "availability": "none",
            },
            "subsequent_system": {
                "confidentiality": "none",
                "integrity": "none",
                "availability": "none",
            },
        },
        "confirmation": {"critic_verdict": "confirm", "confidence": 0.8},
    }


class PrimitiveFinalizeTest(unittest.TestCase):
    def test_primitive_id_is_stable_across_domain_ref_order_and_duplicates(self):
        first = {
            **_primitive_a(),
            "domain_refs": {
                "entity_ids": ["entity:b", "entity:a", "entity:a"],
                "seam_ids": ["seam:a"],
            },
        }
        second = {
            **_primitive_a(),
            "domain_refs": {
                "seam_ids": ["seam:a"],
                "entity_ids": ["entity:a", "entity:b"],
            },
        }
        self.assertEqual(nodes.stable_primitive_id(first), nodes.stable_primitive_id(second))

    def test_chain_id_ignores_explanations_advisories_and_binding_order(self):
        binding_a = {
            "consumer_primitive_id": "prim_a",
            "required_capability": _primitive_a()["required_capabilities"][0],
            "provider": {
                "type": "attacker_entry",
                "capability": _primitive_a()["required_capabilities"][0],
            },
            "compatibility_reason": "first explanation",
            "evidence": ["src/a.c:10"],
            "deterministic_advisory": {"compatible": True},
        }
        binding_b = {
            "consumer_primitive_id": "prim_b",
            "required_capability": _primitive_b()["required_capabilities"][0],
            "provider": {
                "type": "primitive",
                "primitive_id": "prim_a",
                "capability": _primitive_a()["capabilities_gained"][0],
            },
            "compatibility_reason": "second explanation",
        }
        changed = [
            {**binding_b, "compatibility_reason": "rewritten by another agent", "edge_id": "noise"},
            {**binding_a, "evidence": ["different.c:99"], "deterministic_advisory": {"compatible": False}},
        ]
        self.assertEqual(
            nodes.stable_chain_id(["prim_a", "prim_b"], [binding_a, binding_b]),
            nodes.stable_chain_id(["prim_a", "prim_b"], changed),
        )

    def test_edge_id_is_stable_across_binding_order(self):
        binding = {
            "consumer_primitive_id": "prim_b",
            "required_capability": _primitive_b()["required_capabilities"][0],
            "provider": {
                "type": "primitive",
                "primitive_id": "prim_a",
                "capability": _primitive_a()["capabilities_gained"][0],
            },
        }
        self.assertEqual(nodes.stable_edge_id(binding, 0), nodes.stable_edge_id(binding, 9))

    def test_domain_registry_validation_rejects_unknown_references(self):
        registry = {
            "schema_version": "1.0",
            "entities": [{"entity_id": "entity:a", "kind": "state", "name": "A", "source_locations": []}],
            "representations": [],
            "invariants": [],
            "transitions": [],
            "seams": [{"seam_id": "seam:a", "kind": "producer_consumer", "producer_ids": ["entity:missing"], "consumer_ids": ["entity:a"], "invariant_ids": [], "candidate_locations": []}],
        }
        parsed, error = nodes.validate_domain_registry(registry)
        self.assertIsNone(parsed)
        self.assertIn("unknown domain id", error)

    def test_domain_registry_validation_checks_transition_and_invariant_links(self):
        registry = {
            "schema_version": "1.0",
            "entities": [{"entity_id": "entity:a", "kind": "state", "name": "A", "source_locations": []}],
            "representations": [],
            "invariants": [],
            "transitions": [{"transition_id": "transition:a", "name": "A to missing", "input_entity_ids": ["entity:a"], "output_entity_ids": ["entity:missing"], "source_locations": []}],
            "seams": [],
        }
        parsed, error = nodes.validate_domain_registry(registry)
        self.assertIsNone(parsed)
        self.assertIn("transition references unknown entity id", error)

    def test_domain_registry_validation_enforces_required_field_types(self):
        registry = {
            "schema_version": "1.0",
            "entities": [{"entity_id": "entity:a", "kind": "state", "name": "A", "source_locations": "src/a.c:1"}],
            "representations": [],
            "invariants": [],
            "transitions": [],
            "seams": [],
        }
        parsed, error = nodes.validate_domain_registry(registry)
        self.assertIsNone(parsed)
        self.assertIn("source_locations must be an array of strings", error)

    def test_legacy_workspace_gets_explicit_unavailable_registry(self):
        registry = nodes.read_domain_registry("/definitely/missing/registry.json", target="libfoo")
        self.assertEqual(registry["status"], "legacy_unavailable")
        self.assertEqual(registry["target"], "libfoo")

    def test_confirmed_primitive_is_persisted_without_cvss_vulnerability(self):
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="libfoo", task_id="primitive")
            state = {
                **_workspace_state(ws),
                "subtask": {"id": "vuln-001", "bucket": "vuln", "objective": "check primitive", "hints": {}},
                "iteration": 1,
                "investigation": json.dumps(
                    {
                        "title": "attacker obtains victim session reference",
                        "detail": "validated primitive",
                        "evidence": {
                            "code_locations": ["src/a.c:10"],
                            "call_path": ["entry -> accept_sid"],
                        },
                        "primitive": {
                            "component": "session",
                            "root_cause_anchor": {"symbol": "accept_sid", "locations": ["src/a.c:10"]},
                            "capabilities_gained": [
                                {
                                    "kind": "object_reference",
                                    "object_type": "session",
                                    "principal": "victim",
                                    "address_space": "server-process",
                                }
                            ],
                        },
                    }
                ),
                "review": {
                    "verdict": "confirm",
                    "outcome_type": "confirmed_primitive",
                    "reasoning": "local primitive is proven but not standalone impact",
                    "selected_skills": [],
                    "confidence": 0.7,
                    "cvss_applicable": False,
                    "primitive": {
                        "component": "session",
                        "root_cause_anchor": {"symbol": "accept_sid", "locations": ["src/a.c:10"]},
                        "capabilities_gained": [
                            {
                                "kind": "object_reference",
                                "object_type": "session",
                                "principal": "victim",
                                "address_space": "server-process",
                            }
                        ],
                    },
                },
                "review_history": [],
            }

            update = nodes.finalize_subtask(state)

            self.assertEqual(len(update["confirmed_primitives"]), 1)
            primitive = update["confirmed_primitives"][0]
            self.assertTrue(primitive["primitive_id"].startswith("prim_"))
            self.assertEqual(update["observations"][0]["outcome_type"], "confirmed_primitive")
            self.assertFalse(update["observations"][0]["qualification_gate_passed"])
            self.assertTrue((ws.log_path("primitive_res") / f"{primitive['primitive_id']}.json").is_file())


class ChainPlanningTest(unittest.TestCase):
    def test_materialize_chain_pool_ignores_stale_package_primitive(self):
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="libfoo", task_id="chain-pool-package")
            result_dir = ws.log_path("subtask_res")
            active_path = result_dir / "spec-028--active.json"
            active_primitive = {
                **_primitive_a(),
                "source_subtask_ids": ["spec-028--hyp-active"],
                "component": "active",
            }
            stale_primitive = {
                **_primitive_b(),
                "source_subtask_ids": ["spec-028--hyp-stale"],
                "component": "stale",
            }
            (result_dir / "spec-028.json").write_text(
                json.dumps(
                    {
                        "result_type": "hypothesis_package",
                        "package_id": "spec-028",
                        "artifacts": [
                            {"hypothesis_id": "hyp-active", "path": str(active_path)}
                        ],
                    }
                )
            )
            active_path.write_text(
                json.dumps(
                    {
                        "package_id": "spec-028",
                        "outcome_type": "confirmed_primitive",
                        "primitive": active_primitive,
                    }
                )
            )
            (result_dir / "spec-028--stale.json").write_text(
                json.dumps(
                    {
                        "package_id": "spec-028",
                        "outcome_type": "confirmed_primitive",
                        "primitive": stale_primitive,
                    }
                )
            )
            for primitive in (active_primitive, stale_primitive):
                (ws.log_path("primitive_res") / f"{primitive['component']}.json").write_text(
                    json.dumps(primitive)
                )

            update = nodes.materialize_chain_pool(_workspace_state(ws))

            self.assertEqual(
                [item["component"] for item in update["chain_pool"]],
                ["active"],
            )
            self.assertEqual(
                [item["component"] for item in graph_mod._primitive_res_payloads(ws)],
                ["active"],
            )

    def test_restore_does_not_publish_primitive_from_uncommitted_package(self):
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="libfoo", task_id="chain-pool-orphan")
            primitive = {
                **_primitive_a(),
                "source_subtask_ids": ["spec-028--hyp-orphan"],
                "component": "orphan",
            }
            (ws.log_path("subtask_res") / "spec-028--orphan.json").write_text(
                json.dumps(
                    {
                        "package_id": "spec-028",
                        "outcome_type": "confirmed_primitive",
                        "primitive": primitive,
                    }
                )
            )
            (ws.log_path("primitive_res") / "orphan.json").write_text(
                json.dumps(primitive)
            )

            update = nodes.materialize_chain_pool(_workspace_state(ws))

            self.assertEqual(update["chain_pool"], [])
            self.assertEqual(graph_mod._primitive_res_payloads(ws), [])

    def test_plan_chains_is_native_subagent_required(self):
        for runtime in ("codex", "traex", "claude_code"):
            variants = nodes.agent_config_variants_for_node(
                "plan_chains", None, {"plan_chains": {"runtime": runtime}}
            )
            self.assertEqual(variants[0]["runtime"], runtime)
        with self.assertRaisesRegex(ValueError, r"unsupported runtime\(s\): kimi"):
            nodes.agent_config_variants_for_node(
                "plan_chains", None, {"plan_chains": {"runtime": "kimi"}}
            )

    def _fake_chain_planner(self, payload):
        def run(*args, **kwargs):
            del args
            res = AgentResult(
                stdout=json.dumps(payload),
                stderr="",
                returncode=0,
                backend="codex",
                cwd="",
            )
            ok, detail = kwargs["validate"](res)
            return res, [] if ok else [detail]

        return run

    def test_plan_chains_uses_capability_closure_and_skips_unrelated_terminal(self):
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="libfoo", task_id="chain-plan")
            unrelated_terminal = {
                **_primitive_b(),
                "primitive_id": "prim_unrelated_terminal",
                "required_capabilities": [],
            }
            state = {
                **_workspace_state(ws),
                "chain_pool": [_primitive_a(), _primitive_b(), unrelated_terminal],
                "top_K": {"chain": 8},
            }

            payload = {
                "chains": [
                    {
                        "ordered_primitive_ids": ["prim_a", "prim_b"],
                        "attacker_entry": {"capabilities": [_primitive_a()["required_capabilities"][0]]},
                        "bindings": [
                            {
                                "consumer_primitive_id": "prim_a",
                                "required_capability": _primitive_a()["required_capabilities"][0],
                                "provider": {
                                    "type": "attacker_entry",
                                    "capability": _primitive_a()["required_capabilities"][0],
                                },
                                "compatibility_reason": "attacker can supply the initial controlled request",
                                "evidence": ["src/a.c:10"],
                            },
                            {
                                "consumer_primitive_id": "prim_b",
                                "required_capability": _primitive_b()["required_capabilities"][0],
                                "provider": {
                                    "type": "primitive",
                                    "primitive_id": "prim_a",
                                    "capability": _primitive_a()["capabilities_gained"][0],
                                },
                                "compatibility_reason": "primitive A provides the victim session object consumed by B",
                                "evidence": ["src/a.c:10", "src/b.c:20"],
                            }
                        ],
                        "expected_terminal_impact": _primitive_b()["terminal_impact"],
                        "rank_score": 0.9,
                    }
                ]
            }
            state["chain_config"] = {
                "attacker_entry_capabilities": [_primitive_a()["required_capabilities"][0]]
            }
            with patch("zeromdash.nodes._invoke_with_output_retry", side_effect=self._fake_chain_planner(payload)):
                update = nodes.plan_chains(state)

            chains = update["chain_plan"]
            self.assertEqual(len(chains), 1)
            self.assertEqual(chains[0]["ordered_primitive_ids"], ["prim_a", "prim_b"])
            self.assertEqual(chains[0]["status"], "planned")
            plan = json.loads(ws.state_path("chain_plan.json").read_text())
            self.assertEqual(plan["chain_count"], 1)
            self.assertEqual(plan["planned_by"], "agent")
            prefilter = json.loads((ws.log_path("review_log") / "chain_prefilter.json").read_text())
            self.assertEqual(prefilter["chain_count"], 1)
            pruning = (ws.log_path("review_log") / "chain_pruning.jsonl").read_text()
            self.assertIn("successor has no requirement", pruning)

    def test_plan_chains_accepts_agent_semantic_repair_after_prefilter_miss(self):
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="libfoo", task_id="chain-plan-agent")
            producer = {
                **_primitive_a(),
                "capabilities_gained": [
                    {
                        "kind": "object_reference",
                        "object_type": "session_handle",
                        "scope": "same-service",
                        "principal": "victim",
                        "tenant": "same-tenant",
                        "address_space": "server-process",
                    }
                ],
                "handoff_objects": [{"type": "session-handle", "evidence": ["src/a.c:10"]}],
            }
            state = {
                **_workspace_state(ws),
                "chain_pool": [producer, _primitive_b()],
                "top_K": {"chain": 8},
                "chain_config": {
                    "attacker_entry_capabilities": [_primitive_a()["required_capabilities"][0]]
                },
            }
            payload = {
                "chains": [
                    {
                        "ordered_primitive_ids": ["prim_a", "prim_b"],
                        "attacker_entry": {"capabilities": [_primitive_a()["required_capabilities"][0]]},
                        "bindings": [
                            {
                                "consumer_primitive_id": "prim_a",
                                "required_capability": _primitive_a()["required_capabilities"][0],
                                "provider": {
                                    "type": "attacker_entry",
                                    "capability": _primitive_a()["required_capabilities"][0],
                                },
                                "compatibility_reason": "attacker can supply the initial controlled request",
                                "evidence": ["src/a.c:10"],
                            },
                            {
                                "consumer_primitive_id": "prim_b",
                                "required_capability": _primitive_b()["required_capabilities"][0],
                                "provider": {
                                    "type": "primitive",
                                    "primitive_id": "prim_a",
                                    "capability": producer["capabilities_gained"][0],
                                },
                                "compatibility_reason": (
                                    "source evidence shows the session_handle is the session object "
                                    "later dereferenced by read_profile"
                                ),
                                "evidence": ["src/a.c:10", "src/b.c:20"],
                            }
                        ],
                        "expected_terminal_impact": _primitive_b()["terminal_impact"],
                        "rank_score": 0.7,
                    }
                ]
            }
            with patch("zeromdash.nodes._invoke_with_output_retry", side_effect=self._fake_chain_planner(payload)):
                update = nodes.plan_chains(state)

            prefilter = json.loads((ws.log_path("review_log") / "chain_prefilter.json").read_text())
            self.assertEqual(prefilter["chain_count"], 0)
            self.assertEqual(update["chain_plan"][0]["ordered_primitive_ids"], ["prim_a", "prim_b"])
            self.assertIn("session_handle", update["chain_plan"][0]["bindings"][1]["compatibility_reason"])

    def test_plan_chains_does_not_require_configured_attacker_entry_capabilities(self):
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="libfoo", task_id="chain-plan-no-entry-config")
            state = {
                **_workspace_state(ws),
                "chain_pool": [_primitive_a(), _primitive_b()],
                "top_K": {"chain": 8},
            }
            attacker_cap = {
                **_primitive_a()["required_capabilities"][0],
                "properties": ["agent-inferred from primitive evidence"],
            }
            payload = {
                "chains": [
                    {
                        "ordered_primitive_ids": ["prim_a", "prim_b"],
                        "attacker_entry": {"capabilities": [attacker_cap]},
                        "bindings": [
                            {
                                "consumer_primitive_id": "prim_a",
                                "required_capability": _primitive_a()["required_capabilities"][0],
                                "provider": {
                                    "type": "attacker_entry",
                                    "capability": attacker_cap,
                                },
                                "compatibility_reason": "agent inferred the initial attacker request from primitive evidence",
                                "evidence": ["src/a.c:10"],
                            },
                            {
                                "consumer_primitive_id": "prim_b",
                                "required_capability": _primitive_b()["required_capabilities"][0],
                                "provider": {
                                    "type": "primitive",
                                    "primitive_id": "prim_a",
                                    "capability": _primitive_a()["capabilities_gained"][0],
                                },
                                "compatibility_reason": "primitive A provides the victim session object consumed by B",
                                "evidence": ["src/a.c:10", "src/b.c:20"],
                            },
                        ],
                        "expected_terminal_impact": _primitive_b()["terminal_impact"],
                        "rank_score": 0.6,
                    }
                ]
            }
            with patch("zeromdash.nodes._invoke_with_output_retry", side_effect=self._fake_chain_planner(payload)):
                update = nodes.plan_chains(state)

            prefilter = json.loads((ws.log_path("review_log") / "chain_prefilter.json").read_text())
            self.assertEqual(prefilter["chain_count"], 0)
            self.assertEqual(update["chain_plan"][0]["attacker_entry"]["capabilities"][0]["properties"], attacker_cap["properties"])

    def test_plan_chains_rejects_binding_that_invents_provider_capability(self):
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="libfoo", task_id="chain-plan-invented")
            invented = {**_primitive_a()["capabilities_gained"][0], "object_type": "invented-object"}
            payload = {
                "chains": [
                    {
                        "ordered_primitive_ids": ["prim_a", "prim_b"],
                        "attacker_entry": {"capabilities": [_primitive_a()["required_capabilities"][0]]},
                        "bindings": [
                            {
                                "consumer_primitive_id": "prim_a",
                                "required_capability": _primitive_a()["required_capabilities"][0],
                                "provider": {"type": "attacker_entry", "capability": _primitive_a()["required_capabilities"][0]},
                                "compatibility_reason": "entry",
                                "evidence": ["src/a.c:10"],
                            },
                            {
                                "consumer_primitive_id": "prim_b",
                                "required_capability": _primitive_b()["required_capabilities"][0],
                                "provider": {"type": "primitive", "primitive_id": "prim_a", "capability": invented},
                                "compatibility_reason": "invented by planner",
                                "evidence": ["src/a.c:10", "src/b.c:20"],
                            },
                        ],
                    }
                ]
            }
            state = {
                **_workspace_state(ws),
                "chain_pool": [_primitive_a(), _primitive_b()],
                "chain_config": {"attacker_entry_capabilities": [_primitive_a()["required_capabilities"][0]]},
                "top_K": {"chain": 8},
            }
            with patch("zeromdash.nodes._invoke_with_output_retry", side_effect=self._fake_chain_planner(payload)):
                update = nodes.plan_chains(state)

            self.assertEqual(update["chain_plan"], [])
            plan = json.loads(ws.state_path("chain_plan.json").read_text())
            self.assertIn("invents a capability", "; ".join(plan["validation_errors"]))


class ChainFinalizeTest(unittest.TestCase):
    def _simple_candidate(self) -> tuple[dict, list[dict]]:
        binding_a = {
            "consumer_primitive_id": "prim_a",
            "required_capability": _primitive_a()["required_capabilities"][0],
            "provider": {
                "type": "attacker_entry",
                "capability": _primitive_a()["required_capabilities"][0],
            },
            "compatibility_reason": "entry",
            "evidence": ["src/a.c:10"],
        }
        binding_b = {
            "consumer_primitive_id": "prim_b",
            "required_capability": _primitive_b()["required_capabilities"][0],
            "provider": {
                "type": "primitive",
                "primitive_id": "prim_a",
                "capability": _primitive_a()["capabilities_gained"][0],
            },
            "compatibility_reason": "handoff",
            "evidence": ["src/a.c:10", "src/b.c:20"],
        }
        binding_a["edge_id"] = nodes.stable_edge_id(binding_a, 0)
        binding_b["edge_id"] = nodes.stable_edge_id(binding_b, 1)
        candidate = {
            "chain_id": "chain_simple",
            "ordered_primitive_ids": ["prim_a", "prim_b"],
            "attacker_entry": {"capabilities": [_primitive_a()["required_capabilities"][0]]},
            "bindings": [binding_a, binding_b],
            "global_constraints": {},
            "expected_terminal_impact": {},
        }
        return candidate, [binding_a, binding_b]

    def _simple_investigation(self, bindings: list[dict], facts: dict | None = None) -> dict:
        return {
            "title": "simple chain",
            "detail": "confirmed chain",
            "ordered_primitive_ids": ["prim_a", "prim_b"],
            "bindings": bindings,
            "binding_claims": [
                {
                    "edge_id": binding["edge_id"],
                    "claim": binding["compatibility_reason"],
                    "registry_refs": [],
                    "evidence": ["src/a.c:10", "src/b.c:20"],
                }
                for binding in bindings
            ],
            "emergent_transitions": [
                {
                    "transition_id": "emergent-simple",
                    "combined_operation": "compose",
                    "resulting_state": "impact",
                    "violated_invariant_ids": [],
                    "evidence": ["src/b.c:20"],
                }
            ],
            "evidence": {"code_locations": ["src/a.c:10", "src/b.c:20"], "call_path": ["a -> b"]},
            "direct_security_impact": _primitive_b()["terminal_impact"],
            "violated_security_property": "simple property",
            "cvss4_vector": _CVSS4_C_HIGH_VECTOR,
            **(
                facts
                if facts is not None
                else {
                    "blocking_unmet_facts": [],
                    "validation_gaps": [],
                    "deployment_constraints": [],
                    "impact_limits": [],
                }
            ),
        }

    def _simple_review(self, bindings: list[dict], fact_verdicts: list[dict] | None = None) -> dict:
        return {
            "verdict": "confirm",
            "reasoning": "confirmed",
            "all_primitives_confirmed": True,
            "bindings_valid": True,
            "global_constraints_satisfiable": True,
            "required_external_primitives": [],
            "direct_security_impact": _primitive_b()["terminal_impact"],
            "violated_security_property": "simple property",
            "cvss4_vector": _CVSS4_C_HIGH_VECTOR,
            "selected_skills": [],
            "edge_verdicts": [
                {
                    "edge_id": binding["edge_id"],
                    "verdict": "confirm",
                    "reasoning": "verified",
                    "evidence": ["src/a.c:10", "src/b.c:20"],
                }
                for binding in bindings
            ],
            "transition_verdicts": [
                {
                    "transition_id": "emergent-simple",
                    "verdict": "confirm",
                    "reasoning": "verified",
                    "evidence": ["src/b.c:20"],
                }
            ],
            "emergent_impact_verdict": {
                "confirmed": True,
                "reasoning": "confirmed impact",
                "evidence": ["src/b.c:20"],
            },
            "closure_verdict": "closed",
            "fact_verdicts": list(fact_verdicts or []),
        }

    def test_legacy_unmet_facts_are_not_reclassified_by_python(self):
        candidate, bindings = self._simple_candidate()
        investigation = self._simple_investigation(
            bindings,
            facts={"unmet_facts": ["needs runtime trace"]},
        )
        review = self._simple_review(bindings)

        finding, failed, failures = nodes.close_chain_candidate(
            candidate=candidate,
            investigation=investigation,
            review=review,
            chain_pool=[_primitive_a(), _primitive_b()],
            domain_registry=nodes.legacy_domain_registry("libfoo"),
        )

        self.assertIsNone(finding)
        self.assertIsNotNone(failed)
        self.assertTrue(any("missing chain fact verdict" in item for item in failures))

    def test_nonblocking_chain_facts_close_only_with_critic_verdicts(self):
        candidate, bindings = self._simple_candidate()
        validation_gap = _nonblocking_fact("fact_validation", "runtime trace missing", ["src/b.c:20"])
        deployment = _nonblocking_fact("fact_deploy", "non-default config", ["src/a.c:10"])
        impact_limit = _nonblocking_fact("fact_impact", "availability only", ["src/b.c:20"])
        investigation = self._simple_investigation(
            bindings,
            facts={
                "blocking_unmet_facts": [],
                "validation_gaps": [validation_gap],
                "deployment_constraints": [deployment],
                "impact_limits": [impact_limit],
            },
        )
        review = self._simple_review(
            bindings,
            fact_verdicts=[
                _fact_verdict(validation_gap, "validation_gap"),
                _fact_verdict(deployment, "deployment_constraint"),
                _fact_verdict(impact_limit, "impact_limit"),
            ],
        )

        finding, failed, failures = nodes.close_chain_candidate(
            candidate=candidate,
            investigation=investigation,
            review=review,
            chain_pool=[_primitive_a(), _primitive_b()],
            domain_registry=nodes.legacy_domain_registry("libfoo"),
        )

        self.assertIsNotNone(finding)
        self.assertIsNone(failed)
        self.assertEqual(failures, [])
        self.assertEqual(finding["closure_verdict"], "closed")
        self.assertEqual(len(finding["fact_verdicts"]), 3)

    def test_finalize_chain_outputs_finding_only_after_closure_gate(self):
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="libfoo", task_id="chain-finalize")
            payload = {
                "chains": [
                    {
                        "ordered_primitive_ids": ["prim_a", "prim_b"],
                        "attacker_entry": {"capabilities": [_primitive_a()["required_capabilities"][0]]},
                        "bindings": [
                            {
                                "consumer_primitive_id": "prim_a",
                                "required_capability": _primitive_a()["required_capabilities"][0],
                                "provider": {
                                    "type": "attacker_entry",
                                    "capability": _primitive_a()["required_capabilities"][0],
                                },
                                "compatibility_reason": "attacker can supply the initial controlled request",
                                "evidence": ["src/a.c:10"],
                            },
                            {
                                "consumer_primitive_id": "prim_b",
                                "required_capability": _primitive_b()["required_capabilities"][0],
                                "provider": {
                                    "type": "primitive",
                                    "primitive_id": "prim_a",
                                    "capability": _primitive_a()["capabilities_gained"][0],
                                },
                                "compatibility_reason": "primitive A provides the victim session object consumed by B",
                                "evidence": ["src/a.c:10", "src/b.c:20"],
                            }
                        ],
                        "expected_terminal_impact": _primitive_b()["terminal_impact"],
                    }
                ]
            }
            with patch("zeromdash.nodes._invoke_with_output_retry", side_effect=ChainPlanningTest()._fake_chain_planner(payload)):
                candidate = nodes.plan_chains(
                    {
                        **_workspace_state(ws),
                        "chain_pool": [_primitive_a(), _primitive_b()],
                        "top_K": {"chain": 1},
                    }
                )["chain_plan"][0]
            investigation = {
                "title": "session reference chains to profile disclosure",
                "detail": "primitive A provides the victim session reference consumed by primitive B",
                "ordered_primitive_ids": ["prim_a", "prim_b"],
                "bindings": candidate["bindings"],
                "binding_claims": [
                    {
                        "edge_id": binding["edge_id"],
                        "provider_primitive_id": (binding.get("provider") or {}).get("primitive_id", ""),
                        "consumer_primitive_id": binding["consumer_primitive_id"],
                        "registry_refs": [],
                        "claim": binding["compatibility_reason"],
                        "evidence": ["src/a.c:10", "src/b.c:20"],
                        "deterministic_advisories": [],
                    }
                    for binding in candidate["bindings"]
                ],
                "emergent_transitions": [
                    {
                        "transition_id": "emergent-profile-disclosure",
                        "input_states": ["victim session reference"],
                        "combined_operation": "reuse victim session in profile reader",
                        "resulting_state": "victim profile disclosed",
                        "violated_invariant_ids": [],
                        "evidence": ["src/a.c:10", "src/b.c:20"],
                    }
                ],
                "evidence": {
                    "code_locations": ["src/a.c:10", "src/b.c:20"],
                    "call_path": ["entry -> accept_sid", "read_profile -> leak"],
                },
                "direct_security_impact": _primitive_b()["terminal_impact"],
                "violated_security_property": "victim profile data must not be disclosed cross-session",
                "cvss4_vector": _CVSS4_C_HIGH_VECTOR,
                "confidence": 0.8,
                "blocking_unmet_facts": [],
                "validation_gaps": [],
                "deployment_constraints": [],
                "impact_limits": [],
            }
            review = {
                "verdict": "confirm",
                "reasoning": "all bindings and terminal impact are confirmed",
                "all_primitives_confirmed": True,
                "bindings_valid": True,
                "global_constraints_satisfiable": True,
                "required_external_primitives": [],
                "violated_security_property": "victim profile data must not be disclosed cross-session",
                "direct_security_impact": _primitive_b()["terminal_impact"],
                "cvss4_vector": _CVSS4_C_HIGH_VECTOR,
                "selected_skills": [],
                "confidence": 0.8,
                "edge_verdicts": [
                    {
                        "edge_id": binding["edge_id"],
                        "verdict": "confirm",
                        "reasoning": "source evidence confirms the handoff",
                        "evidence": ["src/a.c:10", "src/b.c:20"],
                    }
                    for binding in candidate["bindings"]
                ],
                "transition_verdicts": [
                    {
                        "transition_id": "emergent-profile-disclosure",
                        "verdict": "confirm",
                        "reasoning": "the combined operation reaches the disclosure state",
                        "evidence": ["src/a.c:10", "src/b.c:20"],
                    }
                ],
                "emergent_impact_verdict": {
                    "confirmed": True,
                    "reasoning": "the composition discloses victim profile data",
                    "evidence": ["src/a.c:10", "src/b.c:20"],
                    "violated_invariant_ids": [],
                },
                **_closed_fact_contract(),
            }
            state = {
                **_workspace_state(ws),
                "chain_candidate": candidate,
                "chain_pool": [_primitive_a(), _primitive_b()],
                "chain_investigation": json.dumps(investigation),
                "chain_review": review,
                "iteration": 1,
                "chain_review_history": [],
            }

            update = nodes.finalize_chain_subtask(state)

            self.assertEqual(len(update["chain_findings"]), 1)
            finding = update["chain_findings"][0]
            self.assertEqual(finding["chain_id"], candidate["chain_id"])
            self.assertTrue(finding["qualification_gate_passed"])
            self.assertEqual(finding["ordered_primitive_ids"], ["prim_a", "prim_b"])
            self.assertTrue((ws.log_path("chain_res") / f"{candidate['chain_id']}.json").is_file())

    def test_finalize_chain_agent_can_promote_confirmed_contract_mismatch(self):
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="libfoo", task_id="chain-agent-finalize")
            candidate, bindings = self._simple_candidate()
            investigation = self._simple_investigation(bindings)
            investigation["binding_claims"][1]["edge_id"] = "edge_semantic_handoff"
            review = self._simple_review(bindings)
            review["edge_verdicts"][1]["edge_id"] = "edge_semantic_handoff"
            finalizer = {
                "decision": "accept",
                "reasoning": "The only failures are edge-id contract mismatches; the binding is semantically identical and source-backed.",
                "chain_is_valid": True,
                "deterministic_failures_are_contract_only": True,
                "all_primitives_confirmed": True,
                "bindings_valid": True,
                "global_constraints_satisfiable": True,
                "no_external_primitives_required": True,
                "direct_security_impact": _primitive_b()["terminal_impact"],
                "cvss4_vector": _CVSS4_C_HIGH_VECTOR,
                "confidence": 0.83,
                "title": "agent-finalized chain",
                "detail": "A confirmed chain accepted despite deterministic edge-id mismatch.",
                "violated_security_property": "simple property",
                "evidence": {
                    "code_locations": ["src/a.c:10", "src/b.c:20"],
                    "call_path": ["entry -> accept_sid", "read_profile -> leak"],
                },
                "scope_verdict": "full_repository",
                "gate_decision": "ignore",
                "accepted_failure_reasons": ["edge id mismatch"],
                "blocking_failure_reasons": [],
            }
            result = AgentResult(
                stdout=json.dumps(finalizer),
                stderr="",
                returncode=0,
                backend="codex",
            )
            state = {
                **_workspace_state(ws),
                "chain_candidate": candidate,
                "chain_pool": [_primitive_a(), _primitive_b()],
                "chain_investigation": json.dumps(investigation),
                "chain_review": review,
                "iteration": 1,
                "chain_review_history": [],
            }

            with patch.object(nodes, "_make_agent", return_value=object()), patch.object(
                nodes,
                "_run_agent_with_config",
                return_value=result,
            ):
                update = nodes.finalize_chain_subtask(state)

            self.assertEqual(len(update["chain_findings"]), 1)
            finding = update["chain_findings"][0]
            self.assertEqual(finding["title"], "agent-finalized chain")
            self.assertTrue(finding["qualification_gate_passed"])
            self.assertIn("deterministic_gate_failures", finding)
            payload = json.loads((ws.log_path("chain_res") / f"{candidate['chain_id']}.json").read_text())
            self.assertEqual(payload["outcome_type"], "chain_finding")
            self.assertEqual(payload["finalizer"]["decision"], "accept")

    def test_finalize_chain_agent_reject_keeps_candidate_out_of_chain_res(self):
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="libfoo", task_id="chain-agent-reject")
            candidate, bindings = self._simple_candidate()
            investigation = self._simple_investigation(bindings)
            investigation["binding_claims"][1]["edge_id"] = "edge_semantic_handoff"
            review = self._simple_review(bindings)
            review["edge_verdicts"][1]["edge_id"] = "edge_semantic_handoff"
            finalizer = {
                "decision": "reject",
                "reasoning": "The mismatch hides a real missing handoff.",
                "chain_is_valid": False,
                "deterministic_failures_are_contract_only": False,
                "all_primitives_confirmed": True,
                "bindings_valid": False,
                "global_constraints_satisfiable": True,
                "no_external_primitives_required": True,
                "direct_security_impact": _primitive_b()["terminal_impact"],
                "cvss4_vector": _CVSS4_C_HIGH_VECTOR,
                "confidence": 0.5,
                "title": "rejected chain",
                "detail": "Rejected.",
                "evidence": {"code_locations": ["src/a.c:10"]},
                "accepted_failure_reasons": [],
                "blocking_failure_reasons": ["missing handoff"],
            }
            result = AgentResult(
                stdout=json.dumps(finalizer),
                stderr="",
                returncode=0,
                backend="codex",
            )
            state = {
                **_workspace_state(ws),
                "chain_candidate": candidate,
                "chain_pool": [_primitive_a(), _primitive_b()],
                "chain_investigation": json.dumps(investigation),
                "chain_review": review,
                "iteration": 1,
                "chain_review_history": [],
            }

            with patch.object(nodes, "_make_agent", return_value=object()), patch.object(
                nodes,
                "_run_agent_with_config",
                return_value=result,
            ):
                update = nodes.finalize_chain_subtask(state)

            self.assertIn("chain_candidates", update)
            self.assertFalse((ws.log_path("chain_res") / f"{candidate['chain_id']}.json").exists())
            self.assertTrue((ws.log_path("chain_candidates") / f"{candidate['chain_id']}.json").is_file())

    def test_finalize_chain_accepts_agent_confirmed_emergent_impact_without_primitive_terminal_impact(self):
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="libfoo", task_id="emergent-chain")
            primitive_a = {
                **_primitive_a(),
                "terminal_impact": {},
                "capabilities_gained": [
                    {
                        **_primitive_a()["capabilities_gained"][0],
                        "object_type": "session_handle",
                    }
                ],
            }
            primitive_b = {**_primitive_b(), "terminal_impact": {}}
            attacker_binding = {
                "consumer_primitive_id": "prim_a",
                "required_capability": primitive_a["required_capabilities"][0],
                "provider": {
                    "type": "attacker_entry",
                    "capability": primitive_a["required_capabilities"][0],
                },
                "compatibility_reason": "attacker supplies the initial request",
                "evidence": ["src/a.c:10"],
            }
            binding = {
                "consumer_primitive_id": "prim_b",
                "required_capability": primitive_b["required_capabilities"][0],
                "provider": {
                    "type": "primitive",
                    "primitive_id": "prim_a",
                    "capability": primitive_a["capabilities_gained"][0],
                },
                "compatibility_reason": "agent-confirmed semantic handoff",
                "evidence": ["src/a.c:10", "src/b.c:20"],
            }
            from zeromdash.nodes.core.chain_compatibility import stable_edge_id
            attacker_binding["edge_id"] = stable_edge_id(attacker_binding, 0)
            binding["edge_id"] = stable_edge_id(binding, 1)
            compatible, reasons = nodes.capability_compatible(
                binding["provider"]["capability"],
                binding["required_capability"],
                provider_primitive=primitive_a,
                consumer_primitive=primitive_b,
            )
            self.assertFalse(compatible)
            self.assertIn("object_scope_mismatch", reasons)
            candidate = {
                "chain_id": "chain_emergent",
                "ordered_primitive_ids": ["prim_a", "prim_b"],
                "attacker_entry": {"capabilities": [primitive_a["required_capabilities"][0]]},
                "bindings": [attacker_binding, binding],
                "global_constraints": {},
                "expected_terminal_impact": {},
            }
            impact = {
                "vulnerable_system": {"confidentiality": "high", "integrity": "none", "availability": "none"},
                "subsequent_system": {"confidentiality": "none", "integrity": "none", "availability": "none"},
            }
            investigation = {
                "title": "emergent disclosure",
                "detail": "neither primitive has impact alone; composition violates isolation",
                "ordered_primitive_ids": ["prim_a", "prim_b"],
                "bindings": [attacker_binding, binding],
                "binding_claims": [
                    {"edge_id": attacker_binding["edge_id"], "claim": "attacker reaches primitive A", "registry_refs": [], "evidence": ["src/a.c:10"]},
                    {"edge_id": binding["edge_id"], "claim": "same object across the handoff", "registry_refs": [], "evidence": ["src/a.c:10", "src/b.c:20"]},
                ],
                "emergent_transitions": [{"transition_id": "emergent-1", "combined_operation": "compose references", "resulting_state": "disclosure", "violated_invariant_ids": [], "evidence": ["src/b.c:20"]}],
                "evidence": {"code_locations": ["src/a.c:10", "src/b.c:20"], "call_path": ["a -> b"]},
                "direct_security_impact": impact,
                "violated_security_property": "cross-session isolation",
                "cvss4_vector": _CVSS4_C_HIGH_VECTOR,
                "blocking_unmet_facts": [],
                "validation_gaps": [],
                "deployment_constraints": [],
                "impact_limits": [],
            }
            review = {
                "verdict": "confirm",
                "all_primitives_confirmed": True,
                "bindings_valid": True,
                "global_constraints_satisfiable": True,
                "required_external_primitives": [],
                "direct_security_impact": impact,
                "violated_security_property": "cross-session isolation",
                "cvss4_vector": _CVSS4_C_HIGH_VECTOR,
                "selected_skills": [],
                "edge_verdicts": [
                    {"edge_id": attacker_binding["edge_id"], "verdict": "confirm", "reasoning": "verified entry", "evidence": ["src/a.c:10"]},
                    {"edge_id": binding["edge_id"], "verdict": "confirm", "reasoning": "verified", "evidence": ["src/a.c:10", "src/b.c:20"]},
                ],
                "transition_verdicts": [{"transition_id": "emergent-1", "verdict": "confirm", "reasoning": "verified composition", "evidence": ["src/b.c:20"]}],
                "emergent_impact_verdict": {"confirmed": True, "reasoning": "composition creates impact", "evidence": ["src/b.c:20"]},
                **_closed_fact_contract(),
            }
            update = nodes.finalize_chain_subtask({**_workspace_state(ws), "chain_candidate": candidate, "chain_pool": [primitive_a, primitive_b], "chain_investigation": json.dumps(investigation), "chain_review": review, "iteration": 1, "chain_review_history": []})
            self.assertEqual(len(update["chain_findings"]), 1)


if __name__ == "__main__":
    unittest.main()
