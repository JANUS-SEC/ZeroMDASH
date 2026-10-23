"""Unit tests for zeromdash.skills (runtime expert-skill discovery)."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from zeromdash import skills


class ExtractSummaryTest(unittest.TestCase):
    def test_frontmatter_summary_wins(self):
        text = (
            "---\n"
            "summary: Memory safety expert.\n"
            "extra: ignored\n"
            "---\n"
            "# Heading\n\nA later paragraph.\n"
        )
        self.assertEqual(skills._extract_summary(text), "Memory safety expert.")

    def test_frontmatter_fallback_keys(self):
        for key in ("description", "when_to_use", "purpose"):
            text = f"---\n{key}: lens for {key}\n---\nbody"
            self.assertEqual(skills._extract_summary(text), f"lens for {key}")

    def test_frontmatter_block_scalar_description(self):
        text = (
            "---\n"
            "description: |\n"
            "  Memory safety expert.\n"
            "  Use when buffer boundaries cross trust boundaries.\n"
            "type: skill\n"
            "---\n"
            "body"
        )
        self.assertEqual(
            skills._extract_summary(text),
            "Memory safety expert. Use when buffer boundaries cross trust boundaries.",
        )

    def test_frontmatter_folded_block_scalar_fallback_key(self):
        text = (
            "---\n"
            "when_to_use: >-\n"
            "  Parser and state-machine lens.\n"
            "  Use when input format validity gates memory access.\n"
            "type: skill\n"
            "---\n"
            "body"
        )
        self.assertEqual(
            skills._extract_summary(text),
            "Parser and state-machine lens. Use when input format validity gates memory access.",
        )

    def test_frontmatter_quotes_stripped(self):
        text = '---\nsummary: "Quoted summary."\n---\nbody'
        self.assertEqual(skills._extract_summary(text), "Quoted summary.")

    def test_first_paragraph_after_heading(self):
        text = "# Memory safety\n\nUse this when buffers cross trust boundaries.\n\nMore later.\n"
        self.assertEqual(
            skills._extract_summary(text),
            "Use this when buffers cross trust boundaries.",
        )

    def test_first_paragraph_when_no_heading(self):
        text = "Crypto pitfalls expert.\n\nMore details.\n"
        self.assertEqual(skills._extract_summary(text), "Crypto pitfalls expert.")

    def test_collapses_multiline_paragraph(self):
        text = "line one\nline two\nline three\n\nnext para"
        self.assertEqual(
            skills._extract_summary(text),
            "line one line two line three",
        )

    def test_empty_text(self):
        self.assertEqual(skills._extract_summary(""), "(no summary)")

    def test_long_summary_truncated(self):
        long = "x" * 400
        text = f"---\nsummary: {long}\n---\nbody"
        out = skills._extract_summary(text)
        self.assertLessEqual(len(out), 280)
        self.assertTrue(out.endswith("…"))


class ParseSimpleFrontmatterTest(unittest.TestCase):
    def test_parses_key_value(self):
        block = "summary: hello\ndescription: world"
        self.assertEqual(
            skills._parse_simple_frontmatter(block),
            {"summary": "hello", "description": "world"},
        )

    def test_skips_blank_and_comment(self):
        block = "\n# comment\nsummary: hi\n"
        self.assertEqual(skills._parse_simple_frontmatter(block), {"summary": "hi"})

    def test_ignores_lines_without_colon(self):
        block = "summary: ok\nnotakv\n"
        self.assertEqual(skills._parse_simple_frontmatter(block), {"summary": "ok"})

    def test_lowercases_keys(self):
        block = "Summary: ok"
        self.assertEqual(skills._parse_simple_frontmatter(block), {"summary": "ok"})

    def test_parses_block_scalar_value(self):
        block = "description: |\n  line one\n  line two\nkind: skill"
        self.assertEqual(
            skills._parse_simple_frontmatter(block),
            {"description": "line one\nline two", "kind": "skill"},
        )


class DiscoverSkillsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _write(self, rel: str, content: str) -> Path:
        p = self.tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return p

    def test_finds_flat_md_files(self):
        self._write("memory_safety.md", "---\nsummary: memory expert\n---\n")
        self._write("crypto.md", "Crypto expert lens.\n")
        out = skills.discover_skills([self.tmp])
        names = [s.name for s in out]
        self.assertEqual(names, ["crypto", "memory_safety"])
        by_name = {s.name: s for s in out}
        self.assertEqual(by_name["memory_safety"].summary, "memory expert")
        self.assertEqual(by_name["crypto"].summary, "Crypto expert lens.")

    def test_finds_directory_skill_with_skill_md(self):
        self._write("parser/SKILL.md", "---\nsummary: parser expert\n---\n")
        out = skills.discover_skills([self.tmp])
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].name, "parser")
        self.assertTrue(out[0].path.endswith("parser/SKILL.md"))
        self.assertEqual(out[0].summary, "parser expert")

    def test_finds_directory_skill_with_readme(self):
        self._write("auth_logic/README.md", "Auth-logic expert.\n")
        out = skills.discover_skills([self.tmp])
        self.assertEqual([s.name for s in out], ["auth_logic"])

    def test_skips_readme_and_index_at_top_level(self):
        self._write("README.md", "this is a manifest\n")
        self._write("index.md", "ignore me\n")
        self._write("real.md", "Real skill.\n")
        out = skills.discover_skills([self.tmp])
        self.assertEqual([s.name for s in out], ["real"])

    def test_ignores_non_markdown_files(self):
        self._write("script.py", "print('not a skill')")
        self._write("note.txt", "not markdown")
        out = skills.discover_skills([self.tmp])
        self.assertEqual(out, [])

    def test_missing_dir_is_silently_ignored(self):
        out = skills.discover_skills([self.tmp / "no_such_dir"])
        self.assertEqual(out, [])

    def test_none_entry_ignored(self):
        out = skills.discover_skills([None])  # type: ignore[list-item]
        self.assertEqual(out, [])

    def test_later_dir_overrides_earlier_by_name(self):
        # 模拟 [bundled, sub_workspace] 顺序: 后者覆盖
        bundled = self.tmp / "bundled"
        local = self.tmp / "local"
        bundled.mkdir()
        local.mkdir()
        (bundled / "memory_safety.md").write_text("Bundled lens.\n")
        (local / "memory_safety.md").write_text("Local override lens.\n")
        out = skills.discover_skills([bundled, local])
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].summary, "Local override lens.")
        self.assertTrue(out[0].path.startswith(str(local)))

    def test_dedup_across_dirs(self):
        a = self.tmp / "a"
        b = self.tmp / "b"
        a.mkdir()
        b.mkdir()
        (a / "shared.md").write_text("from a")
        (b / "shared.md").write_text("from b")
        (b / "extra.md").write_text("from b extra")
        out = skills.discover_skills([a, b])
        self.assertEqual({s.name for s in out}, {"shared", "extra"})

    def test_results_sorted_by_name(self):
        for n in ("zeta", "alpha", "mu"):
            self._write(f"{n}.md", f"{n} lens")
        out = skills.discover_skills([self.tmp])
        self.assertEqual([s.name for s in out], ["alpha", "mu", "zeta"])


class RenderCatalogTest(unittest.TestCase):
    def test_empty_catalog_label(self):
        self.assertEqual(skills.render_catalog([]), "(no expert skills available)")

    def test_renders_bullet_list(self):
        infos = [
            skills.SkillInfo(name="memory_safety", path="/x/memory_safety.md",
                             summary="Memory expert."),
            skills.SkillInfo(name="crypto", path="/x/crypto.md",
                             summary="Crypto expert."),
        ]
        out = skills.render_catalog(infos)
        self.assertIn("- `memory_safety` — Memory expert.", out)
        self.assertIn("- `crypto` — Crypto expert.", out)
        # 一行一个 skill
        self.assertEqual(len(out.splitlines()), 2)


class NamesHelperTest(unittest.TestCase):
    def test_names_extracts_in_order(self):
        infos = [
            skills.SkillInfo(name="b", path="/b", summary=""),
            skills.SkillInfo(name="a", path="/a", summary=""),
        ]
        self.assertEqual(skills.names(infos), ["b", "a"])


class IntegrationWithBundledPresetsTest(unittest.TestCase):
    """Smoke-test: bundled presets/skills/ 至少要能被发现 (即便只有 README)."""

    def test_bundled_skills_dir_scannable(self):
        from zeromdash import presets as presets_mod
        d = presets_mod.default_presets_dir() / "skills"
        # README.md 不算 skill，所以可能为 0；关键是不报错
        out = skills.discover_skills([d])
        self.assertIsInstance(out, list)
        # 不应把 README.md 当成 skill
        self.assertNotIn("README", [s.name for s in out])
        self.assertNotIn("readme", [s.name.lower() for s in out])

    def test_bundled_skill_summaries_are_short_and_informative(self):
        from zeromdash import presets as presets_mod
        d = presets_mod.default_presets_dir() / "skills"
        out = skills.discover_skills([d])

        self.assertGreater(len(out), 0)
        for info in out:
            with self.subTest(skill=info.name):
                self.assertTrue(info.summary.strip())
                self.assertNotEqual(info.summary.strip(), "|")
                self.assertNotIn("\n", info.summary)
                self.assertLessEqual(len(info.summary), 280)


if __name__ == "__main__":
    unittest.main()
