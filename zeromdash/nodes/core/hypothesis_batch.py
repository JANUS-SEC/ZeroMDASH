"""Structural contracts for agent-owned hypothesis work packages.

This module deliberately does not discover, merge, rank, or adjudicate
hypotheses. Those are agent responsibilities. The helpers only check stable
identities, monotonic ledgers, complete cross-references, and closure
consistency so a broad work package cannot silently collapse to one outcome.
"""

from __future__ import annotations

from typing import Any

from zeromdash.state import Subtask


HYPOTHESIS_BATCH_SCHEMA_VERSION = "1.0"
_TERMINAL_VERDICTS = {"confirm", "reject"}
_DOMAIN_REF_KEYS = {
    "entity_ids",
    "representation_ids",
    "invariant_ids",
    "transition_ids",
    "seam_ids",
}


def _nonempty(value: Any) -> str:
    return str(value or "").strip()


def _object_list(value: Any) -> list[dict[str, Any]] | None:
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        return None
    return [dict(item) for item in value]


def _ids(items: list[dict[str, Any]], key: str) -> tuple[list[str], str]:
    values = [_nonempty(item.get(key)) for item in items]
    if any(not value for value in values):
        return [], f"every item requires non-empty {key}"
    if len(values) != len(set(values)):
        return [], f"duplicate {key}"
    return values, ""


def _current_discoveries(value: dict[str, Any]) -> tuple[list[dict[str, Any]] | None, str]:
    """Read this iteration's discoveries, accepting the pre-rename field."""
    canonical_present = "newly_discovered_hypotheses" in value
    legacy_present = "discovered_hypotheses" in value
    if canonical_present and legacy_present:
        return None, (
            "use only newly_discovered_hypotheses; discovered_hypotheses is a "
            "deprecated alias"
        )
    raw = (
        value.get("newly_discovered_hypotheses")
        if canonical_present
        else value.get("discovered_hypotheses")
    )
    discoveries = _object_list(raw)
    if discoveries is None:
        return None, "newly_discovered_hypotheses must be an array"
    return discoveries, ""


def _current_discovery_decisions(
    value: dict[str, Any],
) -> tuple[list[dict[str, Any]] | None, str]:
    """Read decisions for this iteration's discoveries only."""
    canonical_present = "new_hypothesis_decisions" in value
    legacy_present = "discovery_decisions" in value
    if canonical_present and legacy_present:
        return None, (
            "use only new_hypothesis_decisions; discovery_decisions is a "
            "deprecated alias"
        )
    raw = (
        value.get("new_hypothesis_decisions")
        if canonical_present
        else value.get("discovery_decisions")
    )
    decisions = _object_list(raw)
    if decisions is None:
        return None, "new_hypothesis_decisions must be an array"
    return decisions, ""


def _validate_counterexample_attempts(
    attempts_value: Any,
    unresolved_value: Any,
    *,
    prefix: str,
    closure_claimed: bool,
) -> str:
    """Validate an agent-authored adversarial coverage record structurally."""
    attempts = _object_list(attempts_value)
    if attempts is None:
        return f"{prefix}.counterexample_attempts must be an array"
    if (
        not isinstance(unresolved_value, list)
        or any(not isinstance(item, str) or not item.strip() for item in unresolved_value)
    ):
        return f"{prefix}.unresolved_cases must be an array of non-empty strings"
    for index, attempt in enumerate(attempts):
        item_prefix = f"{prefix}.counterexample_attempts[{index}]"
        if not _nonempty(attempt.get("dimension")):
            return f"{item_prefix}.dimension is empty"
        cases = attempt.get("cases")
        if (
            not isinstance(cases, list)
            or len(cases) < 2
            or any(not isinstance(item, str) or not item.strip() for item in cases)
        ):
            return f"{item_prefix}.cases must contain at least two non-empty cases"
        if not _nonempty(attempt.get("result")):
            return f"{item_prefix}.result is empty"
        evidence = attempt.get("evidence")
        if (
            not isinstance(evidence, list)
            or not evidence
            or any(not isinstance(item, str) or not item.strip() for item in evidence)
        ):
            return f"{item_prefix}.evidence must contain non-empty source references"
    if closure_claimed and not attempts:
        return f"{prefix} cannot claim closure without a counterexample attempt"
    if closure_claimed and unresolved_value:
        return f"{prefix} cannot claim closure while unresolved_cases is non-empty"
    return ""


def _validate_domain_refs_shape(value: Any, prefix: str) -> str:
    if value is None:
        return ""
    if not isinstance(value, dict):
        return f"{prefix}.domain_refs must be an object"
    unknown = set(value) - _DOMAIN_REF_KEYS
    if unknown:
        return f"{prefix}.domain_refs has unknown collection(s): " + ", ".join(sorted(unknown))
    invalid = [
        key
        for key, values in value.items()
        if not isinstance(values, list)
        or any(not isinstance(item, str) or not item.strip() for item in values)
    ]
    if invalid:
        return (
            f"{prefix}.domain_refs collection(s) must be arrays of non-empty strings: "
            + ", ".join(sorted(invalid))
        )
    return ""


def is_hypothesis_package(subtask: Any) -> bool:
    return isinstance(subtask, dict) and (
        "coverage_obligations" in subtask or "seed_hypotheses" in subtask
    )


def validate_hypothesis_definition(
    value: Any,
    *,
    obligation_ids: set[str],
    prefix: str = "hypothesis",
) -> tuple[dict[str, Any] | None, str]:
    if not isinstance(value, dict):
        return None, f"{prefix} must be an object"
    hypothesis_id = _nonempty(value.get("hypothesis_id"))
    statement = _nonempty(value.get("statement"))
    covered = value.get("obligation_ids")
    if not hypothesis_id:
        return None, f"{prefix}.hypothesis_id is empty"
    if not statement:
        return None, f"{prefix}.statement is empty"
    if (
        not isinstance(covered, list)
        or not covered
        or any(not isinstance(item, str) or not item.strip() for item in covered)
    ):
        return None, f"{prefix}.obligation_ids must contain non-empty strings"
    unknown = set(covered) - obligation_ids
    if unknown:
        return None, f"{prefix} references unknown obligation id(s): " + ", ".join(sorted(unknown))
    domain_error = _validate_domain_refs_shape(value.get("domain_refs"), prefix)
    if domain_error:
        return None, domain_error
    return dict(value), ""


def validate_hypothesis_package(subtask: Any) -> tuple[dict[str, Any] | None, str]:
    """Validate a planner-produced work package without judging semantics."""
    if not isinstance(subtask, dict):
        return None, "subtask must be an object"
    package_id = _nonempty(subtask.get("id"))
    if not package_id:
        return None, "subtask.id is empty"
    obligations = _object_list(subtask.get("coverage_obligations"))
    if not obligations:
        return None, f"subtask {package_id} coverage_obligations must be a non-empty array"
    obligation_values, error = _ids(obligations, "obligation_id")
    if error:
        return None, f"subtask {package_id} coverage_obligations: {error}"
    for index, obligation in enumerate(obligations):
        if not _nonempty(obligation.get("statement")):
            return None, f"subtask {package_id} coverage_obligations[{index}].statement is empty"
        domain_error = _validate_domain_refs_shape(
            obligation.get("domain_refs"),
            f"subtask {package_id} coverage_obligations[{index}]",
        )
        if domain_error:
            return None, domain_error

    seeds = _object_list(subtask.get("seed_hypotheses"))
    if not seeds:
        return None, f"subtask {package_id} seed_hypotheses must be a non-empty array"
    hypothesis_values, error = _ids(seeds, "hypothesis_id")
    if error:
        return None, f"subtask {package_id} seed_hypotheses: {error}"
    obligation_set = set(obligation_values)
    for index, seed in enumerate(seeds):
        _, error = validate_hypothesis_definition(
            seed,
            obligation_ids=obligation_set,
            prefix=f"subtask {package_id} seed_hypotheses[{index}]",
        )
        if error:
            return None, error

    referenced = {
        obligation_id
        for seed in seeds
        for obligation_id in seed.get("obligation_ids", [])
    }
    missing = obligation_set - referenced
    if missing:
        return None, (
            f"subtask {package_id} seed_hypotheses do not map obligation(s): "
            + ", ".join(sorted(missing))
        )
    normalized = dict(subtask)
    normalized["coverage_obligations"] = obligations
    normalized["seed_hypotheses"] = seeds
    return normalized, ""


def initial_hypothesis_manifest(subtask: Subtask) -> dict[str, Any]:
    parsed, error = validate_hypothesis_package(subtask)
    if parsed is None:
        raise ValueError(error)
    return {
        "schema_version": HYPOTHESIS_BATCH_SCHEMA_VERSION,
        "package_id": str(parsed["id"]),
        "revision": 0,
        "coverage_obligations": list(parsed["coverage_obligations"]),
        "hypotheses": list(parsed["seed_hypotheses"]),
    }


def _manifest_parts(
    subtask: Subtask,
    prior_manifest: Any,
) -> tuple[dict[str, Any] | None, set[str], dict[str, dict[str, Any]], str]:
    try:
        initial = initial_hypothesis_manifest(subtask)
    except ValueError as exc:
        return None, set(), {}, str(exc)
    manifest = dict(prior_manifest) if isinstance(prior_manifest, dict) else initial
    if _nonempty(manifest.get("package_id")) != _nonempty(subtask.get("id")):
        return None, set(), {}, "hypothesis manifest package_id does not match subtask.id"
    hypotheses = _object_list(manifest.get("hypotheses"))
    if hypotheses is None:
        return None, set(), {}, "hypothesis manifest hypotheses must be an array"
    ids, error = _ids(hypotheses, "hypothesis_id")
    if error:
        return None, set(), {}, f"hypothesis manifest: {error}"
    obligation_ids = {
        _nonempty(item.get("obligation_id"))
        for item in initial["coverage_obligations"]
    }
    definitions: dict[str, dict[str, Any]] = {}
    for index, hypothesis in enumerate(hypotheses):
        parsed, error = validate_hypothesis_definition(
            hypothesis,
            obligation_ids=obligation_ids,
            prefix=f"hypothesis manifest hypotheses[{index}]",
        )
        if parsed is None:
            return None, set(), {}, error
        definitions[ids[index]] = parsed
    seed_ids = {
        _nonempty(item.get("hypothesis_id"))
        for item in initial["hypotheses"]
    }
    if not seed_ids.issubset(definitions):
        return None, set(), {}, "hypothesis manifest dropped planner seed hypothesis id(s)"
    return manifest, obligation_ids, definitions, ""


def is_hypothesis_batch(value: Any) -> bool:
    return isinstance(value, dict) and (
        "hypothesis_results" in value or "package_id" in value
    )


def validate_hypothesis_investigation(
    value: Any,
    *,
    subtask: Subtask,
    prior_manifest: Any = None,
) -> tuple[dict[str, Any] | None, str]:
    """Validate one complete agent-produced hypothesis ledger revision."""
    if not isinstance(value, dict):
        return None, "hypothesis investigation is not a JSON object"
    manifest, obligation_ids, known, error = _manifest_parts(subtask, prior_manifest)
    if manifest is None:
        return None, error
    if _nonempty(value.get("package_id")) != _nonempty(subtask.get("id")):
        return None, "investigation package_id does not match subtask.id"
    revision = value.get("manifest_revision")
    previous_revision = manifest.get("revision", 0)
    if (
        not isinstance(revision, int)
        or isinstance(revision, bool)
        or revision != int(previous_revision or 0) + 1
    ):
        return None, "manifest_revision must equal the prior revision plus one"

    results = _object_list(value.get("hypothesis_results"))
    if not results:
        return None, "hypothesis_results must be a non-empty array"
    result_ids, error = _ids(results, "hypothesis_id")
    if error:
        return None, f"hypothesis_results: {error}"
    result_id_set = set(result_ids)
    known_ids = set(known)
    if not known_ids.issubset(result_id_set):
        return None, (
            "hypothesis_results dropped known hypothesis id(s): "
            + ", ".join(sorted(known_ids - result_id_set))
        )

    discovered, error = _current_discoveries(value)
    if discovered is None:
        return None, error
    discovered_ids, error = _ids(discovered, "hypothesis_id") if discovered else ([], "")
    if error:
        return None, f"newly_discovered_hypotheses: {error}"
    discovered_id_set = set(discovered_ids)
    if discovered_id_set & known_ids:
        return None, (
            "newly_discovered_hypotheses re-declare manifest hypothesis id(s): "
            + ", ".join(sorted(discovered_id_set & known_ids))
        )
    extras = result_id_set - known_ids
    if extras != discovered_id_set:
        return None, (
            "result IDs outside the manifest must exactly match "
            "newly_discovered_hypotheses IDs"
        )
    for index, hypothesis in enumerate(discovered):
        _, error = validate_hypothesis_definition(
            hypothesis,
            obligation_ids=obligation_ids,
            prefix=f"newly_discovered_hypotheses[{index}]",
        )
        if error:
            return None, error

    for index, result in enumerate(results):
        for field in ("title", "detail"):
            if not _nonempty(result.get(field)):
                return None, f"hypothesis_results[{index}].{field} is empty"
        evidence = result.get("evidence")
        if not isinstance(evidence, dict):
            return None, f"hypothesis_results[{index}].evidence must be an object"
        for field in ("code_locations", "call_path"):
            values = evidence.get(field)
            if (
                not isinstance(values, list)
                or not values
                or any(not isinstance(item, str) or not item.strip() for item in values)
            ):
                return None, (
                    f"hypothesis_results[{index}].evidence.{field} "
                    "must contain non-empty strings"
                )

    matrix = _object_list(value.get("coverage_matrix"))
    if matrix is None:
        return None, "coverage_matrix must be an array"
    matrix_ids, error = _ids(matrix, "obligation_id") if matrix else ([], "")
    if error:
        return None, f"coverage_matrix: {error}"
    if set(matrix_ids) != obligation_ids:
        return None, "coverage_matrix must contain exactly one row per coverage obligation"
    for index, row in enumerate(matrix):
        mapped = row.get("hypothesis_ids")
        if (
            not isinstance(mapped, list)
            or not mapped
            or any(not isinstance(item, str) or not item.strip() for item in mapped)
        ):
            return None, f"coverage_matrix[{index}].hypothesis_ids must contain non-empty strings"
        unknown = set(mapped) - result_id_set
        if unknown:
            return None, (
                f"coverage_matrix[{index}] references unknown hypothesis id(s): "
                + ", ".join(sorted(unknown))
            )
        if not _nonempty(row.get("assessment")):
            return None, f"coverage_matrix[{index}].assessment is empty"
    if not isinstance(value.get("proposed_coverage_closed"), bool):
        return None, "proposed_coverage_closed must be a JSON boolean"
    counterexample_error = _validate_counterexample_attempts(
        value.get("counterexample_attempts"),
        value.get("unresolved_cases"),
        prefix="investigation",
        closure_claimed=value["proposed_coverage_closed"],
    )
    if counterexample_error:
        return None, counterexample_error
    normalized = dict(value)
    normalized["newly_discovered_hypotheses"] = discovered
    normalized.pop("discovered_hypotheses", None)
    return normalized, ""


def validate_hypothesis_review(
    value: Any,
    *,
    subtask: Subtask,
    investigation: dict[str, Any],
) -> tuple[dict[str, Any] | None, str]:
    """Check critic accounting and package-closure consistency."""
    if not isinstance(value, dict):
        return None, "hypothesis review is not a JSON object"
    if _nonempty(value.get("package_id")) != _nonempty(subtask.get("id")):
        return None, "review package_id does not match subtask.id"
    package_decision = _nonempty(value.get("package_decision")).lower()
    if package_decision not in {"close", "revise"}:
        return None, "package_decision must be close or revise"
    if not _nonempty(value.get("reasoning")):
        return None, "review reasoning is empty"

    results = investigation.get("hypothesis_results") or []
    result_ids = {
        _nonempty(item.get("hypothesis_id"))
        for item in results
        if isinstance(item, dict)
    }
    verdicts = _object_list(value.get("hypothesis_verdicts"))
    if verdicts is None:
        return None, "hypothesis_verdicts must be an array"
    verdict_ids, error = _ids(verdicts, "hypothesis_id") if verdicts else ([], "")
    if error:
        return None, f"hypothesis_verdicts: {error}"
    if set(verdict_ids) != result_ids:
        return None, "hypothesis_verdicts must contain exactly one verdict per hypothesis_result"
    for index, verdict in enumerate(verdicts):
        if _nonempty(verdict.get("verdict")).lower() not in {"confirm", "reject", "revise"}:
            return None, f"hypothesis_verdicts[{index}].verdict is invalid"
        if not _nonempty(verdict.get("reasoning")):
            return None, f"hypothesis_verdicts[{index}].reasoning is empty"

    current_discoveries, discovery_error = _current_discoveries(investigation)
    if current_discoveries is None:
        return None, discovery_error
    discovered_ids = {
        _nonempty(item.get("hypothesis_id"))
        for item in current_discoveries
        if isinstance(item, dict)
    }
    decisions, error = _current_discovery_decisions(value)
    if decisions is None:
        return None, error
    decision_ids, error = _ids(decisions, "hypothesis_id") if decisions else ([], "")
    if error:
        return None, f"new_hypothesis_decisions: {error}"
    if set(decision_ids) != discovered_ids:
        missing = sorted(discovered_ids - set(decision_ids))
        extra = sorted(set(decision_ids) - discovered_ids)
        details = []
        if missing:
            details.append("missing current discoveries: " + ", ".join(missing))
        if extra:
            details.append("not newly discovered this iteration: " + ", ".join(extra))
        return None, (
            "new_hypothesis_decisions must account for exactly this iteration's "
            "newly_discovered_hypotheses"
            + (" (" + "; ".join(details) + ")" if details else "")
        )
    for index, decision in enumerate(decisions):
        action = _nonempty(decision.get("decision")).lower()
        if action not in {"accept", "merge", "reject"}:
            return None, f"new_hypothesis_decisions[{index}].decision is invalid"
        if not _nonempty(decision.get("reasoning")):
            return None, f"new_hypothesis_decisions[{index}].reasoning is empty"
        if action == "merge":
            target_id = _nonempty(decision.get("merge_target_id"))
            if target_id not in result_ids:
                return None, f"new_hypothesis_decisions[{index}].merge_target_id is unknown"
            if target_id == _nonempty(decision.get("hypothesis_id")):
                return None, f"new_hypothesis_decisions[{index}] cannot merge a hypothesis into itself"
    decision_by_id = {
        _nonempty(item.get("hypothesis_id")): _nonempty(item.get("decision")).lower()
        for item in decisions
    }
    retained_ids = (result_ids - discovered_ids) | {
        hypothesis_id
        for hypothesis_id, decision in decision_by_id.items()
        if decision == "accept"
    }

    package, error = validate_hypothesis_package(subtask)
    if package is None:
        return None, error
    obligation_ids = {
        _nonempty(item.get("obligation_id"))
        for item in package["coverage_obligations"]
    }
    coverage = value.get("coverage_verdict")
    if not isinstance(coverage, dict):
        return None, "coverage_verdict must be an object"
    coverage_status = _nonempty(coverage.get("status")).lower()
    if coverage_status not in {"closed", "open"}:
        return None, "coverage_verdict.status must be closed or open"
    if not _nonempty(coverage.get("reasoning")):
        return None, "coverage_verdict.reasoning is empty"
    counterexample_error = _validate_counterexample_attempts(
        coverage.get("counterexample_attempts"),
        coverage.get("unresolved_cases"),
        prefix="coverage_verdict",
        closure_claimed=(package_decision == "close" or coverage_status == "closed"),
    )
    if counterexample_error:
        return None, counterexample_error
    assessments = _object_list(coverage.get("obligation_assessments"))
    if assessments is None:
        return None, "coverage_verdict.obligation_assessments must be an array"
    assessment_ids, error = _ids(assessments, "obligation_id") if assessments else ([], "")
    if error:
        return None, f"coverage_verdict.obligation_assessments: {error}"
    if set(assessment_ids) != obligation_ids:
        return None, "coverage_verdict must assess every coverage obligation exactly once"
    for index, assessment in enumerate(assessments):
        status = _nonempty(assessment.get("status")).lower()
        if status not in {"satisfied", "open"}:
            return None, f"obligation_assessments[{index}].status is invalid"
        if not _nonempty(assessment.get("reasoning")):
            return None, f"obligation_assessments[{index}].reasoning is empty"
        mapped = assessment.get("hypothesis_ids")
        if not isinstance(mapped, list) or any(_nonempty(item) not in result_ids for item in mapped):
            return None, f"obligation_assessments[{index}].hypothesis_ids references unknown hypothesis"
        if (
            _nonempty(assessment.get("status")).lower() == "satisfied"
            and not set(mapped) & retained_ids
        ):
            return None, (
                f"obligation_assessments[{index}] cannot be satisfied only by "
                "merged or rejected discoveries"
            )

    required = _object_list(value.get("required_hypotheses"))
    if required is None:
        return None, "required_hypotheses must be an array"
    required_ids, error = _ids(required, "hypothesis_id") if required else ([], "")
    if error:
        return None, f"required_hypotheses: {error}"
    if set(required_ids) & result_ids:
        return None, "required_hypotheses must use new hypothesis IDs"
    for index, hypothesis in enumerate(required):
        _, error = validate_hypothesis_definition(
            hypothesis,
            obligation_ids=obligation_ids,
            prefix=f"required_hypotheses[{index}]",
        )
        if error:
            return None, error

    terminal = all(
        _nonempty(item.get("verdict")).lower() in _TERMINAL_VERDICTS
        for item in verdicts
    )
    all_satisfied = all(
        _nonempty(item.get("status")).lower() == "satisfied"
        and bool(item.get("hypothesis_ids"))
        for item in assessments
    )
    if package_decision == "close" and (
        coverage_status != "closed" or not terminal or not all_satisfied or required
    ):
        return None, (
            "package_decision=close requires closed coverage, terminal verdicts, "
            "satisfied mapped obligations, and no required hypotheses"
        )
    if coverage_status == "closed" and package_decision != "close":
        return None, "coverage_verdict.status=closed requires package_decision=close"
    has_open_assessment = any(
        _nonempty(item.get("status")).lower() == "open"
        for item in assessments
    )
    has_revise_verdict = any(
        _nonempty(item.get("verdict")).lower() == "revise"
        for item in verdicts
    )
    if coverage_status == "open" and not has_open_assessment:
        return None, "coverage_verdict.status=open requires an open obligation assessment"
    if package_decision == "revise" and not (has_revise_verdict or required):
        return None, (
            "package_decision=revise requires a revise hypothesis verdict or "
            "at least one required hypothesis"
        )
    normalized = dict(value)
    normalized["new_hypothesis_decisions"] = decisions
    normalized.pop("discovery_decisions", None)
    return normalized, ""


def advance_hypothesis_manifest(
    subtask: Subtask,
    prior_manifest: Any,
    investigation: dict[str, Any],
    review: dict[str, Any],
) -> dict[str, Any]:
    """Append only critic-accepted/newly-required definitions to the ledger."""
    manifest, _, known, error = _manifest_parts(subtask, prior_manifest)
    if manifest is None:
        raise ValueError(error)
    current_discoveries, discovery_error = _current_discoveries(investigation)
    if current_discoveries is None:
        raise ValueError(discovery_error)
    discovered = {
        _nonempty(item.get("hypothesis_id")): dict(item)
        for item in current_discoveries
        if isinstance(item, dict)
    }
    current_decisions, decision_error = _current_discovery_decisions(review)
    if current_decisions is None:
        raise ValueError(decision_error)
    for decision in current_decisions:
        if (
            not isinstance(decision, dict)
            or _nonempty(decision.get("decision")).lower() != "accept"
        ):
            continue
        hypothesis_id = _nonempty(decision.get("hypothesis_id"))
        if hypothesis_id in discovered:
            known[hypothesis_id] = discovered[hypothesis_id]
    for hypothesis in review.get("required_hypotheses", []) or []:
        if isinstance(hypothesis, dict):
            known[_nonempty(hypothesis.get("hypothesis_id"))] = dict(hypothesis)
    return {
        "schema_version": HYPOTHESIS_BATCH_SCHEMA_VERSION,
        "package_id": _nonempty(subtask.get("id")),
        "revision": int(investigation.get("manifest_revision") or 0),
        "coverage_obligations": list(
            manifest.get("coverage_obligations")
            or subtask.get("coverage_obligations")
            or []
        ),
        "hypotheses": list(known.values()),
    }


def hypothesis_package_closed(review: Any) -> bool:
    if not isinstance(review, dict):
        return False
    coverage = review.get("coverage_verdict")
    verdicts = review.get("hypothesis_verdicts")
    counterexample_attempts = (
        coverage.get("counterexample_attempts")
        if isinstance(coverage, dict)
        else None
    )
    return (
        _nonempty(review.get("package_decision")).lower() == "close"
        and isinstance(coverage, dict)
        and _nonempty(coverage.get("status")).lower() == "closed"
        and isinstance(verdicts, list)
        and bool(verdicts)
        and isinstance(counterexample_attempts, list)
        and bool(counterexample_attempts)
        and not coverage.get("unresolved_cases")
        and all(
            isinstance(item, dict)
            and _nonempty(item.get("verdict")).lower() in _TERMINAL_VERDICTS
            for item in verdicts
        )
        and not review.get("required_hypotheses")
        and not review.get("batch_contract_errors")
    )


__all__ = [
    "HYPOTHESIS_BATCH_SCHEMA_VERSION",
    "advance_hypothesis_manifest",
    "hypothesis_package_closed",
    "initial_hypothesis_manifest",
    "is_hypothesis_batch",
    "is_hypothesis_package",
    "validate_hypothesis_definition",
    "validate_hypothesis_investigation",
    "validate_hypothesis_package",
    "validate_hypothesis_review",
]
