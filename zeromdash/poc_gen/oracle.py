"""OracleSpec validation and deterministic observation matching."""

from __future__ import annotations

from typing import Any

from .io import canonical_json, sha256_text

_KINDS = {"sanitizer", "signal", "exit_code", "output", "state_invariant", "plugin"}


def oracle_hash(spec: dict[str, Any]) -> str:
    return sha256_text(canonical_json(spec))


def validate_oracle_spec(value: Any) -> tuple[dict[str, Any] | None, str]:
    if not isinstance(value, dict):
        return None, "oracle_spec must be an object"
    kind = str(value.get("kind") or "").strip()
    if kind not in _KINDS:
        return None, f"unsupported oracle kind: {kind!r}"
    expected = value.get("expected")
    if not isinstance(expected, dict) or not expected:
        return None, "oracle_spec.expected must be a non-empty object"
    reachability = value.get("reachability") or {}
    if not isinstance(reachability, dict):
        return None, "oracle_spec.reachability must be an object"
    markers = reachability.get("required_markers", [])
    if not isinstance(markers, list) or any(not isinstance(item, str) or not item.strip() for item in markers):
        return None, "oracle_spec.reachability.required_markers must contain strings"
    controls = value.get("controls", [])
    if not isinstance(controls, list):
        return None, "oracle_spec.controls must be an array"
    for control in controls:
        if not isinstance(control, dict) or not str(control.get("kind") or "").strip():
            return None, "each oracle control requires a kind"
        if not isinstance(control.get("required", False), bool):
            return None, "oracle control required must be bool"
    stability = value.get("stability")
    if not isinstance(stability, dict):
        return None, "oracle_spec.stability must be an object"
    runs, min_matches = stability.get("runs"), stability.get("min_matches")
    if any(not isinstance(item, int) or isinstance(item, bool) for item in (runs, min_matches)):
        return None, "oracle stability runs/min_matches must be integers"
    if runs <= 0 or min_matches <= 0 or min_matches > runs:
        return None, "oracle stability requires 1 <= min_matches <= runs"
    profile = str(value.get("profile") or "").strip()
    if not profile:
        return None, "oracle_spec.profile is required"
    normalized = dict(value)
    normalized["kind"] = kind
    normalized["profile"] = profile
    return normalized, ""


def _symbols(observation: dict[str, Any]) -> set[str]:
    symbols: set[str] = set()
    backtrace = observation.get("backtrace") or []
    if isinstance(backtrace, str):
        return {backtrace}
    if isinstance(backtrace, list):
        for frame in backtrace:
            if isinstance(frame, str):
                symbols.add(frame)
            elif isinstance(frame, dict) and frame.get("symbol"):
                symbols.add(str(frame["symbol"]))
    return symbols


def _state_value(state: dict[str, Any], path: str) -> Any:
    current: Any = state
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def match_oracle(spec: dict[str, Any], observation: dict[str, Any]) -> tuple[bool, str]:
    """Return whether one structured run observation matches the frozen spec."""
    runner_status = str(observation.get("runner_status") or "completed")
    if runner_status not in {"completed", "expected_terminal"}:
        return False, f"runner status is not oracle-evaluable: {runner_status}"
    required = (spec.get("reachability") or {}).get("required_markers", [])
    markers = {str(item) for item in observation.get("markers") or []}
    missing = [item for item in required if item not in markers]
    if missing:
        return False, "missing reachability markers: " + ", ".join(missing)

    expected = spec.get("expected") or {}
    kind = spec.get("kind")
    if kind == "sanitizer":
        sanitizer = observation.get("sanitizer") or {}
        actual_name = str(sanitizer.get("name") or "").lower()
        actual_error = str(sanitizer.get("error") or "").lower()
        if str(expected.get("sanitizer") or "").lower() not in actual_name:
            return False, "sanitizer name does not match"
        if str(expected.get("error") or "").lower() not in actual_error:
            return False, "sanitizer error does not match"
        symbols = _symbols(observation)
        missing_symbols = [item for item in expected.get("top_symbols") or [] if str(item) not in symbols]
        if missing_symbols:
            return False, "missing backtrace symbols: " + ", ".join(missing_symbols)
    elif kind == "signal":
        if str(observation.get("signal") or "") != str(expected.get("signal") or ""):
            return False, "signal does not match"
    elif kind == "exit_code":
        if observation.get("exit_code") != expected.get("exit_code"):
            return False, "exit code does not match"
    elif kind == "output":
        text = str(observation.get("stdout") or "") + str(observation.get("stderr") or "")
        contains = expected.get("contains") or []
        if isinstance(contains, str):
            contains = [contains]
        if any(str(item) not in text for item in contains):
            return False, "required output is absent"
        not_contains = expected.get("not_contains") or []
        if isinstance(not_contains, str):
            not_contains = [not_contains]
        if any(str(item) in text for item in not_contains):
            return False, "forbidden output is present"
    elif kind == "state_invariant":
        state = observation.get("state") or {}
        violation = str(expected.get("violation") or "")
        if not violation or state.get(violation) is not True:
            return False, "expected state-invariant violation is absent"
        missing_fields = [path for path in expected.get("required_fields") or [] if _state_value(state, path) is None]
        if missing_fields:
            return False, "missing state fields: " + ", ".join(missing_fields)
    elif kind == "plugin":
        plugin = observation.get("plugin") or {}
        if str(plugin.get("name") or "") != str(expected.get("plugin") or ""):
            return False, "oracle plugin does not match"
        if expected.get("plugin_version") and str(plugin.get("version") or "") != str(expected["plugin_version"]):
            return False, "oracle plugin version does not match"
        metrics = observation.get("metrics") or {}
        minimum = expected.get("min_absolute_milliseconds")
        if minimum is not None and float(metrics.get("duration_ms") or 0) < float(minimum):
            return False, "duration threshold is not met"
        ratio = expected.get("min_ratio_to_baseline")
        if ratio is not None and float(metrics.get("ratio_to_baseline") or 0) < float(ratio):
            return False, "baseline ratio threshold is not met"
        if expected.get("operation") and plugin.get("operation") != expected["operation"]:
            return False, "plugin operation does not match"
    return True, "matched"


def evaluate_verification(spec: dict[str, Any], payload: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    runs = payload.get("runs") or []
    controls = payload.get("controls") or []
    matches = [match_oracle(spec, run) for run in runs if isinstance(run, dict)]
    match_count = sum(1 for matched, _ in matches if matched)
    stability = spec["stability"]
    failures: list[str] = []
    if len(runs) < stability["runs"]:
        failures.append(f"verification has {len(runs)} runs, requires {stability['runs']}")
    if match_count < stability["min_matches"]:
        failures.append(f"oracle matched {match_count} runs, requires {stability['min_matches']}")
    by_kind = {str(item.get("kind") or ""): item for item in controls if isinstance(item, dict)}
    for control in spec.get("controls") or []:
        kind = str(control["kind"])
        result = by_kind.get(kind)
        if result is None:
            if control.get("required", False):
                failures.append(f"required control missing: {kind}")
            continue
        status = str(result.get("status") or "")
        if status == "skipped":
            if control.get("required", False) or not str(result.get("skip_reason") or "").strip():
                failures.append(f"control skipped without an allowed reason: {kind}")
        elif status != "passed":
            failures.append(f"control did not pass: {kind}")
        observation = result.get("observation")
        if isinstance(observation, dict) and match_oracle(spec, observation)[0]:
            failures.append(f"control triggered the target oracle: {kind}")
    details = {
        "run_count": len(runs),
        "oracle_match_count": match_count,
        "required_runs": stability["runs"],
        "required_matches": stability["min_matches"],
        "failures": failures,
    }
    return ("validated" if not failures else "reproduced_unstable" if match_count else "not_reproduced"), details
