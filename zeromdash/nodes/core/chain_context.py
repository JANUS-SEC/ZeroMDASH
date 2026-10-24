"""File references for shared chain-analysis inputs."""

from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from zeromdash.state import ZeroMDASHState

from .context import _ws
from .domain_registry import domain_registry_from_state


def _write_snapshot(path: Path, payload: Any) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    # Chain subtasks run concurrently. Each writer needs its own temporary file.
    with NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as fp:
        temporary_path = Path(fp.name)
        fp.write(text)
    try:
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def chain_prompt_context(state: ZeroMDASHState) -> dict[str, Any]:
    """Keep complete state inputs on disk, including on resumed node runs."""
    ws = _ws(state)
    primitives = [
        primitive for primitive in state.get("chain_pool") or []
        if isinstance(primitive, dict)
    ]
    pool_path = ws.state_path("chain_pool.json")
    registry_path = ws.state_path("chain_domain_registry.json")
    _write_snapshot(
        pool_path,
        {
            "schema_version": "2.0",
            "primitive_count": len(primitives),
            "primitives": primitives,
        },
    )
    _write_snapshot(registry_path, domain_registry_from_state(state))
    return {
        "chain_pool_path": str(pool_path),
        "primitive_count": len(primitives),
        "domain_registry_path": str(registry_path),
    }


__all__ = ["chain_prompt_context"]
