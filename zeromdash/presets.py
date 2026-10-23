"""Preset materialization for sub_workspaces.

Each sub_workspace gets a copy of:
- Common files: skills/ and output.schema.json when the node has a JSON
  contract.
- Claude Code runtime: CLAUDE.md, .claude/settings.json, and
  .claude/settings.local.json.
- Codex runtime: AGENTS.md and .codex/config.toml.
- TraeX runtime: AGENTS.md. Workspace permissions and structured-output schema
  selection are supplied by the TraeX adapter.
- Kimi runtime: .kimi-code/AGENTS.md and .kimi-code/local.toml.
- DeepSeek Harness runtime: .dsh/AGENTS.md and
  .dsh/headless-minimal.patch.yml.

`render_into` 会把 `presets_dir`（默认指向打包内的 ``zeromdash/presets/``)
中与当前 backend 相关的模板文件按 `str.format(**ctx)` 渲染后写入
sub_workspace。``skills/`` 下的文件是 agent 可读取的原始资料, 不做模板渲染。
``roles/`` 与 ``contracts/`` 这两个内部目录不会被原样拷贝 ——
它们由本模块按 node 单独注入到 runtime 指令文件的 ``{role_block}`` /
``{contract_block}`` 占位符, 以及 ``output.schema.json``。

ctx 默认会包含:
- workspace_base / main / similar / log / sub_workspace
- node / subtask_id / target / backend
- role_block / contract_block (本模块自动派生, 调用方不必传)

settings 里的 sandbox 写权限范围会自动扩到整个 workspace_base —— 这正是
"sandbox 范围 allowWrite 整个 workspace 而非 sub_workspace" 的诉求。
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Iterable

# 文本类型通常做 str.format 渲染；skills/ 原始资料除外。其它二进制按字节拷。
_TEXT_SUFFIXES: tuple[str, ...] = (
    ".md", ".mdx", ".txt", ".json", ".jsonc", ".toml", ".yaml", ".yml",
    ".sh", ".py", ".rules", ".cfg", ".ini",
)

# 内部目录: 不会被原样拷贝到 sub_workspace。
# - roles/    : 按 node 注入到 {role_block}
# - contracts/: 按 node 拷贝单个 schema 为 ./output.schema.json
_INTERNAL_DIRS: tuple[str, ...] = ("roles", "contracts")
_NODE_NAME_ALIASES = {
    "critic_one": "critic_subtask",
    "investigate_subagent": "investigate_subtask",
}


# ----------------------------------------------------------- node mappings
# node -> contract schema filename under presets/contracts/.
# 仅列出真正需要发结构化 JSON 的 node; 其它 node 输出 Markdown, 用
# role 段落里的"输出契约"自描述。
NODE_CONTRACTS: dict[str, str] = {
    "plan_by_spec":            "plan.schema.json",
    "plan_by_vuln_similar":    "plan.schema.json",
    "plan_by_vuln_patch":      "plan.schema.json",
    "plan_by_new_feature":     "plan.schema.json",
    "plan_chains":             "chain-plan.schema.json",
    "investigate_subtask":    "investigation.schema.json",
    "critic_subtask":              "review.schema.json",
    "chain_investigate_subtask": "chain-investigation.schema.json",
    "chain_critic_subtask": "chain-review.schema.json",
    "chain_finalizer_subtask": "chain-finalizer.schema.json",
    "report_group_adjudicator": "report-group-adjudication.schema.json",
    "gather_analyze_attack_surface": "cross-target-registry.schema.json",
    "gather_plan_chains": "gather-chain-plan.schema.json",
    "gather_chain_investigate_subtask": "gather-chain-investigation.schema.json",
    "gather_chain_critic_subtask": "gather-chain-review.schema.json",
    "gather_chain_finalizer_subtask": "gather-chain-finalizer.schema.json",
    "gather_report_group_adjudicator": "report-group-adjudication.schema.json",
}

# Nodes that write a structured side artifact in addition to their primary
# Markdown output. The schema keeps its descriptive filename in the agent CWD
# instead of becoming output.schema.json.
NODE_AUXILIARY_CONTRACTS: dict[str, tuple[str, ...]] = {
    "search_target_history": ("patch-manifest.schema.json",),
    "analyze_attack_surface": ("domain-invariant-registry.schema.json",),
}

NATIVE_SUBAGENT_REQUIRED_NODES = frozenset(
    {
        "investigate_subtask",
        "critic_subtask",
        "plan_chains",
        "chain_investigate_subtask",
        "chain_critic_subtask",
        "chain_finalizer_subtask",
        "report_group_adjudicator",
        "gather_analyze_attack_surface",
        "gather_plan_chains",
        "gather_chain_investigate_subtask",
        "gather_chain_critic_subtask",
        "gather_chain_finalizer_subtask",
        "gather_report_group_adjudicator",
        "summary",
    }
)

# Fallback role 文本, 当某 node 缺少 roles/{node}.md 时注入。
_ROLE_FALLBACK = (
    "_(no role card bundled for this node — fall back to the per-call "
    "prompt for behaviour. The orchestrator is still responsible for "
    "passing all parameters.)_"
)

# Fallback contract 文本, 当某 node 不在 NODE_CONTRACTS 中时注入。
_CONTRACT_FALLBACK_MARKDOWN = (
    "This node produces **Markdown**. The required structure is described "
    "in the role section above. Save the final artifact to the path the "
    "orchestrator names in the prompt."
)

_CONTRACT_FALLBACK_JSON = (
    "This node produces **JSON** validated against `./output.schema.json` "
    "(materialized in your CWD). Emit JSON only — no prose, no code "
    "fences, no commentary."
)

CLAUDE_WEBFETCH_DOMAIN_ALLOWS: tuple[str, ...] = (
    # Common public source hosting / archive domains. Claude Code's
    # sandbox.network is not enough for tool-level domain permissions; these
    # explicit grants let Claude nodes fetch source pages, tarballs, specs,
    # CVE records, advisories, and public security references.
    "WebFetch(domain:github.com)",
    "WebFetch(domain:api.github.com)",
    "WebFetch(domain:codeload.github.com)",
    "WebFetch(domain:raw.githubusercontent.com)",
    "WebFetch(domain:objects.githubusercontent.com)",
    "WebFetch(domain:github.blog)",
    "WebFetch(domain:githubsecuritylab.github.com)",
    "WebFetch(domain:gitlab.com)",
    "WebFetch(domain:gitlab.freedesktop.org)",
    "WebFetch(domain:bitbucket.org)",
    "WebFetch(domain:codeberg.org)",
    "WebFetch(domain:git.sr.ht)",
    "WebFetch(domain:repo.or.cz)",
    "WebFetch(domain:gitee.com)",
    "WebFetch(domain:sourceforge.net)",
    "WebFetch(domain:svnweb.freebsd.org)",
    "WebFetch(domain:git.kernel.org)",
    "WebFetch(domain:www.kernel.org)",
    "WebFetch(domain:docs.kernel.org)",
    "WebFetch(domain:lore.kernel.org)",
    "WebFetch(domain:patchwork.kernel.org)",
    "WebFetch(domain:bugzilla.kernel.org)",
    "WebFetch(domain:kernel.googlesource.com)",
    "WebFetch(domain:chromium.googlesource.com)",
    "WebFetch(domain:go.googlesource.com)",
    "WebFetch(domain:android.googlesource.com)",
    "WebFetch(domain:boringssl.googlesource.com)",
    "WebFetch(domain:webrtc.googlesource.com)",
    "WebFetch(domain:skia.googlesource.com)",
    "WebFetch(domain:git.savannah.gnu.org)",
    "WebFetch(domain:sourceware.org)",
    "WebFetch(domain:git.openssl.org)",
    "WebFetch(domain:hg.mozilla.org)",
    "WebFetch(domain:bugzilla.mozilla.org)",
    "WebFetch(domain:sqlite.org)",
    "WebFetch(domain:fossil-scm.org)",
    "WebFetch(domain:www.rfc-editor.org)",
    "WebFetch(domain:datatracker.ietf.org)",
    "WebFetch(domain:www.ietf.org)",
    "WebFetch(domain:www.w3.org)",
    "WebFetch(domain:docs.oasis-open.org)",
    "WebFetch(domain:standards.ieee.org)",
    "WebFetch(domain:www.khronos.org)",
    "WebFetch(domain:cve.org)",
    "WebFetch(domain:cve.mitre.org)",
    "WebFetch(domain:nvd.nist.gov)",
    "WebFetch(domain:osv.dev)",
    "WebFetch(domain:securitylab.github.com)",
    "WebFetch(domain:googleprojectzero.blogspot.com)",
    "WebFetch(domain:projectzero.google)",
    "WebFetch(domain:bugs.chromium.org)",
    "WebFetch(domain:issues.chromium.org)",
    "WebFetch(domain:seclists.org)",
    "WebFetch(domain:www.openwall.com)",
    "WebFetch(domain:oss-security.openwall.org)",
    "WebFetch(domain:security-tracker.debian.org)",
    "WebFetch(domain:lists.debian.org)",
    "WebFetch(domain:ubuntu.com)",
    "WebFetch(domain:access.redhat.com)",
    "WebFetch(domain:bugzilla.redhat.com)",
)


def default_presets_dir() -> Path:
    """Return the package-bundled presets directory."""
    return Path(__file__).resolve().parent / "presets"


def _is_text(p: Path) -> bool:
    return p.suffix.lower() in _TEXT_SUFFIXES


def _should_format_text(rel: Path) -> bool:
    """Return False for copied source material that is not a preset template."""
    return not rel.parts or rel.parts[0] != "skills"


def _safe_format(text: str, ctx: dict[str, Any]) -> str:
    """str.format 但容忍模板里没用到的占位符 (例如示例代码块里的 `{var}`).

    我们用 `string.Formatter` 的 vformat + 自定义 dict 来兜底。
    """
    import string

    class _SafeDict(dict):
        def __missing__(self, key: str) -> str:  # type: ignore[override]
            return "{" + key + "}"

    try:
        return string.Formatter().vformat(text, (), _SafeDict(ctx))
    except (IndexError, ValueError):
        # 模板含 `{}` 这种位置参数会进这里；直接原样返回
        return text


# ----------------------------------------------------------- internal helpers
def _is_under_internal_dir(rel: Path) -> bool:
    """Return True if `rel` is inside any of the _INTERNAL_DIRS."""
    parts = rel.parts
    return bool(parts) and parts[0] in _INTERNAL_DIRS


def _resolve_role_block(presets_root: Path, node: str | None, ctx: dict[str, Any]) -> str:
    """Read the node role card for the requested language.

    Default English cards live at ``presets/roles/{node}.md`` for backwards
    compatibility. Localized cards live at ``presets/roles/{role_lang}/{node}.md``
    and fall back to English if the requested localization is incomplete.
    """
    if not node:
        return _ROLE_FALLBACK
    role_lang = str(ctx.get("role_lang") or "en").strip()
    role_files: list[Path] = []
    if role_lang and role_lang not in {"en", "en_US"}:
        role_files.append(presets_root / "roles" / role_lang / f"{node}.md")
    role_files.append(presets_root / "roles" / f"{node}.md")
    for role_file in role_files:
        if role_file.is_file():
            return _safe_format(role_file.read_text(), ctx)
    return _ROLE_FALLBACK


def _resolve_contract_block(node: str | None) -> str:
    """Return a short blurb describing this node's output contract."""
    if node and node in NODE_CONTRACTS:
        return _CONTRACT_FALLBACK_JSON
    return _CONTRACT_FALLBACK_MARKDOWN


def _materialize_output_schema(
    presets_root: Path, dst: Path, node: str | None
) -> None:
    """Write a self-contained contract to ``dst/output.schema.json``.

    TraeX accepts a single ``--output-schema`` path. Inline local sibling
    references such as ``subtask.schema.json`` so every runtime receives the
    same portable schema without exposing the internal ``contracts/`` tree.
    """
    if not node:
        return
    schema_name = NODE_CONTRACTS.get(node)
    if not schema_name:
        return
    src = presets_root / "contracts" / schema_name
    if not src.is_file():
        return
    target = dst / "output.schema.json"
    target.write_text(
        json.dumps(
            _inline_local_schema_refs(json.loads(src.read_text()), src.parent),
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )


def _materialize_auxiliary_schemas(
    presets_root: Path, dst: Path, node: str | None
) -> None:
    if not node:
        return
    for schema_name in NODE_AUXILIARY_CONTRACTS.get(node, ()):
        src = presets_root / "contracts" / schema_name
        if not src.is_file():
            continue
        (dst / schema_name).write_text(
            json.dumps(
                _inline_local_schema_refs(json.loads(src.read_text()), src.parent),
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )


def _inline_local_schema_refs(value: Any, schema_dir: Path) -> Any:
    """Recursively replace local file ``$ref`` entries with their schemas."""
    if isinstance(value, list):
        return [_inline_local_schema_refs(item, schema_dir) for item in value]
    if not isinstance(value, dict):
        return value

    ref = value.get("$ref")
    if isinstance(ref, str) and ref and not ref.startswith(("#", "http://", "https://")):
        ref_path = (schema_dir / ref).resolve()
        try:
            ref_path.relative_to(schema_dir.resolve())
        except ValueError as exc:
            raise ValueError(f"schema reference escapes contracts directory: {ref}") from exc
        referenced = json.loads(ref_path.read_text())
        inlined = _inline_local_schema_refs(referenced, ref_path.parent)
        siblings = {
            key: _inline_local_schema_refs(item, schema_dir)
            for key, item in value.items()
            if key != "$ref"
        }
        if siblings and isinstance(inlined, dict):
            return {**inlined, **siblings}
        return inlined

    return {
        key: _inline_local_schema_refs(item, schema_dir)
        for key, item in value.items()
    }


def _is_claude_code_backend(backend: Any) -> bool:
    return str(backend or "").strip().replace("-", "_") in {"claude", "claude_code"}


def _normalize_backend(backend: Any) -> str:
    return str(backend or "").strip().lower().replace("-", "_")


def _is_codex_backend(backend: Any) -> bool:
    return _normalize_backend(backend) in {"codex", "codex_cli", "openai_codex"}


def _is_traex_backend(backend: Any) -> bool:
    return _normalize_backend(backend) in {
        "trae",
        "trae_cli",
        "traecli",
        "trae_code",
        "traecode",
        "traex",
    }


def _is_kimi_backend(backend: Any) -> bool:
    return _normalize_backend(backend) in {"kimi", "kimi_code", "kimi_cli"}


def _is_dsh_backend(backend: Any) -> bool:
    return _normalize_backend(backend) in {
        "dsh",
        "deepseek_harness",
        "deepseek_harness_cli",
    }


def _runtime_for_rel(rel: Path) -> str | None:
    if rel == Path("CLAUDE.md") or (rel.parts and rel.parts[0] == ".claude"):
        return "claude_code"
    if rel == Path("AGENTS.md"):
        return "agents_md"
    if rel.parts and rel.parts[0] == ".codex":
        return "codex"
    if rel.parts and rel.parts[0] == ".kimi-code":
        return "kimi"
    if rel.parts and rel.parts[0] == ".dsh":
        return "dsh"
    return None


def _should_materialize_runtime_file(rel: Path, backend: Any) -> bool:
    runtime = _runtime_for_rel(rel)
    if runtime is None:
        return True
    if runtime == "claude_code":
        return _is_claude_code_backend(backend)
    if runtime == "agents_md":
        return _is_codex_backend(backend) or _is_traex_backend(backend)
    if runtime == "codex":
        return _is_codex_backend(backend)
    if runtime == "kimi":
        return _is_kimi_backend(backend)
    if runtime == "dsh":
        return _is_dsh_backend(backend)
    return False


def _materialize_claude_local(dst: Path, backend: Any, node: str | None) -> None:
    """Write Claude local settings for tool-level WebFetch domain grants.

    Keep public WebFetch grants in settings.local.json instead of broadening the
    shared settings.json template. Only Claude Code reads this file; Codex and
    opencode sub_workspaces should not get backend-specific local settings.
    """
    if not _is_claude_code_backend(backend):
        return
    local = dst / ".claude" / "settings.local.json"
    local.parent.mkdir(parents=True, exist_ok=True)
    allow = list(CLAUDE_WEBFETCH_DOMAIN_ALLOWS)
    if node in NATIVE_SUBAGENT_REQUIRED_NODES:
        allow.append("Agent")
    local.write_text(
        json.dumps(
            {
                "permissions": {
                    "allow": allow,
                }
            },
            indent=2,
        )
    )


def render_into(
    dst: Path,
    ctx: dict[str, Any],
    presets_dir: str | Path | None = None,
    extra_files: Iterable[tuple[str, str]] = (),
) -> None:
    """Materialize presets into `dst` (mkdir -p inside, files + subtrees).

    `extra_files` is `[(relative_path, content), ...]` for caller-supplied
    overrides (e.g. node-specific instructions).

    Behaviour:
    - `roles/` and `contracts/` from the source tree are NOT copied to
      `dst`. Their content reaches the agent through the
      ``{role_block}`` / ``{contract_block}`` placeholders inside the
      bundled runtime instruction file, and through a single
      ``output.schema.json`` file copied to ``dst`` for nodes whose
      contract is in ``NODE_CONTRACTS``.
    - Runtime-specific files are filtered by ``ctx["backend"]``; common files
      such as skills are copied for every backend.
    """
    src = Path(presets_dir) if presets_dir else default_presets_dir()
    dst = Path(dst)
    dst.mkdir(parents=True, exist_ok=True)

    # 注入两个派生占位符 (调用方不必显式传)
    raw_node = str(ctx.get("node") or "")
    node = _NODE_NAME_ALIASES.get(raw_node, raw_node) or None
    enriched_ctx: dict[str, Any] = dict(ctx)
    if node:
        enriched_ctx["node"] = node
    enriched_ctx.setdefault(
        "role_block",
        _resolve_role_block(src, node, ctx) if src.exists() else _ROLE_FALLBACK,
    )
    enriched_ctx.setdefault("contract_block", _resolve_contract_block(node))
    main = str(ctx.get("main", "{main}"))
    similar = str(ctx.get("similar", "{similar}"))
    if node == "fetch_target_repo":
        enriched_ctx.setdefault("claude_repo_permission_denies", "")
        enriched_ctx.setdefault("claude_repo_sandbox_deny_write", "")
        enriched_ctx.setdefault(
            "source_tree_policy",
            f"`{main}/repo` and `{main}/repos` are writable only for this "
            "acquisition step. Materialize target source trees at the exact "
            "prompt destinations, then treat them as read-only.",
        )
    else:
        enriched_ctx.setdefault(
            "claude_repo_permission_denies",
            f'"Write({main}/repo/**)",\n      "Edit({main}/repo/**)",\n      '
            f'"Write({main}/repos/**)",\n      "Edit({main}/repos/**)",\n      '
            f'"Write({similar}/**/repo/**)",\n      "Edit({similar}/**/repo/**)"',
        )
        enriched_ctx.setdefault(
            "claude_repo_sandbox_deny_write",
            f'"{main}/repo",\n        "{main}/repos",\n        "{similar}"',
        )
        enriched_ctx.setdefault(
            "source_tree_policy",
            f"`{main}/repo`, `{main}/repos`, and `{similar}/*/repo` are "
            "**read-only** — never patch, format, or reformat them.",
        )

    if src.exists():
        for entry in src.rglob("*"):
            rel = entry.relative_to(src)
            # 跳过内部目录: roles/ 与 contracts/ 不直接拷到 sub_workspace
            if _is_under_internal_dir(rel):
                continue
            if not _should_materialize_runtime_file(rel, enriched_ctx.get("backend")):
                continue
            target = dst / rel
            if entry.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if _is_text(entry) and _should_format_text(rel):
                target.write_text(_safe_format(entry.read_text(), enriched_ctx))
            elif _is_text(entry):
                target.write_text(entry.read_text())
            else:
                shutil.copyfile(entry, target)

        # 单独把对应 contract schema 拷出来当 ./output.schema.json
        _materialize_output_schema(src, dst, node)
        _materialize_auxiliary_schemas(src, dst, node)

        # Claude Code nodes need tool-level WebFetch domain grants. Put them in
        # local settings so the shared template stays conservative and other
        # runtimes do not receive Claude-specific configuration.
        _materialize_claude_local(dst, enriched_ctx.get("backend"), node)

    for rel, content in extra_files:
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_safe_format(content, enriched_ctx))
