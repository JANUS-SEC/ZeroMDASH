"""CVSS v4.0 scoring and vulnerability-qualification regression tests."""

from __future__ import annotations

import unittest

from zeromdash import nodes
from zeromdash.cvss4 import CVSS4ValidationError, has_direct_impact, score_base_vector


HIGH_VECTOR = (
    "CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/"
    "VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"
)
NO_IMPACT_VECTOR = (
    "CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/"
    "VC:N/VI:N/VA:N/SC:N/SI:N/SA:N"
)


class CVSS4ScoringTest(unittest.TestCase):
    def test_scores_and_canonicalizes_complete_base_vector(self):
        result = score_base_vector(HIGH_VECTOR)

        self.assertEqual(result.vector, HIGH_VECTOR)
        self.assertEqual(result.score, 8.5)
        self.assertEqual(result.severity, "high")
        self.assertTrue(has_direct_impact(result))

    def test_zero_impact_vector_scores_none(self):
        result = score_base_vector(NO_IMPACT_VECTOR)

        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.severity, "none")
        self.assertFalse(has_direct_impact(result))

    def test_rejects_missing_base_metric(self):
        with self.assertRaisesRegex(CVSS4ValidationError, "missing Base metrics: SA"):
            score_base_vector(HIGH_VECTOR.rsplit("/", 1)[0])

    def test_rejects_threat_environmental_or_supplemental_metrics(self):
        with self.assertRaisesRegex(CVSS4ValidationError, "non-Base metrics are not allowed: E"):
            score_base_vector(HIGH_VECTOR + "/E:A")


class VulnerabilityQualificationTest(unittest.TestCase):
    def test_valid_vulnerability_uses_computed_cvss_not_claimed_severity(self):
        review = nodes._normalize_qualification_review(
            {
                "verdict": "confirm",
                "disposition": "confirmed_vulnerability",
                "documented_expected_behavior": False,
                "security_contract_violation": True,
                "violated_security_property": "bounds check must dominate the copy",
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
                "cvss4_vector": HIGH_VECTOR,
                "severity": "critical",
            }
        )

        self.assertTrue(review["qualification_gate_passed"])
        self.assertEqual(review["cvss4_score"], 8.5)
        self.assertEqual(review["severity"], "high")
        self.assertEqual(review["verdict"], "confirm")

        finding = {
            "subtask_id": "vuln-002",
            "kind": "vuln",
            "title": "documented JIT hardening default",
            "detail": "The documented optional mitigation is disabled.",
            "evidence": {
                "code_locations": ["kernel/bpf/core.c:550"],
                "call_path": ["cBPF immediate -> JIT image"],
            },
            "review": review,
            "disposition": review["disposition"],
            "qualification_gate_passed": False,
            "severity": "none",
        }
        state = {"vuln_candidates": [finding], "observations": [finding]}
        compact = nodes._compact_summary_buckets(state)
        observations = nodes._compact_summary_observations(state)

        self.assertEqual(compact["vuln_candidates"], [])
        self.assertEqual([item["id"] for item in observations], ["vuln-002"])

    def test_documented_hardening_behavior_is_not_a_vulnerability(self):
        review = nodes._normalize_qualification_review(
            {
                "verdict": "confirm",
                "disposition": "expected_behavior",
                "documented_expected_behavior": True,
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
                "required_external_primitives": [
                    "independent kernel control-flow hijack",
                    "JIT image address discovery",
                ],
                "cvss_applicable": False,
                "cvss4_vector": "",
                "severity": "medium",
            }
        )

        self.assertEqual(review["disposition"], "expected_behavior")
        self.assertFalse(review["qualification_gate_passed"])
        self.assertFalse(review["cvss_applicable"])
        self.assertEqual(review["severity"], "none")
        self.assertNotIn("cvss4_score", review)
        self.assertEqual(review["verdict"], "confirm")

    def test_unproven_external_primitive_forces_revise(self):
        review = nodes._normalize_qualification_review(
            {
                "verdict": "confirm",
                "disposition": "confirmed_vulnerability",
                "documented_expected_behavior": False,
                "security_contract_violation": True,
                "violated_security_property": "attacker bytes should not execute",
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
                "required_external_primitives": ["instruction-pointer diversion"],
                "cvss_applicable": True,
                "cvss4_vector": NO_IMPACT_VECTOR,
            }
        )

        self.assertFalse(review["qualification_gate_passed"])
        self.assertEqual(review["claimed_disposition"], "confirmed_vulnerability")
        self.assertEqual(review["disposition"], "insufficient_evidence")
        self.assertEqual(review["verdict"], "revise")
        self.assertEqual(
            review["orchestrator_override"],
            "vulnerability_qualification_gate_failed",
        )
        self.assertTrue(
            any("separate unproven vulnerability" in gap for gap in review["feedback"]["gaps"])
        )


if __name__ == "__main__":
    unittest.main()
