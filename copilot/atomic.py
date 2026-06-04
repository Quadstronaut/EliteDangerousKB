# copilot/atomic.py
"""Crash-safe file I/O and STATE.toml access.

All writes go through write_atomic: write to .tmp sibling → flush → fsync →
os.replace (atomic rename on POSIX and Windows NTFS). A crash between write
and replace leaves the original untouched.
"""

import json
import os
import tomllib
from datetime import datetime, timezone
from pathlib import Path

import tomli_w


def write_atomic(path: Path, data: str) -> None:
    """Write *data* (str, UTF-8) to *path* atomically via a .tmp sibling.

    Steps: mkdir parents → open .tmp → write → flush → fsync → os.replace.
    If os.replace raises, the .tmp may remain but *path* is unmodified.
    """
    # Create the destination directory if missing — a KB page may target a
    # subdir (e.g. kb/careers/exobiology/) that has not been created yet.
    # Without this, open(.tmp) raises FileNotFoundError and crashes the loop.
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


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
