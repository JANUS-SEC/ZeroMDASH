"""Run-scoped human recovery after a node exhausts automatic attempts.

LangChain copies ContextVars into its worker threads. Each worker therefore
sees the same coordinator, without putting locks or callbacks in graph state.
The outermost decorated call owns recovery; nested invocations finish their
normal retries and artifact validation before human input can be requested.
"""

from __future__ import annotations

import copy
import inspect
import json
import os
import sys
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import contextmanager
from contextvars import ContextVar, copy_context
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from queue import Empty, Queue
from typing import Any, Callable

from zeromdash.workspace import Workspace

from .config import agent_config_variants_for_node, canonical_node_name


class RuntimeRecoveryAborted(RuntimeError):
    """The operator could not supply a replacement; stop the run."""


@dataclass(frozen=True)
class RecoveryRequest:
    node: str
    subtask_id: str
    current: dict[str, Any]
    failure: str
    log_dir: Path


class RuntimeRecovery:
    def __init__(self, request_config: Callable[[RecoveryRequest], dict[str, Any]]):
        self.request_config = request_config
        self.console_lock = threading.RLock()
        self._state_lock = threading.Lock()
        self._overrides: dict[str, tuple[int, dict[str, Any]]] = {}
        self._aborted = ""
        self._requests: Queue | None = None
        self._pending: set[Future] = set()

    def run(self, operation: Callable[[], Any]) -> Any:
        """Run the graph in a worker; service terminal input on this thread."""
        self._requests = Queue()
        try:
            with runtime_recovery_scope(self), ThreadPoolExecutor(max_workers=1) as pool:
                work = pool.submit(copy_context().run, operation)
                try:
                    while not work.done():
                        try:
                            request, revision, reply = self._requests.get(timeout=0.1)
                        except Empty:
                            continue
                        if reply.done():
                            continue
                        try:
                            self._recover(request, revision)
                        except RuntimeRecoveryAborted as exc:
                            self.abort(str(exc))
                        else:
                            reply.set_result(None)
                        finally:
                            with self._state_lock:
                                self._pending.discard(reply)
                    self.snapshot("")  # A swallowed worker exception must not turn cancellation into success.
                    return work.result()
                except BaseException as exc:
                    # Wake every queued requester before the executor joins.
                    self.abort(str(exc) or "runtime recovery cancelled")
                    raise
        finally:
            self._requests = None

    def abort(self, message: str) -> None:
        with self._state_lock:
            self._aborted = self._aborted or message
            pending = list(self._pending)
            self._pending.clear()
        for reply in pending:
            if not reply.done():
                reply.set_exception(RuntimeRecoveryAborted(self._aborted))

    def snapshot(self, node: str) -> tuple[int, dict[str, Any] | None]:
        with self._state_lock:
            if self._aborted:
                raise RuntimeRecoveryAborted(self._aborted)
            revision, config = self._overrides.get(node, (0, None))
            return revision, copy.deepcopy(config)

    def recover(self, request: RecoveryRequest, revision: int) -> None:
        if self._requests is None:
            return self._recover(request, revision)
        reply: Future = Future()
        with self._state_lock:
            if self._aborted:
                raise RuntimeRecoveryAborted(self._aborted)
            self._pending.add(reply)
            self._requests.put((request, revision, reply))
        reply.result()

    def _recover(self, request: RecoveryRequest, revision: int) -> None:
        # No state lock is held while waiting for terminal input/health checks.
        # Other workers may finish, and only one callback owns the terminal.
        with self.console_lock:
            current_revision, _ = self.snapshot(request.node)
            if current_revision != revision:
                return  # Another failed worker has already replaced this config.
            try:
                config = copy.deepcopy(self.request_config(request))
                config.pop("fallbacks", None)
                self._record(request, "configured", revision + 1, config)
            except BaseException as exc:
                # Cancellation is shared so every waiter stops without prompting.
                message = (
                    f"Runtime recovery stopped for {request.node}"
                    f"/{request.subtask_id or '-'}: {exc or type(exc).__name__}. "
                    f"Existing artifacts are under {request.log_dir.parent}."
                )
                with self._state_lock:
                    self._aborted = message
                raise RuntimeRecoveryAborted(message) from exc
            with self._state_lock:
                self._overrides[request.node] = (revision + 1, config)

    @staticmethod
    def _record(request: RecoveryRequest, event: str, revision: int, config: dict) -> None:
        request.log_dir.mkdir(parents=True, exist_ok=True)
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "node": request.node,
            "subtask_id": request.subtask_id,
            "event": event,
            "revision": revision,
            # Do not persist env/credentials from the selected runtime here.
            "config": {key: config.get(key, "") for key in ("runtime", "config", "provider", "model")},
        }
        with (request.log_dir / "runtime_recovery.jsonl").open("a") as fp:
            fp.write(json.dumps(record, ensure_ascii=False) + "\n")

    def overrides(self) -> dict[str, dict[str, Any]]:
        with self._state_lock:
            return {node: copy.deepcopy(config) for node, (_, config) in self._overrides.items()}


_runtime_recovery: ContextVar[RuntimeRecovery | None] = ContextVar("runtime_recovery", default=None)
_recovery_owner: ContextVar[bool] = ContextVar("recovery_owner", default=False)
_recovery_round: ContextVar[int] = ContextVar("recovery_round", default=0)


@contextmanager
def runtime_recovery_scope(coordinator: RuntimeRecovery):
    token = _runtime_recovery.set(coordinator)
    try:
        yield coordinator
    finally:
        _runtime_recovery.reset(token)


@contextmanager
def runtime_console():
    coordinator = _runtime_recovery.get()
    if coordinator is None:
        yield
    else:
        with coordinator.console_lock:
            yield


def recovery_round() -> int:
    return _recovery_round.get()


def check_runtime_cancelled() -> None:
    coordinator = _runtime_recovery.get()
    if coordinator is not None:
        coordinator.snapshot("")


def invocation_failure(result) -> str:
    if isinstance(result, tuple):
        return "; ".join(result[1])
    if result.ok:
        return ""
    return f"backend={result.backend} rc={result.returncode}: {result.stderr or result.stdout or '(no output)'}"


def node_runtime_failure(update: dict) -> str:
    errors = list(update.get("errors") or [])
    review = update.get("review") or update.get("chain_review") or {}
    errors.extend(review.get("batch_contract_errors") or [])
    if review.get("output_validation_error"):
        errors.append(review["output_validation_error"])
    elif review.get("invalid_review_shape") or ("raw" in review and not review.get("reasoning")):
        errors.append("critic output is not a valid review JSON object")
    elif review and str(review.get("verdict") or "").lower() not in {"confirm", "reject", "revise"}:
        errors.append("critic verdict must be confirm, reject or revise")
    # A valid critic revise/reject is a business result, not a runtime failure.
    return "; ".join(errors)


def recover_runtime(*, node: str | None = None, failure=invocation_failure):
    """Wrap a complete automatic retry/fallback cycle, preserving its signature.

    Both invocation helpers (ws/node/agent_configs) and node functions (state)
    are supported. Config replacement affects only call-local copies; shared
    LangGraph input and the YAML configuration are never mutated by workers.
    """
    def decorate(fn):
        signature = inspect.signature(fn)

        @wraps(fn)
        def wrapped(*args, **kwargs):
            coordinator = _runtime_recovery.get()
            if coordinator is None or _recovery_owner.get():
                return fn(*args, **kwargs)
            original = signature.bind(*args, **kwargs)
            original.apply_defaults()
            name = canonical_node_name(node or original.arguments["node"])
            state = original.arguments.get("state") or {}
            configs = state.get("agent_configs", original.arguments.get("agent_configs"))
            backends = original.arguments.get("backends")
            ws = original.arguments.get("ws")
            if ws is None:
                ws = Workspace.open(state["workspace_root"], state["task_id"])
            task = (
                original.arguments.get("subtask_id")
                or (state.get("subtask") or {}).get("id")
                or (state.get("chain_candidate") or {}).get("chain_id")
                or (original.arguments.get("candidate") or {}).get("chain_id")
                or ""
            )
            selected_dir = (
                state.get("selected_subtask_log_dir") or state.get("selected_subagent_log_dir")
                or state.get("selected_chain_log_dir")
                or (original.arguments.get("extra_context") or {}).get("_command_log_dir")
            )
            log_dir = Path(selected_dir) if selected_dir else ws.log
            attempt_round = 0
            owner_token = _recovery_owner.set(True)
            try:
                while True:
                    revision, override = coordinator.snapshot(name)
                    call = signature.bind(*args, **kwargs)
                    call.apply_defaults()
                    selected_configs = copy.deepcopy(configs or {})
                    selected_backends = dict(backends or {})
                    if override is not None:
                        selected_configs[name] = override
                        selected_backends[name] = override["runtime"]
                    if "state" in call.arguments:
                        call.arguments["state"] = {**state, "agent_configs": selected_configs}
                    else:
                        call.arguments["agent_configs"] = selected_configs
                    call.arguments["backends"] = selected_backends
                    round_token = _recovery_round.set(attempt_round)
                    try:
                        result = fn(*call.args, **call.kwargs)
                    finally:
                        _recovery_round.reset(round_token)
                    detail = failure(result)
                    if not detail:
                        return result
                    if os.environ.get("ZEROMDASH_NONINTERACTIVE", "").strip() == "1":
                        # Unattended/batch runs must never block on (or die from)
                        # the interactive recovery prompt. Keep the recorded
                        # failure so callers can finish this finding/subtask and
                        # continue with the remaining work.
                        with runtime_console():
                            sys.stderr.write(
                                f"Runtime recovery skipped (ZEROMDASH_NONINTERACTIVE=1): "
                                f"node={name} subtask={task or '-'}; returning the recorded "
                                f"failure so the workflow can continue: {detail}\n"
                            )
                            sys.stderr.flush()
                        return result
                    current = agent_config_variants_for_node(name, selected_backends, selected_configs)[-1]
                    # Focus belongs to the node, even when the failed fallback
                    # configuration did not repeat it.
                    if "focus" in selected_configs.get(name, {}):
                        current["focus"] = selected_configs[name]["focus"]
                    coordinator.recover(RecoveryRequest(name, str(task), current, detail, log_dir), revision)
                    attempt_round += 1
            finally:
                _recovery_owner.reset(owner_token)

        return wrapped
    return decorate
