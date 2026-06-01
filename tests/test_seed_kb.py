"""Verify seed KB files exist and parse without error via chunker.chunk_page."""
from pathlib import Path

import pytest

# Paths relative to repo root.
SEED_FILES = [
    "cmdr/duvrazh.md",
    "kb/trunk.md",
    "kb/engineers/felicity-farseer.md",
    "kb/mechanics/frame-shift-drive.md",
    "kb/ships/python-mk-ii.md",
]


def _repo_root() -> Path:
    from copilot.paths import repo_root
    return repo_root()


@pytest.mark.parametrize("rel_path", SEED_FILES)
def test_seed_file_exists(rel_path):
    path = _repo_root() / rel_path
    assert path.exists(), f"Seed file missing: {path}"


@pytest.mark.parametrize("rel_path", [f for f in SEED_FILES if f.startswith("kb/")])
def test_seed_file_parses_to_chunks(rel_path):
    from copilot.chunker import chunk_page
    path = _repo_root() / rel_path
    chunks = chunk_page(path)
    assert len(chunks) >= 1, f"chunk_page returned no chunks for {rel_path}"
    for c in chunks:
        assert c.chunk_id, "Chunk missing chunk_id"
        assert c.text, "Chunk has empty text"
        assert c.kb_path == rel_path, f"kb_path mismatch: {c.kb_path!r} != {rel_path!r}"
