"""
F3 (MC-8 / MC-9) guard — every golden-question expectation is GROUNDED.

A golden question that expects a substring not literally present in its target
page is a silent eval lie: the metric can never hit it for the right reason, and
worse, a typo like '1680' vs '1,680' or 'class 3' vs '**Size class:** 3' makes a
green eval meaningless. This guard pins:

  * every expect_kb_paths entry references a kb page that exists at HEAD;
  * every expect_chunk_substring is LITERALLY present (exact bytes, including
    commas and markdown) in the named page's raw text;
  * the exact record schema {question, expect_kb_paths, expect_chunk_substrings,
    off_topic} holds for every record;
  * the 4 off-topic refusal records are preserved (empty paths/substrings,
    off_topic true);
  * the on-topic records collectively reference all 16 previously-dark pages.
"""
import json
from pathlib import Path

import pytest

from copilot.paths import repo_root

_SCHEMA_KEYS = {"question", "expect_kb_paths", "expect_chunk_substrings", "off_topic"}

# The 16 pages that had zero golden coverage before F3 (spec §F3).
_DARK_PAGES = {
    "kb/outfitting/cargo-rack.md",
    "kb/outfitting/frame-shift-drive.md",
    "kb/outfitting/fuel-scoop.md",
    "kb/outfitting/hull-reinforcement.md",
    "kb/outfitting/limpet-controllers.md",
    "kb/outfitting/mining-tools.md",
    "kb/outfitting/refinery.md",
    "kb/outfitting/shield-booster.md",
    "kb/outfitting/shield-generator.md",
    "kb/ships/cobra-mk-v.md",
    "kb/ships/mandalay.md",
    "kb/ships/panther-clipper-mk-ii.md",
    "kb/ships/type-11-prospector.md",
    "kb/ships/type-8-transporter.md",
    "kb/ships/type-9-heavy.md",
    "kb/locations/hip-23759.md",
}


def _golden() -> list[dict]:
    path = repo_root() / "eval" / "golden_questions.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_schema_holds_for_every_record():
    for rec in _golden():
        assert set(rec.keys()) == _SCHEMA_KEYS, (
            f"record has wrong keys {set(rec.keys())}: {rec.get('question')!r}"
        )
        assert isinstance(rec["expect_kb_paths"], list)
        assert isinstance(rec["expect_chunk_substrings"], list)
        assert isinstance(rec["off_topic"], bool)
        assert isinstance(rec["question"], str) and rec["question"].strip()


def test_four_off_topic_refusal_records_preserved():
    off = [r for r in _golden() if r["off_topic"]]
    assert len(off) == 4, f"expected exactly 4 off-topic records, got {len(off)}"
    for rec in off:
        assert rec["expect_kb_paths"] == [], "off-topic record must have no kb paths"
        assert rec["expect_chunk_substrings"] == [], "off-topic record must have no substrings"


def test_every_expect_kb_path_exists_at_head():
    root = repo_root()
    for rec in _golden():
        for kp in rec["expect_kb_paths"]:
            assert (root / kp).exists(), (
                f"golden question references missing page {kp}: {rec['question']!r}"
            )


def test_every_substring_is_literally_greppable():
    """Exact-byte presence — catches '1680' vs '1,680', 'class 3' vs
    '**Size class:** 3'."""
    root = repo_root()
    failures = []
    for rec in _golden():
        if rec["off_topic"]:
            continue
        # The target text is the union of every expected page's raw bytes.
        corpus = ""
        for kp in rec["expect_kb_paths"]:
            page = root / kp
            if page.exists():
                corpus += page.read_text(encoding="utf-8")
        for sub in rec["expect_chunk_substrings"]:
            if sub not in corpus:
                failures.append(
                    f"{rec['question']!r}: substring {sub!r} not literally in "
                    f"{rec['expect_kb_paths']}"
                )
    assert not failures, "ungrounded golden substrings:\n" + "\n".join(failures)


def test_on_topic_records_cover_all_sixteen_dark_pages():
    covered = {
        kp
        for rec in _golden()
        if not rec["off_topic"]
        for kp in rec["expect_kb_paths"]
    }
    missing = _DARK_PAGES - covered
    assert not missing, f"dark pages still without golden coverage: {sorted(missing)}"
