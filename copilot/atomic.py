# copilot/atomic.py
"""Crash-safe file I/O and STATE.toml access.

All writes go through write_atomic: write to .tmp sibling → flush → fsync →
os.replace (atomic rename on POSIX and Windows NTFS). A crash between write
and replace leaves the original untouched.
"""

import json
import os
import threading
import tomllib
from datetime import datetime, timezone
from pathlib import Path

import tomli_w

# Per-process monotonic counter for unique tmp filenames — avoids AV-scanner
# collisions when multiple processes/threads write the same target path.
_tmp_counter_lock = threading.Lock()
_tmp_counter = 0


def _next_tmp(path: Path) -> Path:
    """Return a per-process-unique .tmp sibling path for *path*."""
    global _tmp_counter
    with _tmp_counter_lock:
        n = _tmp_counter
        _tmp_counter += 1
    pid = os.getpid()
    return path.with_suffix(f".{pid}.{n}.tmp")


def write_atomic(path: Path, data: str) -> None:
    """Write *data* (str, UTF-8) to *path* atomically via a .tmp sibling.

    Steps: mkdir parents → open .tmp → write → flush → fsync → os.replace.
    The temp file uses a per-process-unique name to prevent interference between
    concurrent processes (or an AV scanner touching a shared .tmp filename) even
    if two callers target the same destination.
    On Windows, os.replace can transiently fail with WinError 32 (file in use)
    or WinError 5 (access denied); we retry up to 20 times before giving up.
    If os.replace ultimately raises, the .tmp may remain but *path* is
    unmodified.
    """
    # Create the destination directory if missing — a KB page may target a
    # subdir (e.g. kb/careers/exobiology/) that has not been created yet.
    # Without this, open(.tmp) raises FileNotFoundError and crashes the loop.
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = _next_tmp(path)
    try:
        with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        # Retry loop for Windows AV / handle-release lag on os.replace.
        _replace_with_retry(tmp, path)
    except BaseException:
        # Clean up the tmp file on any failure so we don't litter.
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def _replace_with_retry(
    src: Path, dst: Path, *, retries: int = 20, delay: float = 0.005
) -> None:
    """Atomic rename, retrying on Windows WinError 32/5 (transient file locks)."""
    import errno as _errno
    import time as _time
    for attempt in range(retries):
        try:
            os.replace(src, dst)
            return
        except OSError as exc:
            winerr = getattr(exc, "winerror", 0)
            if winerr in (5, 32) or exc.errno in (_errno.EACCES, _errno.EBUSY):
                if attempt < retries - 1:
                    _time.sleep(delay)
                    continue
            raise


def write_json_atomic(path: Path, obj) -> None:
    """Serialise *obj* to JSON and write atomically to *path*.

    Uses ensure_ascii=False so Unicode characters survive the round-trip.
    """
    write_atomic(path, json.dumps(obj, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# STATE.toml helpers
# ---------------------------------------------------------------------------

def _state_path() -> Path:
    """Return the canonical path to STATE.toml (indirected for testability)."""
    from copilot.paths import repo_root
    return repo_root() / "STATE.toml"


def read_state() -> dict:
    """Parse STATE.toml and return it as a dict."""
    path = _state_path()
    with open(path, "rb") as fh:
        return tomllib.load(fh)


def write_state(state: dict) -> None:
    """Write *state* to STATE.toml atomically, stamping *updated_at* with now (UTC ISO 8601)."""
    # Stamp regardless of what the caller passed in
    state = dict(state)  # shallow copy; do not mutate caller's dict
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_atomic(_state_path(), tomli_w.dumps(state))
