"""
tests/test_loop_state.py — TDD tests for copilot/loop_state.py

Run: python -m pytest tests/test_loop_state.py -v
"""
import json
import hashlib
from pathlib import Path
import pytest
from copilot.loop_state import (
    advance_phase,
    is_resumable,
    record_source,
    check_inara_rate,
    PHASE_ORDER,
)


# ---------------------------------------------------------------------------
# advance_phase
# ---------------------------------------------------------------------------

class TestAdvancePhase:
    def test_none_advances_to_triage(self):
        assert advance_phase("none") == "triage"

    def test_triage_advances_to_search(self):
        assert advance_phase("triage") == "search"

    def test_search_advances_to_summarize(self):
        assert advance_phase("search") == "summarize"

    def test_summarize_advances_to_synthesize(self):
        assert advance_phase("summarize") == "synthesize"

    def test_synthesize_advances_to_index(self):
        assert advance_phase("synthesize") == "index"

    def test_index_advances_to_commit(self):
        assert advance_phase("index") == "commit"

    def test_commit_advances_to_triage(self):
        """After commit, next loop starts at triage."""
        assert advance_phase("commit") == "triage"

    def test_invalid_phase_raises(self):
        with pytest.raises(ValueError, match="Unknown phase"):
            advance_phase("unknown-phase")

    def test_phase_order_complete(self):
        """PHASE_ORDER must contain all 7 canonical phase names."""
        expected = {"none", "triage", "search", "summarize", "synthesize", "index", "commit"}
        assert set(PHASE_ORDER) == expected


# ---------------------------------------------------------------------------
# is_resumable
# ---------------------------------------------------------------------------

class TestIsResumable:
    def test_new_url_is_resumable(self, tmp_path):
        seen = tmp_path / "seen.json"
        seen.write_text("{}", encoding="utf-8")
        assert is_resumable("https://example.com/page", str(seen)) is True

    def test_seen_url_different_content_is_resumable(self, tmp_path):
        """Same URL but different content hash -> should re-fetch (content changed)."""
        url = "https://example.com/page"
        url_sha = hashlib.sha256(url.encode()).hexdigest()
        data = {url_sha: {"first_seen": "2026-01-01T00:00:00Z", "content_sha256": "old_hash"}}
        seen = tmp_path / "seen.json"
        seen.write_text(json.dumps(data), encoding="utf-8")
        assert is_resumable(url, str(seen), content_sha256="new_hash") is True

    def test_seen_url_same_content_not_resumable(self, tmp_path):
        """Same URL + same content hash -> skip (already processed)."""
        url = "https://example.com/page"
        url_sha = hashlib.sha256(url.encode()).hexdigest()
        content_sha = "abc123"
        data = {url_sha: {"first_seen": "2026-01-01T00:00:00Z", "content_sha256": content_sha}}
        seen = tmp_path / "seen.json"
        seen.write_text(json.dumps(data), encoding="utf-8")
        assert is_resumable(url, str(seen), content_sha256=content_sha) is False

    def test_missing_seen_file_is_resumable(self, tmp_path):
        """Missing seen.json -> treat all URLs as new."""
        nonexistent = str(tmp_path / "seen.json")
        assert is_resumable("https://example.com/x", nonexistent) is True


# ---------------------------------------------------------------------------
# record_source
# ---------------------------------------------------------------------------

class TestRecordSource:
    def test_record_creates_entry(self, tmp_path):
        seen = tmp_path / "seen.json"
        seen.write_text("{}", encoding="utf-8")
        url = "https://example.com/page"
        record_source(url, "content_hash_123", str(seen))
        data = json.loads(seen.read_text(encoding="utf-8"))
        url_sha = hashlib.sha256(url.encode()).hexdigest()
        assert url_sha in data
        assert data[url_sha]["content_sha256"] == "content_hash_123"
        assert "first_seen" in data[url_sha]

    def test_record_is_idempotent(self, tmp_path):
        """Recording the same URL twice preserves first_seen and updates content_sha256."""
        seen = tmp_path / "seen.json"
        seen.write_text("{}", encoding="utf-8")
        url = "https://example.com/page"
        record_source(url, "hash_v1", str(seen))
        first_seen_val = json.loads(seen.read_text())
        url_sha = hashlib.sha256(url.encode()).hexdigest()
        original_first_seen = first_seen_val[url_sha]["first_seen"]
        record_source(url, "hash_v2", str(seen))
        data = json.loads(seen.read_text(encoding="utf-8"))
        assert data[url_sha]["first_seen"] == original_first_seen  # preserved
        assert data[url_sha]["content_sha256"] == "hash_v2"         # updated

    def test_record_uses_atomic_write(self, tmp_path, monkeypatch):
        """record_source must call write_json_atomic, not open(...,'w')."""
        from copilot import loop_state
        calls = []
        monkeypatch.setattr(loop_state, "write_json_atomic",
                            lambda path, obj: calls.append((path, obj)))
        seen = tmp_path / "seen.json"
        seen.write_text("{}", encoding="utf-8")
        record_source("https://x.com", "h", str(seen))
        assert len(calls) == 1

    def test_record_creates_seen_if_missing(self, tmp_path):
        """If seen.json does not exist, record_source creates it."""
        seen = tmp_path / "seen.json"
        assert not seen.exists()
        record_source("https://example.com/new", "hash_new", str(seen))
        assert seen.exists()
        data = json.loads(seen.read_text(encoding="utf-8"))
        assert len(data) == 1


# ---------------------------------------------------------------------------
# check_inara_rate
# ---------------------------------------------------------------------------

class TestCheckInaraRate:
    def test_no_backoff_entry_allows_fetch(self):
        state = {"loop_number": 1, "last_completed_phase": "triage"}
        assert check_inara_rate(state) is True

    def test_expired_backoff_allows_fetch(self):
        past = "2000-01-01T00:00:00"
        state = {"inara_backoff_until": past}
        assert check_inara_rate(state) is True

    def test_future_backoff_blocks_fetch(self):
        from datetime import datetime, timezone, timedelta
        future = (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat()
        state = {"inara_backoff_until": future}
        assert check_inara_rate(state) is False

    def test_empty_string_backoff_allows_fetch(self):
        state = {"inara_backoff_until": ""}
        assert check_inara_rate(state) is True
