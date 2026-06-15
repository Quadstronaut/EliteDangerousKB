"""
tests/test_chunker_tables.py — Groups B1 and B2: atomic table chunking + round-trip.

All tests use real GFM markdown fixtures and run without a live Ollama.
B2 round-trip tests mock ollama_client.embed to return deterministic vectors.
"""

from __future__ import annotations

import hashlib
import json
import textwrap
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Fixture: a >512-token Elite Dangerous module stat table
# ---------------------------------------------------------------------------

# This table is deliberately large (>512 approx tokens) so that the atomic-emit
# code path is exercised — a naive windower would split it across multiple chunks.
SHIP_STAT_TABLE_MD = textwrap.dedent("""\
    ---
    source_url: https://inara.cz/elite/ships
    source_tier: 1
    source_count: 2
    verified: true
    availability: live
    ---

    # Ship Stats

    ## Module Stats

    | Module | Class | Rating | Mass (t) | Power (MW) | Integrity | Cost (CR) | Notes |
    |--------|-------|--------|----------|------------|-----------|-----------|-------|
    | Burst Laser | 1 | F | 2.00 | 0.39 | 40 | 6,600 | Fixed small turret |
    | Burst Laser | 1 | E | 2.00 | 0.46 | 40 | 13,200 | Fixed small turret |
    | Burst Laser | 2 | F | 4.00 | 0.74 | 51 | 21,100 | Fixed medium |
    | Burst Laser | 2 | E | 4.00 | 0.86 | 51 | 42,200 | Fixed medium |
    | Burst Laser | 3 | F | 8.00 | 1.39 | 64 | 67,600 | Fixed large |
    | Burst Laser | 3 | E | 8.00 | 1.60 | 64 | 135,200 | Fixed large |
    | Pulse Laser | 1 | F | 2.00 | 0.32 | 40 | 6,300 | Fixed small |
    | Pulse Laser | 1 | E | 2.00 | 0.39 | 40 | 12,600 | Fixed small |
    | Pulse Laser | 2 | F | 4.00 | 0.60 | 51 | 20,200 | Fixed medium |
    | Pulse Laser | 2 | E | 4.00 | 0.72 | 51 | 40,400 | Fixed medium |
    | Pulse Laser | 3 | F | 8.00 | 1.15 | 64 | 64,700 | Fixed large |
    | Pulse Laser | 3 | E | 8.00 | 1.36 | 64 | 129,400 | Fixed large |
    | Beam Laser | 1 | F | 2.00 | 0.62 | 40 | 37,450 | Fixed small |
    | Beam Laser | 1 | E | 2.00 | 0.75 | 40 | 74,900 | Fixed small |
    | Beam Laser | 2 | F | 4.00 | 1.20 | 51 | 119,840 | Fixed medium |
    | Beam Laser | 2 | E | 4.00 | 1.44 | 51 | 239,680 | Fixed medium |
    | Beam Laser | 3 | F | 8.00 | 2.29 | 64 | 383,490 | Fixed large |
    | Beam Laser | 3 | E | 8.00 | 2.74 | 64 | 766,980 | Fixed large |
    | Multi-cannon | 1 | F | 2.00 | 0.28 | 40 | 9,500 | Fixed small |
    | Multi-cannon | 1 | E | 2.00 | 0.33 | 40 | 19,000 | Fixed small |
    | Multi-cannon | 2 | F | 4.00 | 0.46 | 51 | 30,400 | Fixed medium |
    | Multi-cannon | 2 | E | 4.00 | 0.54 | 51 | 60,800 | Fixed medium |
    | Multi-cannon | 3 | F | 8.00 | 0.86 | 64 | 97,320 | Fixed large |
    | Multi-cannon | 3 | E | 8.00 | 1.01 | 64 | 194,640 | Fixed large |
    | Cannon | 1 | F | 2.00 | 0.34 | 40 | 10,000 | Fixed small |
    | Cannon | 1 | E | 2.00 | 0.40 | 40 | 20,000 | Fixed small |
    | Cannon | 2 | F | 4.00 | 0.66 | 51 | 32,000 | Fixed medium |
    | Cannon | 2 | E | 4.00 | 0.78 | 51 | 64,000 | Fixed medium |
    | Cannon | 3 | F | 8.00 | 1.24 | 64 | 102,400 | Fixed large |
    | Cannon | 3 | E | 8.00 | 1.46 | 64 | 204,800 | Fixed large |
    | Fragment Cannon | 1 | E | 2.00 | 0.34 | 40 | 14,400 | Fixed small |
    | Fragment Cannon | 1 | D | 2.00 | 0.40 | 40 | 21,600 | Fixed small |
    | Fragment Cannon | 2 | E | 4.00 | 0.49 | 51 | 46,080 | Fixed medium |
    | Fragment Cannon | 2 | D | 4.00 | 0.57 | 51 | 69,120 | Fixed medium |
    | Fragment Cannon | 3 | E | 8.00 | 0.74 | 64 | 147,456 | Fixed large |
    | Fragment Cannon | 3 | D | 8.00 | 0.86 | 64 | 221,184 | Fixed large |
    | Plasma Accelerator | 2 | C | 4.00 | 1.40 | 51 | 539,800 | Fixed medium |
    | Plasma Accelerator | 3 | C | 8.00 | 1.97 | 64 | 1,295,520 | Fixed large |
    | Railgun | 1 | D | 2.00 | 1.15 | 40 | 51,600 | Fixed small |
    | Railgun | 2 | B | 4.00 | 1.63 | 51 | 330,240 | Fixed medium |
    | Missile Rack | 2 | B | 4.00 | 1.20 | 51 | 48,000 | Fixed medium |
    | Missile Rack | 3 | A | 8.00 | 1.62 | 64 | 153,600 | Fixed large |
    | Torpedo Pylon | 1 | I | 2.00 | 0.40 | 40 | 15,200 | Fixed small |
    | Torpedo Pylon | 2 | I | 4.00 | 0.74 | 51 | 48,640 | Fixed medium |
    | Mine Launcher | 1 | I | 2.00 | 0.35 | 40 | 8,200 | Fixed small |
    | Mine Launcher | 2 | I | 4.00 | 0.55 | 51 | 26,240 | Fixed medium |
    | Shock Mine Launcher | 1 | I | 2.00 | 0.40 | 40 | 13,000 | Fixed small |
    | Enzyme Missile Rack | 2 | B | 4.00 | 1.28 | 51 | 1,072,000 | AX medium |
    | Flak Launcher | 2 | B | 4.00 | 1.20 | 51 | 261,400 | AX medium |
    | Guardian Shard Cannon | 1 | D | 2.00 | 0.87 | 40 | 337,600 | Guardian small |
    | Guardian Shard Cannon | 2 | D | 4.00 | 1.21 | 51 | 1,080,320 | Guardian medium |
    | Guardian Gauss Cannon | 1 | D | 2.00 | 1.61 | 40 | 540,160 | Guardian small |
    | Guardian Gauss Cannon | 2 | C | 4.00 | 2.61 | 51 | 1,081,200 | Guardian medium |
    | Guardian Plasma Charger | 2 | D | 4.00 | 1.40 | 51 | 1,080,320 | Guardian medium |
    | Guardian Plasma Charger | 3 | C | 8.00 | 2.61 | 64 | 3,456,000 | Guardian large |
    | FSD Booster (Guardian) | 1 | H | 1.30 | 0.00 | 32 | 584,800 | Jump range +4 ly |
    | FSD Booster (Guardian) | 2 | H | 1.30 | 0.00 | 32 | 1,169,600 | Jump range +6 ly |
    | FSD Booster (Guardian) | 3 | H | 1.30 | 0.00 | 32 | 2,339,200 | Jump range +7.75 ly |
    | FSD Booster (Guardian) | 4 | H | 1.30 | 0.00 | 32 | 4,678,400 | Jump range +9.25 ly |
    | FSD Booster (Guardian) | 5 | H | 1.30 | 0.00 | 32 | 9,356,800 | Jump range +10.5 ly |

    ## Notes

    Class ratings: A (best) → E/H/I (variable). Mass and power figures are
    for the base module without engineering. Cost in CR is approximate and
    varies by station. Guardian modules require permit from the Ram Tah mission.
""")


# ---------------------------------------------------------------------------
# Fixture: mixed prose + table section
# ---------------------------------------------------------------------------

MIXED_PROSE_TABLE_MD = textwrap.dedent("""\
    ---
    source_tier: 2
    source_count: 1
    verified: true
    availability: live
    ---

    # Engineer Materials

    ## Required Materials

    Before visiting Felicity Farseer, gather these materials. She is located in
    the Deciat system, roughly 14 ly from Sol. You will need an exploration rank
    of Scout or higher plus the following trade goods:

    | Material | Amount | Type | Notes |
    |----------|--------|------|-------|
    | Meta-Alloys | 1 | Trade | From Darnielle's Progress or Maia |
    | Occupied Escape Pod | 0 | Optional | Not required for unlock |
    | Micro-Woven Carbon Fibre | 3 | Manufactured | Grade 3 engineering |
    | Conductive Polymers | 2 | Manufactured | Grade 4+ mods |
    | Pharmaceutical Isolators | 1 | Trade | Higher grade blueprints |
    | Proprietary Composites | 2 | Manufactured | FSD blueprints grade 5 |

    Check the Inara website for current material requirements per blueprint grade.
""")


# ---------------------------------------------------------------------------
# Helper: fake deterministic embeddings (no Ollama)
# ---------------------------------------------------------------------------

def _fake_embed(texts: list[str]) -> np.ndarray:
    vecs = []
    for t in texts:
        seed = int(hashlib.sha256(t.encode()).hexdigest()[:8], 16) % (2**31)
        rng = np.random.default_rng(seed)
        v = rng.standard_normal(1024).astype(np.float32)
        v /= np.linalg.norm(v)
        vecs.append(v)
    return np.array(vecs, dtype=np.float32)


def _patch_dirs(monkeypatch, tmp_path: Path):
    monkeypatch.setattr("copilot.paths.embeddings_dir", lambda: tmp_path / "embeddings")
    monkeypatch.setattr("copilot.paths.indexes_dir", lambda: tmp_path / "indexes")
    monkeypatch.setattr("copilot.paths.repo_root", lambda: tmp_path)
    (tmp_path / "embeddings").mkdir(exist_ok=True)
    (tmp_path / "indexes").mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# B1-1: oversized table emitted atomically
# ---------------------------------------------------------------------------

def test_oversized_table_emitted_atomically(tmp_path):
    """A >512-token GFM table section must appear in exactly one chunk."""
    from copilot.chunker import chunk_page, _approx_tokens

    p = tmp_path / "ship-stats.md"
    p.write_text(SHIP_STAT_TABLE_MD, encoding="utf-8")
    chunks = chunk_page(p)

    # The table section body alone must exceed 512 tokens (validates fixture is real)
    header_row = "| Module | Class | Rating | Mass (t) | Power (MW) | Integrity | Cost (CR) | Notes |"
    last_row = "| FSD Booster (Guardian) | 5 | H | 1.30 | 0.00 | 32 | 9,356,800 | Jump range +10.5 ly |"

    # Find the chunk containing the table
    table_chunks = [c for c in chunks if header_row in c.text and last_row in c.text]
    assert len(table_chunks) == 1, (
        f"Expected exactly 1 chunk containing both header and last row. "
        f"Found {len(table_chunks)} chunks. "
        f"All chunk heading_paths: {[c.heading_path for c in chunks]}"
    )


# ---------------------------------------------------------------------------
# B1-2: header row stays with data rows
# ---------------------------------------------------------------------------

def test_table_header_stays_with_data(tmp_path):
    """In the table chunk, header row and sampled data rows co-occur."""
    from copilot.chunker import chunk_page

    p = tmp_path / "ship-stats.md"
    p.write_text(SHIP_STAT_TABLE_MD, encoding="utf-8")
    chunks = chunk_page(p)

    header_row = "| Module | Class | Rating | Mass (t) | Power (MW) | Integrity | Cost (CR) | Notes |"
    sampled_data_rows = [
        "| Burst Laser | 1 | F | 2.00 | 0.39 | 40 | 6,600 | Fixed small turret |",
        "| Railgun | 2 | B | 4.00 | 1.63 | 51 | 330,240 | Fixed medium |",
        "| FSD Booster (Guardian) | 3 | H | 1.30 | 0.00 | 32 | 2,339,200 | Jump range +7.75 ly |",
    ]

    # Find a chunk that has all sampled rows AND the header
    found = False
    for chunk in chunks:
        if header_row in chunk.text and all(row in chunk.text for row in sampled_data_rows):
            found = True
            break

    assert found, (
        "No single chunk contains the table header AND all 3 sampled data rows. "
        f"Chunks: {[(c.heading_path, c.text[:80]) for c in chunks]}"
    )


# ---------------------------------------------------------------------------
# B1-3: no table row split mid-cell across windows
# ---------------------------------------------------------------------------

def test_table_rows_never_split_midcell(tmp_path):
    """Every line beginning with | in any chunk also ends with | (no mid-cell split)."""
    from copilot.chunker import chunk_page

    p = tmp_path / "ship-stats.md"
    p.write_text(SHIP_STAT_TABLE_MD, encoding="utf-8")
    chunks = chunk_page(p)

    for chunk in chunks:
        for line in chunk.text.splitlines():
            stripped = line.strip()
            if stripped.startswith("|"):
                # It must also end with |
                assert stripped.endswith("|"), (
                    f"Table row appears truncated (starts but does not end with |):\n"
                    f"  Line: {stripped!r}\n"
                    f"  In chunk: {chunk.heading_path!r}"
                )


# ---------------------------------------------------------------------------
# B1-4: the table chunk deliberately exceeds max_tokens (512)
# ---------------------------------------------------------------------------

def test_table_chunk_exceeds_max_tokens_allowed(tmp_path):
    """The atomic table chunk's token count > 512 (windowing was suppressed)."""
    from copilot.chunker import chunk_page, _approx_tokens

    p = tmp_path / "ship-stats.md"
    p.write_text(SHIP_STAT_TABLE_MD, encoding="utf-8")
    chunks = chunk_page(p)

    header_row = "| Module | Class | Rating | Mass (t) | Power (MW) | Integrity | Cost (CR) | Notes |"
    table_chunks = [c for c in chunks if header_row in c.text]

    assert table_chunks, "No table chunk found — fixture or detection broken"

    table_chunk = table_chunks[0]
    tok_count = _approx_tokens(table_chunk.text)
    assert tok_count > 512, (
        f"Expected table chunk to exceed 512 tokens (got {tok_count}). "
        "Windowing may not be suppressed for atomic tables."
    )


# ---------------------------------------------------------------------------
# B1-5: mixed prose + table — table stays contiguous
# ---------------------------------------------------------------------------

def test_mixed_prose_and_table_section(tmp_path):
    """A section with leading prose + a table keeps the table in one contiguous chunk."""
    from copilot.chunker import chunk_page

    p = tmp_path / "engineer-materials.md"
    p.write_text(MIXED_PROSE_TABLE_MD, encoding="utf-8")
    chunks = chunk_page(p)

    header_row = "| Material | Amount | Type | Notes |"
    last_row = "| Proprietary Composites | 2 | Manufactured | FSD blueprints grade 5 |"

    # The table must appear entirely in a single chunk (header + last row together)
    table_chunks = [c for c in chunks if header_row in c.text and last_row in c.text]
    assert len(table_chunks) >= 1, (
        f"Table header and last row must co-occur in one chunk. "
        f"All chunks: {[(c.heading_path, c.text[:120]) for c in chunks]}"
    )

    # Verify no table row is split: every | line ends with |
    for chunk in chunks:
        for line in chunk.text.splitlines():
            stripped = line.strip()
            if stripped.startswith("|"):
                assert stripped.endswith("|"), (
                    f"Mid-cell split in mixed section: {stripped!r}"
                )


# ---------------------------------------------------------------------------
# B1-6: chunk_ids unique with table
# ---------------------------------------------------------------------------

def test_chunk_ids_unique_with_table(tmp_path):
    """All chunk_ids on the table page are unique (no collision from atomic path)."""
    from copilot.chunker import chunk_page

    p = tmp_path / "ship-stats.md"
    p.write_text(SHIP_STAT_TABLE_MD, encoding="utf-8")
    chunks = chunk_page(p)

    ids = [c.chunk_id for c in chunks]
    assert len(ids) == len(set(ids)), f"Duplicate chunk_ids found: {ids}"


# ---------------------------------------------------------------------------
# B1-7: clean_for_embedding preserves pipes
# ---------------------------------------------------------------------------

def test_clean_for_embedding_preserves_pipes():
    """clean_for_embedding must not strip or mangle table pipes/rows."""
    from copilot.chunker import clean_for_embedding

    table_row = "| Burst Laser | 1 | F | 2.00 | 0.39 | 40 | 6,600 | Fixed small turret |"
    header_row = "| Module | Class | Rating | Mass (t) | Power (MW) | Integrity | Cost (CR) | Notes |"
    delimiter_row = "|--------|-------|--------|----------|------------|-----------|-----------|-------|"
    table_block = f"{header_row}\n{delimiter_row}\n{table_row}"

    result = clean_for_embedding(table_block)

    assert "|" in result, "Pipes stripped from table"
    assert "Module" in result, "Header content lost"
    assert "Burst Laser" in result, "Data row content lost"
    assert table_row in result, f"Table row mangled: {result!r}"


# ---------------------------------------------------------------------------
# B2-1: table chunk round-trip via chunk_by_id
# ---------------------------------------------------------------------------

def test_table_chunk_roundtrip_chunk_by_id(tmp_path, monkeypatch):
    """chunk_by_id(table_chunk.chunk_id) returns a Chunk with identical id/heading_path/text."""
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)

    # Put the fixture in a kb/ subdirectory (chunk_page resolves kb_path from it)
    kb_dir = tmp_path / "kb"
    kb_dir.mkdir()
    p = kb_dir / "ship-stats.md"
    p.write_text(SHIP_STAT_TABLE_MD, encoding="utf-8")

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        from copilot import index
        index.build_index(kb_dir)

    # Find the table chunk among the indexed chunks
    chunk_ids_path = tmp_path / "embeddings" / "chunk_ids.json"
    chunk_ids = json.loads(chunk_ids_path.read_text(encoding="utf-8"))

    header_row = "| Module | Class | Rating | Mass (t) | Power (MW) | Integrity | Cost (CR) | Notes |"
    last_row = "| FSD Booster (Guardian) | 5 | H | 1.30 | 0.00 | 32 | 9,356,800 | Jump range +10.5 ly |"

    table_cid = None
    for cid in chunk_ids:
        chunk = index.chunk_by_id(cid)
        if chunk and header_row in chunk.text and last_row in chunk.text:
            table_cid = cid
            break

    assert table_cid is not None, "Could not find table chunk in index"

    # Round-trip
    retrieved = index.chunk_by_id(table_cid)
    assert retrieved is not None
    assert retrieved.chunk_id == table_cid
    assert retrieved.heading_path  # non-empty
    assert header_row in retrieved.text
    assert last_row in retrieved.text


# ---------------------------------------------------------------------------
# B2-2: content_hash is stable across repeated chunk_page calls
# ---------------------------------------------------------------------------

def test_table_content_hash_stable(tmp_path):
    """_content_hash(chunk.text) is identical across two independent chunk_page calls."""
    from copilot.chunker import chunk_page
    from copilot.index import _content_hash

    p = tmp_path / "ship-stats.md"
    p.write_text(SHIP_STAT_TABLE_MD, encoding="utf-8")

    chunks_a = chunk_page(p)
    chunks_b = chunk_page(p)

    header_row = "| Module | Class | Rating | Mass (t) | Power (MW) | Integrity | Cost (CR) | Notes |"

    def _find_table_chunk(chunks):
        for c in chunks:
            if header_row in c.text:
                return c
        return None

    table_a = _find_table_chunk(chunks_a)
    table_b = _find_table_chunk(chunks_b)

    assert table_a is not None and table_b is not None, "Table chunk not found in one of the calls"
    assert table_a.chunk_id == table_b.chunk_id, "chunk_id not deterministic"
    assert _content_hash(table_a.text) == _content_hash(table_b.text), "content_hash not stable"


# ---------------------------------------------------------------------------
# B2-3: upsert reports table chunk as unchanged after no-op
# ---------------------------------------------------------------------------

def test_upsert_unchanged_for_unmodified_table(tmp_path, monkeypatch):
    """Index the table page, then upsert_changed with no edits reports table chunk unchanged."""
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)

    kb_dir = tmp_path / "kb"
    kb_dir.mkdir()
    p = kb_dir / "ship-stats.md"
    p.write_text(SHIP_STAT_TABLE_MD, encoding="utf-8")

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        from copilot import index
        index.build_index(kb_dir)
        result = index.upsert_changed(kb_dir)

    assert result["added"] == 0, f"Expected 0 added on no-op upsert, got {result['added']}"
    assert result["unchanged"] >= 1, f"Expected >= 1 unchanged, got {result['unchanged']}"


# ---------------------------------------------------------------------------
# B1-bonus: _is_table_block helper
# ---------------------------------------------------------------------------

def test_is_table_block_detects_gfm_table():
    """_is_table_block returns True for a valid GFM table."""
    from copilot.chunker import _is_table_block

    table = textwrap.dedent("""\
        | A | B | C |
        |---|---|---|
        | 1 | 2 | 3 |
        | 4 | 5 | 6 |
    """)
    assert _is_table_block(table) is True


def test_is_table_block_rejects_plain_prose():
    """_is_table_block returns False for plain prose."""
    from copilot.chunker import _is_table_block

    prose = "This is just some text.\nNo table here at all.\nJust words."
    assert _is_table_block(prose) is False


def test_is_table_block_rejects_incomplete_table():
    """_is_table_block returns False when there is a header but no delimiter."""
    from copilot.chunker import _is_table_block

    incomplete = "| A | B |\nSome text without a delimiter row."
    assert _is_table_block(incomplete) is False


def test_split_section_preserving_tables_atomic_for_table():
    """_split_section_preserving_tables emits the table as one segment."""
    from copilot.chunker import _split_section_preserving_tables

    # Build a table section that exceeds 512 tokens
    rows = [f"| Module {i} | {i} | A | {i*1.5:.2f} | {i*0.1:.2f} | {i*10} | {i*1000} | Note {i} |"
            for i in range(1, 70)]
    table = (
        "| Module | Class | Rating | Mass (t) | Power (MW) | Integrity | Cost (CR) | Notes |\n"
        "|--------|-------|--------|----------|------------|-----------|-----------|-------|\n"
        + "\n".join(rows)
    )

    from copilot.chunker import _approx_tokens
    assert _approx_tokens(table) > 512, "Fixture must exceed 512 tokens to test atomic path"

    windows = _split_section_preserving_tables(table, min_tok=128, max_tok=512, overlap=0.15)
    # The table must be entirely in one window
    header = "| Module | Class | Rating | Mass (t) | Power (MW) | Integrity | Cost (CR) | Notes |"
    last_row = rows[-1]
    table_windows = [w for w in windows if header in w and last_row in w]
    assert len(table_windows) == 1, (
        f"Expected 1 atomic table window, got {len(table_windows)}. Windows: {[w[:80] for w in windows]}"
    )
