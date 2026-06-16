"""
Round-2 F6 hardening tests for copilot/commit_guard.py + copilot/loop_state.py.

Every HC-* / FIX-* artifact here is REVERT-SENSITIVE (AC-3): it PASSES on the
merged candidate and FAILS if its fix is reverted. The mapping:

  HC-3  -> test_recover_rejects_queue_escape
  HC-4  -> test_recover_never_raises
  HC-5  -> test_recover_transaction_no_orphan_state / test_recover_append_fail_keeps_seen
  HC-6  -> test_discard_marker_is_authoritative
  HC-7  -> test_body_source_urls_ignored
  FIX-2 -> test_no_dotall_body_bracket_not_swept
  FIX-3 -> test_recover_rejects_newline_url
  K1    -> test_reader_inline_flow_list / test_union_includes_feeders
  K5    -> test_recover_dedup_no_duplicate_bullet
  AC-4  -> test_live_kb_feeders_all_committed (in tests/test_kb_feeders.py)
"""
import hashlib
import json
from pathlib import Path

import pytest

from copilot import commit_guard
from copilot import loop_state


def _seed_repo(tmp_path: Path, pages: dict[str, str] | None = None) -> Path:
    root = tmp_path / "repo"
    kb = root / "kb"
    kb.mkdir(parents=True)
    (root / "indexes").mkdir(parents=True, exist_ok=True)
    (root / "queue").mkdir(parents=True, exist_ok=True)
    (root / "journal").mkdir(parents=True, exist_ok=True)
    for rel, src_url in (pages or {}).items():
        p = kb / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(
            f"---\nsource_url: {src_url}\nsource_tier: 0\n---\n\n# {rel}\n\nbody\n",
            encoding="utf-8",
        )
    return root


def _write_page(root: Path, rel: str, frontmatter: str, body: str = "body\n") -> Path:
    p = root / "kb" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"---\n{frontmatter}\n---\n\n{body}", encoding="utf-8")
    return p


# ===========================================================================
# loop_state: record_discard / forget_source / discarded_source_keys
# ===========================================================================

class TestLoopStateDiscardMarker:
    def test_record_source_unchanged_no_discard_key(self, tmp_path):
        """record_source MUST NOT regress: no 'discarded' key appears."""
        seen = tmp_path / "seen.json"
        loop_state.record_source("https://x/a", "h1", str(seen))
        data = json.loads(seen.read_text(encoding="utf-8"))
        key = hashlib.sha256(b"https://x/a").hexdigest()
        assert "discarded" not in data[key]

    def test_record_discard_sets_flag_and_keeps_hash(self, tmp_path):
        seen = tmp_path / "seen.json"
        loop_state.record_discard("https://x/obs", "h2", str(seen))
        data = json.loads(seen.read_text(encoding="utf-8"))
        key = hashlib.sha256(b"https://x/obs").hexdigest()
        assert data[key]["discarded"] is True
        assert data[key]["content_sha256"] == "h2"
        # Deduped: same content -> not resumable.
        assert loop_state.is_resumable("https://x/obs", str(seen), "h2") is False

    def test_record_discard_preserves_first_seen(self, tmp_path):
        seen = tmp_path / "seen.json"
        loop_state.record_source("https://x/a", "h1", str(seen))
        first = json.loads(seen.read_text())[hashlib.sha256(b"https://x/a").hexdigest()]["first_seen"]
        loop_state.record_discard("https://x/a", "h2", str(seen))
        data = json.loads(seen.read_text())
        assert data[hashlib.sha256(b"https://x/a").hexdigest()]["first_seen"] == first

    def test_discarded_source_keys_reads_flag(self, tmp_path):
        seen = tmp_path / "seen.json"
        loop_state.record_source("https://x/kept", "h", str(seen))
        loop_state.record_discard("https://x/gone", "h", str(seen))
        keys = loop_state.discarded_source_keys(str(seen))
        assert hashlib.sha256(b"https://x/gone").hexdigest() in keys
        assert hashlib.sha256(b"https://x/kept").hexdigest() not in keys

    def test_discarded_source_keys_missing_file(self, tmp_path):
        assert loop_state.discarded_source_keys(str(tmp_path / "nope.json")) == set()

    def test_forget_removes_key_and_resumable_again(self, tmp_path):
        seen = tmp_path / "seen.json"
        loop_state.record_source("https://x/a", "h", str(seen))
        assert loop_state.is_resumable("https://x/a", str(seen), "h") is False
        assert loop_state.forget_source("https://x/a", str(seen)) is True
        assert loop_state.is_resumable("https://x/a", str(seen), "h") is True

    def test_forget_absent_is_false_idempotent(self, tmp_path):
        seen = tmp_path / "seen.json"
        loop_state.record_source("https://x/a", "h", str(seen))
        assert loop_state.forget_source("https://x/missing", str(seen)) is False
        loop_state.forget_source("https://x/a", str(seen))
        # second call on an already-removed key -> False, never raises
        assert loop_state.forget_source("https://x/a", str(seen)) is False

    def test_forget_missing_file_returns_false(self, tmp_path):
        assert loop_state.forget_source("https://x/a", str(tmp_path / "none.json")) is False


# ===========================================================================
# K1: fence-only inline flow-list reader + union
# ===========================================================================

class TestReaderAndUnion:
    def test_reader_inline_flow_list(self):
        text = '---\nsource_url: https://a\nsource_urls: ["https://a", "https://b"]\n---\nbody\n'
        assert commit_guard._read_frontmatter_source_urls(text) == ["https://a", "https://b"]

    def test_reader_single_quotes_and_bare(self):
        text = "---\nsource_urls: ['https://a', https://b]\n---\nbody\n"
        assert commit_guard._read_frontmatter_source_urls(text) == ["https://a", "https://b"]

    def test_reader_empty_list(self):
        text = "---\nsource_urls: []\n---\nbody\n"
        assert commit_guard._read_frontmatter_source_urls(text) == []

    def test_reader_no_inline_value_returns_empty(self):
        """source_urls: with no [...] (e.g. a block sequence) -> [] (no body fallback)."""
        text = "---\nsource_urls:\n  - https://a\n  - https://b\n---\nbody\n"
        assert commit_guard._read_frontmatter_source_urls(text) == []

    def test_union_includes_feeders(self, tmp_path):
        root = _seed_repo(tmp_path)
        _write_page(
            root, "loc/deciat.md",
            'source_url: https://own\nsource_urls: ["https://own", "https://feeder1", "https://feeder2"]',
        )
        urls = commit_guard.committed_source_urls(repo_root=root)
        assert {"https://own", "https://feeder1", "https://feeder2"} <= urls

    def test_feeder_clears_strand(self, tmp_path):
        root = _seed_repo(tmp_path)
        _write_page(
            root, "loc/deciat.md",
            'source_url: https://own\nsource_urls: ["https://own", "https://feeder1"]',
        )
        # feeder1 has no page of its own, but the union covers it -> not stranded.
        assert commit_guard.find_stranded_urls(["https://feeder1"], repo_root=root) == []


# ===========================================================================
# FIX-2: no re.DOTALL — a `]` in the body is never swept into the flow list.
# ===========================================================================

def test_no_dotall_body_bracket_not_swept(tmp_path):
    """source_urls has a one-element inline list; the BODY contains a stray `]`.
    Without DOTALL the body `]` cannot close the list. If someone reverts to a
    DOTALL/greedy parse, the body text gets swept in and this asserts != .
    """
    text = (
        '---\n'
        'source_url: https://a\n'
        'source_urls: ["https://a"]\n'
        '---\n\n'
        'A markdown table cell with a stray bracket ] and a url https://evil ]\n'
    )
    assert commit_guard._read_frontmatter_source_urls(text) == ["https://a"]


# ===========================================================================
# HC-7: a source_urls line in the BODY (outside the fence) is ignored entirely.
# ===========================================================================

def test_body_source_urls_ignored(tmp_path):
    text = (
        '---\n'
        'source_url: https://a\n'
        '---\n\n'
        'Here is some prose.\n'
        'source_urls: ["https://body-injected"]\n'
    )
    assert commit_guard._read_frontmatter_source_urls(text) == []


def test_committed_union_ignores_body_source_urls(tmp_path):
    root = _seed_repo(tmp_path)
    p = root / "kb" / "x.md"
    p.write_text(
        '---\nsource_url: https://a\n---\n\nbody line\nsource_urls: ["https://injected"]\n',
        encoding="utf-8",
    )
    urls = commit_guard.committed_source_urls(repo_root=root)
    assert "https://a" in urls
    assert "https://injected" not in urls


# ===========================================================================
# HC-6: the seen.json discard MARKER is authoritative; journal text is not.
# ===========================================================================

def test_discard_marker_is_authoritative(tmp_path):
    """A journal that mentions the URL but NO seen marker -> still stranded.
    A seen marker with NO journal mention -> not stranded. Proves the marker
    (not journal scraping) decides. Reverting to journal scraping flips both.
    """
    root = _seed_repo(tmp_path)
    seen = root / "indexes" / "seen.json"
    # Journal mentions journal_only but it has NO marker -> must be stranded.
    (root / "journal" / "loop-1.md").write_text(
        "## Discards\n- https://journal-only obsolete\n", encoding="utf-8"
    )
    loop_state.record_discard("https://marked", "h", str(seen))
    stranded = commit_guard.find_stranded_urls(
        ["https://journal-only", "https://marked"],
        seen_path=str(seen), repo_root=root,
    )
    assert stranded == ["https://journal-only"]


def test_seen_path_none_empty_discard_set(tmp_path):
    """Back-compat: seen_path None -> nothing is treated as discarded."""
    root = _seed_repo(tmp_path)
    stranded = commit_guard.find_stranded_urls(["https://x"], repo_root=root)
    assert stranded == ["https://x"]


# ===========================================================================
# Recovery — FIX-1 transaction, FIX-3 sanitation, HC-3 containment, HC-4 no-raise.
# ===========================================================================

def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def test_recover_happy_path(tmp_path):
    root = _seed_repo(tmp_path)
    seen = root / "indexes" / "seen.json"
    queue = root / "queue" / "next-targets.md"
    journal = root / "journal" / "loop-1.md"
    loop_state.record_source("https://stranded", "h", str(seen))  # recorded, no page
    recovered = commit_guard.recover_stranded_urls(
        ["https://stranded"],
        seen_path=str(seen), queue_path=str(queue),
        journal_path=str(journal), repo_root=root,
    )
    assert recovered == ["https://stranded"]
    assert "https://stranded" in _read(queue)               # queued
    assert loop_state.is_resumable("https://stranded", str(seen)) is True  # purged
    assert "F6 RECOVERY" in _read(journal)                  # logged loudly


def test_recover_transaction_no_orphan_state(tmp_path):
    """HC-5 invariant: no exit state leaves a URL absent-from-queue AND
    non-resumable-in-seen. After a successful recovery, the URL is in the queue
    AND resumable. If forget fails (monkeypatched), the URL stays queued (NOT
    purged) and is NOT reported recovered — still no orphan state."""
    root = _seed_repo(tmp_path)
    seen = root / "indexes" / "seen.json"
    queue = root / "queue" / "next-targets.md"
    loop_state.record_source("https://s", "h", str(seen))
    recovered = commit_guard.recover_stranded_urls(
        ["https://s"], seen_path=str(seen), queue_path=str(queue), repo_root=root
    )
    assert recovered == ["https://s"]
    # Invariant: queued AND resumable (both true) — never the forbidden pair.
    assert "https://s" in _read(queue)
    assert loop_state.is_resumable("https://s", str(seen)) is True


def test_recover_forget_fail_keeps_queued_not_recovered(tmp_path, monkeypatch):
    """If forget_source fails AFTER the append, the URL is queued (retryable) but
    still seen, and NOT reported recovered. The forbidden {absent-and-non-
    resumable} state cannot occur because the queue append already succeeded."""
    root = _seed_repo(tmp_path)
    seen = root / "indexes" / "seen.json"
    queue = root / "queue" / "next-targets.md"
    loop_state.record_source("https://s", "h", str(seen))

    def boom(url, seen_path):
        raise OSError("simulated forget failure")

    monkeypatch.setattr(loop_state, "forget_source", boom)
    recovered = commit_guard.recover_stranded_urls(
        ["https://s"], seen_path=str(seen), queue_path=str(queue), repo_root=root
    )
    assert recovered == []                       # NOT recovered
    assert "https://s" in _read(queue)           # but queued (retryable)
    assert loop_state.is_resumable("https://s", str(seen)) is False  # still seen


def test_recover_append_fail_keeps_seen(tmp_path, monkeypatch):
    """FIX-1 step (a): if the queue append fails, the URL stays seen (retryable),
    is NOT purged, and is NOT recovered."""
    root = _seed_repo(tmp_path)
    seen = root / "indexes" / "seen.json"
    queue = root / "queue" / "next-targets.md"
    loop_state.record_source("https://s", "h", str(seen))
    monkeypatch.setattr(commit_guard, "_append_bullet", lambda qp, url: False)
    recovered = commit_guard.recover_stranded_urls(
        ["https://s"], seen_path=str(seen), queue_path=str(queue), repo_root=root
    )
    assert recovered == []
    assert loop_state.is_resumable("https://s", str(seen)) is False  # NOT purged


def test_recover_rejects_newline_url(tmp_path):
    """FIX-3: a URL with \\n or \\r is rejected before any write — not appended,
    not recovered."""
    root = _seed_repo(tmp_path)
    seen = root / "indexes" / "seen.json"
    queue = root / "queue" / "next-targets.md"
    bad = "https://evil\n- https://smuggled"
    loop_state.record_source(bad, "h", str(seen))
    recovered = commit_guard.recover_stranded_urls(
        [bad], seen_path=str(seen), queue_path=str(queue), repo_root=root
    )
    assert recovered == []
    assert "smuggled" not in _read(queue)


def test_recover_rejects_queue_escape(tmp_path):
    """HC-3: a queue_path that escapes repo_root is rejected — nothing written,
    nothing recovered, the stranded URL stays seen."""
    root = _seed_repo(tmp_path)
    seen = root / "indexes" / "seen.json"
    outside = tmp_path / "outside.md"            # sibling of repo, escapes root
    loop_state.record_source("https://s", "h", str(seen))
    recovered = commit_guard.recover_stranded_urls(
        ["https://s"], seen_path=str(seen), queue_path=str(outside), repo_root=root
    )
    assert recovered == []
    assert not outside.exists()
    assert loop_state.is_resumable("https://s", str(seen)) is False


def test_recover_dedup_no_duplicate_bullet(tmp_path):
    """K5: re-queuing a URL already present does not add a duplicate bullet."""
    root = _seed_repo(tmp_path)
    seen = root / "indexes" / "seen.json"
    queue = root / "queue" / "next-targets.md"
    queue.write_text("- https://s\n", encoding="utf-8")  # already queued
    loop_state.record_source("https://s", "h", str(seen))
    commit_guard.recover_stranded_urls(
        ["https://s"], seen_path=str(seen), queue_path=str(queue), repo_root=root
    )
    assert _read(queue).count("https://s") == 1  # not duplicated


def test_recover_never_raises(tmp_path, monkeypatch):
    """HC-4: recover must NEVER raise, even if the inner machinery throws."""
    root = _seed_repo(tmp_path)
    seen = root / "indexes" / "seen.json"
    queue = root / "queue" / "next-targets.md"

    def boom(*a, **k):
        raise RuntimeError("catastrophe")

    monkeypatch.setattr(commit_guard, "find_stranded_urls", boom)
    # Must not raise.
    out = commit_guard.recover_stranded_urls(
        ["https://s"], seen_path=str(seen), queue_path=str(queue), repo_root=root
    )
    assert out == []


def test_recover_committed_url_not_recovered(tmp_path):
    """A URL that DOES have a page is not stranded -> not touched by recovery."""
    root = _seed_repo(tmp_path, pages={"a.md": "https://has-page"})
    seen = root / "indexes" / "seen.json"
    queue = root / "queue" / "next-targets.md"
    loop_state.record_source("https://has-page", "h", str(seen))
    recovered = commit_guard.recover_stranded_urls(
        ["https://has-page"], seen_path=str(seen), queue_path=str(queue), repo_root=root
    )
    assert recovered == []
    assert "https://has-page" not in _read(queue)
    # still seen (it was legitimately processed)
    assert loop_state.is_resumable("https://has-page", str(seen)) is False
