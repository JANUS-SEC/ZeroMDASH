"""Unit tests for critic_subtask skill-selection post-processing."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from zeromdash import nodes
from zeromdash.agents import AgentResult
from zeromdash.workspace import Workspace


_QUALIFIED_REVIEW = {
    "disposition": "confirmed_vulnerability",
    "documented_expected_behavior": False,
    "security_contract_violation": True,
    "violated_security_property": "validated input must not corrupt privileged state",
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
    "cvss4_vector": (
        "CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/"
        "VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"
    ),
}


class _FakeAgent:
    def __init__(self, stdout: str, returncode: int = 0) -> None:
        self.stdout = stdout
        self.returncode = returncode
        self.prompts: list[str] = []
        self.cwd: Path | None = None
        self.extra_args = None
        self.env = None

    def run(self, prompt: str, cwd=None, timeout=None, extra_args=None, env=None):
        del timeout
        self.prompts.append(prompt)
        self.cwd = Path(cwd)
        self.extra_args = extra_args
        self.env = env
        return AgentResult(
            stdout=self.stdout,
            stderr="boom" if self.returncode else "",
            returncode=self.returncode,
            backend="codex",
            cwd=str(cwd),
        )


def _write_skill(root: Path, name: str, summary: str) -> None:
    skill_file = root / "skills" / f"{name}.md"
    skill_file.parent.mkdir(parents=True, exist_ok=True)
    skill_file.write_text(f"---\nsummary: {summary}\n---\n")


def _state(ws: Workspace, *, min_skills: int = 2) -> dict:
    return {
        "target": "libfoo",
        "task_id": ws.task_id,
        "workspace_root": str(ws.root),
        "repo_path": str(ws.main_path("repo")),
        "subtask": {"id": "patch-001", "bucket": "patch_miss", "objective": "review patch"},
        "iteration": 1,
        "investigation": '{"title": "maybe bug"}',
        "review_history": [],
        "min_critic_skills": min_skills,
    }


class CriticOneSkillSelectionTest(unittest.TestCase):
    def _run_critic(
        self,
        review: dict,
        *,
        min_skills: int = 2,
        returncode: int = 0,
        state_overrides: dict | None = None,
    ):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        presets_root = root / "presets"
        _write_skill(presets_root, "memory", "Memory-safety lens")
        _write_skill(presets_root, "parser", "Parser/state-machine lens")
        ws = Workspace.create(root / "workspaces", target="libfoo", task_id="critic")
        fake_agent = _FakeAgent(json.dumps(review), returncode=returncode)
        state = _state(ws, min_skills=min_skills)
        state.update(state_overrides or {})

        with patch.object(nodes.presets, "default_presets_dir", return_value=presets_root), patch.object(
            nodes, "_make_agent", return_value=fake_agent
        ):
            update = nodes.critic_subtask(state, backends={"critic_subtask": "codex"})

        return update, ws, fake_agent

    def test_filters_unknown_selected_skills_and_marks_selection_incomplete(self):
        review = {
            "verdict": "revise",
            "reasoning": "needs more proof",
            "severity": "medium",
            "confidence": 0.4,
            "selected_skills": ["memory", "does-not-exist"],
            "feedback": {"gaps": ["original gap"], "requested_evidence": []},
        }

        update, ws, fake_agent = self._run_critic(review, min_skills=2)

        processed = update["review"]
        self.assertEqual(processed["selected_skills"], ["memory"])
        self.assertEqual(processed["available_skills"], ["memory", "parser"])
        self.assertFalse(processed["skill_selection_ok"])
        self.assertIn("original gap", processed["feedback"]["gaps"])
        self.assertIn("critic selected 1 skill(s); required >= 2", processed["feedback"]["gaps"])
        self.assertEqual(update["review_history"][0]["review"], processed)
        self.assertIn("- `memory`", fake_agent.prompts[0])
        self.assertTrue((fake_agent.cwd / "skills_catalog.md").is_file())
        self.assertTrue((ws.log_path("review_log") / "patch-001.review.log").is_file())

    def test_keeps_valid_selection_and_marks_selection_ok(self):
        review = {
            "verdict": "confirm",
            "reasoning": "looks real",
            "confidence": 0.8,
            "selected_skills": ["memory", "parser"],
            "feedback": {"gaps": [], "requested_evidence": []},
            **_QUALIFIED_REVIEW,
        }

        update, _, _ = self._run_critic(review, min_skills=2)

        processed = update["review"]
        self.assertEqual(processed["selected_skills"], ["memory", "parser"])
        self.assertTrue(processed["skill_selection_ok"])
        self.assertEqual(processed["feedback"]["gaps"], [])
        self.assertEqual(update["errors"], [])

    def test_agent_failure_is_reported_in_errors(self):
        review = {"verdict": "revise", "selected_skills": ["memory", "parser"], "feedback": {}}

        update, _, _ = self._run_critic(review, min_skills=2, returncode=7)

        self.assertEqual(update["errors"], ["[critic_subtask/patch-001] backend=codex rc=7: boom"])

    def test_array_review_output_is_coerced_to_revise(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        presets_root = root / "presets"
        _write_skill(presets_root, "memory", "Memory-safety lens")
        _write_skill(presets_root, "parser", "Parser/state-machine lens")
        ws = Workspace.create(root / "workspaces", target="libfoo", task_id="critic-array")
        fake_agent = _FakeAgent(json.dumps([{"verdict": "confirm"}]))

        with patch.object(nodes.presets, "default_presets_dir", return_value=presets_root), patch.object(
            nodes, "_make_agent", return_value=fake_agent
        ):
            update = nodes.critic_subtask(_state(ws), backends={"critic_subtask": "codex"})

        review = update["review"]
        self.assertEqual(review["verdict"], "revise")
        self.assertEqual(review["invalid_review_shape"], "list")
        self.assertEqual(review["raw"], '[{"verdict": "confirm"}]')
        self.assertEqual(update["review_history"][0]["review"], review)

    def test_first_iteration_no_finding_reject_is_forced_to_revise(self):
        review = {
            "verdict": "reject",
            "reasoning": "reference path applies the guard",
            "severity": "low",
            "confidence": 0.7,
            "selected_skills": ["memory", "parser"],
            "feedback": {},
        }
        investigation = json.dumps(
            {
                "title": "no-finding",
                "status": "no-finding",
                "detail": "the known path is guarded",
                "evidence": {"code_locations": ["parser.c:42"]},
            }
        )

        update, _, _ = self._run_critic(
            review,
            state_overrides={
                "investigation": investigation,
                "iteration": 1,
                "max_iterations": 1,
            },
        )

        processed = update["review"]
        self.assertEqual(processed["verdict"], "revise")
        self.assertEqual(processed["original_verdict"], "reject")
        self.assertEqual(processed["orchestrator_override"], "first_no_finding_requires_second_pass")
        self.assertIn("first-iteration no-finding", processed["feedback"]["gaps"][0])
        self.assertIn("attacker-influenced entrypoints", processed["feedback"]["requested_evidence"][0])
        self.assertIn("Divergently enumerate", processed["feedback"]["next_focus"])
        self.assertEqual(update["review_history"][0]["review"]["verdict"], "revise")

    def test_critic_subtask_prompt_includes_threat_model(self):
        # The critic must see the global threat model so it can judge
        # attacker position / trust boundary / impact, not just the JSON.
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        presets_root = root / "presets"
        _write_skill(presets_root, "memory", "Memory-safety lens")
        _write_skill(presets_root, "parser", "Parser lens")
        ws = Workspace.create(root / "workspaces", target="libfoo", task_id="critic-focus")
        fake_agent = _FakeAgent(
            json.dumps({"verdict": "confirm", "selected_skills": ["memory", "parser"], "feedback": {}})
        )
        state = {**_state(ws), "common_focus": "guest-to-host escape threat model"}

        with patch.object(nodes.presets, "default_presets_dir", return_value=presets_root), patch.object(
            nodes, "_make_agent", return_value=fake_agent
        ):
            nodes.critic_subtask(state, backends={"critic_subtask": "codex"})

        self.assertIn('Global focus: "guest-to-host escape threat model"', fake_agent.prompts[0])

    def test_critic_subtask_prompt_includes_upstream_context_and_rederivation_rule(self):
        # A no-finding resting on a completeness claim ("every path is safe",
        # "sole consumer", "value is clean at the sink") must be independently
        # re-derived by the critic with a different search — not restated from
        # the investigation. The critic also needs the attack-surface +
        # writeup/patch context as challenge context, while the current target
        # code and concrete evidence drive the verdict.
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        presets_root = root / "presets"
        _write_skill(presets_root, "memory", "Memory-safety lens")
        _write_skill(presets_root, "parser", "Parser lens")
        ws = Workspace.create(root / "workspaces", target="libfoo", task_id="critic-ctx")
        fake_agent = _FakeAgent(
            json.dumps({"verdict": "confirm", "selected_skills": ["memory", "parser"], "feedback": {}})
        )
        attack_surface = str(ws.main_path("attack_surface") / "attack_surface.md")
        state = {**_state(ws), "attack_surface": attack_surface}

        with patch.object(nodes.presets, "default_presets_dir", return_value=presets_root), patch.object(
            nodes, "_make_agent", return_value=fake_agent
        ):
            nodes.critic_subtask(state, backends={"critic_subtask": "codex"})

        prompt = fake_agent.prompts[0]
        self.assertIn("Upstream context", prompt)
        self.assertIn(attack_surface, prompt)
        self.assertIn(str(ws.main_path("writeup")), prompt)
        self.assertIn(str(ws.main_path("patch")), prompt)
        self.assertIn("independently re-derive", prompt)
        self.assertIn(
            "the investigation's enumeration as your own is not verification",
            prompt,
        )
        self.assertIn("writeup/patch hints as context", prompt)
        self.assertIn("current target code and concrete", prompt)
        self.assertIn("evidence drive the verdict", prompt)
        self.assertIn("first investigation for the subtask", prompt)
        self.assertIn("do not close with `confirm` or `reject`", prompt)
        self.assertNotIn("ground truth to challenge against", prompt)

    def test_critic_subtask_passes_agent_config_to_agent_run(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        presets_root = root / "presets"
        _write_skill(presets_root, "memory", "Memory-safety lens")
        _write_skill(presets_root, "parser", "Parser lens")
        ws = Workspace.create(root / "workspaces", target="libfoo", task_id="critic-config")
        fake_agent = _FakeAgent(
            json.dumps({"verdict": "confirm", "selected_skills": ["memory", "parser"], "feedback": {}})
        )
        state = {
            **_state(ws),
            "agent_configs": {
                "critic_subtask": {
                    "runtime": "codex_cli",
                    "config": "foundry",
                    "model": "gpt-5.5",
                }
            },
            "agent_config_task_types": {"critic_subtask": "legacy-type"},
        }

        with patch.dict("os.environ", {"ZEROMDASH_CODEX_MODEL": "global-default"}, clear=True), patch.object(
            nodes.presets, "default_presets_dir", return_value=presets_root
        ), patch.object(nodes, "_make_agent", return_value=fake_agent) as make_agent:
            update = nodes.critic_subtask(state, backends={})

        make_agent.assert_called_once_with("codex")
        self.assertEqual(update["errors"], [])
        self.assertEqual(
            fake_agent.extra_args,
            ["--enable", "multi_agent", "--profile", "foundry", "--model", "gpt-5.5"],
        )
        self.assertEqual(fake_agent.env, {"ZEROMDASH_CODEX_MODEL": None})


class ScopeGateNormalizationTest(unittest.TestCase):
    def test_confirmed_high_diff_causal_finding_blocks(self):
        review = nodes._normalize_scope_review(
            {
                "scan_scope": {"mode": "diff"},
            },
            {
                "scope_relation": "enabled",
                "severity": "high",
                "evidence": {
                    "diff_evidence": {
                        "change_to_sink_path": ["changed registration -> old sink"],
                        "causal_explanation": "the new callback exposes the old unsafe parser",
                    }
                },
            },
            {
                "verdict": "confirm",
                "severity": "high",
                "qualification_gate_passed": True,
                "scope_verdict": "enabled",
            },
        )

        self.assertEqual(review["scope_verdict"], "enabled")
        self.assertEqual(review["gate_decision"], "block")

    def test_pre_existing_finding_does_not_block(self):
        review = nodes._normalize_scope_review(
            {"scan_scope": {"mode": "diff"}},
            {
                "scope_relation": "pre_existing",
                "severity": "critical",
                "evidence": {
                    "diff_evidence": {
                        "change_to_sink_path": ["old entry -> old sink"],
                        "causal_explanation": "the diff is adjacent only",
                    }
                },
            },
            {
                "verdict": "confirm",
                "severity": "critical",
                "qualification_gate_passed": True,
                "scope_verdict": "pre_existing",
                "gate_decision": "block",
            },
        )

        self.assertEqual(review["gate_decision"], "warn")

    def test_missing_diff_causal_evidence_cannot_block(self):
        review = nodes._normalize_scope_review(
            {"scan_scope": {"mode": "diff"}},
            {
                "scope_relation": "introduced",
                "severity": "critical",
                "evidence": {"diff_evidence": {}},
            },
            {
                "verdict": "confirm",
                "severity": "critical",
                "qualification_gate_passed": True,
                "scope_verdict": "introduced",
            },
        )

        self.assertEqual(review["gate_decision"], "warn")
        self.assertIn("diff scope attribution", review["feedback"]["gaps"][0])


if __name__ == "__main__":
    unittest.main()
