"""Unit tests for Agent-Native PoC generation and deterministic evidence gates."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from zeromdash.agents import AgentResult
from zeromdash.poc_gen.findings import load_finding_records
from zeromdash.poc_gen.io import safe_relative_path
from zeromdash.poc_gen.oracle import evaluate_verification, match_oracle, validate_oracle_spec
from zeromdash.poc_gen.service import PocGenService
from zeromdash.workspace import Workspace


def _spec(runs=2, matches=2):
    return {
        "kind": "exit_code",
        "expected": {"exit_code": 42},
        "reachability": {"required_markers": ["entry"]},
        "controls": [{"kind": "benign_input", "required": True}],
        "stability": {"runs": runs, "min_matches": matches},
        "profile": "plain",
    }


def _run(exit_code=42):
    return {
        "runner_status": "completed",
        "command": "python3 poc.py",
        "exit_code": exit_code,
        "signal": None,
        "stdout": "",
        "stderr": "",
        "markers": ["entry"],
        "backtrace": [],
        "duration_ms": 1,
    }


def _record():
    finding = {
        "title": "controlled exit",
        "subtask_id": "vuln-001",
        "evidence": {"code_locations": ["src/main.c:10"]},
    }
    return {
        "request_id": "pocreq_0123456789abcdef",
        "request_revision": 1,
        "finding_id": "VULN-001",
        "finding_type": "standalone_finding",
        "finding": finding,
        "group": {"group_id": "VULN-001", "primary_finding": finding},
        "source_result_path": "log/report_groups.json",
        "source_artifact_sha256": "abc",
        "aliases": ["VULN-001", "vuln-001"],
    }


class OracleTest(unittest.TestCase):
    def test_spec_validation_and_exit_code_match(self):
        spec, failure = validate_oracle_spec(_spec())
        self.assertIsNotNone(spec, failure)
        self.assertEqual(match_oracle(spec, _run())[0], True)
        self.assertEqual(match_oracle(spec, _run(0))[0], False)
        self.assertEqual(match_oracle(spec, {**_run(), "markers": []})[0], False)

    def test_sanitizer_requires_symbols(self):
        spec = {
            "kind": "sanitizer",
            "expected": {"sanitizer": "AddressSanitizer", "error": "heap-buffer-overflow", "top_symbols": ["copy"]},
            "reachability": {"required_markers": ["entry"]},
            "stability": {"runs": 1, "min_matches": 1},
            "profile": "asan",
        }
        observation = {**_run(1), "sanitizer": {"name": "AddressSanitizer", "error": "heap-buffer-overflow"}, "backtrace": [{"symbol": "copy"}]}
        self.assertEqual(match_oracle(spec, observation)[0], True)
        observation["backtrace"] = []
        self.assertEqual(match_oracle(spec, observation)[0], False)

    def test_verification_requires_stability_and_controls(self):
        spec, _ = validate_oracle_spec(_spec())
        payload = {
            "runs": [_run(), _run()],
            "controls": [{"kind": "benign_input", "status": "passed", "observation": _run(0)}],
        }
        verdict, details = evaluate_verification(spec, payload)
        self.assertEqual(verdict, "validated", details)
        payload["controls"][0]["observation"] = _run()
        verdict, details = evaluate_verification(spec, payload)
        self.assertEqual(verdict, "reproduced_unstable")
        self.assertIn("control triggered the target oracle: benign_input", details["failures"])

    def test_unsafe_artifact_path_is_rejected(self):
        for value in ("../target", "/tmp/target", "./target"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                safe_relative_path(value)


class FindingLoaderTest(unittest.TestCase):
    def test_report_group_and_local_alias_selection(self):
        finding = {
            "title": "qualified",
            "subtask_id": "vuln-001",
            "disposition": "confirmed_vulnerability",
            "qualification_gate_passed": True,
            "cvss4_vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
        }
        group = {
            "group_id": "VULN-001",
            "summary_format": "full",
            "primary_finding": finding,
            "source_subtasks": ["vuln-001"],
            "source_chains": [],
        }
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="libfoo")
            state = {
                "task_id": ws.task_id,
                "workspace_root": str(ws.root),
                "report_groups": [group],
                "report_groups_path": str(ws.log / "report_groups.json"),
            }
            stats: dict = {}
            selected = load_finding_records(state, "vuln-001", stats=stats)
            self.assertEqual(selected[0]["finding_id"], "VULN-001")
            self.assertEqual(selected[0]["qualification"], "gate")
            self.assertEqual(stats["admitted_gate"], 1)
            with self.assertRaisesRegex(ValueError, "available finding IDs"):
                load_finding_records(state, "vuln-999")

    def _legacy_review_res(self, tmp, name, review):
        ws = Workspace.create(tmp, target="libfoo")
        review_res = ws.log_path("review_res")
        review_res.mkdir(parents=True, exist_ok=True)
        (review_res / f"{name}.json").write_text(
            json.dumps(
                {
                    "finding": {
                        "title": f"legacy {name}",
                        "subtask_id": name,
                        "evidence": {"code_locations": ["src/main.c:10"]},
                        "review": review,
                    }
                }
            )
        )
        return ws

    def test_legacy_confirm_finding_admitted_via_fallback(self):
        # Pre-qualification-gate workspaces carry no gate fields; a critic
        # confirm verdict must still be selectable for PoC generation.
        with TemporaryDirectory() as tmp:
            ws = self._legacy_review_res(tmp, "vuln-001", {"verdict": "confirm"})
            state = {"task_id": ws.task_id, "workspace_root": str(ws.root)}
            stats: dict = {}
            records = load_finding_records(state, stats=stats)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["finding_id"], "vuln-001")
            self.assertEqual(records[0]["qualification"], "legacy_confirm")
            self.assertEqual(stats["considered"], 1)
            self.assertEqual(stats["admitted_legacy_confirm"], 1)
            selected = load_finding_records(state, "vuln-001")
            self.assertEqual(selected[0]["finding_id"], "vuln-001")

    def test_legacy_revise_finding_skipped_with_stats(self):
        with TemporaryDirectory() as tmp:
            ws = self._legacy_review_res(tmp, "vuln-001", {"verdict": "revise"})
            state = {"task_id": ws.task_id, "workspace_root": str(ws.root)}
            stats: dict = {}
            records = load_finding_records(state, stats=stats)
            self.assertEqual(records, [])
            self.assertEqual(stats["considered"], 1)
            self.assertEqual(stats["skipped_legacy_not_confirmed"], 1)

    def test_new_schema_confirm_still_requires_gate(self):
        # Once a finding carries the gate schema, a bare confirm verdict
        # must NOT bypass the strict qualification gate.
        review = {
            "verdict": "confirm",
            "qualification_gate_passed": False,
            "qualification_gate_version": "cvss4-v1",
        }
        with TemporaryDirectory() as tmp:
            ws = self._legacy_review_res(tmp, "vuln-001", review)
            state = {"task_id": ws.task_id, "workspace_root": str(ws.root)}
            stats: dict = {}
            records = load_finding_records(state, stats=stats)
            self.assertEqual(records, [])
            self.assertEqual(stats["skipped_gate_failed"], 1)
            self.assertEqual(stats.get("admitted_legacy_confirm", 0), 0)

    def test_group_records_admit_legacy_primary_finding(self):
        finding = {
            "title": "legacy group finding",
            "subtask_id": "vuln-001",
            "review": {"verdict": "confirm"},
        }
        group = {
            "group_id": "VULN-001",
            "summary_format": "full",
            "primary_finding": finding,
            "source_subtasks": ["vuln-001"],
            "source_chains": [],
        }
        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="libfoo")
            state = {
                "task_id": ws.task_id,
                "workspace_root": str(ws.root),
                "report_groups": [group],
                "report_groups_path": str(ws.log / "report_groups.json"),
            }
            stats: dict = {}
            records = load_finding_records(state, stats=stats)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["qualification"], "legacy_confirm")
            self.assertEqual(stats["admitted_legacy_confirm"], 1)


class PocGenNodeTest(unittest.TestCase):
    def test_node_reports_selection_stats(self):
        from zeromdash.poc_gen.node import poc_gen

        with TemporaryDirectory() as tmp:
            ws = Workspace.create(tmp, target="libfoo")
            state = {"task_id": ws.task_id, "workspace_root": str(ws.root), "poc_finding_id": ""}
            with patch("zeromdash.poc_gen.node.PocGenService") as service_cls:
                service_cls.return_value.run.return_value = []
                result = poc_gen(state)
        self.assertIn("poc_selection_stats", result)
        self.assertIn("poc_results", result)
        service_cls.return_value.run.assert_called_once_with("", stats={})


class PocGenServiceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        root = Path(self.tmp.name)
        self.ws = Workspace.create(root, target="libfoo")
        (self.ws.main_path("repo") / "main.c").write_text("int main(void) { return 0; }\n")
        self.invoked_nodes = []
        self.prompts = []
        self.state = {
            "target": "libfoo",
            "task_id": self.ws.task_id,
            "workspace_root": str(self.ws.root),
            "repo_path": str(self.ws.main_path("repo")),
            "agent_configs": {},
            "poc_config": {
                "enabled": True,
                "max_debug_rounds_per_strategy": 2,
                "verification_runs": 2,
                "verification_min_matches": 2,
            },
        }

    def tearDown(self):
        self.tmp.cleanup()

    def _fake_invoke(self, responses, calls):
        def fake(ws, node, prompt, backends, state, **kwargs):
            del ws, backends, state
            self.invoked_nodes.append(node)
            self.prompts.append(prompt)
            for json_path in re.findall(r"(/[^\s;]+\.json)", prompt):
                self.assertTrue(Path(json_path).is_file(), f"prompt input was not materialized: {json_path}")
            phase = kwargs["extra_context"]["poc_phase"]
            calls.append(phase)
            value = responses[phase]
            payload = value(prompt) if callable(value) else value
            result = AgentResult(stdout=json.dumps(payload), stderr="", returncode=0, backend="codex")
            valid, failure = kwargs["validate"](result)
            return result, [] if valid else [failure]
        return fake

    def _responses(self):
        return {
            "plan_poc": {
                "oracle_spec": _spec(),
                "environment_requirements": {},
                "strategies": [{"objective": "trigger controlled exit", "kind": "cli", "entry_point": "main", "novelty_key": "cli"}],
            },
            "prepare_environment": {"status": "ready", "environment_manifest": {"backend": "agent_sandbox"}, "summary": "ready", "error": ""},
            "generate_poc": {"summary": "candidate", "files": [{"path": "poc.py", "content": "raise SystemExit(42)\n"}], "run": {"command": "python3 poc.py"}},
            "execute_poc": {"runner_status": "completed", "build": {}, "runs": [_run()], "notes": "observed"},
            "verify_poc": {"environment_status": "ready", "runs": [_run(), _run()], "controls": [{"kind": "benign_input", "status": "passed", "skip_reason": "", "observation": _run(0)}], "notes": "verified"},
            "release_poc": {"readme": "# VULN-001\nStatus: validated", "report": "# Reproduction report\nFinding: VULN-001\nStatus: validated\n"},
        }

    def test_end_to_end_validated_and_release_report(self):
        calls = []
        with patch("zeromdash.poc_gen.service.load_finding_records", return_value=[_record()]), patch(
            "zeromdash.poc_gen.service._invoke_with_output_retry",
            side_effect=self._fake_invoke(self._responses(), calls),
        ):
            results = PocGenService(self.state).run()
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["status"], "validated", result.get("errors"))
        self.assertEqual(result["attempt_count"], 1)
        release = Path(result["release_path"])
        self.assertEqual((release / "poc" / "poc.py").read_text(), "raise SystemExit(42)\n")
        self.assertIn("validated", (release / "repro_report.md").read_text())
        manifest = json.loads((release / "manifest.json").read_text())
        self.assertEqual(manifest["status"], "validated")
        self.assertIn("execute_poc", calls)
        self.assertIn("verify_poc", calls)
        self.assertIn("release_poc", calls)
        self.assertTrue(all('{"' not in prompt for prompt in self.prompts))
        self.assertEqual(
            self.invoked_nodes,
            [
                "plan_poc",
                "prepare_environment_and_debugger",
                "generate_poc",
                "build_and_execute_poc",
                "verify_poc",
                "release_poc",
            ],
        )

    def test_no_match_obeys_debug_budget(self):
        responses = self._responses()
        responses["execute_poc"] = {"runner_status": "completed", "build": {}, "runs": [_run(0)], "notes": "no match"}
        responses["debug_poc"] = {"hypothesis": "wrong input", "changes": "adjust input", "progress_markers": []}
        calls = []
        with patch("zeromdash.poc_gen.service.load_finding_records", return_value=[_record()]), patch(
            "zeromdash.poc_gen.service._invoke_with_output_retry",
            side_effect=self._fake_invoke(responses, calls),
        ):
            result = PocGenService(self.state).run()[0]
        self.assertEqual(result["status"], "not_reproduced")
        self.assertEqual(calls.count("generate_poc"), 2)
        self.assertEqual(calls.count("debug_poc"), 1)
        self.assertNotIn("verify_poc", calls)

    def test_source_drift_fails_closed(self):
        responses = self._responses()
        repo = self.ws.main_path("repo")
        def execute(prompt):
            del prompt
            (repo / "unexpected.c").write_text("drift")
            return {"runner_status": "completed", "build": {}, "runs": [_run(0)], "notes": "drift"}
        responses["execute_poc"] = execute
        with patch("zeromdash.poc_gen.service.load_finding_records", return_value=[_record()]), patch(
            "zeromdash.poc_gen.service._invoke_with_output_retry",
            side_effect=self._fake_invoke(responses, []),
        ):
            result = PocGenService(self.state).run()[0]
        self.assertEqual(result["status"], "environment_failed")
        self.assertFalse(result["source_integrity_ok"])


if __name__ == "__main__":
    unittest.main()
