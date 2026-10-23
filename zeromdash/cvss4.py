"""Deterministic CVSS v4.0 Base-vector validation and scoring.

Agents provide metric judgments and evidence.  This module owns parsing,
canonicalization, scoring, and severity so an agent cannot invent a numeric
score that disagrees with its vector.
"""

from __future__ import annotations

from dataclasses import dataclass

from cvss import CVSS4
from cvss.exceptions import CVSS4Error


BASE_METRICS = (
    "AV",
    "AC",
    "AT",
    "PR",
    "UI",
    "VC",
    "VI",
    "VA",
    "SC",
    "SI",
    "SA",
)
IMPACT_METRICS = ("VC", "VI", "VA", "SC", "SI", "SA")
_BASE_METRIC_SET = frozenset(BASE_METRICS)


class CVSS4ValidationError(ValueError):
    """Raised when a vector is not a complete CVSS v4.0 Base vector."""


@dataclass(frozen=True)
class CVSS4Score:
    vector: str
    score: float
    severity: str
    metrics: dict[str, str]


def _provided_metrics(vector: str) -> list[str]:
    fields = vector.split("/")[1:]
    metrics: list[str] = []
    for field in fields:
        if ":" not in field:
            raise CVSS4ValidationError(f"malformed CVSS v4.0 field: {field!r}")
        metric, _ = field.split(":", 1)
        metrics.append(metric)
    return metrics


def score_base_vector(vector: str) -> CVSS4Score:
    """Validate and score one complete Base-only CVSS v4.0 vector.

    Threat, Environmental, and Supplemental metrics are rejected here.  A
    vulnerability finding should carry an intrinsic Base score; deployment-
    specific enrichment can be added by a downstream risk process.
    """

    normalized = str(vector or "").strip()
    if not normalized.startswith("CVSS:4.0/"):
        raise CVSS4ValidationError("vector must start with 'CVSS:4.0/'")

    provided = _provided_metrics(normalized)
    duplicates = sorted({metric for metric in provided if provided.count(metric) > 1})
    if duplicates:
        raise CVSS4ValidationError(
            "duplicate CVSS v4.0 metrics: " + ", ".join(duplicates)
        )
    provided_set = set(provided)
    missing = [metric for metric in BASE_METRICS if metric not in provided_set]
    extra = sorted(provided_set - _BASE_METRIC_SET)
    if missing or extra:
        parts = []
        if missing:
            parts.append("missing Base metrics: " + ", ".join(missing))
        if extra:
            parts.append("non-Base metrics are not allowed: " + ", ".join(extra))
        raise CVSS4ValidationError("; ".join(parts))

    try:
        parsed = CVSS4(normalized)
    except CVSS4Error as exc:
        raise CVSS4ValidationError(str(exc)) from exc

    metrics = {metric: parsed.metrics[metric] for metric in BASE_METRICS}
    score = float(parsed.scores()[0])
    severity = str(parsed.severities()[0]).strip().lower()
    return CVSS4Score(
        vector=parsed.clean_vector(),
        score=score,
        severity=severity,
        metrics=metrics,
    )


def has_direct_impact(score: CVSS4Score) -> bool:
    """Return whether the vector claims any direct system impact."""

    return any(score.metrics[metric] != "N" for metric in IMPACT_METRICS)
