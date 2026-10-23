"""Markdown and Mermaid report diagnostics shared by report nodes."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .io import _read_text_lossy


def _each_vulnerability_has_both_diagrams(text: str) -> bool:
    """Require a data-flow and attack-sequence diagram in every VULN section."""
    matches = list(
        re.finditer(r"^###\s+(VULN-\d{3}):", text, re.MULTILINE)
    )
    if not matches:
        return False
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[match.start():end]
        mermaid_blocks = re.findall(
            r"```mermaid[ \t]*\n(.*?)```",
            section,
            re.DOTALL,
        )
        if not any(re.match(r"\s*flowchart\b", block) for block in mermaid_blocks):
            return False
        if not any(
            re.match(r"\s*sequenceDiagram\b", block)
            for block in mermaid_blocks
        ):
            return False
    return True


_MERMAID_BLOCK_RE = re.compile(
    r"```mermaid[ \t]*\n(.*?)```",
    re.DOTALL,
)
_SEQUENCE_PARTICIPANT_RE = re.compile(
    r"^(\s*(?:participant|actor)\s+)([A-Za-z_][A-Za-z0-9_-]*)(\b.*)$",
    re.IGNORECASE,
)
_SEQUENCE_RESERVED_IDS = {
    "activate",
    "actor",
    "alt",
    "and",
    "autonumber",
    "box",
    "break",
    "create",
    "critical",
    "deactivate",
    "destroy",
    "else",
    "end",
    "link",
    "links",
    "loop",
    "note",
    "opt",
    "par",
    "participant",
    "properties",
    "rect",
}
_SEQUENCE_ARROW_RE = re.compile(
    r"(?:--|-)>>|(?:--|-)x|(?:--|-)\)|(?:--|-)\]|(?:--|-)>"
)


def _mermaid_blocks_with_lines(text: str) -> list[tuple[int, int, str]]:
    """Return Markdown Mermaid blocks with 1-based fence line numbers."""
    blocks: list[tuple[int, int, str]] = []
    lines = text.splitlines()
    in_block = False
    start = 0
    body: list[str] = []
    for index, line in enumerate(lines, start=1):
        if not in_block and line.strip() == "```mermaid":
            in_block = True
            start = index
            body = []
            continue
        if in_block and line.strip() == "```":
            blocks.append((start, index, "\n".join(body)))
            in_block = False
            continue
        if in_block:
            body.append(line)
    if in_block:
        blocks.append((start, len(lines), "\n".join(body)))
    return blocks


def _safe_sequence_participant_id(
    participant_id: str,
    used: set[str],
) -> str:
    base = re.sub(r"[^A-Za-z0-9_]", "_", participant_id).strip("_") or "Actor"
    if not re.match(r"^[A-Za-z_]", base):
        base = f"Actor_{base}"
    if base.lower() in _SEQUENCE_RESERVED_IDS:
        base = f"{base}Node"
    candidate = base
    suffix = 2
    while candidate in used or candidate.lower() in _SEQUENCE_RESERVED_IDS:
        candidate = f"{base}{suffix}"
        suffix += 1
    return candidate


def _polish_sequence_diagram_block(block: str) -> tuple[str, list[str]]:
    """Fix common Mermaid sequenceDiagram syntax hazards without changing flow."""
    lines = block.splitlines()
    used: set[str] = set()
    rename: dict[str, str] = {}
    changed: list[str] = []
    rewritten: list[str] = []

    for line in lines:
        match = _SEQUENCE_PARTICIPANT_RE.match(line)
        if not match:
            rewritten.append(line)
            continue
        prefix, participant_id, suffix = match.groups()
        new_id = participant_id
        if (
            participant_id.lower() in _SEQUENCE_RESERVED_IDS
            or not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", participant_id)
        ):
            new_id = _safe_sequence_participant_id(participant_id, used)
            rename[participant_id] = new_id
            changed.append(f"renamed sequence participant {participant_id!r} to {new_id!r}")
        used.add(new_id)
        rewritten.append(f"{prefix}{new_id}{suffix}")

    if rename:
        renamed: list[str] = []
        for line in rewritten:
            next_line = line
            for old, new in rename.items():
                next_line = re.sub(
                    rf"(?<![A-Za-z0-9_]){re.escape(old)}(?![A-Za-z0-9_])",
                    new,
                    next_line,
                )
            renamed.append(next_line)
        rewritten = renamed

    final_lines: list[str] = []
    for line in rewritten:
        if _SEQUENCE_ARROW_RE.search(line) and ":" in line:
            prefix, message = line.split(":", 1)
            if ";" in message:
                line = f"{prefix}:{message.replace(';', ',')}"
                changed.append("replaced semicolon in sequence message")
        final_lines.append(line)

    return "\n".join(final_lines), changed


def _polish_mermaid_blocks(text: str) -> tuple[str, list[str]]:
    """Apply deterministic report-format repairs to Mermaid code blocks."""
    changes: list[str] = []

    def replace(match: re.Match[str]) -> str:
        block = match.group(1)
        stripped = block.lstrip()
        indent_len = len(block) - len(stripped)
        prefix = block[:indent_len]
        if not stripped.startswith("sequenceDiagram"):
            return match.group(0)
        fixed, block_changes = _polish_sequence_diagram_block(stripped.rstrip("\n"))
        if block_changes:
            changes.extend(block_changes)
            return f"```mermaid\n{prefix}{fixed}\n```"
        return match.group(0)

    return _MERMAID_BLOCK_RE.sub(replace, text), changes


def _sequence_diagram_issues(block: str, *, start_line: int) -> list[str]:
    issues: list[str] = []
    for offset, line in enumerate(block.splitlines(), start=0):
        line_no = start_line + offset
        match = _SEQUENCE_PARTICIPANT_RE.match(line)
        if match and match.group(2).lower() in _SEQUENCE_RESERVED_IDS:
            issues.append(
                f"line {line_no}: sequence participant id {match.group(2)!r} "
                "collides with Mermaid syntax"
            )
        if _SEQUENCE_ARROW_RE.search(line) and ":" in line:
            _, message = line.split(":", 1)
            if ";" in message:
                issues.append(
                    f"line {line_no}: sequence message contains raw semicolon"
                )
    return issues


def _report_format_issues(text: str) -> list[str]:
    issues: list[str] = []
    if text.count("```") % 2:
        issues.append("unclosed fenced code block")
    if re.search(r"^###\s+VULN-\d{3}:", text, re.MULTILINE) and not _each_vulnerability_has_both_diagrams(text):
        issues.append("one or more VULN sections lack both flowchart and sequenceDiagram blocks")
    for start, end, block in _mermaid_blocks_with_lines(text):
        stripped = block.lstrip()
        first_line = stripped.splitlines()[0].strip() if stripped.splitlines() else ""
        if not first_line:
            issues.append(f"lines {start}-{end}: empty Mermaid block")
        elif first_line.startswith("sequenceDiagram"):
            issues.extend(_sequence_diagram_issues(stripped, start_line=start + 1))
    return issues


def _report_format_diagnostics(path: Path) -> dict[str, Any]:
    text = _read_text_lossy(path)
    _, deterministic_changes = _polish_mermaid_blocks(text)
    return {
        "path": str(path),
        "exists": path.is_file(),
        "issues": _report_format_issues(text),
        "suggested_deterministic_repairs": deterministic_changes,
    }


__all__ = [
    "_each_vulnerability_has_both_diagrams",
    "_mermaid_blocks_with_lines",
    "_polish_mermaid_blocks",
    "_polish_sequence_diagram_block",
    "_report_format_diagnostics",
    "_report_format_issues",
    "_safe_sequence_participant_id",
    "_sequence_diagram_issues",
]

