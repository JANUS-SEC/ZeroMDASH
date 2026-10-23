"""Unit tests for zeromdash.presets."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from zeromdash import nodes, presets


def _ctx(**overrides) -> dict:
    base = {
        "workspace_base": "/ws",
        "main": "/ws/main",
        "similar": "/ws/similar",
        "log": "/ws/log",
        "sub_workspace": "/ws/sub_workspace/node_x",
        "node": "x",
        "subtask_id": "",
        "target": "libfoo",
        "backend": "codex",
    }
    base.update(overrides)
    return base


class IsTextTest(unittest.TestCase):
    def test_recognized_text_suffixes(self):
        for name in ("a.md", "b.MD", "c.json", "d.toml", "e.yaml", "f.txt", "g.cfg"):
            self.assertTrue(presets._is_text(Path(name)), name)

    def test_unknown_suffix_is_binary(self):
        for name in ("a.png", "b.bin", "c", "d.tar.gz"):
            self.assertFalse(presets._is_text(Path(name)), name)


class SafeFormatTest(unittest.TestCase):
    def test_substitutes_known_keys(self):
        out = presets._safe_format("hello {target}", _ctx(target="foo"))
        self.assertEqual(out, "hello foo")

    def test_unknown_key_kept_as_literal(self):
        # 模板里出现的未知占位符必须原样保留，便于把模板原样喂给 agent
        out = presets._safe_format("path={var_we_did_not_define}", _ctx())
        self.assertEqual(out, "path={var_we_did_not_define}")

    def test_double_braces_are_literal(self):
        # `{{` -> `{`, `}}` -> `}`
        out = presets._safe_format("a={{b}}", _ctx())
        self.assertEqual(out, "a={b}")

    def test_positional_braces_returned_unchanged(self):
        # 模板里出现的 `{}` 会让 Formatter 抛 IndexError，应返回原文
        out = presets._safe_format("[{}]({target})", _ctx(target="t"))
        self.assertEqual(out, "[{}]({target})")

    def test_settings_template_renders(self):
        # 模拟 .claude/settings.json 这种含 `{{ }}` + `{key}` 混合的场景
        tmpl = '{{"target": "{target}", "node": "{node}"}}'
        rendered = presets._safe_format(tmpl, _ctx(target="libfoo", node="plan"))
        self.assertEqual(json.loads(rendered), {"target": "libfoo", "node": "plan"})


class DefaultPresetsDirTest(unittest.TestCase):
    def test_points_to_bundled_presets(self):
        d = presets.default_presets_dir()
        self.assertTrue(d.is_dir(), f"presets dir should exist at {d}")
        # bundled 模板里至少这几样必须有
        self.assertTrue((d / "CLAUDE.md").is_file())
        self.assertTrue((d / "AGENTS.md").is_file())
        self.assertTrue((d / ".claude" / "settings.json").is_file())
        self.assertTrue((d / ".codex" / "config.toml").is_file())
        self.assertTrue((d / ".dsh" / "AGENTS.md").is_file())
        self.assertTrue((d / ".dsh" / "headless-minimal.patch.yml").is_file())
        self.assertTrue((d / ".kimi-code" / "AGENTS.md").is_file())
        self.assertTrue((d / ".kimi-code" / "local.toml").is_file())


class RenderIntoTest(unittest.TestCase):
    def setUp(self):
        self._tmp = TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.src = self.tmp / "src"
        self.dst = self.tmp / "dst"
        self.src.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    # ---------------------------------------------------------- text rendering
    def test_renders_text_files_with_substitution(self):
        (self.src / "CLAUDE.md").write_text("target={target}\nnode={node}\n")
        presets.render_into(self.dst, _ctx(target="libfoo", node="search_spec", backend="claude_code"),
                            presets_dir=self.src)
        out = (self.dst / "CLAUDE.md").read_text()
        self.assertIn("target=libfoo", out)
        self.assertIn("node=search_spec", out)

    def test_creates_destination_if_missing(self):
        (self.src / "a.md").write_text("hi {target}")
        nested = self.dst / "x" / "y"
        presets.render_into(nested, _ctx(target="t"), presets_dir=self.src)
        self.assertTrue((nested / "a.md").is_file())

    def test_preserves_subdirectory_layout(self):
        (self.src / ".claude").mkdir()
        (self.src / ".claude" / "settings.json").write_text(
            '{{"target": "{target}"}}'
        )
        (self.src / "skills").mkdir()
        (self.src / "skills" / "README.md").write_text("skills for {node}")

        presets.render_into(self.dst, _ctx(target="libfoo", node="plan_by_spec", backend="claude_code"),
                            presets_dir=self.src)

        settings = json.loads((self.dst / ".claude" / "settings.json").read_text())
        self.assertEqual(settings, {"target": "libfoo"})
        self.assertEqual(
            (self.dst / "skills" / "README.md").read_text(),
            "skills for {node}",
        )

    def test_skill_references_are_copied_without_formatting(self):
        (self.src / "skills" / "rory" / "references").mkdir(parents=True)
        source = (
            "target={target}\n"
            "```go\n"
            "func mountStub(dest string) error {\n"
            "    os.MkdirAll(dest, 0755)\n"
            "    return unix.Mount(source, dest, \"none\", unix.MS_BIND, \"\")\n"
            "}\n"
            "```\n"
        )
        (self.src / "skills" / "rory" / "references" / "case.md").write_text(source)

        presets.render_into(
            self.dst,
            _ctx(target="libfoo", node="fetch_target_repo", backend="codex"),
            presets_dir=self.src,
        )

        self.assertEqual(
            (self.dst / "skills" / "rory" / "references" / "case.md").read_text(),
            source,
        )

    # -------------------------------------------------------- binary handling
    def test_binary_files_copied_unchanged(self):
        blob = bytes(range(256))
        (self.src / "icon.png").write_bytes(blob)
        presets.render_into(self.dst, _ctx(), presets_dir=self.src)
        self.assertEqual((self.dst / "icon.png").read_bytes(), blob)

    def test_binary_with_brace_bytes_not_corrupted(self):
        # 二进制不应跑 str.format，因此即使含 `{x}` 字节也要原样
        blob = b"\x00{target}\x01\x02"
        (self.src / "blob.bin").write_bytes(blob)
        presets.render_into(self.dst, _ctx(target="libfoo"), presets_dir=self.src)
        self.assertEqual((self.dst / "blob.bin").read_bytes(), blob)

    # ------------------------------------------------------- robustness paths
    def test_missing_presets_dir_is_ok(self):
        # 不存在的 src 不应炸 —— 仅创建 dst 然后写 extra_files
        ghost = self.tmp / "no_such_dir"
        presets.render_into(self.dst, _ctx(target="libfoo"),
                            presets_dir=ghost,
                            extra_files=[("only.md", "hi {target}")])
        self.assertEqual((self.dst / "only.md").read_text(), "hi libfoo")

    def test_extra_files_override_and_extend(self):
        (self.src / "CLAUDE.md").write_text("orig {target}")
        presets.render_into(
            self.dst,
            _ctx(target="libfoo", backend="claude_code"),
            presets_dir=self.src,
            extra_files=[
                ("CLAUDE.md", "override {target}"),     # 覆盖
                ("nested/extra.md", "extra {node}"),    # 新建嵌套
            ],
        )
        self.assertEqual((self.dst / "CLAUDE.md").read_text(), "override libfoo")
        self.assertEqual((self.dst / "nested" / "extra.md").read_text(), "extra x")

    def test_unknown_placeholder_in_template_is_preserved(self):
        # 即使文档里写了 ctx 里没有的 key，也不应抛错
        (self.src / "guide.md").write_text("see {undocumented_var}")
        presets.render_into(self.dst, _ctx(), presets_dir=self.src)
        self.assertEqual(
            (self.dst / "guide.md").read_text(),
            "see {undocumented_var}",
        )


class RenderBundledPresetsTest(unittest.TestCase):
    """端到端: 用 bundled presets 渲染, 确保 runtime 文件过滤 + 内容合法."""

    def test_render_bundled_presets_for_codex(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp) / "sub_ws"
            ctx = _ctx(
                workspace_base="/ws/workspace_for_libfoo",
                main="/ws/workspace_for_libfoo/main",
                similar="/ws/workspace_for_libfoo/similar",
                log="/ws/workspace_for_libfoo/log",
                sub_workspace=str(dst),
                node="plan_by_spec",
                subtask_id="spec-001",
                target="libfoo 1.2.3",
                backend="codex",
            )
            presets.render_into(dst, ctx)

            # 关键文件存在
            for rel in ("AGENTS.md",
                        ".codex/config.toml",
                        "skills/README.md"):
                self.assertTrue((dst / rel).is_file(), f"missing {rel}")
            self.assertFalse((dst / "CLAUDE.md").exists())
            self.assertFalse((dst / ".claude").exists())
            self.assertFalse((dst / ".kimi-code").exists())

            # 内部目录不应被原样拷出
            self.assertFalse((dst / "roles").exists(),
                             "roles/ should not be copied to sub_workspace")
            self.assertFalse((dst / "contracts").exists(),
                             "contracts/ should not be copied to sub_workspace")

            # AGENTS.md 完成路径替换
            agents = (dst / "AGENTS.md").read_text()
            self.assertIn("/ws/workspace_for_libfoo", agents)
            self.assertIn("plan_by_spec", agents)
            self.assertIn("spec-001", agents)

            # config.toml 必须可被标准库 tomllib 解析
            try:
                import tomllib
            except ImportError:  # py<3.11
                import tomli as tomllib  # type: ignore[no-redef]
            cfg = tomllib.loads((dst / ".codex" / "config.toml").read_text())
            self.assertEqual(cfg["sandbox_mode"], "workspace-write")
            self.assertIn(
                "/ws/workspace_for_libfoo",
                cfg["sandbox_workspace_write"]["writable_roots"],
            )
            self.assertEqual(
                cfg["shell_environment_policy"]["set"]["ZEROMDASH_NODE"],
                "plan_by_spec",
            )
            self.assertEqual(
                cfg["shell_environment_policy"]["set"]["ZEROMDASH_SUBTASK"],
                "spec-001",
            )

    def test_render_bundled_presets_for_traex(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp) / "sub_ws"
            ctx = _ctx(
                workspace_base="/ws/workspace_for_libfoo",
                main="/ws/workspace_for_libfoo/main",
                similar="/ws/workspace_for_libfoo/similar",
                log="/ws/workspace_for_libfoo/log",
                sub_workspace=str(dst),
                node="plan_by_spec",
                subtask_id="spec-001",
                target="libfoo 1.2.3",
                backend="traex",
            )
            presets.render_into(dst, ctx)

            for rel in ("AGENTS.md", "skills/README.md", "output.schema.json"):
                self.assertTrue((dst / rel).is_file(), f"missing {rel}")
            self.assertFalse((dst / "CLAUDE.md").exists())
            self.assertFalse((dst / ".claude").exists())
            self.assertFalse((dst / ".codex").exists())
            self.assertFalse((dst / ".kimi-code").exists())
            self.assertFalse((dst / ".dsh").exists())

            agents = (dst / "AGENTS.md").read_text()
            self.assertIn("runs the `traex` runtime", agents)
            self.assertIn("TraeX receives it through `--add-dir`", agents)
            self.assertIn("plan_by_spec", agents)
            self.assertIn("spec-001", agents)

            schema = json.loads((dst / "output.schema.json").read_text())
            self.assertEqual(schema["type"], "array")
            self.assertEqual(schema["items"]["title"], "Subtask")
            self.assertNotIn("$ref", schema["items"])

    def test_render_bundled_presets_for_claude_code(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp) / "sub_ws"
            ctx = _ctx(
                workspace_base="/ws/workspace_for_libfoo",
                main="/ws/workspace_for_libfoo/main",
                similar="/ws/workspace_for_libfoo/similar",
                log="/ws/workspace_for_libfoo/log",
                sub_workspace=str(dst),
                node="plan_by_spec",
                subtask_id="spec-001",
                target="libfoo 1.2.3",
                backend="claude_code",
            )
            presets.render_into(dst, ctx)

            for rel in ("CLAUDE.md", ".claude/settings.json", ".claude/settings.local.json", "skills/README.md"):
                self.assertTrue((dst / rel).is_file(), f"missing {rel}")
            self.assertFalse((dst / "AGENTS.md").exists())
            self.assertFalse((dst / ".codex").exists())
            self.assertFalse((dst / ".kimi-code").exists())

            claude = (dst / "CLAUDE.md").read_text()
            self.assertIn("/ws/workspace_for_libfoo", claude)
            self.assertIn("plan_by_spec", claude)
            self.assertIn("spec-001", claude)

            # settings.json 必须是合法 JSON, 且 sandbox 写权限指向整个 workspace
            settings = json.loads((dst / ".claude" / "settings.json").read_text())
            self.assertIn("permissions", settings)
            allow = settings["permissions"]["allow"]
            self.assertTrue(any("/ws/workspace_for_libfoo" in rule for rule in allow))
            self.assertIn("/ws/workspace_for_libfoo", settings["permissions"]["additionalDirectories"])
            self.assertIn(
                "Write(/ws/workspace_for_libfoo/main/repo/**",
                settings["permissions"]["deny"][0],
            )
            self.assertTrue(
                any(
                    "Write(/ws/workspace_for_libfoo/main/repos/**" in rule
                    for rule in settings["permissions"]["deny"]
                )
            )
            self.assertIn(
                "/ws/workspace_for_libfoo/main/repo",
                settings["sandbox"]["filesystem"]["denyWrite"],
            )
            self.assertIn(
                "/ws/workspace_for_libfoo/main/repos",
                settings["sandbox"]["filesystem"]["denyWrite"],
            )

    def test_render_shared_investigation_discipline_for_claude_code(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp) / "sub_ws"
            ctx = _ctx(
                workspace_base="/ws/workspace_for_libfoo",
                main="/ws/workspace_for_libfoo/main",
                similar="/ws/workspace_for_libfoo/similar",
                log="/ws/workspace_for_libfoo/log",
                sub_workspace=str(dst),
                node="investigate_subtask",
                subtask_id="vuln-001",
                target="libfoo 1.2.3",
                backend="claude_code",
            )
            presets.render_into(dst, ctx)

            claude = (dst / "CLAUDE.md").read_text()
            self.assertIn("domain-adaptive investigation discipline", claude)
            self.assertIn("terminal check, boundary, or effect", claude)
            self.assertIn("reachable implementations", claude)
            self.assertIn("invariant gaps, reachability, and demonstrated", claude)
            self.assertIn("impact separate when reporting severity", claude)

    def test_render_bundled_presets_for_kimi(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp) / "sub_ws"
            ctx = _ctx(
                workspace_base="/ws/workspace_for_libfoo",
                main="/ws/workspace_for_libfoo/main",
                similar="/ws/workspace_for_libfoo/similar",
                log="/ws/workspace_for_libfoo/log",
                sub_workspace=str(dst),
                node="plan_by_spec",
                subtask_id="spec-001",
                target="libfoo 1.2.3",
                backend="kimi",
            )
            presets.render_into(dst, ctx)

            for rel in (".kimi-code/AGENTS.md", ".kimi-code/local.toml", "skills/README.md"):
                self.assertTrue((dst / rel).is_file(), f"missing {rel}")
            self.assertFalse((dst / "CLAUDE.md").exists())
            self.assertFalse((dst / "AGENTS.md").exists())
            self.assertFalse((dst / ".claude").exists())
            self.assertFalse((dst / ".codex").exists())

            agents = (dst / ".kimi-code" / "AGENTS.md").read_text()
            self.assertIn("/ws/workspace_for_libfoo", agents)
            self.assertIn("plan_by_spec", agents)
            self.assertIn("spec-001", agents)

            try:
                import tomllib
            except ImportError:  # py<3.11
                import tomli as tomllib  # type: ignore[no-redef]
            kimi_cfg = tomllib.loads((dst / ".kimi-code" / "local.toml").read_text())
            self.assertEqual(
                kimi_cfg["workspace"]["additional_dir"],
                ["/ws/workspace_for_libfoo"],
            )

    def test_render_bundled_presets_for_dsh_minimal(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp) / "sub_ws"
            ctx = _ctx(
                workspace_base="/ws/workspace_for_libfoo",
                main="/ws/workspace_for_libfoo/main",
                similar="/ws/workspace_for_libfoo/similar",
                log="/ws/workspace_for_libfoo/log",
                sub_workspace=str(dst),
                node="investigate_subtask",
                subtask_id="vuln-001",
                target="libfoo 1.2.3",
                backend="dsh",
            )
            presets.render_into(dst, ctx)

            for rel in (
                ".dsh/AGENTS.md",
                ".dsh/headless-minimal.patch.yml",
                "skills/README.md",
                "output.schema.json",
            ):
                self.assertTrue((dst / rel).is_file(), f"missing {rel}")
            self.assertFalse((dst / "CLAUDE.md").exists())
            self.assertFalse((dst / "AGENTS.md").exists())
            self.assertFalse((dst / ".claude").exists())
            self.assertFalse((dst / ".codex").exists())
            self.assertFalse((dst / ".kimi-code").exists())

            instructions = (dst / ".dsh" / "AGENTS.md").read_text()
            self.assertIn("/ws/workspace_for_libfoo", instructions)
            self.assertIn("investigate_subtask", instructions)
            self.assertIn("vuln-001", instructions)
            self.assertIn("persistent `bash`, direct file `read`/`write`/`edit`", instructions)
            self.assertIn("`glob`, and `grep`", instructions)
            self.assertIn("deterministic\nartifact creation", instructions)
            self.assertIn("Prefer batched, repository-wide inspection", instructions)

            patch_text = (
                dst / ".dsh" / "headless-minimal.patch.yml"
            ).read_text()
            self.assertIn("ZEROMDASH_DSH_PROMPT_FILE", patch_text)
            self.assertIn("ZEROMDASH_DSH_SESSION_ROOT", patch_text)
            self.assertIn("zeromdash-minimal-shell", patch_text)
            self.assertIn("persistent-bash", patch_text)
            self.assertNotIn("domain-adaptive investigation discipline", patch_text)
            self.assertIn("zeromdash-search-tools", patch_text)
            self.assertIn("@deepseek-ai/dsh-tool-fs-search", patch_text)
            self.assertIn("globMaxResults: 200", patch_text)
            self.assertIn("grepMaxMatches: 500", patch_text)
            self.assertIn("- id: tool-fs\n  disabled: false", patch_text)
            self.assertIn("- id: tool-web\n  disabled: true", patch_text)
            self.assertIn("tool-subagent", patch_text)
            self.assertNotIn("tool-subagent-report", patch_text)
            self.assertNotIn("llm-lb-proxy", patch_text)
            self.assertNotIn("DeepSeek-V4.1-Flash", patch_text)
            self.assertIn("disabled: true", patch_text)


# ----------------------------------------------------------------------------
# 方案 B: role / contract 注入逻辑
# ----------------------------------------------------------------------------
class RoleAndContractInjectionTest(unittest.TestCase):
    """覆盖 presets/roles/{node}.md 与 presets/contracts/*.schema.json 的注入路径."""

    def setUp(self):
        self._tmp = TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.src = self.tmp / "src"
        (self.src / "roles").mkdir(parents=True)
        (self.src / "contracts").mkdir(parents=True)
        # 一个最小 CLAUDE.md, 仅含两个占位符 + 几个上下文字段
        (self.src / "CLAUDE.md").write_text(
            "node={node}\n"
            "ROLE>>>{role_block}<<<\n"
            "CONTRACT>>>{contract_block}<<<\n"
        )
        # 一个最小 AGENTS.md
        (self.src / "AGENTS.md").write_text(
            "node={node}\nROLE>>>{role_block}<<<\n"
        )

    def tearDown(self):
        self._tmp.cleanup()

    def test_role_block_filled_from_roles_md(self):
        (self.src / "roles" / "search_spec.md").write_text(
            "I am the spec archaeologist for {target}."
        )
        dst = self.tmp / "dst"
        presets.render_into(
            dst, _ctx(node="search_spec", target="libfoo", backend="claude_code"), presets_dir=self.src
        )
        claude = (dst / "CLAUDE.md").read_text()
        self.assertIn("ROLE>>>I am the spec archaeologist for libfoo.<<<", claude)
        # 内部目录不应被拷贝
        self.assertFalse((dst / "roles").exists())
        self.assertFalse((dst / "contracts").exists())

    def test_role_block_uses_localized_role_when_requested(self):
        (self.src / "roles" / "search_spec.md").write_text("English role for {target}.")
        (self.src / "roles" / "zh_CN").mkdir()
        (self.src / "roles" / "zh_CN" / "search_spec.md").write_text("中文角色：{target}")
        dst = self.tmp / "dst"

        presets.render_into(
            dst,
            _ctx(node="search_spec", target="libfoo", role_lang="zh_CN", backend="claude_code"),
            presets_dir=self.src,
        )

        claude = (dst / "CLAUDE.md").read_text()
        self.assertIn("ROLE>>>中文角色：libfoo<<<", claude)
        self.assertNotIn("English role", claude)

    def test_role_block_falls_back_to_english_when_localized_role_missing(self):
        (self.src / "roles" / "search_spec.md").write_text("English fallback for {target}.")
        (self.src / "roles" / "zh_CN").mkdir()
        dst = self.tmp / "dst"

        presets.render_into(
            dst,
            _ctx(node="search_spec", target="libfoo", role_lang="zh_CN", backend="claude_code"),
            presets_dir=self.src,
        )

        claude = (dst / "CLAUDE.md").read_text()
        self.assertIn("ROLE>>>English fallback for libfoo.<<<", claude)

    def test_role_block_falls_back_when_node_card_missing(self):
        dst = self.tmp / "dst"
        presets.render_into(
            dst, _ctx(node="some_unknown_node", backend="claude_code"), presets_dir=self.src
        )
        claude = (dst / "CLAUDE.md").read_text()
        # 使用 fallback 文案, 而非 KeyError 或空串
        self.assertIn("no role card bundled", claude)

    def test_contract_block_says_markdown_when_node_not_in_NODE_CONTRACTS(self):
        # search_spec 不在 NODE_CONTRACTS 中, 应得到 markdown fallback
        (self.src / "roles" / "search_spec.md").write_text("role text")
        dst = self.tmp / "dst"
        presets.render_into(
            dst, _ctx(node="search_spec", backend="claude_code"), presets_dir=self.src
        )
        claude = (dst / "CLAUDE.md").read_text()
        self.assertIn("CONTRACT>>>", claude)
        self.assertIn("Markdown", claude)
        # 不应复制 output.schema.json
        self.assertFalse((dst / "output.schema.json").exists())

    def test_contract_block_and_schema_for_json_node(self):
        # plan_by_spec 在 NODE_CONTRACTS 中, 期望 contract_block 提到 JSON
        # 且 contracts/plan.schema.json 被拷为 ./output.schema.json
        (self.src / "roles" / "plan_by_spec.md").write_text("planner role")
        (self.src / "contracts" / "plan.schema.json").write_text(
            json.dumps({"$id": "stub-plan", "type": "array"})
        )
        dst = self.tmp / "dst"
        presets.render_into(
            dst, _ctx(node="plan_by_spec", backend="claude_code"), presets_dir=self.src
        )
        claude = (dst / "CLAUDE.md").read_text()
        self.assertIn("JSON", claude)
        self.assertIn("output.schema.json", claude)
        # output.schema.json 必须被拷出且内容等同于 plan.schema.json
        schema_file = dst / "output.schema.json"
        self.assertTrue(schema_file.is_file())
        self.assertEqual(
            json.loads(schema_file.read_text()),
            {"$id": "stub-plan", "type": "array"},
        )

    def test_unknown_json_node_without_schema_does_not_crash(self):
        # 即便 NODE_CONTRACTS 写了某 node, 但对应 schema 文件缺失也不应炸
        original = presets.NODE_CONTRACTS.copy()
        try:
            presets.NODE_CONTRACTS["temporary_node"] = "missing.schema.json"
            (self.src / "roles" / "temporary_node.md").write_text("temp")
            dst = self.tmp / "dst"
            presets.render_into(
                dst, _ctx(node="temporary_node", backend="claude_code"), presets_dir=self.src
            )
            self.assertFalse((dst / "output.schema.json").exists())
        finally:
            presets.NODE_CONTRACTS.clear()
            presets.NODE_CONTRACTS.update(original)


class BundledRolesAndContractsTest(unittest.TestCase):
    """端到端: bundled presets 必须为每个被引用的 node 提供 role + (可选)contract."""

    def test_bundled_role_files_for_every_node(self):
        roles_dir = presets.default_presets_dir() / "roles"
        self.assertTrue(roles_dir.is_dir())
        for node in nodes.DEFAULT_BACKENDS:
            self.assertTrue(
                (roles_dir / f"{node}.md").is_file(),
                f"missing roles/{node}.md",
            )

    def test_bundled_zh_cn_role_files_for_every_node(self):
        roles_dir = presets.default_presets_dir() / "roles" / "zh_CN"
        self.assertTrue(roles_dir.is_dir())
        for node in nodes.DEFAULT_BACKENDS:
            self.assertTrue(
                (roles_dir / f"{node}.md").is_file(),
                f"missing roles/zh_CN/{node}.md",
            )

    def test_bundled_render_uses_zh_cn_role_when_requested(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp) / "sub_ws"
            presets.render_into(dst, _ctx(node="critic_subtask", role_lang="zh_CN", backend="claude_code"))
            claude = (dst / "CLAUDE.md").read_text()
            self.assertIn("角色：critic reviewer", claude)
            self.assertIn("你负责审查", claude)
            self.assertIn("output.schema.json", claude)

    def test_legacy_critic_one_preset_name_uses_critic_subtask_role(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp) / "sub_ws"
            presets.render_into(
                dst,
                _ctx(node="critic_one", backend="claude_code"),
            )
            claude = (dst / "CLAUDE.md").read_text()
            self.assertIn("Role: critic reviewer", claude)
            self.assertTrue((dst / "output.schema.json").is_file())

    def test_claude_required_nodes_allow_native_agent_tool(self):
        for node in nodes.NATIVE_SUBAGENT_REQUIRED_NODES:
            with self.subTest(node=node), TemporaryDirectory() as tmp:
                dst = Path(tmp) / "sub_ws"
                presets.render_into(
                    dst,
                    _ctx(node=node, backend="claude_code"),
                )
                settings = json.loads(
                    (dst / ".claude" / "settings.local.json").read_text()
                )
                self.assertIn("Agent", settings["permissions"]["allow"])

    def test_claude_non_required_node_does_not_receive_agent_permission(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp) / "sub_ws"
            presets.render_into(
                dst,
                _ctx(node="plan_by_spec", backend="claude_code"),
            )
            settings = json.loads(
                (dst / ".claude" / "settings.local.json").read_text()
            )
            self.assertNotIn("Agent", settings["permissions"]["allow"])

    def test_required_node_roles_mandate_native_subagent_delegation(self):
        roles_dir = presets.default_presets_dir() / "roles"
        for lang in ("", "zh_CN"):
            root = roles_dir / lang if lang else roles_dir
            for node in nodes.NATIVE_SUBAGENT_REQUIRED_NODES:
                with self.subTest(lang=lang or "en", node=node):
                    role = (root / f"{node}.md").read_text().lower()
                    self.assertTrue(
                        "native" in role or "原生" in role,
                        f"{lang or 'en'}/{node} does not require native delegation",
                    )
                    self.assertTrue(
                        "subagent" in role or "子 agent" in role,
                        f"{lang or 'en'}/{node} does not name the delegated agent",
                    )

    def test_bundled_contract_schemas_resolvable(self):
        contracts_dir = presets.default_presets_dir() / "contracts"
        self.assertTrue(contracts_dir.is_dir())
        for node, schema_name in presets.NODE_CONTRACTS.items():
            schema_path = contracts_dir / schema_name
            self.assertTrue(
                schema_path.is_file(),
                f"missing contracts/{schema_name} for node {node}",
            )
            # 必须是合法 JSON
            json.loads(schema_path.read_text())

    def test_search_target_history_materializes_patch_manifest_schema(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp) / "sub_ws"
            presets.render_into(
                dst,
                _ctx(node="search_target_history", backend="claude_code"),
            )

            schema_path = dst / "patch-manifest.schema.json"
            self.assertTrue(schema_path.is_file())
            schema = json.loads(schema_path.read_text())
            self.assertEqual(schema["properties"]["schema_version"]["const"], "1.0")
            self.assertIn("repositories", schema["required"])
            self.assertIn("coverage", schema["required"])
            self.assertIn("findings", schema["required"])

    def test_analyze_attack_surface_materializes_domain_registry_schema(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp) / "sub_ws"
            presets.render_into(
                dst,
                _ctx(node="analyze_attack_surface", backend="codex"),
            )
            schema_path = dst / "domain-invariant-registry.schema.json"
            self.assertTrue(schema_path.is_file())
            schema = json.loads(schema_path.read_text())
            self.assertEqual(schema["properties"]["schema_version"]["const"], "1.0")
            self.assertIn("seams", schema["required"])

    def test_bundled_render_for_critic_subtask_includes_role_and_schema(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp) / "sub_ws"
            presets.render_into(dst, _ctx(node="critic_subtask", backend="claude_code"))
            claude = (dst / "CLAUDE.md").read_text()
            self.assertIn("critic", claude.lower())
            self.assertIn("output.schema.json", claude)
            schema = json.loads((dst / "output.schema.json").read_text())
            self.assertEqual(schema["title"], "Review")
            self.assertIn("batchReview", schema["definitions"])
            self.assertIn("hypothesis_verdicts", schema["definitions"]["batchReview"]["required"])
            self.assertIn("new_hypothesis_decisions", schema["definitions"]["batchReview"]["required"])
            coverage = schema["definitions"]["batchReview"]["properties"]["coverage_verdict"]
            self.assertIn("counterexample_attempts", coverage["required"])

    def test_fetch_target_repo_render_allows_materializing_main_repo(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp) / "sub_ws"
            presets.render_into(
                dst,
                _ctx(
                    workspace_base="/ws/workspace_for_libfoo",
                    main="/ws/workspace_for_libfoo/main",
                    similar="/ws/workspace_for_libfoo/similar",
                    log="/ws/workspace_for_libfoo/log",
                    sub_workspace=str(dst),
                    node="fetch_target_repo",
                    backend="claude_code",
                ),
            )

            settings = json.loads((dst / ".claude" / "settings.json").read_text())
            local_settings = json.loads((dst / ".claude" / "settings.local.json").read_text())
            self.assertEqual(settings["permissions"]["deny"], [])
            self.assertEqual(settings["sandbox"]["filesystem"]["denyWrite"], [])
            self.assertNotIn("WebFetch(domain:github.com)", settings["permissions"]["allow"])
            self.assertIn("WebFetch(domain:github.com)", local_settings["permissions"]["allow"])
            self.assertIn("WebFetch(domain:gitlab.com)", local_settings["permissions"]["allow"])
            self.assertIn("WebFetch(domain:codeload.github.com)", local_settings["permissions"]["allow"])
            self.assertIn("WebFetch(domain:nvd.nist.gov)", local_settings["permissions"]["allow"])
            self.assertIn("WebFetch(domain:www.rfc-editor.org)", local_settings["permissions"]["allow"])
            claude = (dst / "CLAUDE.md").read_text()
            self.assertIn("writable only for this acquisition step", claude)
            self.assertIn("/ws/workspace_for_libfoo/main/repo", claude)
            self.assertIn("/ws/workspace_for_libfoo/main/repos", claude)

    def test_claude_code_non_fetch_nodes_get_webfetch_local_settings(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp) / "sub_ws"
            presets.render_into(
                dst,
                _ctx(
                    workspace_base="/ws/workspace_for_libfoo",
                    main="/ws/workspace_for_libfoo/main",
                    similar="/ws/workspace_for_libfoo/similar",
                    log="/ws/workspace_for_libfoo/log",
                    sub_workspace=str(dst),
                    node="search_spec",
                    backend="claude_code",
                ),
            )

            settings = json.loads((dst / ".claude" / "settings.json").read_text())
            local_settings = json.loads((dst / ".claude" / "settings.local.json").read_text())
            self.assertNotIn("WebFetch(domain:github.com)", settings["permissions"]["allow"])
            self.assertIn("WebFetch(domain:github.com)", local_settings["permissions"]["allow"])
            self.assertIn("WebFetch(domain:cve.org)", local_settings["permissions"]["allow"])
            self.assertIn("WebFetch(domain:seclists.org)", local_settings["permissions"]["allow"])

    def test_non_claude_backend_does_not_get_claude_local_settings(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp) / "sub_ws"
            presets.render_into(
                dst,
                _ctx(
                    workspace_base="/ws/workspace_for_libfoo",
                    main="/ws/workspace_for_libfoo/main",
                    similar="/ws/workspace_for_libfoo/similar",
                    log="/ws/workspace_for_libfoo/log",
                    sub_workspace=str(dst),
                    node="search_spec",
                    backend="codex",
                ),
            )

            self.assertFalse((dst / ".claude" / "settings.local.json").exists())


if __name__ == "__main__":
    unittest.main()
