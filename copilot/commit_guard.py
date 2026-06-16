"""
copilot/commit_guard.py — F6 recurrence guard (ADDITIVE; no dedup/discard
semantics changed).

ROOT CAUSE (ed-research-prompt.md PHASE 3): record_source() runs in SUMMARIZE,
before PHASE 4 SYNTHESIZE writes the kb page. A kill between the two permanently
strands the URL — seen.json says "done" (is_resumable -> False), but no page
exists, so the loop never revisits it and the fact is lost.

THE GUARD is a COMMIT-phase parity check, called at the end of a loop with the
URLs that were processed this loop. For each URL it asks, PER-URL (never by
comparing counts — MC-6):

  * Did a kb page get committed whose frontmatter source_url == this URL? -> OK.
  * Was this URL DISCARDED (PHASE 3 DISCARD RULE records-without-page on purpose)?
    A discard is logged to journal/loop-<n>.md; if the URL appears in a journal
    discard context, it is intentionally page-less -> OK (discard-safe).
  * Otherwise the URL is STRANDED -> flag it.

It changes NOTHING about dedup or discard behaviour: it only READS seen-side
state and reports. The caller decides what to do (warn, re-queue, fail the
commit). Every path derived from page frontmatter or kb_dir is containment-
validated (resolve() then is_relative_to(kb) — MC-7); absolute / ../ paths are
rejected, never followed.
"""
from __future__ import annotations

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
# Committed-page index: source_url -> kb page (URL-aware, per-URL — MC-6)
# ---------------------------------------------------------------------------

def committed_source_urls(
    *,
    repo_root: Optional[Path] = None,
    kb_dir: Optional[Path] = None,
) -> set[str]:
    """Return the set of source_url values that have a committed kb page.

    Scans every kb/**/*.md page's frontmatter source_url. This is URL-aware: we
    compare URLs, not page counts vs seen counts (MC-6). Pages are only read if
    they are contained within kb_dir (MC-7) — a symlink or crafted path pointing
    outside kb/ is skipped, never read.
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
    return urls


# ---------------------------------------------------------------------------
# Discard detection (discard-safe — MC-6)
# ---------------------------------------------------------------------------

# A discard is logged under a "## Discards" section (ed-research-prompt.md PHASE
# 3: "log the discard to journal/loop-<n>.md"). We treat a URL as discarded if it
# appears anywhere in any journal loop log — a URL written into the journal at all
# was deliberately handled (kept-with-page OR discarded); a STRANDED url is one
# that was killed before it could be logged anywhere a human would see it. This
# is conservative on the safe side: it never flags a logged URL.
_LOOP_LOG_RE = re.compile(r"loop-\d+\.md$")


def discarded_or_logged_urls(
    *,
    repo_root: Optional[Path] = None,
    journal_dir: Optional[Path] = None,
) -> set[str]:
    """Return URLs that appear in any journal/loop-*.md log.

    Used for discard-safety: a URL the loop logged (e.g. under '## Discards') was
    handled deliberately and must NOT be flagged as stranded.
    """
    _root, _kb, journal = _resolve_roots(repo_root, None, journal_dir)
    logged: set[str] = set()
    if not journal.exists():
        return logged
    # Match http(s) URLs in the logs.
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
    journal_dir: Optional[Path] = None,
) -> list[str]:
    """Return the subset of *urls* that were recorded but never committed and
    never discarded — the F6 failure class.

    *urls* are the source URLs processed this loop (the ones record_source() saw
    in SUMMARIZE). A URL is STRANDED iff it has neither:
      - a committed kb page whose source_url == the URL, NOR
      - any journal log mention (covers the intentional PHASE-3 DISCARD case).

    URL-aware (per-URL membership, never count comparison — MC-6) and discard-safe
    (a discarded/logged URL is never flagged — MC-6). All page/journal paths are
    containment-validated (MC-7).
    """
    committed = committed_source_urls(repo_root=repo_root, kb_dir=kb_dir)
    logged = discarded_or_logged_urls(repo_root=repo_root, journal_dir=journal_dir)

    stranded: list[str] = []
    for url in urls:
        if not isinstance(url, str) or not url:
            continue
        if url in committed:
            continue  # a page exists for this URL — fine
        if url in logged:
            continue  # discarded / logged on purpose — discard-safe, not stranded
        stranded.append(url)
    return stranded


def assert_commit_parity(
    urls: Iterable[str],
    *,
    repo_root: Optional[Path] = None,
    kb_dir: Optional[Path] = None,
    journal_dir: Optional[Path] = None,
) -> None:
    """Raise CommitParityError if any URL processed this loop is stranded.

    Intended call site: the end of the COMMIT phase, BEFORE git commit, so a
    kill-stranded URL fails the loop loudly instead of being silently lost.
    """
    stranded = find_stranded_urls(
        urls, repo_root=repo_root, kb_dir=kb_dir, journal_dir=journal_dir
    )
    if stranded:
        raise CommitParityError(
            "loop recorded sources with no committed page and no discard log "
            f"(stranded by a kill between SUMMARIZE and SYNTHESIZE): {stranded}"
        )


class CommitParityError(RuntimeError):
    """Raised by assert_commit_parity when a recorded URL has no page/discard."""
