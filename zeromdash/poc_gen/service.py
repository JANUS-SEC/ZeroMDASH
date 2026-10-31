"""Agent-Native PoC generation service with deterministic evidence gates."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from zeromdash import prompts
from zeromdash.agents import AgentResult
from zeromdash.nodes.core.context import _node_focus
from zeromdash.nodes.core.invocation import _invoke_with_output_retry
from zeromdash.workspace import Workspace, slugify

from .config import POC_PHASE_NODES, normalize_poc_config
from .findings import load_finding_records
from .io import (
    atomic_write_json,
    atomic_write_text,
    canonical_json,
    directory_manifest,
    parse_json_object,
    safe_relative_path,
    sha256_text,
    tree_sha256,
)
from .oracle import evaluate_verification, match_oracle, oracle_hash, validate_oracle_spec

Validator = Callable[[dict[str, Any]], tuple[dict[str, Any] | None, str]]



def _compact_observation(value: Any, limit: int = 4000) -> Any:
    if isinstance(value, dict):
        return {key: _compact_observation(item, limit) for key, item in value.items()}
    if isinstance(value, list):
        return [_compact_observation(item, limit) for item in value[:20]]
    if isinstance(value, str) and len(value) > limit:
        return value[:limit] + "\n...[truncated]"
    return value


class PocGenService:
    def __init__(self, state: dict[str, Any], *, backends: dict[str, str] | None = None):
        self.state = state
        self.backends = backends
        self.ws = Workspace.open(state["workspace_root"], state["task_id"])
        self.config = normalize_poc_config(state.get("poc_config"), force_enabled=True)
        self.repo_path = Path(state["repo_path"])

    def _call(self, phase: str, prompt: str, subtask_id: str, validate: Validator) -> tuple[dict[str, Any] | None, list[str]]:
        parsed: dict[str, Any] | None = None
        failure = ""

        def _validate(res: AgentResult) -> tuple[bool, str]:
            nonlocal parsed, failure
            try:
                candidate = parse_json_object(res.stdout)
            except ValueError as exc:
                parsed, failure = None, str(exc)
                return False, failure
            parsed, failure = validate(candidate)
            return parsed is not None, failure

        node = POC_PHASE_NODES[phase]
        _res, errors = _invoke_with_output_retry(
            self.ws,
            node,
            prompt,
            self.backends,
            self.state,
            output_desc=f"a valid JSON object for PoC phase {phase}",
            validate=_validate,
            subtask_id=subtask_id,
            attempt_log_subtask_id=subtask_id,
            focus=_node_focus(self.state, f"{node}_focus"),
            artifact_filenames=("output.json",),
            extra_context={"poc_phase": phase},
        )
        return parsed, errors

    @staticmethod
    def _object_validator(required: tuple[str, ...] = ()) -> Validator:
        def validate(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
            missing = [key for key in required if key not in payload]
            return (None, "missing fields: " + ", ".join(missing)) if missing else (payload, "")
        return validate

    def _plan(self, record: dict[str, Any], workdir: Path) -> tuple[dict[str, Any] | None, list[str]]:
        prompt = prompts.POC_PLAN.format(
            request_path=workdir / "request.json",
            repo_path=self.repo_path,
            verification_runs=self.config["verification_runs"],
            verification_min_matches=self.config["verification_min_matches"],
            max_strategies=self.config["max_strategies_per_round"],
        )
        def validate(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
            spec, failure = validate_oracle_spec(payload.get("oracle_spec"))
            if spec is None:
                return None, failure
            strategies = payload.get("strategies")
            if not isinstance(strategies, list) or not strategies:
                return None, "strategies must be a non-empty array"
            normalized = []
            for index, strategy in enumerate(strategies[: self.config["max_strategies_per_round"]], start=1):
                if not isinstance(strategy, dict) or not str(strategy.get("objective") or "").strip():
                    return None, f"strategy {index} requires an objective"
                normalized.append({**strategy, "strategy_id": f"strategy-{index}"})
            return {**payload, "oracle_spec": spec, "strategies": normalized}, ""
        return self._call("plan_poc", prompt, f"{record['finding_id']}-plan", validate)

    def _prepare(self, record: dict[str, Any], workdir: Path) -> tuple[dict[str, Any] | None, list[str]]:
        prompt = prompts.POC_PREPARE_ENVIRONMENT.format(
            plan_path=workdir / "plan.json",
            request_path=workdir / "request.json",
            repo_path=self.repo_path,
            workdir=workdir,
        )
        def validate(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
            if payload.get("status") not in {"ready", "failed"} or not isinstance(payload.get("environment_manifest"), dict):
                return None, "prepare requires status=ready|failed and environment_manifest"
            return payload, ""
        return self._call("prepare_environment", prompt, f"{record['finding_id']}-prepare", validate)

    def _generate(self, record: dict[str, Any], strategy: dict[str, Any], attempt_dir: Path, parent: dict[str, Any] | None, debug: dict[str, Any] | None) -> tuple[dict[str, Any] | None, list[str]]:
        workdir = attempt_dir.parent.parent
        input_dir = attempt_dir / "inputs"
        strategy_path = input_dir / "strategy.json"
        parent_path = input_dir / "parent_attempt.json"
        debug_path = input_dir / "debug.json"
        atomic_write_json(strategy_path, strategy)
        atomic_write_json(parent_path, parent or {})
        atomic_write_json(debug_path, debug or {})
        prompt = prompts.POC_GENERATE.format(
            request_path=workdir / "request.json",
            oracle_path=workdir / "oracle.json",
            strategy_path=strategy_path,
            parent_path=parent_path,
            debug_path=debug_path,
            attempt_dir=attempt_dir,
        )
        def validate(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
            files = payload.get("files")
            if not isinstance(files, list) or not files or len(files) > 20:
                return None, "files must contain 1..20 artifacts"
            total = 0
            for item in files:
                if not isinstance(item, dict) or not isinstance(item.get("content"), str):
                    return None, "each PoC file requires path and text content"
                safe_relative_path(str(item.get("path") or ""))
                total += len(item["content"])
            if total > 2_000_000 or not isinstance(payload.get("run"), dict):
                return None, "PoC content exceeds 2 MB or run declaration is missing"
            return payload, ""
        return self._call("generate_poc", prompt, f"{record['finding_id']}-{strategy['strategy_id']}-{attempt_dir.name}", validate)

    def _execute(self, record: dict[str, Any], attempt_dir: Path) -> tuple[dict[str, Any] | None, list[str]]:
        prompt = prompts.POC_EXECUTE.format(
            generation_path=attempt_dir / "generation.json",
            oracle_path=attempt_dir.parent.parent / "oracle.json",
            attempt_dir=attempt_dir,
        )
        def validate(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
            if not isinstance(payload.get("runs"), list) or not payload["runs"]:
                return None, "execution requires at least one run observation"
            status = str(payload.get("runner_status") or "")
            if status not in {"completed", "expected_terminal", "build_failed", "setup_failed", "runner_failed", "timeout", "oom"}:
                return None, f"invalid runner_status: {status}"
            for run in payload["runs"]:
                if not isinstance(run, dict):
                    return None, "each run must be an object"
                run.setdefault("runner_status", status)
            return payload, ""
        return self._call("execute_poc", prompt, f"{record['finding_id']}-{attempt_dir.name}-execute", validate)

    def _debug(self, record: dict[str, Any], attempt_dir: Path, observation: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
        workdir = attempt_dir.parent.parent
        prompt = prompts.POC_DEBUG.format(
            request_path=workdir / "request.json",
            oracle_path=workdir / "oracle.json",
            generation_path=attempt_dir / "generation.json",
            observation_path=attempt_dir / "observation.json",
        )
        return self._call("debug_poc", prompt, f"{record['finding_id']}-debug-{sha256_text(canonical_json(observation))[:8]}", self._object_validator(("hypothesis", "changes")))

    def _verify(self, record: dict[str, Any], spec: dict[str, Any], attempt_dir: Path) -> tuple[dict[str, Any] | None, list[str]]:
        prompt = prompts.POC_VERIFY.format(
            generation_path=attempt_dir / "generation.json",
            oracle_path=attempt_dir.parent.parent / "oracle.json",
            attempt_dir=attempt_dir,
            verification_runs=spec["stability"]["runs"],
        )
        def validate(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
            if not isinstance(payload.get("runs"), list) or not isinstance(payload.get("controls"), list):
                return None, "verification requires runs and controls arrays"
            for run in payload["runs"]:
                if isinstance(run, dict):
                    run.setdefault("runner_status", "completed")
            return payload, ""
        return self._call("verify_poc", prompt, f"{record['finding_id']}-{attempt_dir.name}-verify", validate)

    def _release(self, record: dict[str, Any], result: dict[str, Any], release_dir: Path, workdir: Path) -> tuple[dict[str, Any] | None, list[str]]:
        release_input_path = workdir / "release_input.json"
        atomic_write_json(release_input_path, _compact_observation(result, 6000))
        prompt = prompts.POC_RELEASE.format(
            release_input_path=release_input_path,
            release_dir=release_dir,
        )
        return self._call("release_poc", prompt, f"{record['finding_id']}-release", self._object_validator(("readme", "report")))

    def _public(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {key: self._public(item) for key, item in value.items()}
        if isinstance(value, list):
            return [self._public(item) for item in value]
        if isinstance(value, str):
            return value.replace(str(self.ws.base), "${WORKSPACE}").replace(str(self.repo_path), "${REPO}")
        return value

    def _publish(self, record: dict[str, Any], result: dict[str, Any], release_dir: Path, documents: dict[str, Any] | None) -> None:
        release_dir.mkdir(parents=True, exist_ok=True)
        status = result["status"]
        readme = str((documents or {}).get("readme") or f"# PoC {record['finding_id']}\n\nStatus: `{status}`.\n")
        report = str((documents or {}).get("report") or "")
        if not report.strip():
            report = (
                f"# Reproduction report: {record['finding_id']}\n\n"
                f"## Status\n\n`{status}`\n\n## Evidence\n\n"
                f"See `evidence/result.json`. Report Agent output was unavailable: {result.get('errors', [])}\n"
            )
        if record["finding_id"] not in report:
            report = f"Finding: `{record['finding_id']}`\n\n" + report
        if status not in report:
            report += f"\n\n## Final status\n\n`{status}`\n"
        combined = readme + report
        if "PRIVATE KEY-----" in combined:
            raise ValueError("release report contains private key material")
        atomic_write_text(release_dir / "README.md", self._public(readme))
        atomic_write_text(release_dir / "repro_report.md", self._public(report))
        best = result.get("best_attempt") or {}
        if best.get("attempt_dir"):
            source = Path(best["attempt_dir"]) / "poc"
            if source.is_dir():
                for path in source.rglob("*"):
                    if path.is_file() and not path.is_symlink():
                        target = release_dir / "poc" / path.relative_to(source)
                        atomic_write_text(target, path.read_text(errors="replace"))
        atomic_write_json(release_dir / "evidence" / "result.json", self._public(result))
        artifacts = [item for item in directory_manifest(release_dir) if item["path"] != "manifest.json"]
        manifest = {
            "schema_version": "1.0",
            "finding_id": record["finding_id"],
            "request_id": record["request_id"],
            "status": status,
            "backend": self.config["backend"],
            "artifacts": artifacts,
        }
        atomic_write_json(release_dir / "manifest.json", manifest)

    def run_record(self, record: dict[str, Any]) -> dict[str, Any]:
        stem = f"{slugify(record['finding_id'])}-{record['request_id'][-8:]}"
        run_stem = stem
        if (self.ws.base / "poc" / run_stem).exists():
            run_stem = f"{stem}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}"
        workdir = self.ws.base / "poc" / run_stem
        attempts_dir = workdir / "attempts"
        release_dir = self.ws.base / "deliverables" / "poc" / run_stem
        workdir.mkdir(parents=True, exist_ok=True)
        atomic_write_json(workdir / "request.json", {k: v for k, v in record.items() if k != "aliases"})
        baseline_hash = tree_sha256(self.repo_path)
        attempts: list[dict[str, Any]] = []
        errors: list[str] = []
        best_attempt: dict[str, Any] | None = None
        status = "inconclusive"
        verification_details: dict[str, Any] = {}
        environment_manifest: dict[str, Any] = {}
        try:
            plan, plan_errors = self._plan(record, workdir)
            errors.extend(plan_errors)
            if plan is None:
                return self._finish(record, workdir, release_dir, status, attempts, best_attempt, errors, baseline_hash, environment_manifest, verification_details)
            spec = plan["oracle_spec"]
            spec_hash = oracle_hash(spec)
            atomic_write_json(workdir / "plan.json", {**plan, "oracle_hash": spec_hash, "full_source_tree_hash": baseline_hash})
            atomic_write_json(workdir / "oracle.json", spec)
            prepared, prepare_errors = self._prepare(record, workdir)
            errors.extend(prepare_errors)
            if prepared is None or prepared.get("status") != "ready":
                status = "environment_failed"
                return self._finish(record, workdir, release_dir, status, attempts, best_attempt, errors, baseline_hash, environment_manifest, verification_details)
            environment_manifest = prepared["environment_manifest"]
            atomic_write_json(workdir / "environment.json", environment_manifest)
            if tree_sha256(self.repo_path) != baseline_hash:
                status = "environment_failed"
                errors.append("source tree drift detected during environment preparation")
                return self._finish(record, workdir, release_dir, status, attempts, best_attempt, errors, baseline_hash, environment_manifest, verification_details)

            any_oracle = False
            valid_execution = False
            environment_failed = False
            for strategy in plan["strategies"]:
                parent: dict[str, Any] | None = None
                debug: dict[str, Any] | None = None
                signatures: dict[str, int] = {}
                for round_index in range(1, self.config["max_debug_rounds_per_strategy"] + 1):
                    attempt_id = f"{strategy['strategy_id']}-attempt-{round_index}"
                    attempt_dir = attempts_dir / attempt_id
                    attempt_dir.mkdir(parents=True, exist_ok=False)
                    generation, generation_errors = self._generate(record, strategy, attempt_dir, parent, debug)
                    errors.extend(generation_errors)
                    if generation is None:
                        break
                    for item in generation["files"]:
                        relative = safe_relative_path(item["path"])
                        atomic_write_text(attempt_dir / "poc" / relative, item["content"])
                    atomic_write_json(attempt_dir / "generation.json", generation)
                    observation, execute_errors = self._execute(record, attempt_dir)
                    errors.extend(execute_errors)
                    if observation is None:
                        break
                    atomic_write_json(attempt_dir / "observation.json", observation)
                    if tree_sha256(self.repo_path) != baseline_hash:
                        status = "environment_failed"
                        errors.append(f"source tree drift detected in {attempt_id}")
                        environment_failed = True
                        break
                    matches = [match_oracle(spec, run) for run in observation["runs"]]
                    matched = any(item[0] for item in matches)
                    any_oracle = any_oracle or matched
                    valid_execution = valid_execution or observation.get("runner_status") in {"completed", "expected_terminal"}
                    attempt = {
                        "attempt_id": attempt_id,
                        "strategy_id": strategy["strategy_id"],
                        "attempt_dir": str(attempt_dir),
                        "generation": generation,
                        "observation": observation,
                        "oracle_match": matched,
                        "oracle_reasons": [item[1] for item in matches],
                    }
                    attempts.append(attempt)
                    parent = attempt
                    if matched:
                        best_attempt = attempt
                        verification, verify_errors = self._verify(record, spec, attempt_dir)
                        errors.extend(verify_errors)
                        if verification is not None:
                            atomic_write_json(attempt_dir / "verification.json", verification)
                            verdict, verification_details = evaluate_verification(spec, verification)
                            attempt["verification"] = verification
                            attempt["verification_details"] = verification_details
                            any_oracle = any_oracle or verification_details.get("oracle_match_count", 0) > 0
                            if verdict == "validated":
                                status = "validated"
                                return self._finish(record, workdir, release_dir, status, attempts, best_attempt, errors, baseline_hash, environment_manifest, verification_details)
                        break
                    if observation.get("runner_status") in {"setup_failed", "runner_failed"}:
                        environment_failed = True
                        break
                    if round_index >= self.config["max_debug_rounds_per_strategy"]:
                        break
                    signature = sha256_text(canonical_json(_compact_observation(observation)))[:16]
                    signatures[signature] = signatures.get(signature, 0) + 1
                    if signatures[signature] >= self.config["max_no_progress_rounds"]:
                        break
                    debug, debug_errors = self._debug(record, attempt_dir, observation)
                    errors.extend(debug_errors)
                    if debug is None:
                        break
                if status == "validated":
                    break
                if environment_failed:
                    status = "environment_failed"
                    break
            if status != "environment_failed":
                status = "reproduced_unstable" if any_oracle else "not_reproduced" if valid_execution else "inconclusive"
        except Exception as exc:
            errors.append(f"unhandled PoC generation error: {type(exc).__name__}: {exc}")
            if status != "validated":
                status = "inconclusive"
        return self._finish(record, workdir, release_dir, status, attempts, best_attempt, errors, baseline_hash, environment_manifest, verification_details)

    def _finish(self, record: dict[str, Any], workdir: Path, release_dir: Path, status: str, attempts: list[dict[str, Any]], best_attempt: dict[str, Any] | None, errors: list[str], source_hash: str, environment: dict[str, Any], verification: dict[str, Any]) -> dict[str, Any]:
        integrity_ok = tree_sha256(self.repo_path) == source_hash
        if not integrity_ok and status == "validated":
            status = "environment_failed"
            errors.append("source tree drift detected before release; validated result rejected")
        result = {
            "schema_version": "1.0",
            "request_id": record["request_id"],
            "finding_id": record["finding_id"],
            "finding_type": record["finding_type"],
            "status": status,
            "backend": self.config["backend"],
            "full_source_tree_hash": source_hash,
            "source_integrity_ok": integrity_ok,
            "environment_manifest": environment,
            "attempt_count": len(attempts),
            "attempts": attempts,
            "best_attempt": best_attempt,
            "verification": verification,
            "cleanup_status": "completed",
            "errors": list(dict.fromkeys(errors)),
        }
        documents, release_errors = self._release(record, result, release_dir, workdir)
        result["errors"].extend(release_errors)
        if tree_sha256(self.repo_path) != source_hash:
            result["source_integrity_ok"] = False
            result["errors"].append("source tree drift detected during release")
            if result["status"] == "validated":
                result["status"] = "environment_failed"
                documents = None
        try:
            self._publish(record, result, release_dir, documents)
            result["release_path"] = str(release_dir)
        except Exception as exc:
            result["errors"].append(f"release failed: {type(exc).__name__}: {exc}")
        result_path = self.ws.log_path("poc_res") / f"{workdir.name}.json"
        result["result_path"] = str(result_path)
        atomic_write_json(result_path, result)
        return result

    def run(self, selected_id: str = "", stats: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        records = load_finding_records(self.state, selected_id, stats=stats)
        records = records[: self.config["max_findings"]]
        return [self.run_record(record) for record in records]
