"""Shared parsing and validation for search nodes."""

from __future__ import annotations

import re
from typing import Any

from .qualification import _try_json

def _candidate_names_from_payload(parsed: Any) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
    if not isinstance(parsed, list):
        return names
    for it in parsed:
        raw_name = ""
        if isinstance(it, dict) and it.get("name"):
            raw_name = str(it["name"])
        elif isinstance(it, str) and it.strip():
            raw_name = it.strip()
        name = _safe_similar_software_name(raw_name)
        if name and name not in seen:
            names.append(name)
            seen.add(name)
    return names

def _parse_candidate_names(text: str) -> tuple[bool, list[str], Any]:
    parsed = _try_json(text, fallback=None)
    if not isinstance(parsed, list):
        return False, [], parsed
    return True, _candidate_names_from_payload(parsed), parsed

def _safe_similar_software_name(value: Any) -> str:
    """Normalize candidate display names before storing them in graph state.

    Candidate names are later used as Send subtask ids and workspace path
    components. Keep human-readable product names, but reject obvious fallback
    paths/URLs and replace path separators that appear inside legitimate names
    such as "MongoDB server / mongod".
    """
    name = str(value or "").strip()
    if not name:
        return ""
    lowered = name.lower()
    if (
        "://" in name
        or lowered.endswith(".json")
        or name.startswith(("/", "\\", "~/", "./", "../"))
        or re.match(r"^[A-Za-z]:[\\/]", name)
    ):
        return ""
    name = re.sub(r"[\\/]+", " - ", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip(" -")

__all__ = ["_candidate_names_from_payload","_parse_candidate_names","_safe_similar_software_name"]

