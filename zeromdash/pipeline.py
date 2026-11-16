"""Bounded, run-scoped task pipelines shared by graph tasks and PoC jobs.

A slot belongs to a whole task, including its feedback/retry loop. Only
``slots`` futures are submitted at a time, and each completion admits the next
queued task without waiting for the rest of the active tasks.
"""

from __future__ import annotations

import json
import threading
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from contextvars import copy_context
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, TypeVar
from uuid import uuid4

from langchain_core.runnables import Runnable, RunnableConfig, RunnableLambda
from langgraph.types import Command

T = TypeVar("T")
R = TypeVar("R")
TASK_CONCURRENCY_KEYS = (
    "subtask_concurrency",
    "chain_subtask_concurrency",
    "poc_task_concurrency",
)


def task_slots(state: dict[str, Any], kind: str, config: RunnableConfig | None = None) -> int:
    value = (state.get("task_concurrency") or {}).get(f"{kind}_concurrency")
    if value is None:
        value = (config or {}).get("max_concurrency", 8)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{kind}_concurrency must be a positive integer")
    return value


class TaskPipeline:
    def __init__(self, slots: int, *, kind: str, log_dir: Path | None = None):
        if isinstance(slots, bool) or not isinstance(slots, int) or slots <= 0:
            raise ValueError("pipeline slots must be a positive integer")
        self.slots = slots
        self.kind = kind
        self.log_path = None
        self._log_lock = threading.Lock()
        if log_dir is not None:
            log_dir.mkdir(parents=True, exist_ok=True)
            self.log_path = log_dir / f"{kind}-{uuid4().hex}.jsonl"

    def _event(self, event: str, task_id: str, **details: Any) -> None:
        if self.log_path is not None:
            payload = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "pipeline": self.kind,
                "event": event,
                "task_id": task_id,
                "slots": self.slots,
                **details,
            }
            with self._log_lock, self.log_path.open("a") as stream:
                stream.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def run(
        self,
        tasks: Iterable[T],
        execute: Callable[[T], R],
        *,
        identify: Callable[[T], str] = str,
    ) -> list[R]:
        tasks = list(tasks)
        identifiers = [identify(task) for task in tasks]
        for task_id in identifiers:
            self._event("queued", task_id)
        results: dict[int, R] = {}

        def work(index: int) -> R:
            task_id = identifiers[index]
            self._event("started", task_id)
            try:
                result = execute(tasks[index])
            except BaseException as exc:
                self._event("failed", task_id, error_type=type(exc).__name__)
                raise
            self._event("finished", task_id)
            return result

        if not tasks:
            return []
        with ThreadPoolExecutor(max_workers=self.slots, thread_name_prefix=self.kind) as pool:
            pending = {}
            next_index = 0
            try:
                while next_index < len(tasks) or pending:
                    while next_index < len(tasks) and len(pending) < self.slots:
                        # Recovery coordination and tracing live in ContextVars.
                        future = pool.submit(copy_context().run, work, next_index)
                        pending[future] = next_index
                        next_index += 1
                    done, _ = wait(pending, return_when=FIRST_COMPLETED)
                    for future in done:
                        index = pending.pop(future)
                        results[index] = future.result()
            except BaseException:
                for future, index in pending.items():
                    if future.cancel():
                        self._event("cancelled", identifiers[index])
                for index in range(next_index, len(tasks)):
                    self._event("cancelled", identifiers[index])
                raise
        # Completion order must not change report ordering or reducer results.
        return [results[index] for index in range(len(tasks))]


def pipeline_log_dir(state: dict[str, Any]) -> Path | None:
    selected = state.get("selected_subtask_log_dir") or state.get("selected_chain_log_dir")
    if selected:
        return Path(selected) / "pipeline"
    if state.get("workspace_root") and state.get("task_id"):
        return Path(state["workspace_root"]) / state["task_id"] / "log" / "pipeline"
    return None


def task_pipeline_node(child_graph, dispatcher, *, kind: str, next_node: str):
    """Adapt existing Send selection to one bounded pipeline in the parent graph.

    Dispatchers retain ranking, restore filtering and empty-plan routing. Child
    output schemas restrict updates to additive result/error lists; scratch
    state never merges into the parent.
    """
    child_graph = child_graph if isinstance(child_graph, Runnable) else RunnableLambda(child_graph)

    def run(state: dict[str, Any], config: RunnableConfig) -> Command:
        dispatch = dispatcher(state)
        if isinstance(dispatch, str):
            return Command(goto=dispatch)
        pipeline = TaskPipeline(
            task_slots(state, kind, config), kind=kind, log_dir=pipeline_log_dir(state),
        )

        def identify(send) -> str:
            child = send.arg
            task = child.get("subtask") or child.get("chain_candidate") or child.get("gather_chain_candidate") or {}
            return str(task.get("id") or task.get("chain_id") or "")

        results = pipeline.run(
            dispatch, lambda send: child_graph.invoke(send.arg, config=config), identify=identify,
        )
        update: dict[str, list[Any]] = {}
        for result in results:
            for key, values in result.items():
                if not isinstance(values, list):
                    raise TypeError(f"pipeline output {key!r} must be an additive list")
                update.setdefault(key, []).extend(values)
        return Command(update=update, goto=next_node)

    return run
