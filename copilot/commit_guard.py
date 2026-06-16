"""
copilot/commit_guard.py — F6 recurrence guard (ADDITIVE; no dedup/discard
semantics changed).

ROOT CAUSE (ed-research-prompt.md PHASE 3): record_source() ran in SUMMARIZE,
before PHASE 4 SYNTHESIZE writes the kb page. A kill between the two permanently
stranded the URL — seen.json says "done" (is_resumable -> False), but no page
exists, so the loop never revisits it and the fact is lost.

THE GUARD is a COMMIT-phase parity check, called at the end of a loop with the
URLs that were processed this loop. For each URL it asks, PER-URL (never by
comparing counts — MC-6):

  * Did a kb page get committed whose frontmatter source_url OR source_urls
    list includes this URL? -> OK.
  * Was this URL DISCARDED?  A discard is recorded via the structured
    `discarded: true` marker in seen.json (Goal B); it is intentionally
    page-less -> OK (discard-safe).
  * Otherwise the URL is STRANDED -> flag it.

URL-AWARE (per-URL, not count-based — MC-6) and discard-safe (MC-6).  All page/
journal/queue/seen paths derived from frontmatter or kb_dir are containment-
validated (resolve() then is_relative_to(kb) — MC-7); absolute / ../ paths are
rejected, never followed.

RECOVERY: recover_stranded_urls() is the safe live-path helper — it re-queues
stranded URLs, purges their seen entries, and logs to the journal, but NEVER
raises.  The live COMMIT phase calls this; assert_commit_parity (raising form)
is reserved for tests/operators and MUST NOT be called on the headless path.

MERGE-PAGE SUPPORT (Goal C): committed_source_urls() now reads both the
singular `source_url:` key AND the optional `source_urls: [u1, u2, ...]`
inline flow list.  The flow list must be on ONE line; block YAML sequences
(multi-line `- url`) are NOT supported by _parse_frontmatter and are not used.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Iterable, Optional

# Reuse the project's frontmatter parser so source_url is read exactly as the
# indexer reads it (no second, divergent YAML dialect).
from copilot.chunker import _parse_frontmatter


# ---------------------------------------------------------------------------
# Path helpers (all containment-validated — MC-7)
# ---------------------------------------------------------------------------

def _resolve_roots(
    repo_root: Optional[Path],
    kb_dir: Optional[Path],
    journal_dir: Optional[Path],
) -> tuple[Path, Path, Path]:
    if repo_root is not None:
        root = Path(repo_root).resolve()
    else:
        from copilot.paths import repo_root as _live_root
        root = _live_root().resolve()
    kb = Path(kb_dir).resolve() if kb_dir is not None else (root / "kb").resolve()
    journal = (
        Path(journal_dir).resolve() if journal_dir is not None else (root / "journal").resolve()
    )
    return root, kb, journal


def _is_contained(path: Path, container: Path) -> bool:
    """True iff *path* resolves inside *container* (rejects ../ and absolute escapes)."""
    try:
        path.resolve().relative_to(container.resolve())
        return True
    except (ValueError, OSError):
        return False


# ---------------------------------------------------------------------------
# Inline flow-list reader for `source_urls: [u1, u2, ...]`
# ---------------------------------------------------------------------------

# Matches a YAML inline flow sequence: `source_urls: [url1, url2]`
# Supports arbitrary whitespace inside the brackets; URLs may be quoted or bare.
_FLOW_LIST_RE = re.compile(r"source_urls\s*:\s*\[([^\]]*)\]", re.IGNORECASE)


def _parse_source_urls_flow(text: str) -> list[str]:
    """Extract URL strings from a `source_urls: [u1, u2, ...]` frontmatter line.

    Handles quoted or unquoted values separated by commas.  Returns an empty
    list when no matching line is found.  This is intentionally a minimalist
    parser: we only call it on the frontmatter block (a small, trusted string).
    """
    m = _FLOW_LIST_RE.search(text)
    if not m:
        return []
    inner = m.group(1)
    # Split on commas, strip whitespace and matched quotes.
    parts = []
    for item in inner.split(","):
        item = item.strip().strip('"').strip("'").strip()
        if item:
            parts.append(item)
    return parts


# ---------------------------------------------------------------------------
# Committed-page index: source_url -> kb page (URL-aware, per-URL — MC-6)
# ---------------------------------------------------------------------------

def committed_source_urls(
    *,
    repo_root: Optional[Path] = None,
    kb_dir: Optional[Path] = None,
) -> set[str]:
    """Return the set of source URLs that have a committed kb page.

    Scans every kb/**/*.md page's frontmatter.  Collects BOTH the singular
    `source_url:` value AND every entry in `source_urls: [u1, u2, ...]`
    (the merge-page back-fill for Goal C).  Single-source pages only need
    `source_url`; merged pages list additional contributing URLs in
    `source_urls`.

    URL-aware: we compare URLs, not page counts vs seen counts (MC-6).
    Containment-validated: pages outside kb_dir are skipped (MC-7).
    """
    _root, kb, _journal = _resolve_roots(repo_root, kb_dir, None)
    urls: set[str] = set()
    if not kb.exists():
        return urls
    for page in kb.rglob("*.md"):
        if not _is_contained(page, kb):
            continue
        try:
            text = page.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        meta, _body = _parse_frontmatter(text)
        # Primary source_url (every page has at most one).
        src = meta.get("source_url")
        if isinstance(src, str) and src:
            urls.add(src)
        # Additional contributing URLs for merged pages (Goal C).
        # _parse_frontmatter yields source_urls as a str (the raw value after
        # the colon) or None if it was empty.  We parse the flow list from the
        # original text so the inline bracket syntax is handled correctly.
        for extra in _parse_source_urls_flow(text):
            if extra:
                urls.add(extra)
    return urls


# ---------------------------------------------------------------------------
# Discard detection (Goal B): reads the structured seen.json marker
# ---------------------------------------------------------------------------

def discarded_urls(
    processed_urls: Iterable[str],
    *,
    seen_path: str,
) -> set[str]:
    """Return the subset of *processed_urls* that are marked discarded in seen.json.

    Uses the `discarded: true` marker written by record_discard() / record_source
    (..., discarded=True).  Comparison is done in the sha256(url) key space,
    consistent with how seen.json stores entries (no raw URL is stored).

    This replaces the legacy journal-text-scraping approach (which was fragile
    and a false-negative risk).
    """
    from copilot.loop_state import discarded_source_keys, _url_sha
    discard_keys = discarded_source_keys(seen_path)
    result: set[str] = set()
    for url in processed_urls:
        if not isinstance(url, str) or not url:
            continue
        if _url_sha(url) in discard_keys:
            result.add(url)
    return result


# ---------------------------------------------------------------------------
# Legacy journal-text reader (kept for operator/test reference; deprecated)
# ---------------------------------------------------------------------------

_LOOP_LOG_RE = re.compile(r"loop-\d+\.md$")


def discarded_or_logged_urls(
    *,
    repo_root: Optional[Path] = None,
    journal_dir: Optional[Path] = None,
) -> set[str]:
    """DEPRECATED — use discarded_urls(seen_path=...) instead.

    Kept for backward compatibility with existing tests that seeded journal
    files.  Returns URLs that appear in any journal/loop-*.md log.  The live
    guard now uses the structured seen.json marker (Goal B).
    """
    _root, _kb, journal = _resolve_roots(repo_root, None, journal_dir)
    logged: set[str] = set()
    if not journal.exists():
        return logged
    url_re = re.compile(r"https?://[^\s)>\]]+")
    for log in journal.glob("loop-*.md"):
        if not _LOOP_LOG_RE.search(log.name) or not _is_contained(log, journal):
            continue
        try:
            text = log.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for m in url_re.finditer(text):
            logged.add(m.group(0).rstrip(".,;"))
    return logged


# ---------------------------------------------------------------------------
# Public guard
# ---------------------------------------------------------------------------

def find_stranded_urls(
    urls: Iterable[str],
    *,
    repo_root: Optional[Path] = None,
    kb_dir: Optional[Path] = None,
    seen_path: Optional[str] = None,
    # Legacy keyword kept for old callers that pass journal_dir:
    journal_dir: Optional[Path] = None,
) -> list[str]:
    """Return the subset of *urls* that were recorded but never committed and
    never discarded — the F6 failure class.

    *urls* are the source URLs processed this loop (the ones record_source() saw
    in SUMMARIZE or COMMIT).  A URL is STRANDED iff it has neither:
      - a committed kb page whose source_url OR source_urls list == the URL, NOR
      - a `discarded: true` marker in seen.json.

    URL-aware (per-URL membership, never count comparison — MC-6) and discard-
    safe (a discarded URL is never flagged — MC-6).  All page paths are
    containment-validated (MC-7).

    When *seen_path* is provided, discard-safety uses the structured seen.json
    marker (Goal B).  When only *journal_dir* is provided, falls back to the
    legacy journal-text scan (backward compat).  When neither is given, the
    discard check is skipped (conservative: may flag a discard as stranded —
    only acceptable in tests that don't need discard-safety).
    """
    url_list = list(urls)
    committed = committed_source_urls(repo_root=repo_root, kb_dir=kb_dir)

    # Build discard set: prefer structured marker, fall back to journal text.
    if seen_path is not None:
        discarded_set = discarded_urls(url_list, seen_path=seen_path)
    elif journal_dir is not None:
        discarded_set = discarded_or_logged_urls(
            repo_root=repo_root, journal_dir=journal_dir
        )
    else:
        discarded_set = set()

    stranded: list[str] = []
    for url in url_list:
        if not isinstance(url, str) or not url:
            continue
        if url in committed:
            continue  # a page exists for this URL — fine
        if url in discarded_set:
            continue  # discarded on purpose — discard-safe, not stranded
        stranded.append(url)
    return stranded


def assert_commit_parity(
    urls: Iterable[str],
    *,
    repo_root: Optional[Path] = None,
    kb_dir: Optional[Path] = None,
    seen_path: Optional[str] = None,
    journal_dir: Optional[Path] = None,
) -> None:
    """Raise CommitParityError if any URL processed this loop is stranded.

    OPERATOR/TEST USE ONLY — do NOT call on the live headless path.  Calling
    this on the live path would raise before the loop_number-advancing
    STATE.toml write, causing livelock (F6 blocker).  The live recovery path
    calls recover_stranded_urls() instead (Goal A).
    """
    stranded = find_stranded_urls(
        urls,
        repo_root=repo_root,
        kb_dir=kb_dir,
        seen_path=seen_path,
        journal_dir=journal_dir,
    )
    if stranded:
        raise CommitParityError(
            "loop recorded sources with no committed page and no discard marker "
            f"(stranded by a kill between SUMMARIZE and SYNTHESIZE): {stranded}"
        )


# ---------------------------------------------------------------------------
# Live-path recovery helper (Goal A) — NEVER raises on the live path
# ---------------------------------------------------------------------------

def recover_stranded_urls(
    urls: Iterable[str],
    *,
    seen_path: str,
    queue_path: str,
    journal_path: Optional[str] = None,
    repo_root: Optional[Path] = None,
    kb_dir: Optional[Path] = None,
) -> list[str]:
    """Detect and recover stranded URLs in PHASE 6 COMMIT — NEVER raises.

    For each URL in *urls* that find_stranded_urls flags as stranded:
      (a) Re-append it to queue/next-targets.md (via write_atomic) so it is
          fetched in a future loop.
      (b) Purge its key from seen.json (via forget_source + write_json_atomic
          under file_lock) so is_resumable returns True next loop.
      (c) Log to journal/loop-<n>.md (via write_atomic) if journal_path given.

    MUST NOT raise — all exceptions are caught and logged to stderr so the
    caller (PHASE 6) can still advance loop_number.  This satisfies Goal A3:
    the STATE.toml loop_number write is ALWAYS reachable after this call.

    Returns the list of recovered URLs (empty when nothing was stranded).
    """
    import sys
    from copilot.atomic import write_atomic
    from copilot.loop_state import forget_source

    # Containment-check helper for queue/journal paths.
    def _safe_path(p_str: str, label: str) -> Optional[Path]:
        p = Path(p_str).resolve()
        # Allow any path the caller supplies — containment is the caller's
        # responsibility for queue/journal (they come from config, not user input).
        return p

    recovered: list[str] = []
    try:
        stranded = find_stranded_urls(
            urls,
            repo_root=repo_root,
            kb_dir=kb_dir,
            seen_path=seen_path,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[GUARD] recover_stranded_urls: find_stranded_urls error: {exc}", file=sys.stderr)
        return recovered

    for url in stranded:
        try:
            # (b) Purge seen.json so next loop re-fetches.
            forget_source(url, seen_path)
        except Exception as exc:  # noqa: BLE001
            print(f"[GUARD] forget_source({url!r}): {exc}", file=sys.stderr)

        try:
            # (a) Re-append to queue.
            qp = _safe_path(queue_path, "queue")
            if qp is not None:
                existing = ""
                try:
                    existing = qp.read_text(encoding="utf-8")
                except (OSError, FileNotFoundError):
                    pass
                sep = "\n" if existing and not existing.endswith("\n") else ""
                write_atomic(qp, existing + sep + url + "\n")
        except Exception as exc:  # noqa: BLE001
            print(f"[GUARD] queue append for {url!r}: {exc}", file=sys.stderr)

        try:
            # (c) Log to journal.
            if journal_path is not None:
                jp = _safe_path(journal_path, "journal")
                if jp is not None:
                    existing = ""
                    try:
                        existing = jp.read_text(encoding="utf-8")
                    except (OSError, FileNotFoundError):
                        pass
                    entry = f"\n## STRAND RECOVERY\n\nRecovered stranded URL: {url}\n"
                    sep = "\n" if existing and not existing.endswith("\n") else ""
                    write_atomic(jp, existing + sep + entry)
        except Exception as exc:  # noqa: BLE001
            print(f"[GUARD] journal log for {url!r}: {exc}", file=sys.stderr)

        recovered.append(url)
        print(f"[GUARD] strand recovered: {url}", file=sys.stderr)

    return recovered


class CommitParityError(RuntimeError):
    """Raised by assert_commit_parity when a recorded URL has no page/discard."""
