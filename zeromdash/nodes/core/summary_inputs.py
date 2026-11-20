"""Persist report inputs so summary prompts contain only counts and paths."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_summary_inputs(
    directory: Path, datasets: dict[str, list[Any]]
) -> tuple[Path, str]:
    """Write every dataset, including empty lists, before invoking the agent."""
    directory.mkdir(parents=True, exist_ok=True)
    entries = {}
    catalog = []
    for name, records in datasets.items():
        path = directory / f"{name}.json"
        path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
        entries[name] = {"count": len(records), "path": str(path)}
        catalog.append(f"- {name}: {len(records)} records; JSON: {path}")
    manifest_path = directory / "manifest.json"
    manifest_path.write_text(
        json.dumps({"schema_version": 1, "datasets": entries}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return manifest_path, "\n".join(catalog)
