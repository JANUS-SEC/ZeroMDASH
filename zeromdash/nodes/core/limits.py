"""Shared parsing for per-bucket planner and dispatch limits."""

from __future__ import annotations

from typing import Any

from zeromdash.state import ZeroMDASHState


def _configured_bucket_limit(value: Any, bucket: str) -> int | None:
    if not isinstance(value, dict):
        return None
    raw = value.get(bucket)
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int) and raw > 0:
        return raw
    return None


def _top_k_limit(state: ZeroMDASHState, bucket: str) -> int | None:
    return _configured_bucket_limit(state.get("top_K"), bucket)


__all__ = ["_configured_bucket_limit", "_top_k_limit"]
