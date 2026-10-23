"""Deterministic report grouping for standalone and chain findings."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from zeromdash.state import ChainFinding, Finding, ReportGroup

from .qualification import (
    _compact_summary_finding,
    _finding_qualification_passed,
    _known_cve_patch_gap_ids,
    _summary_list,
)


def _string(value: Any) -> str:
    return str(value or "").strip()


def _dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return []


def _evidence_locations(finding: dict[str, Any]) -> list[str]:
    evidence = _dict(finding.get("evidence"))
    return sorted(_string(item) for item in _summary_list(evidence.get("code_locations")) if _string(item))


def _group_key(finding: dict[str, Any]) -> str:
    review = _dict(finding.get("review"))
    payload = {
        "root": _string(review.get("violated_security_property") or finding.get("violated_security_property") or finding.get("title")),
        "sink": _summary_list(_dict(finding.get("evidence")).get("call_path"))[-1:] or _summary_list(_dict(finding.get("evidence")).get("call_paths"))[-1:],
        "locations": _evidence_locations(finding)[:3],
    }
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _score(finding: dict[str, Any]) -> float:
    try:
        return float(finding.get("cvss4_score") or _dict(finding.get("review")).get("cvss4_score") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _confidence(finding: dict[str, Any]) -> float:
    try:
        return float(finding.get("confidence") or _dict(finding.get("review")).get("confidence") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _source_subtasks(finding: dict[str, Any]) -> list[str]:
    values = _summary_list(finding.get("subtask_id")) + _summary_list(finding.get("source_subtask_ids"))
    return sorted({_string(item) for item in values if _string(item)})


def _source_primitives(finding: dict[str, Any]) -> list[str]:
    return sorted({_string(item) for item in _summary_list(finding.get("source_primitive_ids")) if _string(item)})


def _group_sort_key(group: dict[str, Any]) -> tuple[float, float, str]:
    findings = _list(group.get("findings"))
    return (
        -max((_score(finding) for finding in findings if isinstance(finding, dict)), default=_score(group)),
        -max((_confidence(finding) for finding in findings if isinstance(finding, dict)), default=_confidence(group)),
        _string(group.get("group_key")),
    )


def _report_group_from_findings(index: int, key: str, findings: list[dict[str, Any]]) -> ReportGroup:
    ordered = sorted(findings, key=lambda item: (-_score(item), -_confidence(item), _string(item.get("subtask_id"))))
    primary = ordered[0]
    group_id = f"VULN-{index:03d}"
    source_chains = sorted({_string(item.get("chain_id")) for item in ordered if _string(item.get("chain_id"))})
    source_subtasks = sorted({subtask for item in ordered for subtask in _source_subtasks(item)})
    source_primitives = sorted({primitive for item in ordered for primitive in _source_primitives(item)})
    absorbed = sorted(
        {
            _string(item.get("subtask_id") or item.get("id"))
            for item in ordered[1:]
            if _string(item.get("subtask_id") or item.get("id"))
        }
    )
    return {
        "schema_version": "2.0",
        "group_id": group_id,
        "group_key": key,
        "title": _string(primary.get("title")),
        "status": "confirm",
        "summary_format": "full",
        "primary_finding": primary,
        "findings": ordered,
        "source_subtasks": source_subtasks,
        "source_chains": source_chains,
        "source_primitive_ids": source_primitives,
        "absorbed_finding_ids": absorbed,
        "cvss4_vector": _string(primary.get("cvss4_vector") or _dict(primary.get("review")).get("cvss4_vector")),
        "cvss4_score": _score(primary),
        "severity": _string(primary.get("severity") or _dict(primary.get("review")).get("severity")),
        "confidence": _confidence(primary),
    }


def _renumber_full_groups(groups: list[ReportGroup]) -> list[ReportGroup]:
    result: list[ReportGroup] = []
    for index, group in enumerate(sorted(groups, key=_group_sort_key), start=1):
        result.append({**group, "group_id": f"VULN-{index:03d}"})
    return result


def build_report_groups(
    *,
    standalone_findings: list[Finding],
    chain_findings: list[ChainFinding],
) -> list[ReportGroup]:
    groups: dict[str, list[dict[str, Any]]] = {}
    patch_groups: list[ReportGroup] = []
    for finding in [*standalone_findings, *chain_findings]:
        if not isinstance(finding, dict):
            continue
        compact = _compact_summary_finding(finding, "patch" if finding.get("kind") == "patch_miss" else str(finding.get("kind") or "vuln"))
        if compact and compact.get("summary_format") == "patch_gap":
            patch_groups.append(
                {
                    "schema_version": "2.0",
                    "group_id": "",
                    "group_key": "patch_gap:" + ",".join(_known_cve_patch_gap_ids(finding, "patch")),
                    "title": _string(finding.get("title")),
                    "status": "confirm",
                    "summary_format": "patch_gap",
                    "primary_finding": finding,
                    "findings": [finding],
                    "source_subtasks": _source_subtasks(finding),
                    "cvss4_score": 0.0,
                    "severity": "none",
                    "confidence": _confidence(finding),
                }
            )
            continue
        if not _finding_qualification_passed(finding):
            continue
        key = _group_key(finding)
        groups.setdefault(key, []).append(finding)

    ordered_groups = sorted(
        groups.items(),
        key=lambda item: (
            -max(_score(finding) for finding in item[1]),
            -max(_confidence(finding) for finding in item[1]),
            item[0],
        ),
    )
    result = [
        _report_group_from_findings(index, key, findings)
        for index, (key, findings) in enumerate(ordered_groups, start=1)
    ]
    for patch_index, group in enumerate(patch_groups, start=1):
        group["group_id"] = f"PATCH-GAP-{patch_index:03d}"
    return result + patch_groups


def apply_report_group_adjudication(
    groups: list[ReportGroup],
    adjudication: dict[str, Any],
) -> tuple[list[ReportGroup], list[str]]:
    """Apply agent-proposed semantic merges to deterministic report groups.

    The agent is allowed to choose equivalence classes only.  It cannot create
    new findings, change severity/CVSS, or rewrite primary evidence; those
    remain derived from the original group members.
    """
    full_groups = [
        group
        for group in groups
        if isinstance(group, dict) and group.get("summary_format") != "patch_gap"
    ]
    patch_groups = [
        group
        for group in groups
        if isinstance(group, dict) and group.get("summary_format") == "patch_gap"
    ]
    by_id = {
        _string(group.get("group_id")): group
        for group in full_groups
        if _string(group.get("group_id"))
    }
    failures: list[str] = []
    merge_items = adjudication.get("merge_groups")
    if not isinstance(merge_items, list):
        return groups, ["merge_groups must be an array"]

    used: set[str] = set()
    merged_groups: list[ReportGroup] = []
    for index, item in enumerate(merge_items):
        if not isinstance(item, dict):
            failures.append(f"merge_groups[{index}] must be an object")
            continue
        source_ids = [
            _string(group_id)
            for group_id in _list(item.get("source_group_ids"))
            if _string(group_id)
        ]
        if len(source_ids) < 2:
            failures.append(f"merge_groups[{index}].source_group_ids must contain at least two ids")
            continue
        duplicate_ids = sorted({group_id for group_id in source_ids if source_ids.count(group_id) > 1})
        if duplicate_ids:
            failures.append(
                f"merge_groups[{index}] duplicates source group id(s): "
                + ", ".join(duplicate_ids)
            )
            continue
        unknown = [group_id for group_id in source_ids if group_id not in by_id]
        if unknown:
            failures.append(
                f"merge_groups[{index}] references unknown group id(s): "
                + ", ".join(unknown)
            )
            continue
        reused = [group_id for group_id in source_ids if group_id in used]
        if reused:
            failures.append(
                f"merge_groups[{index}] reuses group id(s): "
                + ", ".join(reused)
            )
            continue
        if not _string(item.get("reasoning")):
            failures.append(f"merge_groups[{index}].reasoning is empty")
            continue
        used.update(source_ids)
        findings = [
            finding
            for group_id in source_ids
            for finding in _list(by_id[group_id].get("findings"))
            if isinstance(finding, dict)
        ]
        if not findings:
            failures.append(f"merge_groups[{index}] has no findings to merge")
            continue
        key_payload = {
            "semantic_merge": source_ids,
            "reasoning": _string(item.get("reasoning")),
            "root_cause": _string(item.get("root_cause")),
            "shared_sink": _string(item.get("shared_sink")),
        }
        key = "semantic:" + hashlib.sha256(
            json.dumps(key_payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()[:16]
        merged = _report_group_from_findings(0, key, findings)
        merged["dedup_adjudication"] = {
            "source_group_ids": source_ids,
            "reasoning": _string(item.get("reasoning")),
            "root_cause": _string(item.get("root_cause")),
            "shared_sink": _string(item.get("shared_sink")),
            "trigger_equivalence": _string(item.get("trigger_equivalence")),
            "variant_notes": [
                _string(note)
                for note in _list(item.get("variant_notes"))
                if _string(note)
            ],
        }
        merged_groups.append(merged)

    if failures:
        return groups, failures

    retained = [group for group in full_groups if _string(group.get("group_id")) not in used]
    full_result = _renumber_full_groups([*retained, *merged_groups])
    for patch_index, group in enumerate(patch_groups, start=1):
        group["group_id"] = f"PATCH-GAP-{patch_index:03d}"
    return full_result + patch_groups, []


def compact_report_group(group: ReportGroup) -> dict[str, Any]:
    primary = _dict(group.get("primary_finding"))
    return {
        "group_id": group.get("group_id", ""),
        "summary_format": group.get("summary_format", "full"),
        "title": group.get("title", ""),
        "severity": group.get("severity", ""),
        "cvss4_score": group.get("cvss4_score"),
        "cvss4_vector": group.get("cvss4_vector", ""),
        "confidence": group.get("confidence", 0.0),
        "source_subtasks": group.get("source_subtasks", []),
        "source_chains": group.get("source_chains", []),
        "source_primitive_ids": group.get("source_primitive_ids", []),
        "absorbed_finding_ids": group.get("absorbed_finding_ids", []),
        "primary_kind": primary.get("kind", ""),
        "primary_id": primary.get("chain_id") or primary.get("subtask_id") or "",
    }


__all__ = ["build_report_groups", "apply_report_group_adjudication", "compact_report_group"]
