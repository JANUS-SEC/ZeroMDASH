"""Manifest loading and immutable input preparation for gather scans."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

import yaml

from zeromdash.gather_state import GatherEvidenceUnit, GatherState, GatherTarget
from zeromdash.nodes.core.gather_evidence import (
    merge_evidence_unit,
    source_ref,
    unit_from_chain,
    unit_from_finding,
    unit_from_primitive,
)
from zeromdash.workspace import Workspace, slugify


GATHER_MANIFEST_VERSION = "1.0"


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _resolve_manifest_path(raw: object, *, base: Path, field: str) -> Path:
    value = os.path.expandvars(os.path.expanduser(str(raw or "").strip()))
    if not value:
        raise ValueError(f"gather manifest {field} is required")
    path = Path(value)
    if not path.is_absolute():
        path = base / path
    return path.resolve()


def load_gather_manifest(path: str | Path) -> dict[str, Any]:
    """Load, validate, and canonicalize one multi-target gather manifest."""
    manifest_path = Path(path).expanduser().resolve()
    try:
        raw = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"gather manifest not found: {manifest_path}") from exc
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid gather manifest YAML {manifest_path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError("gather manifest must be a YAML mapping")
    unknown = sorted(set(raw) - {"schema_version", "name", "scenario", "gather_agent_config", "targets"})
    if unknown:
        raise ValueError(f"unknown gather manifest key(s): {', '.join(str(item) for item in unknown)}")
    version = str(raw.get("schema_version") or "").strip()
    if version != GATHER_MANIFEST_VERSION:
        raise ValueError(
            f"unsupported gather manifest schema_version {version!r}; expected {GATHER_MANIFEST_VERSION!r}"
        )
    scenario = str(raw.get("scenario") or "").strip()
    if not scenario:
        raise ValueError("gather manifest scenario must be non-empty")
    raw_targets = raw.get("targets")
    if not isinstance(raw_targets, list) or len(raw_targets) < 2:
        raise ValueError("gather manifest targets must contain at least two entries")

    targets: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    seen_ids: set[str] = set()
    for index, item in enumerate(raw_targets, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"gather manifest targets[{index}] must be a mapping")
        target_unknown = sorted(set(item) - {"name", "agent_config", "workspace", "role"})
        if target_unknown:
            raise ValueError(
                f"unknown gather manifest targets[{index}] key(s): "
                + ", ".join(str(value) for value in target_unknown)
            )
        name = str(item.get("name") or "").strip()
        if not name:
            raise ValueError(f"gather manifest targets[{index}].name is required")
        target_id = slugify(name)
        if name in seen_names:
            raise ValueError(f"duplicate gather target name: {name}")
        if target_id in seen_ids:
            raise ValueError(f"gather target namespace collision after slugify: {target_id}")
        seen_names.add(name)
        seen_ids.add(target_id)
        workspace = _resolve_manifest_path(
            item.get("workspace"), base=manifest_path.parent, field=f"targets[{index}].workspace"
        )
        agent_config = _resolve_manifest_path(
            item.get("agent_config"), base=manifest_path.parent, field=f"targets[{index}].agent_config"
        )
        if not workspace.is_dir():
            raise ValueError(f"gather target {name!r} workspace is not a directory: {workspace}")
        if not agent_config.is_file():
            raise ValueError(f"gather target {name!r} agent_config is not a file: {agent_config}")
        if not (workspace / "workspace.json").is_file():
            raise ValueError(f"gather target {name!r} is missing workspace.json: {workspace}")
        attack_surface = workspace / "main" / "attack_surface"
        if not attack_surface.is_dir() or not any(
            child.is_file() and child.stat().st_size > 0
            for child in attack_surface.rglob("*")
        ):
            raise ValueError(f"gather target {name!r} has no main/attack_surface artifacts")
        evidence_dirs = [
            workspace / "log" / "primitive_res",
            workspace / "log" / "subtask_res",
            workspace / "log" / "review_res",
            workspace / "log" / "chain_res",
        ]
        if not any(
            candidate.is_file() and candidate.stat().st_size > 0
            for directory in evidence_dirs
            if directory.is_dir()
            for candidate in directory.glob("*.json")
        ):
            raise ValueError(f"gather target {name!r} has no chain evidence artifacts")
        targets.append(
            {
                "target_id": target_id,
                "name": name,
                "role": str(item.get("role") or "").strip(),
                "workspace": str(workspace),
                "agent_config": str(agent_config),
            }
        )

    gather_agent_config = ""
    if raw.get("gather_agent_config"):
        gather_config_path = _resolve_manifest_path(
            raw.get("gather_agent_config"),
            base=manifest_path.parent,
            field="gather_agent_config",
        )
        if not gather_config_path.is_file():
            raise ValueError(f"gather_agent_config is not a file: {gather_config_path}")
        gather_agent_config = str(gather_config_path)

    name = str(raw.get("name") or manifest_path.stem).strip()
    normalized = {
        "schema_version": GATHER_MANIFEST_VERSION,
        "name": name,
        "scenario": scenario,
        "targets": targets,
        "manifest_path": str(manifest_path),
    }
    if gather_agent_config:
        normalized["gather_agent_config"] = gather_agent_config
    return normalized


def _workspace_from_base(path: Path) -> Workspace:
    return Workspace.open(path.parent, path.name)


def _sanitized_source_config(path: Path) -> dict[str, Any]:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid source agent config YAML {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError(f"source agent config must be a mapping: {path}")
    common = raw.get("common_focus") or ""
    if isinstance(common, dict):
        common = common.get("focus") or ""
    node_focus: dict[str, str] = {}
    nodes = raw.get("node") or {}
    if isinstance(nodes, dict):
        for name, config in nodes.items():
            if isinstance(config, dict) and config.get("focus"):
                node_focus[str(name)] = str(config["focus"]).strip()
    target_repos = []
    for item in raw.get("target_repos") or []:
        if not isinstance(item, dict):
            continue
        target_repos.append(
            {
                key: str(item.get(key) or "").strip()
                for key in ("id", "name", "role", "description")
                if item.get(key)
            }
        )
    return {
        "common_focus": str(common).strip(),
        "node_focus": node_focus,
        "target_repos": target_repos,
        "config_sha256": _sha256_file(path),
    }


def _git_fingerprint(path: Path) -> dict[str, Any]:
    def run(*args: str) -> str:
        try:
            proc = subprocess.run(
                ["git", "-C", str(path), *args],
                text=True,
                capture_output=True,
                check=False,
                timeout=20,
            )
        except (OSError, subprocess.TimeoutExpired):
            return ""
        return proc.stdout.strip() if proc.returncode == 0 else ""

    head = run("rev-parse", "HEAD")
    status = run("status", "--porcelain=v1")
    fingerprint = {
        "git_head": head,
        "git_dirty": bool(status),
        "git_status_sha256": _sha256_bytes(status.encode("utf-8")),
    }
    if not head:
        digest = hashlib.sha256()
        for item in sorted(path.rglob("*")):
            if ".git" in item.parts or not item.is_file():
                continue
            relative = str(item.relative_to(path))
            digest.update(relative.encode("utf-8"))
            try:
                digest.update(item.read_bytes())
            except OSError:
                digest.update(b"<unreadable>")
        fingerprint["tree_sha256"] = digest.hexdigest()
    return fingerprint


def _copy_source_tree(source: Path, destination: Path) -> list[str]:
    skipped_symlinks: list[str] = []

    def ignore(directory: str, names: list[str]) -> set[str]:
        ignored = {
            name
            for name in names
            if name in {".git", ".zeromdash", "sub_workspace", "__pycache__"}
            or name.endswith(".pyc")
            or (Path(directory) / name).is_symlink()
        }
        for name in ignored:
            path = Path(directory) / name
            if path.is_symlink():
                skipped_symlinks.append(str(path.relative_to(source)))
        return ignored

    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(
        source,
        destination,
        symlinks=False,
        ignore=ignore,
    )
    return sorted(set(skipped_symlinks))


def _copy_artifact(source: Path, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return _sha256_file(destination)


def _source_roots(ws: Workspace) -> list[tuple[str, Path]]:
    roots: list[tuple[str, Path]] = []
    main_repo = ws.main_path("repo")
    if main_repo.is_dir() and any(main_repo.iterdir()):
        roots.append(("main", main_repo))
    repos = ws.main_path("repos")
    if repos.is_dir():
        for child in sorted(repos.iterdir()):
            if child.is_dir() and any(child.iterdir()):
                roots.append((slugify(child.name), child))
    return roots


def _snapshot_target(
    gather_ws: Workspace,
    spec: dict[str, Any],
) -> tuple[GatherTarget, list[GatherEvidenceUnit], list[dict[str, Any]]]:
    from zeromdash.nodes.core.result_artifacts import (
        active_subtask_result_payloads,
        declared_package_ids,
        primitive_has_package_source,
    )

    target_id = spec["target_id"]
    source_base = Path(spec["workspace"])
    source_ws = _workspace_from_base(source_base)
    workspace_meta_path = source_base / "workspace.json"
    if not workspace_meta_path.is_file():
        raise ValueError(f"gather target {spec['name']!r} is missing workspace.json: {source_base}")
    workspace_meta = _read_json(workspace_meta_path)
    if not isinstance(workspace_meta, dict):
        raise ValueError(f"gather target {spec['name']!r} has invalid workspace.json")

    attack_surface_dir = source_ws.main_path("attack_surface")
    attack_files = [path for path in attack_surface_dir.rglob("*") if path.is_file()] if attack_surface_dir.is_dir() else []
    if not attack_files:
        raise ValueError(f"gather target {spec['name']!r} has no main/attack_surface artifacts")

    target_root = gather_ws.base / "inputs" / target_id
    target_root.mkdir(parents=True, exist_ok=True)
    hashes: dict[str, str] = {}
    snapshot_workspace_meta = {
        key: workspace_meta[key]
        for key in ("task_id", "target", "role_lang", "created_at", "scan_mode")
        if key in workspace_meta
    }
    snapshot_workspace_path = target_root / "workspace.json"
    _write_json_atomic(snapshot_workspace_path, snapshot_workspace_meta)
    hashes["workspace.json"] = _sha256_file(snapshot_workspace_path)
    for source in sorted(attack_files):
        relative = source.relative_to(attack_surface_dir)
        destination = target_root / "attack_surface" / relative
        hashes[str(destination.relative_to(gather_ws.base))] = _copy_artifact(source, destination)

    source_config_path = Path(spec["agent_config"])
    source_context = _sanitized_source_config(source_config_path)
    source_context.update(
        {
            "target_id": target_id,
            "name": spec["name"],
            "role": spec.get("role", ""),
            "agent_config_path": str(source_config_path),
        }
    )
    source_context_path = target_root / "source_context.json"
    _write_json_atomic(source_context_path, source_context)
    hashes[str(source_context_path.relative_to(gather_ws.base))] = _sha256_file(source_context_path)

    original_roots = _source_roots(source_ws)
    if not original_roots:
        raise ValueError(f"gather target {spec['name']!r} has no materialized source tree")
    snapshot_roots: list[str] = []
    source_revision: dict[str, Any] = {}
    for repo_id, source_root in original_roots:
        destination = target_root / "source" / repo_id
        skipped_symlinks = _copy_source_tree(source_root, destination)
        if not any(item.is_file() for item in destination.rglob("*")):
            raise ValueError(
                f"gather target {spec['name']!r} source snapshot is empty for repo {repo_id!r}"
            )
        snapshot_roots.append(str(destination))
        source_revision[repo_id] = {
            "source_path": str(source_root.resolve()),
            "snapshot_skipped_symlinks": skipped_symlinks,
            **_git_fingerprint(source_root),
        }

    final_state = _read_json(source_base / "final_state.json")
    prior_state = final_state if isinstance(final_state, dict) else {}
    active_chain_ids: set[str] | None = None
    if isinstance(prior_state.get("chain_findings"), list):
        active_chain_ids = {
            str(item.get("chain_id") or "")
            for item in prior_state["chain_findings"]
            if isinstance(item, dict) and str(item.get("chain_id") or "")
        }
    revision = ""
    if prior_state:
        revision = str((prior_state.get("scan_scope") or {}).get("repo_revision") or "")
    if not revision:
        revision = next(
            (str(item.get("git_head") or "") for item in source_revision.values() if item.get("git_head")),
            "",
        )

    units_by_id: dict[str, GatherEvidenceUnit] = {}
    context_only: list[dict[str, Any]] = []

    active_payloads = active_subtask_result_payloads(source_ws)
    package_ids = declared_package_ids(source_ws)

    primitive_dir = source_ws.log_path("primitive_res")
    if primitive_dir.is_dir():
        for source in sorted(primitive_dir.glob("*.json")):
            payload = _read_json(source)
            if not isinstance(payload, dict) or primitive_has_package_source(payload, package_ids):
                continue
            destination = target_root / "primitive_res" / source.name
            hashes[str(destination.relative_to(gather_ws.base))] = _copy_artifact(source, destination)
            local_id = str(payload.get("primitive_id") or source.stem)
            ref = source_ref(
                target_id=target_id,
                source_ws=source_ws,
                artifact_kind="primitive_res",
                snapshot_path=destination,
                snapshot_base=gather_ws.base,
                local_id=local_id,
                payload=payload,
                revision=revision,
            )
            unit = unit_from_primitive(payload, target_id=target_id, source_ref_value=ref)
            merge_evidence_unit(units_by_id, unit, source_name=spec["name"])

    for source, payload in active_payloads:
        destination = target_root / "subtask_res" / source.name
        hashes[str(destination.relative_to(gather_ws.base))] = _copy_artifact(source, destination)
        primitive = payload.get("primitive")
        finding = payload.get("finding")
        if isinstance(primitive, dict):
            local_id = str(primitive.get("primitive_id") or source.stem)
            ref = source_ref(
                target_id=target_id,
                source_ws=source_ws,
                artifact_kind="subtask_res",
                snapshot_path=destination,
                snapshot_base=gather_ws.base,
                local_id=local_id,
                payload=primitive,
                revision=revision,
                json_pointer="/primitive",
            )
            unit = unit_from_primitive(primitive, target_id=target_id, source_ref_value=ref)
            merge_evidence_unit(units_by_id, unit, source_name=spec["name"])
        if isinstance(finding, dict):
            local_id = str(finding.get("subtask_id") or source.stem)
            ref = source_ref(
                target_id=target_id,
                source_ws=source_ws,
                artifact_kind="subtask_res",
                snapshot_path=destination,
                snapshot_base=gather_ws.base,
                local_id=local_id,
                payload=finding,
                revision=revision,
                json_pointer="/finding",
            )
            unit = unit_from_finding(finding, target_id=target_id, source_ref_value=ref)
            if unit is not None:
                merge_evidence_unit(units_by_id, unit, source_name=spec["name"])
            else:
                context_only.append({"target_id": target_id, "source_ref": ref, "payload": finding})

    chain_dir = source_ws.log_path("chain_res")
    if chain_dir.is_dir():
        for source in sorted(chain_dir.glob("*.json")):
            payload = _read_json(source)
            if not isinstance(payload, dict) or payload.get("outcome_type") != "chain_finding":
                continue
            finding = payload.get("finding")
            if not isinstance(finding, dict):
                continue
            local_id = str(finding.get("chain_id") or source.stem)
            if active_chain_ids is not None and local_id not in active_chain_ids:
                continue
            destination = target_root / "chain_res" / source.name
            hashes[str(destination.relative_to(gather_ws.base))] = _copy_artifact(source, destination)
            ref = source_ref(
                target_id=target_id,
                source_ws=source_ws,
                artifact_kind="chain_res",
                snapshot_path=destination,
                snapshot_base=gather_ws.base,
                local_id=local_id,
                payload=finding,
                revision=revision,
                json_pointer="/finding",
            )
            ref["legacy_activity_unverified"] = active_chain_ids is None
            unit = unit_from_chain(finding, target_id=target_id, source_ref_value=ref)
            merge_evidence_unit(units_by_id, unit, source_name=spec["name"])

    if not units_by_id:
        raise ValueError(f"gather target {spec['name']!r} has no usable chain evidence")
    target: GatherTarget = {
        "target_id": target_id,
        "name": spec["name"],
        "role": spec.get("role", ""),
        "workspace_path": str(source_base),
        "agent_config_path": str(source_config_path),
        "source_scan_mode": str(
            prior_state.get("scan_mode") or workspace_meta.get("scan_mode") or "full"
        ),
        "source_revision": source_revision,
        "source_common_focus": str(source_context.get("common_focus") or ""),
        "source_roots": snapshot_roots,
        "original_source_roots": {
            repo_id: str(path.resolve()) for repo_id, path in original_roots
        },
        "snapshot_root": str(target_root),
        "artifact_hashes": hashes,
    }
    return target, list(units_by_id.values()), context_only


def prepare_gather_state(
    manifest: dict[str, Any],
    *,
    workspace_root: str | Path,
    task_id: str | None = None,
    role_lang: str = "en",
    agent_configs: dict[str, dict[str, Any]] | None = None,
    common_focus: str = "",
    top_K: dict[str, int] | None = None,
    gather_config: dict[str, Any] | None = None,
    min_critic_skills: int = 2,
) -> GatherState:
    """Create a gather workspace and materialize its immutable evidence snapshot."""
    scenario_name = str(manifest.get("name") or "gather").strip()
    ws = Workspace.create(
        workspace_root,
        target=f"gather-{scenario_name}",
        task_id=task_id,
        role_lang=role_lang,
    )
    for directory in (
        ws.base / "inputs",
        ws.log / "gather_chain_res",
        ws.log / "gather_chain_candidates",
    ):
        directory.mkdir(parents=True, exist_ok=True)

    manifest_path = Path(str(manifest["manifest_path"]))
    shutil.copy2(manifest_path, ws.base / "gather_manifest.yaml")
    normalized_path = ws.base / "inputs" / "manifest.normalized.json"
    _write_json_atomic(normalized_path, manifest)

    targets: list[GatherTarget] = []
    evidence: list[GatherEvidenceUnit] = []
    context_only: list[dict[str, Any]] = []
    for target_spec in manifest["targets"]:
        target, target_evidence, target_context = _snapshot_target(ws, target_spec)
        targets.append(target)
        evidence.extend(target_evidence)
        context_only.extend(target_context)

    evidence.sort(key=lambda item: str(item.get("unit_id") or ""))
    evidence_path = ws.state_path("gather_evidence_pool.json")
    _write_json_atomic(
        evidence_path,
        {
            "schema_version": "1.0",
            "unit_count": len(evidence),
            "units": evidence,
            "context_only": context_only,
        },
    )
    manifest_hash = _sha256_file(normalized_path)
    lock = {
        "schema_version": "1.0",
        "manifest_hash": manifest_hash,
        "targets": [
            {
                "target_id": target["target_id"],
                "workspace_path": target["workspace_path"],
                "agent_config_path": target["agent_config_path"],
                "source_revision": target["source_revision"],
                "artifact_hashes": target["artifact_hashes"],
            }
            for target in targets
        ],
    }
    lock_path = ws.base / "inputs" / "gather_inputs.lock.json"
    _write_json_atomic(lock_path, lock)
    lock_hash = _sha256_file(lock_path)
    ws.meta.update(
        {
            "scan_mode": "gather",
            "scenario_name": scenario_name,
            "manifest_path": str(manifest_path),
            "manifest_hash": manifest_hash,
            "input_lock_path": str(lock_path),
            "input_lock_hash": lock_hash,
            "source_targets": [target["target_id"] for target in targets],
        }
    )
    ws._save_meta()
    return {
        "scan_mode": "gather",
        "target": f"gather:{scenario_name}",
        "scenario_name": scenario_name,
        "scenario": str(manifest["scenario"]),
        "manifest_path": str(manifest_path),
        "manifest_hash": manifest_hash,
        "task_id": ws.task_id,
        "workspace_root": str(ws.root),
        "role_lang": role_lang,
        "gather_targets": targets,
        "source_read_roots": [root for target in targets for root in target.get("source_roots", [])],
        "input_lock_path": str(lock_path),
        "input_lock_hash": lock_hash,
        "agent_configs": dict(agent_configs or {}),
        "agent_config_task_types": {},
        "common_focus": common_focus,
        "min_critic_skills": min_critic_skills,
        "top_K": dict(top_K or {}),
        "gather_config": dict(gather_config or {}),
        "gather_evidence_pool": evidence,
        "gather_evidence_pool_path": str(evidence_path),
        "gather_chain_candidates": [],
        "gather_chain_findings": [],
        "errors": [],
    }


def source_drift_errors(state: GatherState) -> list[str]:
    """Return source-repository fingerprint changes since gather preflight."""
    errors: list[str] = []
    for target in state.get("gather_targets") or []:
        recorded = target.get("source_revision") or {}
        original_roots = target.get("original_source_roots") or {}
        for repo_id, path in original_roots.items():
            current = _git_fingerprint(Path(path))
            before = recorded.get(repo_id) or {}
            if current != {
                "git_head": before.get("git_head", ""),
                "git_dirty": bool(before.get("git_dirty")),
                "git_status_sha256": before.get("git_status_sha256", ""),
                **(
                    {"tree_sha256": before.get("tree_sha256", "")}
                    if "tree_sha256" in before
                    else {}
                ),
            }:
                errors.append(f"source_drift:{target.get('target_id')}:{repo_id}")
    return errors


__all__ = [
    "GATHER_MANIFEST_VERSION",
    "load_gather_manifest",
    "prepare_gather_state",
    "source_drift_errors",
]
