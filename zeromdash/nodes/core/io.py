"""Filesystem and structured-output helpers for graph nodes."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

from zeromdash.agents import AgentResult

from .constants import *

def _try_json(text: str, fallback: Any) -> Any:
    """Best-effort JSON extraction (object or array)."""
    if not isinstance(text, str):
        return fallback
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    candidates: list[tuple[int, str, str]] = []
    for opener, closer in (("{", "}"), ("[", "]")):
        try:
            candidates.append((text.index(opener), opener, closer))
        except ValueError:
            continue

    for _, opener, closer in sorted(candidates):
        try:
            i = text.index(opener)
            j = text.rindex(closer) + 1
            return json.loads(text[i:j])
        except (ValueError, json.JSONDecodeError):
            continue
    return fallback

def _read_text_lossy(path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""

def _preview(text: str, limit: int = 300) -> str:
    value = re.sub(r"\s+", " ", (text or "").strip())
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "…"

def _file_has_text(path) -> bool:
    return path.is_file() and bool(_read_text_lossy(path).strip())

def _path_has_materialized_output(path) -> bool:
    if path.name in _IGNORED_OUTPUT_FILENAMES:
        return False
    if path.is_file():
        try:
            return path.stat().st_size > 0
        except OSError:
            return False
    if path.is_dir():
        try:
            return any(_path_has_materialized_output(child) for child in path.iterdir())
        except OSError:
            return False
    return False

def _dir_has_materialized_output(path) -> bool:
    return path.is_dir() and _path_has_materialized_output(path)

def _reset_file_output(path) -> None:
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    path.parent.mkdir(parents=True, exist_ok=True)

def _reset_dir_output(path) -> None:
    if path.exists():
        for child in path.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    else:
        path.mkdir(parents=True, exist_ok=True)

def _write_stdout_fallback_file(path, stdout: str) -> None:
    if not _file_has_text(path) and stdout.strip():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(stdout)

def _planner_fallback_json(res: AgentResult) -> Any:
    """Read a planner JSON artifact that some runtimes write under CWD.

    Stdout remains the protocol. This is only a compatibility path for agents
    that write `plan.json` to their sub_workspace and finish with prose.
    """
    cwd = Path(res.cwd) if res.cwd else None
    if not cwd:
        return None
    path = cwd / "plan.json"
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None

def _run_output_validator(validate, res: AgentResult) -> tuple[bool, str]:
    validation_result = validate(res)
    if isinstance(validation_result, tuple):
        is_valid, detail = validation_result
        return bool(is_valid), str(detail or "")
    return bool(validation_result), ""

__all__ = ["_try_json","_read_text_lossy","_preview","_file_has_text","_path_has_materialized_output","_dir_has_materialized_output","_reset_file_output","_reset_dir_output","_write_stdout_fallback_file","_planner_fallback_json","_run_output_validator"]

