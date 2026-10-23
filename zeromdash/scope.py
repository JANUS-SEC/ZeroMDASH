"""Scan-scope materialization for full-repository and diff-highlight modes."""

from __future__ import annotations

import hashlib
import json
import re
import shlex
import shutil
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any


_DIFF_HEADER_RE = re.compile(r"^diff --git (.+) (.+)$")
_HUNK_RE = re.compile(
    r"^@@ -(?P<old_start>\d+)(?:,(?P<old_count>\d+))? "
    r"\+(?P<new_start>\d+)(?:,(?P<new_count>\d+))? @@(?P<context>.*)$"
)


def _strip_git_prefix(path: str) -> str:
    path = path.strip()
    if path in {"/dev/null", "dev/null"}:
        return ""
    if path.startswith(("a/", "b/")):
        path = path[2:]
    return path


def _safe_repo_path(path: str) -> str:
    path = _strip_git_prefix(path)
    if not path:
        return ""
    pure = PurePosixPath(path)
    if pure.is_absolute() or ".." in pure.parts:
        raise ValueError(f"diff contains unsafe repository path: {path!r}")
    return pure.as_posix()


def _parse_diff_header(line: str) -> tuple[str, str] | None:
    match = _DIFF_HEADER_RE.match(line)
    if not match:
        return None
    try:
        parts = shlex.split(line[len("diff --git ") :])
    except ValueError as exc:
        raise ValueError(f"invalid diff header: {line!r}: {exc}") from exc
    if len(parts) != 2:
        raise ValueError(f"invalid diff header: {line!r}")
    return _safe_repo_path(parts[0]), _safe_repo_path(parts[1])


def parse_unified_diff(text: str) -> dict[str, Any]:
    """Parse the file/hunk metadata needed for diff-highlighted auditing."""
    files: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    current_hunk: dict[str, Any] | None = None

    for line in text.splitlines():
        header = _parse_diff_header(line)
        if header:
            old_path, new_path = header
            current = {
                "old_path": old_path,
                "new_path": new_path,
                "path": new_path or old_path,
                "status": "modified",
                "hunks": [],
            }
            files.append(current)
            current_hunk = None
            continue
        if current is None:
            continue

        if line.startswith("new file mode "):
            current["status"] = "added"
            continue
        if line.startswith("deleted file mode "):
            current["status"] = "deleted"
            continue
        if line.startswith("rename from "):
            current["old_path"] = _safe_repo_path(line[len("rename from ") :])
            current["status"] = "renamed"
            continue
        if line.startswith("rename to "):
            current["new_path"] = _safe_repo_path(line[len("rename to ") :])
            current["path"] = current["new_path"] or current["old_path"]
            current["status"] = "renamed"
            continue
        if line.startswith("--- "):
            old_path = _safe_repo_path(line[4:].split("\t", 1)[0])
            if old_path:
                current["old_path"] = old_path
            continue
        if line.startswith("+++ "):
            new_path = _safe_repo_path(line[4:].split("\t", 1)[0])
            if new_path:
                current["new_path"] = new_path
                current["path"] = new_path
            elif current.get("old_path"):
                current["status"] = "deleted"
                current["path"] = current["old_path"]
            continue

        hunk_match = _HUNK_RE.match(line)
        if hunk_match:
            current_hunk = {
                "old_start": int(hunk_match.group("old_start")),
                "old_count": int(hunk_match.group("old_count") or "1"),
                "new_start": int(hunk_match.group("new_start")),
                "new_count": int(hunk_match.group("new_count") or "1"),
                "section": hunk_match.group("context").strip(),
                "added_lines": 0,
                "deleted_lines": 0,
            }
            current["hunks"].append(current_hunk)
            continue
        if current_hunk is None:
            continue
        if line.startswith("+") and not line.startswith("+++"):
            current_hunk["added_lines"] += 1
        elif line.startswith("-") and not line.startswith("---"):
            current_hunk["deleted_lines"] += 1

    changed_paths: list[str] = []
    changed_symbols: list[dict[str, str]] = []
    seen_paths: set[str] = set()
    for file_entry in files:
        path = str(file_entry.get("path") or "")
        if path and path not in seen_paths:
            changed_paths.append(path)
            seen_paths.add(path)
        for hunk in file_entry["hunks"]:
            section = str(hunk.get("section") or "").strip()
            if section:
                changed_symbols.append({"path": path, "symbol_hint": section})

    return {
        "files": files,
        "changed_files": changed_paths,
        "changed_symbols": changed_symbols,
        "totals": {
            "files": len(files),
            "hunks": sum(len(item["hunks"]) for item in files),
            "added_lines": sum(
                hunk["added_lines"] for item in files for hunk in item["hunks"]
            ),
            "deleted_lines": sum(
                hunk["deleted_lines"] for item in files for hunk in item["hunks"]
            ),
        },
    }


def _validate_patched_repo(repo_path: Path, parsed: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for item in parsed["files"]:
        if item.get("status") == "deleted":
            continue
        path = str(item.get("new_path") or item.get("path") or "")
        if path and not (repo_path / path).exists():
            missing.append(path)
    return missing


def parse_git_range(value: str) -> tuple[str, str]:
    raw = str(value or "").strip()
    if not raw or raw.count("..") != 1 or "..." in raw:
        raise ValueError("--diff-git must use exactly one two-dot range: <before>..<after>")
    before, after = (part.strip() for part in raw.split("..", 1))
    if not before or not after:
        raise ValueError("--diff-git requires non-empty before and after refs")
    if any(char.isspace() for char in before + after):
        raise ValueError("--diff-git refs must not contain whitespace")
    return before, after


def _run_git(repo_path: Path, args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["git", "-C", str(repo_path), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if check and proc.returncode != 0:
        command = " ".join(["git", "-C", str(repo_path), *args])
        detail = proc.stderr.strip() or proc.stdout.strip() or f"rc={proc.returncode}"
        raise ValueError(f"{command} failed: {detail}")
    return proc


def _resolve_git_ref(repo_path: Path, ref: str) -> str:
    proc = _run_git(repo_path, ["rev-parse", "--verify", f"{ref}^{{commit}}"], check=False)
    if proc.returncode == 0:
        return proc.stdout.strip()
    _run_git(repo_path, ["fetch", "--no-tags", "origin", ref])
    proc = _run_git(repo_path, ["rev-parse", "--verify", f"FETCH_HEAD^{{commit}}"])
    return proc.stdout.strip()


def generate_git_range_diff(repo_path: Path, git_range: str) -> tuple[str, dict[str, str]]:
    """Resolve refs, checkout the after commit, and generate a two-dot git diff."""
    if not (repo_path / ".git").exists():
        raise ValueError("--diff-git requires main/repo to be a git clone with .git metadata")
    before_ref, after_ref = parse_git_range(git_range)
    before_commit = _resolve_git_ref(repo_path, before_ref)
    after_commit = _resolve_git_ref(repo_path, after_ref)
    _run_git(repo_path, ["checkout", "--detach", after_commit])
    diff = _run_git(
        repo_path,
        [
            "diff",
            "--binary",
            "--find-renames",
            "--find-copies",
            "--no-ext-diff",
            before_commit,
            after_commit,
            "--",
        ],
    ).stdout
    return diff, {
        "git_range": git_range,
        "before_ref": before_ref,
        "after_ref": after_ref,
        "before_commit": before_commit,
        "after_commit": after_commit,
    }


def materialize_scan_scope(
    *,
    scope_dir: Path,
    repo_path: Path,
    mode: str,
    diff_file: str = "",
    diff_git: str = "",
) -> dict[str, Any]:
    """Create main/scope artifacts without modifying the patched repository."""
    if scope_dir.exists():
        for child in scope_dir.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    else:
        scope_dir.mkdir(parents=True, exist_ok=True)

    if mode == "full":
        scope = {
            "mode": "full",
            "repo_path": str(repo_path),
            "diff_hash": "",
            "changed_files": [],
            "changed_symbols": [],
            "files": [],
            "totals": {"files": 0, "hunks": 0, "added_lines": 0, "deleted_lines": 0},
            "policy": {
                "finding_must_intersect_diff": False,
                "allow_dependency_context": True,
                "allow_sibling_path_expansion": True,
            },
        }
        (scope_dir / "changes.diff").write_text("")
        (scope_dir / "changed_files.txt").write_text("")
        (scope_dir / "changed_symbols.json").write_text("[]\n")
        (scope_dir / "change_summary.md").write_text(
            "# Scan Scope\n\nMode: full repository.\n\n"
            "The complete patched repository is in scope. No diff attribution is required.\n"
        )
    elif mode == "diff":
        if bool(diff_file) == bool(diff_git):
            raise ValueError("diff mode requires exactly one of diff_file or diff_git")
        git_metadata: dict[str, str] = {}
        source = None
        if diff_git:
            text, git_metadata = generate_git_range_diff(repo_path, diff_git)
        else:
            source = Path(diff_file).expanduser().resolve()
            if not source.is_file():
                raise ValueError(f"diff file does not exist: {source}")
            text = source.read_text(encoding="utf-8", errors="replace")
        parsed = parse_unified_diff(text)
        if not parsed["files"]:
            origin = diff_git or str(source)
            raise ValueError(f"diff source contains no 'diff --git' file entries: {origin}")
        missing = _validate_patched_repo(repo_path, parsed)
        scope = {
            "mode": "diff",
            "repo_path": str(repo_path),
            "source_diff": str(source) if source else "",
            "diff_hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            **git_metadata,
            **parsed,
            "patched_repo_validation": {
                "missing_non_deleted_paths": missing,
                "ok": not missing,
            },
            "policy": {
                "finding_must_intersect_diff": True,
                "allow_dependency_context": True,
                "allow_sibling_path_expansion": True,
            },
        }
        (scope_dir / "changes.diff").write_text(text)
        (scope_dir / "changed_files.txt").write_text(
            "".join(f"{path}\n" for path in parsed["changed_files"])
        )
        (scope_dir / "changed_symbols.json").write_text(
            json.dumps(parsed["changed_symbols"], ensure_ascii=False, indent=2)
        )
        lines = [
            "# Scan Scope",
            "",
            "Mode: diff-highlighted analysis over the complete patched repository.",
            "",
            f"- Diff SHA-256: `{scope['diff_hash']}`",
            f"- Changed files: {parsed['totals']['files']}",
            f"- Changed hunks: {parsed['totals']['hunks']}",
            f"- Added lines: {parsed['totals']['added_lines']}",
            f"- Deleted lines: {parsed['totals']['deleted_lines']}",
            "",
            "## Changed Files",
            "",
        ]
        if git_metadata:
            lines[4:4] = [
                f"- Git range: `{git_metadata['git_range']}`",
                f"- Before commit: `{git_metadata['before_commit']}`",
                f"- After commit: `{git_metadata['after_commit']}`",
            ]
        lines.extend(f"- `{path}`" for path in parsed["changed_files"])
        if missing:
            lines.extend(
                [
                    "",
                    "## Validation Gaps",
                    "",
                    "The following non-deleted diff paths were not found in the patched repository:",
                    "",
                    *(f"- `{path}`" for path in missing),
                ]
            )
        (scope_dir / "change_summary.md").write_text("\n".join(lines) + "\n")
    else:
        raise ValueError(f"unknown scan mode: {mode!r}")

    scope_path = scope_dir / "scope.json"
    scope_path.write_text(json.dumps(scope, ensure_ascii=False, indent=2))
    return scope
