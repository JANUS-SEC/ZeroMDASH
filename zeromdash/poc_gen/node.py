"""Top-level ZeroMDASH node for PoC generation."""

from __future__ import annotations

from typing import Any

from .service import PocGenService


def poc_gen(state: dict[str, Any], *, backends=None) -> dict[str, Any]:
    service = PocGenService(state, backends=backends)
    results = service.run(str(state.get("poc_finding_id") or ""))
    errors = [
        f"[poc_gen/{result['finding_id']}] {error}"
        for result in results
        for error in result.get("errors") or []
    ]
    return {"poc_results": results, "errors": errors}


__all__ = ["poc_gen"]
