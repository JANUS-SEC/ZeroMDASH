"""Offline integration tests, runnable with python3.12 -m unittest."""
import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from research.framework.graph import _task_material, apply_editorial_edits, run_research_graph
from research.framework.runner import FRAMEWORK_DIR, PIPELINE_VERSION, load_config


class GraphTests(unittest.TestCase):
    def test_editorial_edits_only_change_exact_prose(self):
        original = {
            "person": "Alice",
            "stages": [{"period": "2020", "capability_change": "卡住时继续分析",
                        "evidence_ids": ["works"], "confidence": "high"}],
            "_run": {"pipeline_version": PIPELINE_VERSION},
        }
        result = apply_editorial_edits(original, [{"path": "/stages/0/capability_change",
                                                   "before": "卡住时继续分析", "after": "研究受阻时继续分析"}])
        self.assertEqual(result["stages"][0]["capability_change"], "研究受阻时继续分析")
        self.assertEqual(original["stages"][0]["capability_change"], "卡住时继续分析")
        for path, before in (("/stages/0/period", "2020"), ("/stages/0/evidence_ids/0", "works"),
                             ("/stages/0/capability_change", "不匹配")):
            with self.assertRaises(ValueError):
                apply_editorial_edits(original, [{"path": path, "before": before, "after": "修改"}])

    def test_task_material_removes_only_run_metadata(self):
        material = {"works": {"_run": {"tokens": 100}, "items": [
            {"claim": "核验文本", "verification": {"verified_in_run": True}}
        ]}}
        self.assertEqual(_task_material(material), {"works": {"items": [
            {"claim": "核验文本", "verification": {"verified_in_run": True}}
        ]}})
        self.assertIn("_run", material["works"])

    def run_case(self, limit, eventually_pass):
        with tempfile.TemporaryDirectory() as directory:
            config = replace(load_config(FRAMEWORK_DIR / "config.example.json"),
                             output_dir=Path(directory), max_concurrency=3)

            class FakeRunner:
                def __init__(self):
                    self.config = config
                    self.round = 0

                def call(self, prompt, schema, label):
                    if schema == "evidence.json":
                        result = {"items": [{"id": label.split(":")[-1], "verification": {"verified_in_run": True}}]}
                    elif schema == "synthesis.json":
                        result = {"stages": [{"evidence_ids": ["works" if self.round == 0 else f"r{self.round}"]}]}
                    elif schema == "review.json":
                        result = {"verdict": "pass" if eventually_pass and self.round else "revise"}
                    else:
                        self.round += 1
                        result = {"invalid_evidence_ids": ["works" if self.round == 1 else f"r{self.round - 1}"],
                                  "new_evidence": [{"id": f"r{self.round}", "verification": {"verified_in_run": True}}]}
                    return {**result, "_run": {"pipeline_version": PIPELINE_VERSION}}

            runner = FakeRunner()
            state = run_research_graph(runner, {"name_or_handle": "Alice"}, max_revisions=limit)
            base = Path(directory) / "alice"
            if eventually_pass and limit:
                self.assertEqual(state["status"], "complete")
                self.assertTrue((base / "FINAL.md").exists())
                merged = json.loads((base / "evidence_merged/v2.json").read_text())
                self.assertEqual(merged["works"]["items"], [])
                self.assertEqual(merged["targeted"]["items"][0]["id"], "r1")
            else:
                self.assertEqual(state["status"], "revision_exhausted")
                self.assertEqual(state["revision_round"], limit)
                self.assertTrue((base / "DRAFT.md").exists())
                self.assertFalse((base / "FINAL.md").exists())

    def test_revise_merges_then_passes(self):
        self.run_case(3, True)

    def test_zero_revision_budget(self):
        self.run_case(0, False)

    def test_large_revision_budget_does_not_hit_graph_default_limit(self):
        self.run_case(8, False)

    def test_editorial_only_issue_is_rewritten_without_research_revision(self):
        with tempfile.TemporaryDirectory() as directory:
            config = replace(load_config(FRAMEWORK_DIR / "config.example.json"),
                             output_dir=Path(directory), max_editorial_revisions=2)

            class FakeRunner:
                def __init__(self):
                    self.config = config
                    self.calls = []

                def call(self, prompt, schema, label):
                    self.calls.append(label)
                    if schema == "evidence.json":
                        result = {"items": [{"id": label.split(":")[-1], "verification": {"verified_in_run": True}}]}
                    elif ":editorial:" in label:
                        if schema != "editorial_edits.json":
                            raise AssertionError("文字修订应返回小型修改清单")
                        result = {"person": "Alice", "edits": [{"path": "/stages/0/capability_change",
                                                              "before": "卡住时继续分析", "after": "研究受阻时继续分析"}]}
                    elif schema == "synthesis.json":
                        result = {"person": "Alice", "stages": [{"capability_change": "卡住时继续分析",
                                                               "evidence_ids": ["works"], "confidence": "high", "period": "2020"}]}
                    elif schema == "review.json":
                        result = {"verdict": "pass", "required_revisions": [],
                                  "editorial_revisions": [] if "-edit-" in label else ["stages[0].capability_change：卡住时→研究受阻时"]}
                    else:
                        raise AssertionError("纯文字问题不得调用定向研究")
                    return {**result, "_run": {"pipeline_version": PIPELINE_VERSION}}

            runner = FakeRunner()
            state = run_research_graph(runner, {"name_or_handle": "Alice"}, max_revisions=0)
            base = Path(directory) / "alice"
            self.assertEqual(state["status"], "complete")
            self.assertEqual(state["revision_round"], 0)
            self.assertEqual(state["editorial_round"], 1)
            self.assertTrue((base / "FINAL.md").exists())
            self.assertFalse(any("targeted-research" in label for label in runner.calls))
            self.assertEqual(json.loads((base / "synthesis.json").read_text())["stages"][0]["capability_change"],
                             "研究受阻时继续分析")

    def test_editorial_limit_retains_draft_without_targeted_research(self):
        with tempfile.TemporaryDirectory() as directory:
            config = replace(load_config(FRAMEWORK_DIR / "config.example.json"),
                             output_dir=Path(directory), max_editorial_revisions=1)

            class FakeRunner:
                def __init__(self):
                    self.config = config
                    self.calls = []

                def call(self, prompt, schema, label):
                    self.calls.append(label)
                    if schema == "evidence.json":
                        result = {"items": [{"id": label.split(":")[-1], "verification": {"verified_in_run": True}}]}
                    elif schema == "editorial_edits.json":
                        result = {"person": "Alice", "edits": [{"path": "/stages/0/capability_change",
                                                              "before": "卡住时继续分析", "after": "研究受阻时继续分析"}]}
                    elif schema == "synthesis.json":
                        result = {"person": "Alice", "stages": [{"period": "2020", "evidence_ids": ["works"],
                                                                   "capability_change": "卡住时继续分析"}]}
                    elif schema == "review.json":
                        result = {"verdict": "pass", "required_revisions": [], "editorial_revisions": ["仍有不规范措辞"]}
                    else:
                        raise AssertionError("纯文字问题不得调用定向研究")
                    return {**result, "_run": {"pipeline_version": PIPELINE_VERSION}}

            runner = FakeRunner()
            state = run_research_graph(runner, {"name_or_handle": "Alice"}, max_revisions=0)
            base = Path(directory) / "alice"
            self.assertEqual(state["status"], "editorial_exhausted")
            self.assertTrue((base / "DRAFT.md").exists())
            self.assertFalse((base / "FINAL.md").exists())
            self.assertFalse(any("targeted-research" in label for label in runner.calls))


if __name__ == "__main__":
    unittest.main()
