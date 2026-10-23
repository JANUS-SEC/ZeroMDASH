"""Runtime discovery of expert-perspective skills.

The pipeline ships a `presets/skills/` directory; users can also drop
extra skills into any per-invocation sub_workspace (`<sub_workspace>/skills/`).
A "skill" is either:

- a single markdown file:        ``<skills_dir>/<name>.md``
- a directory with a SKILL.md:   ``<skills_dir>/<name>/SKILL.md``

Each skill is parsed to extract a short ``summary`` so that the critic
can pick relevant skills *at runtime* without us hard-coding a mapping
between scenarios and skills.

Summary extraction precedence:
  1. YAML frontmatter (``--- ... ---`` at top of file): keys
     ``summary`` / ``description`` / ``when_to_use``. Simple block scalars such
     as ``description: |`` and ``description: >-`` are supported.
  2. First non-empty markdown paragraph after the first H1/H2.
  3. First non-empty paragraph in the file.

The critic prompt receives a catalog rendered by ``render_catalog`` and
is instructed to choose >= 2 relevant skills and emit their names back
in its JSON output (``selected_skills``).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

# README/index files inside skills/ are not themselves skills.
_NON_SKILL_BASENAMES = {"readme", "index", "_meta", "_index"}


@dataclass(frozen=True)
class SkillInfo:
    name: str          # stable identifier (basename without extension)
    path: str          # absolute path to the skill's primary file
    summary: str       # short, single-paragraph description for prompt injection


# ------------------------------------------------------------------ scanning
def discover_skills(skills_dirs: Iterable[str | Path]) -> list[SkillInfo]:
    """Walk every skills_dir and return a de-duplicated, name-sorted list.

    Later entries with the same `name` override earlier ones, so callers
    can pass [bundled_dir, sub_workspace_dir] to let per-task overrides win.
    """
    found: dict[str, SkillInfo] = {}
    for d in skills_dirs:
        d = Path(d) if d else None
        if not d or not d.exists() or not d.is_dir():
            continue
        for entry in sorted(d.iterdir()):
            info = _load_skill(entry)
            if info is not None:
                found[info.name] = info
    return sorted(found.values(), key=lambda s: s.name)


def _load_skill(entry: Path) -> SkillInfo | None:
    if entry.is_file() and entry.suffix.lower() in {".md", ".mdx"}:
        if entry.stem.lower() in _NON_SKILL_BASENAMES:
            return None
        return _parse_skill_file(name=entry.stem, path=entry)

    if entry.is_dir():
        for cand_name in ("SKILL.md", "skill.md", "README.md"):
            cand = entry / cand_name
            if cand.is_file():
                # 用目录名做 skill name (更稳定), 文件给 summary
                return _parse_skill_file(name=entry.name, path=cand)
    return None


def _parse_skill_file(name: str, path: Path) -> SkillInfo:
    text = path.read_text(errors="replace")
    summary = _extract_summary(text)
    return SkillInfo(name=name, path=str(path), summary=summary)


# ----------------------------------------------------------- summary extract
_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _extract_summary(text: str) -> str:
    fm_match = _FRONTMATTER_RE.match(text)
    body = text
    if fm_match:
        fm = _parse_simple_frontmatter(fm_match.group(1))
        for key in ("summary", "description", "when_to_use", "purpose"):
            v = fm.get(key)
            if v:
                return _one_line(v)
        body = text[fm_match.end():]

    # 跳过开头的标题/分割线，找第一段正文
    paragraph_lines: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            if paragraph_lines:
                break
            continue
        if stripped.startswith("#"):  # markdown heading
            if paragraph_lines:
                break
            continue
        paragraph_lines.append(stripped)

    return _one_line(" ".join(paragraph_lines)) or "(no summary)"


def _parse_simple_frontmatter(block: str) -> dict[str, str]:
    """支持简单 YAML frontmatter, 包括 `key: value` 和 block scalar."""
    out: dict[str, str] = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        k, v = line.split(":", 1)
        key = k.strip().lower()
        value = v.strip()
        if key:
            if _is_block_scalar_header(value):
                base_indent = _indent_width(line)
                i += 1
                block_lines: list[str] = []
                while i < len(lines):
                    next_line = lines[i]
                    if not next_line.strip():
                        block_lines.append("")
                        i += 1
                        continue
                    if _indent_width(next_line) <= base_indent:
                        break
                    block_lines.append(next_line)
                    i += 1
                out[key] = _dedent_block_scalar(block_lines)
                continue
            out[key] = value.strip("\"'")
        i += 1
    return out


def _is_block_scalar_header(value: str) -> bool:
    marker = value.split("#", 1)[0].strip()
    return bool(re.fullmatch(r"[>|](?:[+-]?\d*|\d+[+-]?)", marker))


def _indent_width(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _dedent_block_scalar(lines: list[str]) -> str:
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        return ""
    min_indent = min((_indent_width(line) for line in lines if line.strip()), default=0)
    dedented = [line[min_indent:] if len(line) >= min_indent else "" for line in lines]
    return "\n".join(dedented).strip()


def _one_line(s: str, max_chars: int = 280) -> str:
    s = re.sub(r"\s+", " ", (s or "")).strip()
    return s if len(s) <= max_chars else s[: max_chars - 1].rstrip() + "…"


# ---------------------------------------------------------------- rendering
def render_catalog(skills: list[SkillInfo]) -> str:
    """Render skills as a compact markdown catalog for prompt injection."""
    if not skills:
        return "(no expert skills available)"
    lines = []
    for s in skills:
        lines.append(f"- `{s.name}` — {s.summary}")
    return "\n".join(lines)


def names(skills: list[SkillInfo]) -> list[str]:
    return [s.name for s in skills]
