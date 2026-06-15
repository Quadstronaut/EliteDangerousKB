"""
copilot/loop_state.py — Loop idempotency and phase management for the research daemon.

Imported by the research loop (via Python subprocess or direct import) and by wrapper.ps1
(via Python subprocess) to manage STATE.toml phase transitions and seen.json deduplication.
"""
from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from copilot.atomic import write_json_atomic
from copilot.locking import file_lock

# ---------------------------------------------------------------------------
# Phase ordering
# ---------------------------------------------------------------------------

PHASE_ORDER: list[str] = [
    "none",
    "triage",
    "search",
    "summarize",
    "synthesize",
    "verify",
    "index",
    "commit",
]


def advance_phase(current: str) -> str:
    """
    Return the next phase after `current`.

    "none" -> "triage" -> "search" -> "summarize" -> "synthesize" -> "index"
    -> "commit" -> "triage" (next loop).

    Raises ValueError for unknown phase names.
    """
    if current not in PHASE_ORDER:
        raise ValueError(f"Unknown phase: {current!r}. Expected one of {PHASE_ORDER}")
    # "commit" wraps back to "triage" (start of next loop), not "none".
    if current == "commit":
        return "triage"
    idx = PHASE_ORDER.index(current)
    return PHASE_ORDER[idx + 1]


# ---------------------------------------------------------------------------
# seen.json deduplication
# ---------------------------------------------------------------------------

def _url_sha(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def _load_seen(seen_path: str) -> dict:
    """Read seen.json, tolerant of the Windows NTFS delete-pending window.

    A concurrent atomic replace (write_json_atomic -> os.replace) can leave the
    file briefly openable-as-EACCES, or glimpsed half-written. Retry transient
    errors for ~100ms rather than crash a reader or lose data (the prior
    concurrency blocker surfaced here as a PermissionError on read)."""
    p = Path(seen_path)
    last_exc: Exception | None = None
    for _ in range(20):
        if not p.exists():
            return {}
        try:
            text = p.read_text(encoding="utf-8")
            return json.loads(text) if text.strip() else {}
        except (PermissionError, OSError, json.JSONDecodeError) as exc:
            last_exc = exc
            time.sleep(0.005)
    if last_exc:
        raise last_exc
    return {}


def is_resumable(
    url: str,
    seen_path: str,
    content_sha256: Optional[str] = None,
) -> bool:
    """
    Return True if the URL should be fetched/processed this loop.

    Returns False only when the URL has been seen before AND either:
      - no content_sha256 is provided (assume content unchanged), OR
      - the provided content_sha256 matches the stored one.

    True = ALLOW fetching (new, or content changed). False = SKIP (already done).
    """
    data = _load_seen(seen_path)
    key = _url_sha(url)
    if key not in data:
        return True  # never seen -> fetch
    stored_sha = data[key].get("content_sha256")
    if content_sha256 is None:
        return False  # seen, no content to compare -> assume unchanged -> skip
    return content_sha256 != stored_sha  # True = content changed -> re-fetch


def _seen_lock_path(seen_path: str) -> str:
    """Lock token path for a given seen.json — sibling '.lock' file."""
    return seen_path + ".lock"


def record_source(url: str, content_sha256: str, seen_path: str) -> None:
    """
    Record a URL + content hash in seen.json atomically.

    Preserves `first_seen` on subsequent updates; updates `content_sha256`.
    Creates seen.json if it does not exist.

    The ENTIRE load -> mutate -> write cycle runs under a cross-process file
    lock (Bug 1 fix).  Lock path is derived from seen_path so each seen.json
    has its own lock, and monkeypatched tmp_path tests stay isolated.
    """
    with file_lock(_seen_lock_path(seen_path), timeout=30.0):
        data = _load_seen(seen_path)
        key = _url_sha(url)
        now_iso = datetime.now(timezone.utc).isoformat()
        if key in data:
            # Preserve first_seen; update content hash only.
            data[key]["content_sha256"] = content_sha256
        else:
            data[key] = {
                "first_seen": now_iso,
                "content_sha256": content_sha256,
            }
        write_json_atomic(Path(seen_path), data)


# ---------------------------------------------------------------------------
# INARA rate-limit check
# ---------------------------------------------------------------------------

def check_inara_rate(state: dict) -> bool:
    """
    Return True if it is safe to fetch from INARA right now.

    Reads `inara_backoff_until` from the state dict. If it is set to a future
    ISO 8601 datetime, return False (still in backoff window). Empty/missing/
    unparseable -> True (safe).
    """
    raw = state.get("inara_backoff_until", "")
    if not raw:
        return True
    try:
        until_dt = datetime.fromisoformat(raw)
    except ValueError:
        return True  # unparseable -> assume safe
    now = datetime.now(timezone.utc)
    if until_dt.tzinfo is None:
        # naive -> assume UTC so the comparison is well-defined
        until_dt = until_dt.replace(tzinfo=timezone.utc)
    return now >= until_dt  # True = past the backoff window -> safe to fetch
