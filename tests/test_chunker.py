# tests/test_chunker.py
"""Tests for copilot/chunker.py — make_chunk_id, clean_for_embedding, chunk_page."""

import hashlib
import textwrap
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# make_chunk_id
# ---------------------------------------------------------------------------

def test_make_chunk_id_matches_contracts():
    """chunk_id = sha256('{kb_path}::{heading_path}'.encode('utf-8')).hexdigest()[:16]"""
    from copilot.chunker import make_chunk_id
    kb_path = "kb/engineers/felicity-farseer.md"
    heading_path = "Felicity Farseer > Unlock"
    expected = hashlib.sha256(
        f"{kb_path}::{heading_path}".encode("utf-8")
    ).hexdigest()[:16]
    assert make_chunk_id(kb_path, heading_path) == expected


def test_make_chunk_id_length_16():
    from copilot.chunker import make_chunk_id
    cid = make_chunk_id("kb/ships/anaconda.md", "Anaconda > Combat")
    assert len(cid) == 16


def test_make_chunk_id_deterministic():
    from copilot.chunker import make_chunk_id
    a = make_chunk_id("kb/mechanics/fsd.md", "FSD > Engineering")
    b = make_chunk_id("kb/mechanics/fsd.md", "FSD > Engineering")
    assert a == b


def test_make_chunk_id_different_for_different_inputs():
    from copilot.chunker import make_chunk_id
    a = make_chunk_id("kb/a.md", "A > B")
    b = make_chunk_id("kb/a.md", "A > C")
    assert a != b


# ---------------------------------------------------------------------------
# clean_for_embedding
# ---------------------------------------------------------------------------

def test_clean_strips_yaml_frontmatter():
    from copilot.chunker import clean_for_embedding
    md = textwrap.dedent("""\
        ---
        source_url: https://example.com
        source_tier: 1
        verified: true
        ---
        Some real content here.
    """)
    result = clean_for_embedding(md)
    assert "source_url" not in result
    assert "source_tier" not in result
    assert "Some real content here." in result


def test_clean_strips_frontmatter_only_at_top():
    """A --- block that is NOT at the very top must not be stripped."""
    from copilot.chunker import clean_for_embedding
    md = textwrap.dedent("""\
        ## Section

        Some text.

        ---

        More text after a horizontal rule.
    """)
    result = clean_for_embedding(md)
    assert "More text after a horizontal rule." in result


def test_clean_flattens_wikilink_with_alias():
    from copilot.chunker import clean_for_embedding
    result = clean_for_embedding("See [[Felicity Farseer|Farseer]] for details.")
    assert "[[" not in result
    assert "]]" not in result
    assert "Farseer" in result
    assert "Felicity Farseer" not in result  # alias replaces the link target


def test_clean_flattens_wikilink_no_alias():
    from copilot.chunker import clean_for_embedding
    result = clean_for_embedding("Fly to [[Deciat]] first.")
    assert "[[" not in result
    assert "]]" not in result
    assert "Deciat" in result


def test_clean_strips_https_urls():
    from copilot.chunker import clean_for_embedding
    result = clean_for_embedding(
        "Source: https://inara.cz/engineers and http://example.com/page"
    )
    assert "https://" not in result
    assert "http://" not in result
    assert "Source:" in result


def test_clean_combined():
    from copilot.chunker import clean_for_embedding
    md = textwrap.dedent("""\
        ---
        source_url: https://inara.cz
        verified: true
        ---
        See [[Palin|Prof. Palin]] at https://inara.cz/palin for [[FSD Injection]].
    """)
    result = clean_for_embedding(md)
    assert "source_url" not in result
    assert "[[" not in result
    assert "Prof. Palin" in result
    assert "FSD Injection" in result
    assert "https://" not in result


# ---------------------------------------------------------------------------
# chunk_page — using a multi-section test file
# ---------------------------------------------------------------------------

SAMPLE_MARKDOWN = textwrap.dedent("""\
    ---
    source_url: https://inara.cz/engineers/felicity-farseer
    source_type: inara
    source_tier: 1
    captured_at: "2026-05-30"
    source_count: 3
    verified: true
    availability: live
    changed_note: null
    ---

    # Felicity Farseer

    Felicity Farseer is a tier-1 engineer located in [[Deciat]].

    ## Unlock

    To unlock [[Felicity Farseer]], you must:
    - Have a [[reputation]] of friendly with another engineer.
    - Deliver 1 unit of Meta-Alloys. Source: https://inara.cz/commodity/meta-alloys

    ## Blueprints

    <!-- tier:1 src:https://inara.cz/engineer-blueprints verified:true availability:live -->

    Farseer offers the following FSD blueprints up to grade 5:
    - Increased FSD Range
    - FSD Lightweight

    She is one of the best engineers for exploration builds.

    ## On-Foot Location

    <!-- tier:3 src:https://reddit.com/r/EliteDangerous verified:false availability:live -->

    Some commanders report she can be found near the landing pad on foot,
    though this is unconfirmed anecdotal info from Reddit.
""")


@pytest.fixture
def sample_page(tmp_path):
    p = tmp_path / "felicity-farseer.md"
    p.write_text(SAMPLE_MARKDOWN, encoding="utf-8")
    return p


def test_chunk_page_returns_list(sample_page):
    from copilot.chunker import chunk_page
    chunks = chunk_page(sample_page)
    assert isinstance(chunks, list)
    assert len(chunks) >= 1


def test_chunk_page_heading_sections(sample_page):
    from copilot.chunker import chunk_page
    chunks = chunk_page(sample_page)
    heading_paths = [c.heading_path for c in chunks]
    # Must have a chunk for each major section
    assert any("Unlock" in h for h in heading_paths), f"No Unlock chunk; got: {heading_paths}"
    assert any("Blueprints" in h for h in heading_paths), f"No Blueprints chunk; got: {heading_paths}"
    assert any("On-Foot" in h for h in heading_paths), f"No On-Foot chunk; got: {heading_paths}"


def test_chunk_page_breadcrumb_prepended(sample_page):
    from copilot.chunker import chunk_page
    chunks = chunk_page(sample_page)
    for chunk in chunks:
        assert chunk.heading_path in chunk.text, (
            f"Breadcrumb '{chunk.heading_path}' not found in chunk text: {chunk.text[:80]!r}"
        )


def test_chunk_page_no_wikilinks_in_text(sample_page):
    from copilot.chunker import chunk_page
    chunks = chunk_page(sample_page)
    for chunk in chunks:
        assert "[[" not in chunk.text, f"Wikilink found in chunk: {chunk.text[:120]!r}"


def test_chunk_page_no_urls_in_text(sample_page):
    from copilot.chunker import chunk_page
    chunks = chunk_page(sample_page)
    for chunk in chunks:
        assert "https://" not in chunk.text, f"URL found in chunk text: {chunk.text[:120]!r}"
        assert "http://" not in chunk.text


def test_chunk_page_inherits_page_frontmatter(sample_page):
    from copilot.chunker import chunk_page
    chunks = chunk_page(sample_page)
    # All chunks should have source_tier from page defaults unless overridden
    for chunk in chunks:
        assert chunk.source_tier in (1, 3), f"Unexpected tier {chunk.source_tier}"


def test_chunk_page_inline_override_tier3(sample_page):
    """The On-Foot section has <!-- tier:3 --> override — must be reflected in the chunk."""
    from copilot.chunker import chunk_page
    chunks = chunk_page(sample_page)
    on_foot = [c for c in chunks if "On-Foot" in c.heading_path]
    assert on_foot, "No On-Foot chunk found"
    assert on_foot[0].source_tier == 3, (
        f"Expected tier 3 for On-Foot chunk, got {on_foot[0].source_tier}"
    )
    assert on_foot[0].verified is False


def test_chunk_page_default_availability_live(tmp_path):
    """A page with no availability frontmatter defaults to 'live'."""
    from copilot.chunker import chunk_page
    p = tmp_path / "minimal.md"
    p.write_text(textwrap.dedent("""\
        ---
        source_tier: 2
        source_count: 1
        verified: false
        ---

        # Minimal Page

        ## Only Section

        Some content here.
    """), encoding="utf-8")
    chunks = chunk_page(p)
    assert all(c.availability == "live" for c in chunks), (
        f"Expected all 'live'; got: {[(c.heading_path, c.availability) for c in chunks]}"
    )


def test_chunk_page_chunk_ids_are_unique(sample_page):
    from copilot.chunker import chunk_page
    chunks = chunk_page(sample_page)
    ids = [c.chunk_id for c in chunks]
    assert len(ids) == len(set(ids)), f"Duplicate chunk_ids: {ids}"


def test_chunk_page_kb_path_uses_forward_slashes(tmp_path):
    """kb_path stored in chunks must use forward slashes (CONTRACTS convention)."""
    from copilot.chunker import chunk_page
    # Create nested structure like kb/engineers/test.md
    eng_dir = tmp_path / "kb" / "engineers"
    eng_dir.mkdir(parents=True)
    p = eng_dir / "test-engineer.md"
    p.write_text(textwrap.dedent("""\
        ---
        source_tier: 2
        source_count: 1
        verified: false
        ---
        # Test Engineer
        ## Details
        Some content.
    """), encoding="utf-8")
    chunks = chunk_page(p)
    for chunk in chunks:
        assert "\\" not in chunk.kb_path, (
            f"kb_path must use forward slashes: {chunk.kb_path!r}"
        )
