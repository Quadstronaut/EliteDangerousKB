"""
scripts/reconcile_loop13_orphans.py — F2 remediation.

Loop 13 stranded three Coriolis sources: it recorded them in seen.json (PHASE 3
SUMMARIZE) and dropped sources/*.raw + summaries/*.md, then was killed before
PHASE 4 SYNTHESIZE wrote the kb pages. The result: three seen.json keys with no
committed page, STATE.toml frozen at last_completed_phase="summarize", and three
queue targets that dedup-against-seen will now silently skip forever.

This script makes loop 13 a clean no-op: it removes the three orphan keys so the
URLs are eligible for re-processing, deletes the orphan scratch files, resets the
STATE phase to "commit" (the next legal checkpoint, so the next loop starts a
fresh triage), and re-seeds the three targets into the queue.

Public callable:

    reconcile(repo_root=None, *, dry_run=False) -> dict

Every step is independently guarded; the summary dict is returned even on partial
failure, with the failure recorded in errors[]. When a repo_root is passed it is
threaded through EVERY step (including the STATE.toml write) — nothing touches the
live tree under a fixture root. dry_run computes the same summary without writing.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

# Make `copilot` importable when run as a bare script (python scripts/...).
_REPO_ROOT_GUESS = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT_GUESS) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT_GUESS))

from copilot.atomic import write_atomic, write_json_atomic  # noqa: E402
from copilot.locking import LockError, file_lock  # noqa: E402
from copilot.loop_state import _load_seen, _url_sha  # noqa: E402

import tomllib  # noqa: E402
import tomli_w  # noqa: E402


# ---------------------------------------------------------------------------
# The three loop-13 orphan targets. URLs are the SINGLE source of truth; keys
# are derived at runtime via _url_sha (never hardcoded — MC-2). The sha8
# prefixes are FILENAME prefixes for the scratch files only.
# ---------------------------------------------------------------------------

_CORIOLIS_BASE = "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal"

ORPHAN_TARGETS: list[dict] = [
    {
        "slug": "scb",
        "url": f"{_CORIOLIS_BASE}/shield_cell_bank.json",
        "sha8": "c1727ba4",
        "queue_note": "Shield Cell Bank -> kb/outfitting/shield-cell-bank.md. Index.js key scb.",
    },
    {
        "slug": "mrp",
        "url": f"{_CORIOLIS_BASE}/module_reinforcement_package.json",
        "sha8": "f7817a2f",
        "queue_note": "Module Reinforcement Package -> kb/outfitting/module-reinforcement.md. Index.js key mrp.",
    },
    {
        "slug": "mahr",
        "url": f"{_CORIOLIS_BASE}/meta_alloy_hull_reinforcement_package.json",
        "sha8": "7ae9d1f7",
        "queue_note": "Meta-Alloy HRP -> merge into kb/outfitting/hull-reinforcement.md OR new page. Index.js key mahr.",
    },
]


# ---------------------------------------------------------------------------
# repo_root resolution + containment
# ---------------------------------------------------------------------------

def _resolve_repo_root(repo_root: Optional[Path]) -> Path:
    if repo_root is not None:
        return Path(repo_root).resolve()
    from copilot.paths import repo_root as _live_repo_root
    return _live_repo_root().resolve()


def _contained(repo_root: Path, *parts: str) -> Path:
    """Join *parts* under repo_root, then assert the resolved result stays inside
    repo_root (MC-7). Rejects absolute parts and ../ traversal.

    Raises ValueError on any escape attempt — the caller's try/except records it
    in errors[] rather than letting a poisoned path touch the live tree.
    """
    candidate = repo_root.joinpath(*parts).resolve()
    try:
        candidate.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError(
            f"path escapes repo_root: {candidate} not under {repo_root}"
        ) from exc
    return candidate


def _orphan_keys() -> dict[str, str]:
    """Map full sha256 hexdigest -> slug, derived at runtime from the URLs."""
    return {_url_sha(t["url"]): t["slug"] for t in ORPHAN_TARGETS}


# ---------------------------------------------------------------------------
# Individual steps. Each returns its own partial summary; the orchestrator
# wraps each call in try/except so one failure never skips the others (MC-5).
# ---------------------------------------------------------------------------

def _step_seen(repo_root: Path, *, dry_run: bool) -> list[str]:
    """(a) Remove the 3 orphan keys from seen.json under the seen lock.

    Preserves every other entry byte-for-byte. Returns the slugs actually
    removed (idempotent: returns [] when none present). A lock timeout is
    raised to the caller, which records it in errors[] and continues with the
    other steps.
    """
    seen_path = _contained(repo_root, "indexes", "seen.json")
    key_to_slug = _orphan_keys()

    with file_lock(str(seen_path) + ".lock", timeout=30.0):
        data = _load_seen(str(seen_path))
        removed: list[str] = []
        for key, slug in key_to_slug.items():
            if key in data:
                removed.append(slug)
                if not dry_run:
                    del data[key]
        if removed and not dry_run:
            write_json_atomic(seen_path, data)
        return sorted(removed)


def _step_files(repo_root: Path, *, dry_run: bool) -> list[str]:
    """(b) Delete the 3 orphan sources/*.raw and summaries/*.md by sha8 prefix.

    Missing files are not an error (idempotent). Returns the repo-relative paths
    that were (or would be) deleted. Every path is containment-validated.
    """
    deleted: list[str] = []
    for t in ORPHAN_TARGETS:
        sha8 = t["sha8"]
        for sub in ("sources", "summaries"):
            base = _contained(repo_root, sub)
            if not base.exists():
                continue
            for hit in base.glob(f"{sha8}-*"):
                hit_resolved = hit.resolve()
                # Re-validate each glob hit stays inside repo_root.
                try:
                    hit_resolved.relative_to(repo_root)
                except ValueError:
                    continue
                deleted.append(str(hit_resolved.relative_to(repo_root)).replace("\\", "/"))
                if not dry_run:
                    hit_resolved.unlink(missing_ok=True)
    return sorted(deleted)


def _step_state(repo_root: Path, *, dry_run: bool) -> bool:
    """(c) Reset STATE.toml last_completed_phase 'summarize' -> 'commit' ONLY if
    it currently equals 'summarize'. Returns True iff a reset was applied.

    Writes via copilot.atomic (MC-10), targeting the PASSED repo_root (MC-3).
    """
    state_path = _contained(repo_root, "STATE.toml")
    if not state_path.exists():
        return False
    with open(state_path, "rb") as fh:
        state = tomllib.load(fh)
    if state.get("last_completed_phase") != "summarize":
        return False
    if not dry_run:
        state["last_completed_phase"] = "commit"
        # Stamp updated_at like copilot.atomic.write_state would, but target the
        # PASSED path (write_state() always writes the live STATE.toml).
        from datetime import datetime, timezone
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        write_atomic(state_path, tomli_w.dumps(state))
    return True


def _step_queue(repo_root: Path, *, dry_run: bool) -> list[str]:
    """(d) Ensure queue/next-targets.md lists the 3 targets, re-prepending any
    that loop-13 triage consumed.

    A target is "present" if its URL appears anywhere in the file. Missing ones
    are inserted as '- <url> (...)' bullets immediately before the FIRST existing
    '- ' bullet (so they sit at the top of the live target list even when the
    first content line is already a bullet — MC-4). If the file has no bullet at
    all, they are appended after the header prose.

    Returns the slugs that were (or would be) re-added.
    """
    queue_path = _contained(repo_root, "queue", "next-targets.md")
    if not queue_path.exists():
        # Nothing to reconcile against; create a minimal file with all targets.
        added = [t["slug"] for t in ORPHAN_TARGETS]
        if not dry_run:
            lines = ["# Research Queue — next targets", ""]
            lines += [f"- {t['url']} (tier: 0, type: coriolis, note: {t['queue_note']})"
                      for t in ORPHAN_TARGETS]
            write_atomic(queue_path, "\n".join(lines) + "\n")
        return sorted(added)

    text = queue_path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    missing = [t for t in ORPHAN_TARGETS if t["url"] not in text]
    if not missing:
        return []

    lines = text.split("\n")
    # Find the first '- ' bullet line (the top of the live target list).
    insert_at = None
    for i, ln in enumerate(lines):
        if ln.startswith("- "):
            insert_at = i
            break
    new_bullets = [
        f"- {t['url']} (tier: 0, type: coriolis, note: {t['queue_note']})"
        for t in missing
    ]
    if insert_at is None:
        # No bullets at all — append after the existing content.
        body = text.rstrip("\n")
        new_text = body + "\n" + "\n".join(new_bullets) + "\n"
    else:
        lines[insert_at:insert_at] = new_bullets
        new_text = "\n".join(lines)
        if not new_text.endswith("\n"):
            new_text += "\n"
    if not dry_run:
        write_atomic(queue_path, new_text)
    return sorted(t["slug"] for t in missing)


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def reconcile(repo_root: Optional[Path] = None, *, dry_run: bool = False) -> dict:
    """Reconcile the loop-13 orphan state. See module docstring.

    Returns:
        {
            "keys_removed":  list[str],   # slugs whose seen.json key was removed
            "files_deleted": list[str],   # repo-relative scratch paths deleted
            "state_reset":   bool,        # STATE.toml phase reset applied
            "queue_appended": list[str],  # slugs re-seeded into the queue
            "errors":        list[str],   # one per failed step (partial-failure)
        }

    Every step is independently try/except-guarded; a failure in one step records
    an error and the others still run (MC-5). When repo_root is passed, no step
    writes outside it (MC-3 / MC-7).
    """
    root = _resolve_repo_root(repo_root)
    summary: dict = {
        "keys_removed": [],
        "files_deleted": [],
        "state_reset": False,
        "queue_appended": [],
        "errors": [],
    }

    # (a) seen.json
    try:
        summary["keys_removed"] = _step_seen(root, dry_run=dry_run)
    except (LockError, TimeoutError, OSError, ValueError) as exc:
        summary["errors"].append(f"step-a (seen.json): {type(exc).__name__}: {exc}")

    # (b) orphan scratch files
    try:
        summary["files_deleted"] = _step_files(root, dry_run=dry_run)
    except (OSError, ValueError) as exc:
        summary["errors"].append(f"step-b (scratch files): {type(exc).__name__}: {exc}")

    # (c) STATE.toml phase reset
    try:
        summary["state_reset"] = _step_state(root, dry_run=dry_run)
    except (OSError, ValueError, tomllib.TOMLDecodeError) as exc:
        summary["errors"].append(f"step-c (STATE.toml): {type(exc).__name__}: {exc}")

    # (d) queue re-seed
    try:
        summary["queue_appended"] = _step_queue(root, dry_run=dry_run)
    except (OSError, ValueError) as exc:
        summary["errors"].append(f"step-d (queue): {type(exc).__name__}: {exc}")

    return summary


# ---------------------------------------------------------------------------
# CLI — runs against the live tree. Exit 0 on clean run, nonzero on any error.
# ---------------------------------------------------------------------------

def main(argv: Optional[list[str]] = None) -> int:
    import argparse
    import json as _json

    parser = argparse.ArgumentParser(
        description="Reconcile the loop-13 stranded-source orphan state."
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Compute the summary without writing any file.")
    args = parser.parse_args(argv)

    summary = reconcile(dry_run=args.dry_run)
    print(_json.dumps(summary, indent=2))
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
