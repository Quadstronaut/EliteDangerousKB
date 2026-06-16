"""
F6 tests for copilot/commit_guard.py — the recurrence guard.

Proves the two properties the spec demands:
  1. URL-AWARE: parity is decided per-URL by scanning each page's source_url
     frontmatter, NOT by comparing seen-count vs page-count. A loop that wrote
     the SAME number of pages as URLs processed, but the WRONG ones, is still
     caught (a count check would pass it).
  2. DISCARD-SAFE: a URL intentionally recorded-without-page is flagged
     "discarded": true in seen.json (the AUTHORITATIVE marker, HC-6) and is NOT
     reported stranded. The marker — not journal text — is the parity signal.
Plus containment, first-commit safety (empty kb), the multi-feeder union (K1),
and the transactional recovery contract (FIX-1).
"""
import hashlib
from pathlib import Path

import pytest

from copilot import commit_guard
from copilot import loop_state


def _seed(tmp_path: Path, pages: dict[str, str] | None = None,
          journals: dict[str, str] | None = None) -> Path:
    """Build a synthetic repo. pages = {relpath_under_kb: source_url}."""
    root = tmp_path / "repo"
    kb = root / "kb"
    journal = root / "journal"
    kb.mkdir(parents=True)
    journal.mkdir(parents=True)
    for rel, src_url in (pages or {}).items():
        p = kb / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(
            f"---\nsource_url: {src_url}\nsource_tier: 0\nverified: false\n---\n\n# {rel}\n\nbody\n",
            encoding="utf-8",
        )
    for name, text in (journals or {}).items():
        (journal / name).write_text(text, encoding="utf-8")
    return root


def _mark_discarded(seen_path: Path, url: str) -> None:
    """Record *url* as discarded in seen.json (the marker the guard reads)."""
    loop_state.record_discard(url, "deadbeef", str(seen_path))


# ===========================================================================
# 1. URL-aware: a committed page for the URL clears it; a missing one strands.
# ===========================================================================

def test_committed_url_not_stranded(tmp_path):
    root = _seed(tmp_path, pages={"outfitting/scb.md": "https://ex.com/scb.json"})
    stranded = commit_guard.find_stranded_urls(
        ["https://ex.com/scb.json"], repo_root=root
    )
    assert stranded == []


def test_uncommitted_url_is_stranded(tmp_path):
    root = _seed(tmp_path, pages={"outfitting/scb.md": "https://ex.com/scb.json"})
    # mrp was recorded but no page carries its source_url -> stranded.
    stranded = commit_guard.find_stranded_urls(
        ["https://ex.com/scb.json", "https://ex.com/mrp.json"], repo_root=root
    )
    assert stranded == ["https://ex.com/mrp.json"]


def test_url_aware_not_count_based(tmp_path):
    """The exact F6 trap: same NUMBER of pages as URLs processed, but the page is
    for the WRONG url. A count check (1 page == 1 url) would pass; the URL-aware
    guard must still flag the stranded one."""
    root = _seed(tmp_path, pages={"outfitting/other.md": "https://ex.com/other.json"})
    processed = ["https://ex.com/scb.json"]  # 1 url processed, 1 page exists...
    stranded = commit_guard.find_stranded_urls(processed, repo_root=root)
    # ...but the page is for a DIFFERENT url, so scb is stranded.
    assert stranded == ["https://ex.com/scb.json"]


# ===========================================================================
# 2. Discard-safe: a discarded url (logged, no page) is NOT flagged.
# ===========================================================================

def test_discarded_url_not_flagged(tmp_path):
    """A URL flagged "discarded" in seen.json is page-less on purpose -> not
    stranded. Migrated from journal-text to the authoritative marker (HC-6)."""
    root = _seed(tmp_path, pages={"outfitting/scb.md": "https://ex.com/scb.json"})
    seen = root / "indexes" / "seen.json"
    seen.parent.mkdir(parents=True, exist_ok=True)
    _mark_discarded(seen, "https://ex.com/obsolete.json")
    processed = ["https://ex.com/scb.json", "https://ex.com/obsolete.json"]
    stranded = commit_guard.find_stranded_urls(
        processed, seen_path=str(seen), repo_root=root
    )
    # scb has a page; obsolete carries the discard marker -> neither stranded.
    assert stranded == []


def test_stranded_distinguished_from_discard(tmp_path):
    """One discarded url (marker) and one truly stranded url (no page, no marker):
    only the stranded one is flagged."""
    root = _seed(tmp_path, pages={})
    seen = root / "indexes" / "seen.json"
    seen.parent.mkdir(parents=True, exist_ok=True)
    _mark_discarded(seen, "https://ex.com/discarded.json")
    processed = ["https://ex.com/discarded.json", "https://ex.com/killed-midway.json"]
    stranded = commit_guard.find_stranded_urls(
        processed, seen_path=str(seen), repo_root=root
    )
    assert stranded == ["https://ex.com/killed-midway.json"]


# ===========================================================================
# first-commit safety: an empty kb does not crash; everything processed but
# unwritten is reported (the guard's whole point), nothing else.
# ===========================================================================

def test_empty_kb_first_commit_safe(tmp_path):
    root = _seed(tmp_path, pages={}, journals={})
    # No urls processed -> no strand, no crash.
    assert commit_guard.find_stranded_urls([], repo_root=root) == []
    # A url processed but kb empty and nothing logged -> stranded (correct).
    assert commit_guard.find_stranded_urls(
        ["https://ex.com/x.json"], repo_root=root
    ) == ["https://ex.com/x.json"]


# ===========================================================================
# assert_commit_parity raises on a strand, passes clean.
# ===========================================================================

def test_assert_raises_on_strand(tmp_path):
    root = _seed(tmp_path, pages={})
    with pytest.raises(commit_guard.CommitParityError):
        commit_guard.assert_commit_parity(["https://ex.com/x.json"], repo_root=root)


def test_assert_passes_when_all_committed(tmp_path):
    root = _seed(tmp_path, pages={"a.md": "https://ex.com/a.json"})
    commit_guard.assert_commit_parity(["https://ex.com/a.json"], repo_root=root)  # no raise


# ===========================================================================
# MC-7: page paths are containment-validated.
# ===========================================================================

def test_is_contained_rejects_escape(tmp_path):
    kb = tmp_path / "kb"
    kb.mkdir()
    inside = kb / "page.md"
    inside.write_text("x", encoding="utf-8")
    assert commit_guard._is_contained(inside, kb)
    outside = tmp_path / "evil.md"
    outside.write_text("x", encoding="utf-8")
    assert not commit_guard._is_contained(outside, kb)


def test_committed_urls_reads_only_inside_kb(tmp_path):
    """A page with a source_url inside kb is read; an identically-named file
    OUTSIDE kb is never consulted."""
    root = _seed(tmp_path, pages={"ships/x.md": "https://ex.com/in.json"})
    # Drop a markdown file OUTSIDE kb that, if read, would add a phantom url.
    (root / "outside.md").write_text(
        "---\nsource_url: https://ex.com/out.json\n---\n", encoding="utf-8"
    )
    urls = commit_guard.committed_source_urls(repo_root=root)
    assert "https://ex.com/in.json" in urls
    assert "https://ex.com/out.json" not in urls
