"""Single-host Linux commit adapter for synthetic Hearth fixtures.

All writers must cooperate through this gateway and the same stable lock file.
This is neither a Google Drive adapter nor a distributed lock or auth service.
"""
from __future__ import annotations

import copy
import errno
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
import time
from contextlib import contextmanager
from typing import Any

import hearth

STORE_SCHEMA = "HEARTH_LOCAL_COMMIT_STORE_V1"


class IdempotencyConflict(ValueError):
    """The request ID has already been bound to different content."""


class CorruptStore(ValueError):
    """The persisted snapshot cannot be trusted; never reset it automatically."""


class LockTimeout(TimeoutError):
    """The exclusive writer lock could not be acquired within the deadline."""


def _validate_json(value: Any) -> None:
    if value is None or type(value) in (str, bool, int):
        return
    if type(value) is float and math.isfinite(value):
        return
    if type(value) is list:
        for item in value:
            _validate_json(item)
        return
    if type(value) is dict and all(type(key) is str for key in value):
        for item in value.values():
            _validate_json(item)
        return
    raise ValueError("Only string-keyed JSON and finite numbers are supported")


def _encode(value: Any) -> bytes:
    _validate_json(value)
    return json.dumps(value, ensure_ascii=False, allow_nan=False,
                      sort_keys=True, separators=(",", ":")).encode("utf-8")


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_encode(value)).hexdigest()


def _freeze_request(request: dict) -> dict:
    if type(request) is not dict:
        raise ValueError("request must be an object")
    frozen = json.loads(_encode(request))
    request_id = frozen.get("request_id")
    if not isinstance(request_id, str) or not request_id.strip():
        raise ValueError("request_id must be a non-empty string")
    for key in ("schema", "action"):
        if not isinstance(frozen.get(key), str):
            raise ValueError(f"{key} must be a string")
    for key in ("payload", "agent"):
        if key in frozen and not isinstance(frozen[key], dict):
            raise ValueError(f"{key} must be an object")
    revision = frozen.get("expected_revision")
    if revision is not None and (type(revision) is not int or revision < 0):
        raise ValueError("expected_revision must be a nonnegative integer or null")
    return frozen


class LocalCommitGateway:
    """Atomically persist a state transition and its replayable result."""

    def __init__(self, directory: str | Path, session_id: str,
                 lock_timeout: float = 5.0):
        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("session_id must be a non-empty string")
        if (type(lock_timeout) not in (int, float)
                or not math.isfinite(lock_timeout) or lock_timeout < 0):
            raise ValueError("lock_timeout must be finite and nonnegative")
        self.directory = Path(directory).resolve()
        self.session_id = session_id
        self.lock_timeout = float(lock_timeout)
        self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.path = self.directory / "snapshot.json"
        with self._locked():
            if self.path.exists():
                self._load()
            else:
                self._save({"schema": STORE_SCHEMA, "session_id": session_id,
                            "state": hearth.default_state(session_id), "records": {}})

    @contextmanager
    def _locked(self):
        # Do not delete or replace this file: every writer must lock the same inode.
        fd = os.open(self.directory / "writer.lock", os.O_RDWR | os.O_CREAT, 0o600)
        acquired = False
        deadline = time.monotonic() + self.lock_timeout
        try:
            while True:
                try:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    acquired = True
                    break
                except OSError as exc:
                    if exc.errno not in (errno.EAGAIN, errno.EACCES):
                        raise
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise LockTimeout("Exclusive writer lock timed out") from exc
                    time.sleep(min(0.01, remaining))
            yield
        finally:
            if acquired:
                fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)

    def _load(self) -> dict:
        try:
            saved = json.loads(self.path.read_bytes())
            payload = saved["payload"]
            if saved["payload_sha256"] != _digest(payload):
                raise CorruptStore("Snapshot digest mismatch")
            if (payload["schema"] != STORE_SCHEMA
                    or payload["state"]["schema"] != hearth.STATE_SCHEMA
                    or not isinstance(payload["records"], dict)
                    or payload["state"]["session_id"] != payload["session_id"]):
                raise CorruptStore("Invalid snapshot structure")
        except (ValueError, KeyError, TypeError, UnicodeError) as exc:
            raise CorruptStore("Snapshot is corrupt; refusing to reset it") from exc
        if payload["session_id"] != self.session_id:
            raise ValueError("Existing store belongs to another session")
        return payload

    def _sync_directory(self) -> None:
        fd = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def _save(self, payload: dict) -> None:
        encoded = _encode({"payload": payload, "payload_sha256": _digest(payload)})
        fd, name = tempfile.mkstemp(prefix=".pending-", dir=self.directory)
        temporary = Path(name)
        try:
            with os.fdopen(fd, "wb") as output:
                output.write(encoded)
                output.flush()
                os.fsync(output.fileno())
            os.replace(temporary, self.path)
            self._sync_directory()
        finally:
            temporary.unlink(missing_ok=True)

    def snapshot(self) -> dict:
        with self._locked():
            return self._load()

    def submit(self, request: dict) -> dict:
        frozen = _freeze_request(request)
        request_id = frozen["request_id"]
        request_hash = _digest(frozen)
        with self._locked():
            payload = self._load()
            existing = payload["records"].get(request_id)
            if existing is not None:
                if existing["request_sha256"] != request_hash:
                    raise IdempotencyConflict("Request ID is bound to different content")
                # Resolve a prior uncertain acknowledgement after rename/fsync error.
                self._sync_directory()
                return {"replayed": True, "record": copy.deepcopy(existing)}
            after, response, receipt = hearth.apply_request(payload["state"], frozen)
            record = {
                "sequence": len(payload["records"]) + 1,
                "request_id": request_id,
                "request_sha256": request_hash,
                "outcome": receipt["status"],
                "response": response,
                "receipt": receipt,
                "state_sha256": _digest(after),
            }
            payload["state"] = after
            payload["records"][request_id] = record
            self._save(payload)
            return {"replayed": False, "record": copy.deepcopy(record)}
