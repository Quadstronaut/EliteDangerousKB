"""
copilot/commit_guard.py — F6 recurrence guard (ROUND 2: structured discard +
multi-feeder union + transactional recovery).

ROOT CAUSE (ed-research-prompt.md PHASE 3): record_source() ran in SUMMARIZE,
before PHASE 4 SYNTHESIZE writes the kb page. A kill between the two permanently
strands the URL — seen.json says "done" (is_resumable -> False), but no page
exists, so the loop never revisits it and the fact is lost.

THE GUARD is a COMMIT-phase parity check. For each URL processed this loop it
asks, PER-URL (never by comparing counts):

  * Did a kb page get committed citing this URL? A page cites a URL either via
    its single ``source_url`` (the page's own source) OR via a ``source_urls``
    inline flow list (the page's RECORDED FEEDER URLs for a merged page). The
    union of both is the committed set (K1/C1).
  * Was this URL DISCARDED? A discard is recorded in seen.json with a structured
    ``"discarded": true`` flag (the AUTHORITATIVE signal — HC-6). Journal text is
    NOT consulted: a human-readable journal line is no longer the parity signal.
  * Otherwise the URL is STRANDED -> flag it.

recover_stranded_urls() then re-queues each stranded URL and purges its stale
seen marker, in a strict order that NEVER leaves a URL both absent-from-queue
AND non-resumable-in-seen (FIX-1 / HC-5).

Every path derived from page frontmatter or written by recovery is containment-
validated: queue/journal writes anchor on repo_root (HC-3), kb reads anchor on
kb_dir. Absolute / ``..`` escapes are rejected, never followed/written.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Optional

from copilot import loop_state
from copilot.atomic import write_atomic

# Reuse the project's frontmatter parser so the single source_url is read
# exactly as the indexer reads it (no second, divergent YAML dialect). The
# multi-feeder list is parsed separately (the line-based parser cannot read a
# flow list) by _read_frontmatter_source_urls below.
from copilot.chunker import _parse_frontmatter


# ---------------------------------------------------------------------------
# Path helpers (all containment-validated)
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
# Frontmatter source_urls reader — fence-only, flow-list, no DOTALL (K1)
# ---------------------------------------------------------------------------

# Match a single physical `source_urls: [...]` line. NO re.DOTALL (FIX-2): the
# `[^\n]*` and the `^...$` anchors with re.MULTILINE keep the match on ONE line,
# so a `]` many lines down in the body can never be swept into the list. The
# regex is applied ONLY to the fence block text (FIX-4/HC-7), never the body.
_SOURCE_URLS_LINE_RE = re.compile(
    r"^[ \t]*source_urls[ \t]*:[ \t]*\[(?P<items>[^\n\]]*)\][ \t]*$",
    re.MULTILINE,
)

# A single list item: a double- or single-quoted string, or a bare token. We
# split conservatively on commas OUTSIDE quotes by tokenising item-by-item.
_LIST_ITEM_RE = re.compile(
    r"""\s*(?:"(?P<dq>[^"]*)"|'(?P<sq>[^']*)'|(?P<bare>[^,]+?))\s*(?:,|$)""",
)


def _fence_block(text: str) -> Optional[str]:
    """Return the leading YAML fence block (between the first ``---\\n`` and the
    next ``\\n---``), or None if there is no well-formed leading fence.

    This is the SAME boundary _parse_frontmatter uses, recomputed here because we
    need the raw fence text (the line-based parser drops list syntax). Anything
    outside this block — i.e. the page body — is never inspected (HC-7).
    """
    if not text.startswith("---"):
        return None
    # The fence opens at the first line; find the closing "\n---".
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return text[3:end]


def _read_frontmatter_source_urls(text: str) -> list[str]:
    """Parse a SINGLE-LINE inline ``source_urls: ["a","b"]`` flow list from the
    leading fence block ONLY (K1).

    Rules (boundary-hardened):
      * Only the fence block is searched (FIX-4/HC-7) — a ``source_urls:`` line
        in the BODY is ignored entirely.
      * No re.DOTALL (FIX-2): the value must be a single physical line; a block
        sequence (``source_urls:`` then ``  - a`` on later lines) yields [].
      * A ``source_urls:`` key with no inline ``[...]`` value -> [] (NO body
        fallback, NO guessing from the body).
      * Items may be double-quoted, single-quoted, or bare; order preserved;
        empty items dropped.
    """
    fence = _fence_block(text)
    if fence is None:
        return []
    m = _SOURCE_URLS_LINE_RE.search(fence)
    if m is None:
        return []
    inner = m.group("items").strip()
    if not inner:
        return []  # `source_urls: []`
    out: list[str] = []
    for item in _LIST_ITEM_RE.finditer(inner):
        val = item.group("dq")
        if val is None:
            val = item.group("sq")
        if val is None:
            val = item.group("bare")
        if val is None:
            continue
        val = val.strip()
        if val:
            out.append(val)
    return out


# ---------------------------------------------------------------------------
# Committed-page index: single source_url UNION feeder source_urls (K1/C1)
# ---------------------------------------------------------------------------

def committed_source_urls(
    *,
    repo_root: Optional[Path] = None,
    kb_dir: Optional[Path] = None,
) -> set[str]:
    """Return the set of source URLs that have a committed kb page.

    For each contained kb/**/*.md page, UNION:
      * its single ``source_url`` (the page's own source — existing behaviour), and
      * every entry of its inline ``source_urls`` feeder list (K1/C1).

    URL-aware (compares URLs, not counts). Pages are read only if contained
    within kb_dir; a crafted path pointing outside kb/ is skipped, never read.
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
        src = meta.get("source_url")
        if isinstance(src, str) and src:
            urls.add(src)
        for feeder in _read_frontmatter_source_urls(text):
            urls.add(feeder)
    return urls


# ---------------------------------------------------------------------------
# Discard detection — structured seen.json key space (HC-6 / B2)
# ---------------------------------------------------------------------------

def discarded_source_keys(seen_path: Optional[str]) -> set[str]:
    """Return the set of sha256(url) keys flagged discarded in seen.json.

    Delegates to loop_state.discarded_source_keys (the authoritative reader).
    seen_path None -> empty set (back-compat for callers that do not pass it).
    """
    if seen_path is None:
        return set()
    return loop_state.discarded_source_keys(seen_path)


# ---------------------------------------------------------------------------
# Public guard
# ---------------------------------------------------------------------------

def find_stranded_urls(
    urls: Iterable[str],
    *,
    seen_path: Optional[str] = None,
    repo_root: Optional[Path] = None,
    kb_dir: Optional[Path] = None,
    journal_dir: Optional[Path] = None,
) -> list[str]:
    """Return the subset of *urls* recorded but never committed and never
    discarded — the F6 failure class.

    A URL is STRANDED iff BOTH:
      * it is NOT in committed_source_urls (no page cites it via source_url or a
        source_urls feeder list — K1/C1), AND
      * its sha256(url) is NOT in discarded_source_keys(seen_path) (HC-6/B2).

    seen_path None -> empty discarded set (back-compat). ``journal_dir`` is
    accepted for signature compatibility but unused (the marker is authoritative).
    URL-aware and discard-safe. kb paths are containment-validated.
    """
    committed = committed_source_urls(repo_root=repo_root, kb_dir=kb_dir)
    discarded = discarded_source_keys(seen_path)

    stranded: list[str] = []
    for url in urls:
        if not isinstance(url, str) or not url:
            continue
        if url in committed:
            continue  # a page cites this URL (own source or feeder) — fine
        if loop_state._url_sha(url) in discarded:
            continue  # deliberately discarded — page-less on purpose, not stranded
        stranded.append(url)
    return stranded


def assert_commit_parity(
    urls: Iterable[str],
    *,
    seen_path: Optional[str] = None,
    repo_root: Optional[Path] = None,
    kb_dir: Optional[Path] = None,
    journal_dir: Optional[Path] = None,
) -> None:
    """Raise CommitParityError if any URL processed this loop is stranded.

    RAISING form retained for tests/operators (A4). It is NOT called on the live
    headless path — the live path uses recover_stranded_urls (which never raises)
    so a strand re-queues instead of aborting the loop.
    """
    stranded = find_stranded_urls(
        urls,
        seen_path=seen_path,
        repo_root=repo_root,
        kb_dir=kb_dir,
        journal_dir=journal_dir,
    )
    if stranded:
        raise CommitParityError(
            "loop recorded sources with no committed page and no discard marker "
            f"(stranded by a kill between SUMMARIZE and SYNTHESIZE): {stranded}"
        )


class CommitParityError(RuntimeError):
    """Raised by assert_commit_parity when a recorded URL has no page/discard."""


# ---------------------------------------------------------------------------
# Recovery — transactional re-queue + purge (A2 / FIX-1 / FIX-3 / HC-2..5)
# ---------------------------------------------------------------------------

def _has_control_chars(url: str) -> bool:
    """True if *url* contains CR or LF — a bullet-injection / multi-line hazard.

    A URL with \\r or \\n is rejected before any write (FIX-3): appending it as a
    queue bullet would split into multiple lines / smuggle markup. Such a URL is
    NOT appended and NOT reported recovered.
    """
    return "\r" in url or "\n" in url


def _queue_has_url(queue_path: Path, url: str) -> bool:
    """True if *url* already appears in the queue file (per-URL dedup — K5).

    Tolerant of a missing file (returns False). Substring-free: matches the URL
    as a whole token bounded by start/whitespace/EOL so a longer URL that merely
    contains a shorter one is not falsely deduped.
    """
    if not queue_path.exists():
        return False
    try:
        text = queue_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    # Whole-token match: the URL preceded by start/space/( and followed by
    # space/EOL/) — avoids "https://x/a" matching inside "https://x/ab".
    pat = re.compile(
        r"(?:^|[\s(])" + re.escape(url) + r"(?=$|[\s)])",
        re.MULTILINE,
    )
    return pat.search(text) is not None


def _append_bullet(queue_path: Path, url: str) -> bool:
    """Append ``- <url>`` as a new line to *queue_path* via copilot.atomic (HC-2).

    Read-modify-write under the queue's own file lock so a concurrent recoverer
    cannot interleave and drop a bullet. Returns True on a confirmed write,
    False if the append could not be confirmed (caller then leaves the URL seen,
    retryable — FIX-1). Idempotent: if the URL is already queued, returns True
    WITHOUT a duplicate line (the post-condition "URL is in the queue" holds).
    """
    from copilot.locking import file_lock

    lock_token = str(queue_path) + ".lock"
    try:
        with file_lock(lock_token, timeout=30.0):
            if _queue_has_url(queue_path, url):
                return True  # already present — dedup, post-condition satisfied
            existing = ""
            if queue_path.exists():
                try:
                    existing = queue_path.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError):
                    existing = ""
            if existing and not existing.endswith("\n"):
                existing += "\n"
            new_text = existing + f"- {url}\n"
            write_atomic(queue_path, new_text)
            # Confirm the bullet actually landed before reporting success.
            return _queue_has_url(queue_path, url)
    except Exception:
        return False


def _log_recovery(journal_path: Optional[Path], url: str) -> None:
    """Append a loud recovery note to the journal if a path was given. Best-effort
    only — a journal write failure must NEVER affect the recovered/queued state
    (the queue+seen transaction is what matters)."""
    if journal_path is None:
        return
    from copilot.locking import file_lock

    note = (
        f"- F6 RECOVERY: re-queued stranded source {url} "
        "(recorded in seen.json but no committed page; purged seen marker so the "
        "loop revisits it).\n"
    )
    try:
        with file_lock(str(journal_path) + ".lock", timeout=10.0):
            existing = ""
            if journal_path.exists():
                try:
                    existing = journal_path.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError):
                    existing = ""
            if existing and not existing.endswith("\n"):
                existing += "\n"
            write_atomic(journal_path, existing + note)
    except Exception:
        pass  # journal is human-facing; never let it break recovery


def recover_stranded_urls(
    urls: Iterable[str],
    *,
    seen_path: str,
    queue_path: str,
    journal_path: Optional[str] = None,
    repo_root: Optional[Path] = None,
    kb_dir: Optional[Path] = None,
) -> list[str]:
    """Re-queue every stranded URL and purge its stale seen marker (A2 / FIX-1).

    For each URL flagged by find_stranded_urls(seen_path=seen_path, ...):

      1. CONTAINMENT (HC-3): queue_path / journal_path are resolve()'d and must
         be is_relative_to(repo_root). An escape is REJECTED — not written, not
         reported recovered.
      2. SANITATION (FIX-3): a URL containing \\r or \\n is rejected before any
         write — not appended, not recovered.
      3. PRESCRIBED ORDERING (FIX-1, exact):
           a. queue-append FIRST. If it fails -> URL stays seen (retryable), NOT
              recovered, NOT purged.
           b. ONLY after a confirmed-successful append, forget_source to purge
              the seen marker. If forget fails -> URL is now queued (retryable)
              but still seen; NOT recovered.
         No exit state leaves a URL {absent-from-queue AND non-resumable-in-seen}.
      4. Best-effort loud journal log (never affects recovered state).

    NEVER raises (HC-4). Returns ONLY the URLs where BOTH append AND forget
    completed. Recovery is idempotent: a URL already absent from seen (forget
    returns False) is NOT reported recovered, but it is queued — so re-running is
    safe and converges.
    """
    recovered: list[str] = []
    try:
        root, _kb, _journal = _resolve_roots(repo_root, kb_dir, None)

        q_path = Path(queue_path)
        if not q_path.is_absolute():
            q_path = (root / q_path)
        q_resolved = q_path.resolve()

        j_resolved: Optional[Path] = None
        if journal_path is not None:
            j_path = Path(journal_path)
            if not j_path.is_absolute():
                j_path = (root / j_path)
            j_resolved = j_path.resolve()

        # HC-3: reject a queue path that escapes the repo — write nothing.
        if not _is_contained(q_resolved, root):
            return []
        # A journal escape disables journaling but does NOT block recovery.
        if j_resolved is not None and not _is_contained(j_resolved, root):
            j_resolved = None

        stranded = find_stranded_urls(
            urls, seen_path=seen_path, repo_root=root, kb_dir=kb_dir
        )

        seen_already: set[str] = set()  # per-call dedup of repeated input URLs
        for url in stranded:
            if url in seen_already:
                continue
            seen_already.add(url)

            if _has_control_chars(url):  # FIX-3
                continue  # rejected: not appended, not recovered

            # FIX-1 step (a): queue FIRST.
            if not _append_bullet(q_resolved, url):
                continue  # append failed -> stays seen (retryable), not recovered

            # FIX-1 step (b): ONLY after a confirmed append, purge the marker.
            try:
                purged = loop_state.forget_source(url, seen_path)
            except Exception:
                purged = False
            if not purged:
                # Queued but not purged (or already absent) -> NOT recovered.
                # URL is in the queue (retryable); no {absent-and-non-resumable}
                # state can exist.
                continue

            _log_recovery(j_resolved, url)
            recovered.append(url)
    except Exception:
        # HC-4: the live commit path must never crash on recovery. Whatever we
        # confirmed before the failure is already in `recovered`.
        return recovered
    return recovered
