# tests/test_atomic.py
"""Tests for copilot/atomic.py — crash-safe file I/O and STATE.toml helpers."""

import json
import os
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

import pytest


# ---------------------------------------------------------------------------
# write_atomic
# ---------------------------------------------------------------------------

def test_write_atomic_creates_file(tmp_path):
    from copilot.atomic import write_atomic
    target = tmp_path / "output.txt"
    write_atomic(target, "hello world")
    assert target.read_text(encoding="utf-8") == "hello world"


def test_write_atomic_overwrites_existing(tmp_path):
    from copilot.atomic import write_atomic
    target = tmp_path / "data.txt"
    target.write_text("old content", encoding="utf-8")
    write_atomic(target, "new content")
    assert target.read_text(encoding="utf-8") == "new content"


def test_write_atomic_no_tmp_file_left_behind(tmp_path):
    from copilot.atomic import write_atomic
    target = tmp_path / "clean.txt"
    write_atomic(target, "data")
    # No .tmp sibling should remain
    tmp_files = list(tmp_path.glob("*.tmp"))
    assert tmp_files == [], f"Unexpected .tmp files: {tmp_files}"


def test_write_atomic_creates_missing_parent_dirs(tmp_path):
    """write_atomic must create absent parent directories (council fix):
    a KB page targeting a not-yet-created subdir (e.g. kb/careers/exobiology/)
    must not crash with FileNotFoundError."""
    from copilot.atomic import write_atomic
    target = tmp_path / "kb" / "careers" / "exobiology" / "page.md"
    assert not target.parent.exists()
    write_atomic(target, "content")
    assert target.read_text(encoding="utf-8") == "content"
    # No .tmp left behind in the freshly-created dir
    assert list(target.parent.glob("*.tmp")) == []


def test_write_atomic_crash_safety(tmp_path):
    """If os.replace fails (simulated), the original file must be intact."""
    from copilot.atomic import write_atomic

    target = tmp_path / "important.txt"
    original_content = "original safe content"
    target.write_text(original_content, encoding="utf-8")

    # Simulate os.replace raising an OSError (e.g., cross-device or permission)
    with patch("os.replace", side_effect=OSError("simulated failure")):
        with pytest.raises(OSError, match="simulated failure"):
            write_atomic(target, "corrupting write")

    # Original must be untouched
    assert target.read_text(encoding="utf-8") == original_content


# ---------------------------------------------------------------------------
# write_json_atomic
# ---------------------------------------------------------------------------

def test_write_json_atomic_round_trips(tmp_path):
    from copilot.atomic import write_json_atomic
    target = tmp_path / "data.json"
    obj = {"key": "value", "nums": [1, 2, 3], "nested": {"a": True}}
    write_json_atomic(target, obj)
    loaded = json.loads(target.read_text(encoding="utf-8"))
    assert loaded == obj


def test_write_json_atomic_utf8(tmp_path):
    from copilot.atomic import write_json_atomic
    target = tmp_path / "unicode.json"
    obj = {"cmdr": "Duvrazh", "note": "credits: 3×10⁹"}
    write_json_atomic(target, obj)
    loaded = json.loads(target.read_text(encoding="utf-8"))
    assert loaded["note"] == obj["note"]


# ---------------------------------------------------------------------------
# read_state / write_state
# ---------------------------------------------------------------------------

def test_read_state_returns_dict():
    from copilot.atomic import read_state
    state = read_state()
    assert isinstance(state, dict)


def test_read_state_has_required_keys():
    from copilot.atomic import read_state
    state = read_state()
    for key in ("loop_number", "last_completed_phase", "mode",
                "consecutive_empty_loops", "halt", "updated_at"):
        assert key in state, f"Missing STATE.toml key: {key}"


def test_write_state_stamps_updated_at(tmp_path, monkeypatch):
    """write_state must set updated_at to the current UTC ISO timestamp."""
    from copilot import atomic

    # Redirect STATE.toml to a temp file
    fake_state = tmp_path / "STATE.toml"
    fake_state.write_text(
        'loop_number = 0\nlast_completed_phase = "none"\nmode = "search"\n'
        'consecutive_empty_loops = 0\nhalt = false\nupdated_at = ""\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(atomic, "_state_path", lambda: fake_state)

    before = time.time()
    state_dict = {
        "loop_number": 1,
        "last_completed_phase": "triage",
        "mode": "search",
        "consecutive_empty_loops": 0,
        "halt": False,
        "updated_at": "",  # write_state must overwrite this
    }
    atomic.write_state(state_dict)

    import tomllib
    written = tomllib.loads(fake_state.read_text(encoding="utf-8"))
    assert written["updated_at"] != "", "updated_at must be non-empty after write_state"
    # Must be a parseable ISO 8601 string
    from datetime import datetime, timezone
    dt = datetime.fromisoformat(written["updated_at"])
    assert dt.tzinfo is not None, "updated_at must be timezone-aware"
    assert dt.timestamp() >= before


def test_write_state_is_atomic(tmp_path, monkeypatch):
    """Verify write_state calls write_atomic (not a bare open)."""
    from copilot import atomic

    fake_state = tmp_path / "STATE.toml"
    fake_state.write_text(
        'loop_number = 0\nlast_completed_phase = "none"\nmode = "search"\n'
        'consecutive_empty_loops = 0\nhalt = false\nupdated_at = ""\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(atomic, "_state_path", lambda: fake_state)

    calls = []
    original_write_atomic = atomic.write_atomic

    def spy_write_atomic(path, data):
        calls.append(path)
        return original_write_atomic(path, data)

    monkeypatch.setattr(atomic, "write_atomic", spy_write_atomic)

    atomic.write_state({"loop_number": 0, "last_completed_phase": "none",
                        "mode": "search", "consecutive_empty_loops": 0,
                        "halt": False, "updated_at": ""})

    assert len(calls) >= 1, "write_state must delegate to write_atomic"
