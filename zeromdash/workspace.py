"""Workspace manager.

Layout per task (rooted at the user-supplied `--workspace-root`):

    <root>/workspace_for_<sanitized_target>[__<task_id>]/
        main/
            repo/             # 目标软件源码
            repos/            # 多仓库目标的逐仓库源码
            scope/            # full/diff scan scope 与 change artifacts
            spec/             # 相关标准 (RFC, 社区共识)
            feature/          # 新/弱覆盖 feature surface
            attack_surface/   # 数据流 / 攻击面分析
            writeup/          # 目标软件经典历史漏洞
            patch/            # 对应 patch
        similar/
            <similar_software_slug>/
                repo/
                writeup/
                patch/
            ...
        log/
            review_log/       # critic reviewer 全过程日志
            state/            # workflow 结构化状态与计划
            subtask_res/      # 每个 subtask 的终态结果
        sub_workspace/        # 每次 agent 调用的 cwd（拷入 presets）
            node_<node_name>/                          # 单 agent 节点
                selected runtime files + common skills/contracts
            node_<node_name>/subtask_<id>/             # 每个 fan-out subtask
                selected runtime files + common skills/contracts
        workspace.json         # task 元信息
"""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from zeromdash import presets

# Sub-directory schema. Keep in sync with the green boxes in the design diagram.
MAIN_SUBDIRS: tuple[str, ...] = (
    "repo",
    "repos",
    "scope",
    "spec",
    "feature",
    "attack_surface",
    "writeup",
    "patch",
)
# Per-similar-software subdirs (created lazily under similar/<slug>/).
SIMILAR_SUBDIRS: tuple[str, ...] = (
    "repo",
    "writeup",
    "patch",
)
LOG_SUBDIRS: tuple[str, ...] = (
    "review_log",
    "state",
    "subtask_res",
    "primitive_res",
    "chain_res",
    "chain_candidates",
    "poc_res",
)


def slugify(s: str, fallback: str = "unknown") -> str:
    """Make `s` filesystem-safe: keep [A-Za-z0-9_.-], collapse the rest to '_'."""
    s = (s or "").strip()
    s = re.sub(r"[^A-Za-z0-9_.\-]+", "_", s)
    s = s.strip("._-")
    return s.lower() or fallback


@dataclass
class Workspace:
    """Filesystem workspace for a single ZeroMDASH task."""

    root: Path
    task_id: str            # 实际的子目录名，例如 "workspace_for_libfoo" 或 "workspace_for_libfoo__20260101"
    target: str = ""        # 原始目标软件名（保留特殊字符前的形式）
    role_lang: str = "en"   # roles/{role_lang}/ 下的本地化 role 卡；默认英文
    meta: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------ paths
    @property
    def base(self) -> Path:
        return self.root / self.task_id

    @property
    def main(self) -> Path:
        return self.base / "main"

    @property
    def similar(self) -> Path:
        return self.base / "similar"

    @property
    def log(self) -> Path:
        return self.base / "log"

    @property
    def sub_workspace_root(self) -> Path:
        return self.base / "sub_workspace"

    def main_path(self, sub: str) -> Path:
        return self.main / sub

    def log_path(self, sub: str) -> Path:
        return self.log / sub

    def state_path(self, name: str) -> Path:
        """Return the canonical path for a structured workflow state artifact."""
        return self.log_path("state") / name

    def resolve_state_path(self, name: str) -> Path:
        """Resolve a state artifact, falling back to the pre-state-dir layout."""
        canonical = self.state_path(name)
        if canonical.is_file():
            return canonical
        legacy = self.log_path("review_log") / name
        return legacy if legacy.is_file() else canonical

    def subtask_result_dirs(self) -> tuple[Path, ...]:
        """Return existing result dirs, ordered legacy-first for overlay reads."""
        return tuple(
            path
            for path in (self.log_path("review_res"), self.log_path("subtask_res"))
            if path.is_dir()
        )

    def subtask_result_files(self) -> list[Path]:
        """Return merged results, preferring canonical files over legacy namesakes."""
        by_name: dict[str, Path] = {}
        for result_dir in self.subtask_result_dirs():
            by_name.update(
                {path.name: path for path in sorted(result_dir.glob("*.json"))}
            )
        return [by_name[name] for name in sorted(by_name)]

    def similar_for(self, software: str) -> Path:
        """Return (and lazily create) `similar/<sw_slug>/` for one similar software."""
        d = self.similar / slugify(software)
        for sub in SIMILAR_SUBDIRS:
            (d / sub).mkdir(parents=True, exist_ok=True)
        return d

    def path(self, section: str, sub: str) -> Path:
        """Return path for a (section, sub) pair.

        Examples:
            ws.path("main", "spec")          -> <base>/main/spec
            ws.path("log",  "review_log")    -> <base>/log/review_log
            ws.path("similar", "<sw>/repo")  -> <base>/similar/<sw>/repo
        """
        if section == "main":
            return self.main / sub
        if section == "log":
            return self.log / sub
        if section == "similar":
            return self.similar / sub
        raise ValueError(f"unknown section: {section!r}")

    # ---------------------------------------------------------------- factory
    @classmethod
    def create(
        cls,
        root: str | Path,
        target: str,
        task_id: str | None = None,
        role_lang: str = "en",
    ) -> "Workspace":
        root = Path(root).expanduser().resolve()
        slug = slugify(target)
        if task_id:
            folder = f"workspace_for_{slug}__{slugify(task_id)}"
        else:
            folder = f"workspace_for_{slug}"
            # 已存在则追加时间戳，避免覆盖之前的任务
            if (root / folder).exists():
                folder = f"workspace_for_{slug}__" + datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        ws = cls(root=root, task_id=folder, target=target, role_lang=role_lang, meta={"target": target, "role_lang": role_lang})
        ws._materialize()
        ws._save_meta()
        return ws

    @classmethod
    def open(cls, root: str | Path, task_id: str) -> "Workspace":
        root = Path(root).expanduser().resolve()
        ws = cls(root=root, task_id=task_id)
        meta_file = ws.base / "workspace.json"
        if meta_file.exists():
            ws.meta = json.loads(meta_file.read_text())
            ws.target = ws.meta.get("target", "")
            ws.role_lang = ws.meta.get("role_lang", "en")
        return ws

    # --------------------------------------------------------------- internal
    def _materialize(self) -> None:
        for sub in MAIN_SUBDIRS:
            (self.main / sub).mkdir(parents=True, exist_ok=True)
        self.similar.mkdir(parents=True, exist_ok=True)  # 内部再按软件名建子目录
        for sub in LOG_SUBDIRS:
            (self.log / sub).mkdir(parents=True, exist_ok=True)
        self.sub_workspace_root.mkdir(parents=True, exist_ok=True)

    def _save_meta(self) -> None:
        meta = {
            "task_id": self.task_id,
            "target": self.target,
            "role_lang": self.role_lang,
            "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            **{k: v for k, v in self.meta.items() if k not in ("task_id", "target", "role_lang")},
        }
        (self.base / "workspace.json").write_text(json.dumps(meta, indent=2))

    # ------------------------------------------------------- sub_workspace
    def prepare_sub_workspace(
        self,
        node: str,
        subtask_id: str | None = None,
        backend: str | None = None,
        extra_context: dict[str, Any] | None = None,
        presets_dir: str | Path | None = None,
    ) -> Path:
        """Materialize a per-invocation sub_workspace on disk.

        Layout:
            <base>/sub_workspace/node_<node>[/subtask_<id>]/
                selected runtime files, skills/, output.schema.json, ...

        Presets are rendered with str.format using the context below so they
        can reference {workspace_base}, {main}, {similar}, {log}, {sub_workspace},
        {node}, {subtask_id}, {target}, {backend}.
        """
        if subtask_id:
            d = self.sub_workspace_root / f"node_{node}" / f"subtask_{slugify(subtask_id)}"
        else:
            d = self.sub_workspace_root / f"node_{node}"
        d.mkdir(parents=True, exist_ok=True)

        ctx: dict[str, Any] = {
            "workspace_base": str(self.base),
            "main": str(self.main),
            "similar": str(self.similar),
            "log": str(self.log),
            "sub_workspace": str(d),
            "node": node,
            "subtask_id": subtask_id or "",
            "target": self.target,
            "backend": backend or "",
            "role_lang": self.role_lang,
        }
        if extra_context:
            ctx.update(extra_context)

        presets.render_into(d, ctx=ctx, presets_dir=presets_dir)
        return d

    # ----------------------------------------------------------------- helpers
    def write_text(self, section: str, sub: str, name: str, content: str) -> Path:
        p = self.path(section, sub) / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return p

    def append_log(self, name: str, content: str) -> Path:
        p = self.log_path("review_log") / name
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a") as f:
            f.write(content.rstrip() + "\n")
        return p

    def clear(self) -> None:
        if self.base.exists():
            shutil.rmtree(self.base)
