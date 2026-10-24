import copy
import json
import re
import runpy
import subprocess
import tempfile
import threading
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock

from research.framework.runner import (
    FRAMEWORK_DIR,
    ClaudeRunner,
    Config,
    OutputValidationError,
    build_parser,
    cached_result,
    evidence_gate,
    extract_structured,
    load_config,
    merge_evidence,
    read_people,
    render_template,
    run_batch_people,
    select_people,
    slugify,
    specialize_schema,
    stamp_evidence,
    tool_receipts,
    usage_summary,
    validate_content,
)


def _alice_evidence():
    return {
        "person": "Alice", "dimension": "公开作品与技术演化", "identity_check": "confirmed",
        "items": [{
            "id": "alice-work", "date": "2020", "claim": "A published work",
            "status": "documented", "growth_signal": "repeated work",
            "source": {
                "title": "Work", "url": "https://example.com/work", "published": "2020",
                "source_type": "blog", "level": "primary",
            },
        }],
        "contradictions": [], "gaps": [],
    }


def _alice_dimension_prompt():
    return render_template("dimension.md", {
        "PERSON_JSON": '{"name_or_handle":"Alice"}',
        "DIMENSION_NAME": "公开作品与技术演化",
        "DIMENSION_QUESTIONS": "works", "LOCAL_SEED_NOTE": "none",
    })


class TempDirTestCase(unittest.TestCase):
    """Replacement for pytest's ``tmp_path`` fixture."""

    def setUp(self):
        self._temp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._temp_dir.name)
        self.addCleanup(self._temp_dir.cleanup)


class EvidencePipelineTest(TempDirTestCase):
    def test_receipts_require_successful_matching_fetch_not_usage_or_model_claim(self):
        events = [
            {"message": {"content": [{"type": "tool_use", "id": "a", "name": "WebFetch", "input": {"url": "https://example.com"}}]}},
            {"message": {"content": [{"type": "tool_result", "tool_use_id": "a", "content": "Example Domain"}]}},
        ]
        receipts = tool_receipts(events)
        payload = {"items": [{"id": "one", "status": "documented", "source": {"url": "https://example.com", "level": "primary"}}]}
        stamp_evidence(payload, receipts)
        self.assertTrue(payload["items"][0]["verification"]["verified_in_run"])
        events[1]["message"]["content"][0]["is_error"] = True
        stamp_evidence(payload, tool_receipts(events))
        self.assertFalse(payload["items"][0]["verification"]["verified_in_run"])
        self.assertEqual(payload["items"][0]["status"], "unknown")
        self.assertEqual(payload["items"][0]["source"]["level"], "lead_only")
        self.assertFalse(tool_receipts(events[:1])[0]["success"])

    def test_revisions_apply_in_order_without_changing_raw_evidence(self):
        raw = {"works": {"items": [{"id": "old"}]}}
        original = copy.deepcopy(raw)
        merged = merge_evidence(raw, [
            {"invalid_evidence_ids": ["old"], "new_evidence": [{"id": "r1"}]},
            {"invalid_evidence_ids": ["r1"], "new_evidence": [{"id": "r2"}]},
        ])
        self.assertEqual(raw, original)
        self.assertEqual(merged["works"]["items"], [])
        self.assertEqual(merged["targeted"]["items"], [{"id": "r2"}])
        with self.assertRaisesRegex(ValueError, "唯一"):
            merge_evidence(raw, [{"new_evidence": [{"id": "old"}]}])

    def test_gate_rejects_retired_missing_and_unverified_evidence(self):
        evidence = {"works": {"items": [{"id": "ok", "verification": {"verified_in_run": True}}, {"id": "lead"}]}}
        self.assertEqual(evidence_gate(evidence, {"stages": [{"evidence_ids": ["ok"]}]}), [])
        for ids in ([], ["retired"], ["lead"]):
            self.assertTrue(evidence_gate(evidence, {"stages": [{"evidence_ids": ids}]}))

    def test_legacy_cache_cannot_silently_pass_new_pipeline(self):
        path = self.tmp_path / "old.json"
        path.write_text('{"verdict": "pass"}')
        with self.assertRaisesRegex(RuntimeError, "旧版缓存"):
            cached_result(path)

    def test_slugify_researcher_name(self):
        self.assertEqual(slugify("Tavis Ormandy"), "tavis-ormandy")
        self.assertEqual(slugify("name_or_handle"), "name-or-handle")

    def test_select_people_exact_name_and_top(self):
        people = [
            {"name_or_handle": "Alice", "rank": "1"},
            {"name_or_handle": "Bob", "rank": "2"},
        ]
        self.assertEqual(select_people(people, None, 1), people[:1])
        self.assertEqual(select_people(people, ["bob"], None), people[1:])

    def test_extract_claude_structured_output_variants(self):
        self.assertEqual(extract_structured({"structured_output": {"ok": True}}), {"ok": True})
        self.assertEqual(extract_structured({"result": "{\"ok\": true}"}), {"ok": True})
        self.assertEqual(extract_structured({"result": "研究完成，结果如下：\n\n{\"ok\": true}\n"}), {"ok": True})

    def test_extract_selects_full_schema_not_first_fragment(self):
        schema = {"type": "object", "required": ["person", "items"],
                  "properties": {"person": {"type": "string"}, "items": {"type": "array"}}}
        complete = {"person": "Alice", "items": [{"claim": "example"}]}
        text = '片段：\n{"claim":"example"}\n完整结果：\n' + json.dumps(complete)
        self.assertEqual(extract_structured({"result": text}, schema), complete)
        with self.assertRaises(ValueError):
            extract_structured({"result": '{"claim":"example"}'}, schema)
        self.assertEqual(
            extract_structured({"result": json.dumps(complete) + '\n' + json.dumps(complete)}, schema),
            complete,
        )
        punctuated = {**complete, "person": "Alice，researcher"}
        list_punctuated = {**complete, "person": "Alice、researcher"}
        self.assertEqual(
            extract_structured({
                "result": json.dumps(punctuated) + '\n' + json.dumps(list_punctuated)
            }, schema),
            list_punctuated,
        )
        with self.assertRaises(ValueError):
            extract_structured({
                "result": json.dumps(complete) + '\n' + json.dumps({**complete, "person": "Bob"})
            }, schema)

    def test_extract_failure_preserves_candidate_and_complete_schema_errors(self):
        schema = {
            "type": "object",
            "required": ["transfer_boundaries"],
            "properties": {"transfer_boundaries": {"type": "integer"}},
            "additionalProperties": False,
        }
        candidate = {"transferable_boundaries": 7}
        with self.assertRaises(OutputValidationError) as raised:
            extract_structured({"result": json.dumps(candidate)}, schema)
        self.assertEqual(raised.exception.candidate, candidate)
        messages = [error["message"] for error in raised.exception.errors]
        self.assertTrue(any("required property" in message for message in messages))
        self.assertTrue(any("Additional properties" in message for message in messages))

    def test_specialized_schema_binds_task_invariants(self):
        evidence_schema = json.loads((FRAMEWORK_DIR / "schemas/evidence.json").read_text())
        prompt = render_template("dimension.md", {
            "PERSON_JSON": '{"name_or_handle":"Alice"}',
            "DIMENSION_NAME": "关键决策与转折",
            "DIMENSION_QUESTIONS": "questions",
            "LOCAL_SEED_NOTE": "none",
        })
        specialized = specialize_schema(evidence_schema, prompt)
        self.assertEqual(specialized["properties"]["person"]["const"], "Alice")
        self.assertEqual(specialized["properties"]["dimension"]["const"], "关键决策与转折")
        self.assertNotIn("const", evidence_schema["properties"]["person"])

        targeted_schema = json.loads((FRAMEWORK_DIR / "schemas/targeted_research.json").read_text())
        targeted = render_template("targeted_research.md", {
            "PERSON_JSON": '{"name_or_handle":"Alice"}',
            "EVIDENCE_JSON": "{}",
            "SYNTHESIS_JSON": "{}",
            "REVIEW_JSON": "{}",
            "REVISION_ROUND": "3",
        })
        specialized = specialize_schema(targeted_schema, targeted)
        self.assertEqual(specialized["properties"]["person"]["const"], "Alice")
        self.assertEqual(specialized["properties"]["revision_round"]["const"], 3)

    def test_content_validation_rejects_lost_identity_and_placeholder(self):
        prompt = '{"name_or_handle":"Alice"}'
        with self.assertRaisesRegex(ValueError, "身份"):
            validate_content({"person": "unknown"}, prompt)
        with self.assertRaisesRegex(ValueError, "占位"):
            validate_content({"person": "Alice", "dimension": "works", "items": [{"claim": "unknown"}]}, prompt)
        with self.assertRaisesRegex(ValueError, "能力变化"):
            validate_content({"person": "Alice", "stages": [{"capability_change": "输入JSON未提供显式能力变化描述"}]}, prompt)
        validate_content({"person": "Alice", "dimension": "works", "items": [], "gaps": ["No public sources found"]}, prompt)


class RunnerRecoveryTest(TempDirTestCase):
    def test_recovery_uses_candidate_errors_and_stops_bad_output(self):
        prompt = '人物记录：{"name_or_handle":"Alice"} 全部输入证据'
        material = "x" * 81000 + "TAIL_EVIDENCE"
        good = {"person": "Alice", "dimension": "works", "identity_check": "confirmed",
                "items": [], "contradictions": [], "gaps": ["no relevant evidence"]}
        bad = {**good, "person": "unknown"}
        events = [
            {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "a", "content": material}]}},
            {"type": "result", "subtype": "success", "result": '片段 {"claim":"unknown"}'},
        ]

        for recovery_ok in (True, False):
            with self.subTest(recovery_ok=recovery_ok):
                tmp_path = self.tmp_path / f"recovery-{recovery_ok}"
                tmp_path.mkdir()
                config = replace(
                    load_config(FRAMEWORK_DIR / "config.example.json"),
                    comparison_dir=tmp_path / "analysis",
                )
                calls = []

                def run(command, **kwargs):
                    calls.append(kwargs["input"])
                    if len(calls) == 1:
                        (kwargs["cwd"] / "checkpoint.md").write_text("已核验来源：example.com")
                        return subprocess.CompletedProcess(command, 0, '\n'.join(map(json.dumps, events)), '')
                    workspace = kwargs["cwd"]
                    self.assertIn(prompt, (workspace / "original-task.md").read_text())
                    self.assertEqual((workspace / "checkpoint.md").read_text(), "已核验来源：example.com")
                    self.assertIn("Write", json.loads((workspace / ".claude/settings.json").read_text())["permissions"]["deny"])
                    self.assertIn("只读恢复节点", (workspace / "CLAUDE.md").read_text())
                    self.assertFalse((workspace / "recovery-context.md").exists())
                    self.assertFalse((workspace / "recovery-materials.md").exists())
                    candidate_json = workspace / "invalid-candidate.json"
                    candidate_text = workspace / "invalid-candidate.txt"
                    if candidate_json.exists():
                        self.assertEqual(json.loads(candidate_json.read_text()), {"claim": "unknown"})
                    else:
                        self.assertIn("claim", candidate_text.read_text())
                    errors = json.loads((workspace / "recovery-errors.json").read_text())["errors"]
                    self.assertTrue(errors)
                    self.assertTrue(all("phase" in error and "message" in error for error in errors))
                    recovery_schema = json.loads((workspace / "output.schema.json").read_text())
                    self.assertEqual(recovery_schema["properties"]["person"]["const"], "Alice")
                    self.assertLess(len(kwargs["input"]), 200)
                    self.assertEqual(command[command.index("--tools") + 1], "Read")
                    return subprocess.CompletedProcess(
                        command, 0, json.dumps({"structured_output": good if recovery_ok else bad}), ''
                    )

                with mock.patch.object(subprocess, "run", run):
                    runner = ClaudeRunner(config)
                    if recovery_ok:
                        result = runner.call(prompt, "evidence.json", "Alice:works")
                        self.assertEqual(result["person"], "Alice")
                        self.assertTrue(Path(result["_run"]["raw_response_path"]).is_file())
                        self.assertTrue(Path(result["_run"]["recovery_response_path"]).is_file())
                    else:
                        with self.assertRaisesRegex(RuntimeError, "输出恢复失败"):
                            runner.call(prompt, "evidence.json", "Alice:works")
                self.assertEqual(len(calls), 2)  # no expensive research restart on failed recovery
                self.assertEqual(len(list((tmp_path / "runs/responses").glob("*.json"))), 2)

    def test_sub_workspaces_separate_role_schema_and_inputs(self):
        config = replace(load_config(FRAMEWORK_DIR / "config.example.json"), comparison_dir=self.tmp_path / "analysis")
        runner = ClaudeRunner(config)
        evidence = {"works": {"items": [
            {"id": f"evidence-{index}", "claim": "x" * 200}
            for index in range(200)
        ]}}
        prompt = render_template("synthesis.md", {
            "PERSON_JSON": '{"name_or_handle":"Alice"}',
            "EVIDENCE_JSON": json.dumps(evidence, ensure_ascii=False, separators=(",", ":")),
            "REVISION_CONTEXT": '[]',
        })
        schema = json.loads((FRAMEWORK_DIR / "schemas/synthesis.json").read_text())
        first = runner.prepare_sub_workspace(prompt, schema, "Alice:synthesis:v1")
        second = runner.prepare_sub_workspace(prompt, schema, "Alice:synthesis:v1")
        self.assertNotEqual(first, second)
        pattern = r"alice-synthesis-v1-\d{8}-\d{6}-\d{3}(?:-\d{2})?"
        self.assertIsNotNone(re.fullmatch(pattern, first.name))
        self.assertIsNotNone(re.fullmatch(pattern, second.name))
        self.assertEqual(json.loads((first / "output.schema.json").read_text()), schema)
        self.assertEqual(json.loads((first / "inputs/person_json.json").read_text())["name_or_handle"], "Alice")
        evidence_input = first / "inputs/evidence_json.json"
        self.assertEqual(json.loads(evidence_input.read_text()), evidence)
        self.assertGreater(len(evidence_input.read_text().splitlines()), 200)
        task = (first / "task.md").read_text()
        self.assertLess(len(task), 4_000)
        self.assertIn("inputs/evidence_json.json", task)
        self.assertNotIn('"works"', task)
        self.assertTrue((first / "inputs").is_dir())
        self.assertTrue((first / "CLAUDE.md").is_file())
        self.assertIn("Bash", json.loads((first / ".claude/settings.json").read_text())["permissions"]["deny"])

    def test_materialization_accepts_foreign_task_prompt_identity(self):
        class ForeignTaskPrompt(str):
            def __new__(cls):
                instance = super().__new__(cls, "expanded material that must not be inlined")
                instance.template = "材料：{{EVIDENCE_JSON}}"
                instance.values = {"EVIDENCE_JSON": '{"items":[{"id":"one"}]}'}
                return instance

        config = replace(load_config(FRAMEWORK_DIR / "config.example.json"), comparison_dir=self.tmp_path / "analysis")
        runner = ClaudeRunner(config)
        schema = {"type": "object"}
        workspace = runner.prepare_sub_workspace(ForeignTaskPrompt(), schema, "foreign-prompt")

        self.assertEqual((workspace / "task.md").read_text(), "材料：请使用 Read 读取 `inputs/evidence_json.json`。")
        self.assertEqual(json.loads((workspace / "inputs/evidence_json.json").read_text()), {"items": [{"id": "one"}]})

    def test_long_plain_prompt_is_materialized_instead_of_inlined(self):
        config = replace(load_config(FRAMEWORK_DIR / "config.example.json"), comparison_dir=self.tmp_path / "analysis")
        runner = ClaudeRunner(config)
        long_prompt = "完整任务材料\n" + ("evidence\n" * 3_000)
        workspace = runner.prepare_sub_workspace(long_prompt, {"type": "object"}, "long-plain-prompt")

        task = (workspace / "task.md").read_text()
        self.assertLess(len(task), 200)
        self.assertIn("inputs/task.md", task)
        self.assertEqual((workspace / "inputs/task.md").read_text(), long_prompt)

    def test_legacy_module_entry_delegates_to_canonical_runner(self):
        import research.framework.runner as canonical_runner

        called = []

        def fake_main(argv=None):
            called.append((canonical_runner.ClaudeRunner, canonical_runner.TaskPrompt, argv))
            return 0

        with mock.patch.object(canonical_runner, "main", fake_main):
            with self.assertWarnsRegex(RuntimeWarning, "found in sys.modules"):
                with self.assertRaises(SystemExit) as exit_info:
                    runpy.run_module("research.framework.runner", run_name="__main__")

        self.assertEqual(exit_info.exception.code, 0)
        self.assertEqual(called, [(canonical_runner.ClaudeRunner, canonical_runner.TaskPrompt, None)])

    def test_research_workspaces_and_report_agents_require_formal_language(self):
        config = replace(load_config(FRAMEWORK_DIR / "config.example.json"), comparison_dir=self.tmp_path / "analysis")
        runner = ClaudeRunner(config)
        schema = {"type": "object"}
        for recovery in (False, True):
            workspace = runner.prepare_sub_workspace("test", schema, "style-test", recovery=recovery)
            instructions = (workspace / "CLAUDE.md").read_text(encoding="utf-8")
            for prohibited in ("黑话", "俚语", "比喻", "拟人"):
                self.assertIn(prohibited, instructions)
            self.assertIn("专业书面语", instructions)

        synthesis = (FRAMEWORK_DIR / "prompts/synthesis.md").read_text(encoding="utf-8")
        review = (FRAMEWORK_DIR / "prompts/review.md").read_text(encoding="utf-8")
        self.assertIn("最终报告直接采用本节点的叙述字段", synthesis)
        self.assertIn("仅有文字问题时 verdict 为 pass", review)
        self.assertIn("editorial_revisions", review)
        self.assertIn("字段路径、原措辞和可直接采用的专业书面语替换", review)


class CliAndBatchTest(TempDirTestCase):
    def test_revision_limit_defaults_to_three_and_is_overridable(self):
        parser = build_parser()
        self.assertEqual(parser.parse_args(["plan"]).max_revisions, 3)
        self.assertEqual(parser.parse_args(["plan", "--max-revisions", "5"]).max_revisions, 5)
        self.assertEqual(
            parser.parse_args(["batch", "--top", "5", "--people-concurrency", "4"]).people_concurrency, 4
        )

    def test_batch_people_runs_people_concurrently(self):
        import research.framework.runner as runner_module

        config = replace(
            load_config(FRAMEWORK_DIR / "config.example.json"),
            comparison_dir=self.tmp_path / "analysis",
            max_people_concurrency=2,
        )
        runner = ClaudeRunner(config)
        people = [{"name_or_handle": name} for name in ("Alice", "Bob", "Carol")]
        barrier = threading.Barrier(2)
        lock = threading.Lock()
        active = 0
        maximum_active = 0
        started = []

        def fake_run_person(_runner, person, _force, _max_revisions):
            nonlocal active, maximum_active
            with lock:
                active += 1
                maximum_active = max(maximum_active, active)
                started.append(person["name_or_handle"])
                first_wave = len(started) <= 2
            if first_wave:
                barrier.wait(timeout=2)
            with lock:
                active -= 1

        with mock.patch.object(runner_module, "run_person", fake_run_person):
            run_batch_people(runner, people, False, 3)

        self.assertEqual(maximum_active, 2)
        self.assertEqual(sorted(started), ["Alice", "Bob", "Carol"])

    def test_batch_people_preserves_other_results_and_aggregates_failures(self):
        import research.framework.runner as runner_module

        config = replace(
            load_config(FRAMEWORK_DIR / "config.example.json"),
            comparison_dir=self.tmp_path / "analysis",
            max_people_concurrency=2,
        )
        runner = ClaudeRunner(config)
        people = [{"name_or_handle": name} for name in ("Alice", "Bob", "Carol")]
        completed = []

        def fake_run_person(_runner, person, _force, _max_revisions):
            name = person["name_or_handle"]
            if name == "Bob":
                raise RuntimeError("boom")
            completed.append(name)

        with mock.patch.object(runner_module, "run_person", fake_run_person):
            with self.assertRaisesRegex(RuntimeError, r"1/3.*Bob: boom"):
                run_batch_people(runner, people, False, 3)

        self.assertEqual(sorted(completed), ["Alice", "Carol"])

    def test_schemas_and_candidate_csv_are_valid(self):
        for path in (FRAMEWORK_DIR / "schemas").glob("*.json"):
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["type"], "object")
        csv_path = FRAMEWORK_DIR.parent / "vulnerability_researchers_top100_v2.csv"
        people = read_people(csv_path)
        self.assertEqual(len(people), 100)
        self.assertTrue(people[0]["name_or_handle"])

    def test_usage_summary_aggregates_run_metadata(self):
        output = self.tmp_path / "people"
        (output / "alice").mkdir(parents=True)
        (output / "alice" / "synthesis.json").write_text(
            json.dumps({"_run": {"label": "alice:synthesis", "total_cost_usd": 0.2, "model_usage": {"model-x": {"inputTokens": 10, "outputTokens": 4, "cacheReadInputTokens": 3, "costUSD": 0.2}}}}),
            encoding="utf-8",
        )
        config = Config(
            "claude", self.tmp_path / "settings", self.tmp_path / "input.csv", output,
            self.tmp_path / "analysis", 1, 3, 60, 2, 0, (), self.tmp_path,
        )
        result = usage_summary(config)
        self.assertEqual(result["agent_calls"], 1)
        self.assertEqual(result["models"]["model-x"]["input_tokens"], 10)

    def test_valid_workspace_artifact_survives_max_turns(self):
        config = replace(
            load_config(FRAMEWORK_DIR / "config.example.json"),
            comparison_dir=self.tmp_path / "analysis",
            allowed_tools=("Read", "WebFetch", "Edit", "Write"),
        )
        calls = []

        def run(command, **kwargs):
            calls.append(command)
            (kwargs["cwd"] / "output.json").write_text(json.dumps(_alice_evidence()))
            events = [
                {"type": "system", "subtype": "init", "session_id": "session-one", "tools": ["Read", "WebFetch", "Write"]},
                {"message": {"content": [{"type": "tool_use", "id": "fetch-one", "name": "WebFetch",
                                          "input": {"url": "https://example.com/work"}}]}},
                {"message": {"content": [{"type": "tool_result", "tool_use_id": "fetch-one", "content": "Work body"}]}},
                {"type": "result", "subtype": "error_max_turns", "num_turns": 18},
            ]
            return subprocess.CompletedProcess(command, 1, "\n".join(map(json.dumps, events)), "")

        with mock.patch.object(subprocess, "run", run):
            result = ClaudeRunner(config).call(_alice_dimension_prompt(), "evidence.json", "Alice:works")

        self.assertEqual(len(calls), 1)
        self.assertNotIn("--no-session-persistence", calls[0])
        self.assertEqual(calls[0][calls[0].index("--tools") + 1], "Read,WebFetch,Write")
        self.assertEqual(
            calls[0][calls[0].index("--allowedTools") + 1],
            "Read,WebFetch,Edit(./output.json),Edit(./checkpoint.md)",
        )
        self.assertEqual(result["_run"]["output_source"], "artifact")
        self.assertIs(result["items"][0]["verification"]["verified_in_run"], True)
        workspace = Path(result["_run"]["sub_workspace"])
        settings = json.loads((workspace / ".claude/settings.json").read_text())
        self.assertEqual(settings["permissions"]["allow"], [
            "Edit(./output.json)", "Edit(./checkpoint.md)",
        ])

    def test_partial_timeout_resumes_same_session_and_keeps_receipts(self):
        config = replace(load_config(FRAMEWORK_DIR / "config.example.json"), comparison_dir=self.tmp_path / "analysis")
        first_stream = "\n".join(map(json.dumps, [
            {"type": "system", "subtype": "init", "session_id": "session-two"},
            {"message": {"content": [{"type": "tool_use", "id": "fetch-two", "name": "WebFetch",
                                      "input": {"url": "https://example.com/work"}}]}},
            {"message": {"content": [{"type": "tool_result", "tool_use_id": "fetch-two", "content": "Work body"}]}},
        ]))
        calls = []

        def run(command, **kwargs):
            calls.append((command, kwargs["cwd"]))
            if len(calls) == 1:
                raise subprocess.TimeoutExpired(command, kwargs["timeout"], output=first_stream)
            self.assertEqual(command[-2:], ["--resume", "session-two"])
            self.assertTrue((kwargs["cwd"] / "recovery-errors.json").is_file())
            (kwargs["cwd"] / "output.json").write_text(json.dumps(_alice_evidence()))
            return subprocess.CompletedProcess(command, 0, json.dumps({"type": "result", "subtype": "success"}), "")

        with mock.patch.object(subprocess, "run", run):
            result = ClaudeRunner(config).call(_alice_dimension_prompt(), "evidence.json", "Alice:works")

        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][1], calls[1][1])
        self.assertEqual(result["_run"]["output_source"], "artifact")
        self.assertEqual(len(result["_run"]["resume_response_paths"]), 1)
        self.assertIs(result["items"][0]["verification"]["verified_in_run"], True)


if __name__ == "__main__":
    unittest.main()
