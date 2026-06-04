# copilot/chunker.py
"""Markdown chunker for the ED Knowledge Engine.

Entry points:
  make_chunk_id(kb_path, heading_path) -> str         16-hex chunk identifier
  clean_for_embedding(markdown) -> str                strip frontmatter/wikilinks/URLs
  chunk_page(path) -> list[Chunk]                     split page into Chunk objects

Chunking strategy (spec §A / CONTRACTS):
  - Parse YAML frontmatter for page-level defaults.
  - Split body on H2 (## ) and H3 (### ) headings.
  - Window sections to 128–512 approximate tokens (words × 1.3), 15% overlap
    when a section exceeds max.
  - Prepend "PageTitle > Heading" breadcrumb to chunk.text.
  - Apply clean_for_embedding to chunk.text (frontmatter / wikilinks / URLs gone).
  - Honour inline <!-- tier:N src:URL verified:true availability:live --> overrides.
  - Default availability = "live".
"""

import hashlib
import re
from pathlib import Path
from typing import Any

from copilot.models import Chunk


# ---------------------------------------------------------------------------
# chunk_id
# ---------------------------------------------------------------------------

def make_chunk_id(kb_path: str, heading_path: str) -> str:
    """sha256('{kb_path}::{heading_path}'.encode('utf-8')).hexdigest()[:16]"""
    return hashlib.sha256(
        f"{kb_path}::{heading_path}".encode("utf-8")
    ).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Cleaning
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)
_WIKILINK_ALIAS_RE = re.compile(r"\[\[([^\]|]+)\|([^\]]+)\]\]")   # [[target|alias]]
_WIKILINK_PLAIN_RE = re.compile(r"\[\[([^\]]+)\]\]")               # [[target]]
_URL_RE = re.compile(r"https?://\S+")


def clean_for_embedding(markdown: str) -> str:
    """Strip YAML frontmatter, flatten wikilinks, remove raw URLs.

    - Frontmatter: only stripped if the document starts with ---\\n (YAML block).
    - [[target|alias]] → alias
    - [[target]]       → target
    - http(s)://...    → (removed, including trailing punctuation eaten by \\S+)
    """
    # Strip leading YAML frontmatter block (only at top of document)
    text = _FRONTMATTER_RE.sub("", markdown, count=1)
    # Flatten alias wikilinks first (more specific pattern)
    text = _WIKILINK_ALIAS_RE.sub(lambda m: m.group(2), text)
    # Flatten plain wikilinks
    text = _WIKILINK_PLAIN_RE.sub(lambda m: m.group(1), text)
    # Remove raw URLs
    text = _URL_RE.sub("", text)
    return text


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

def _parse_frontmatter(content: str) -> tuple[dict, str]:
    """Return (metadata_dict, body_without_frontmatter).

    Parses simple YAML frontmatter (key: value pairs) without a full YAML
    library to avoid extra dependencies.  Supports str, int, bool, and null.
    """
    meta: dict[str, Any] = {}
    if not content.startswith("---"):
        return meta, content

    end = content.find("\n---", 3)
    if end == -1:
        return meta, content

    fm_block = content[3:end].strip()
    body = content[end + 4:].lstrip("\n")

    for line in fm_block.splitlines():
        if ":" not in line:
            continue
        key, _, raw_val = line.partition(":")
        key = key.strip()
        raw_val = raw_val.strip().strip('"').strip("'")
        if raw_val.lower() == "true":
            meta[key] = True
        elif raw_val.lower() == "false":
            meta[key] = False
        elif raw_val.lower() in ("null", "~", ""):
            meta[key] = None
        else:
            try:
                meta[key] = int(raw_val)
            except ValueError:
                meta[key] = raw_val

    return meta, body


# ---------------------------------------------------------------------------
# Inline override parsing
# ---------------------------------------------------------------------------

_INLINE_OVERRIDE_RE = re.compile(
    r"<!--\s*"
    r"(?:tier:(\d+)\s*)?"
    r"(?:src:(\S+)\s*)?"
    r"(?:verified:(true|false)\s*)?"
    r"(?:availability:(\w+)\s*)?"
    r"-->"
)


def _parse_inline_override(section_text: str) -> dict:
    """Extract the first <!-- key:val ... --> comment from *section_text*.

    Returns a dict with only the keys that were explicitly present in the comment.
    """
    m = _INLINE_OVERRIDE_RE.search(section_text)
    if not m:
        return {}
    overrides: dict = {}
    if m.group(1) is not None:
        overrides["source_tier"] = int(m.group(1))
    if m.group(2) is not None:
        overrides["source_url"] = m.group(2)
    if m.group(3) is not None:
        overrides["verified"] = m.group(3) == "true"
    if m.group(4) is not None:
        overrides["availability"] = m.group(4)
    return overrides


# ---------------------------------------------------------------------------
# Token approximation
# ---------------------------------------------------------------------------

def _approx_tokens(text: str) -> int:
    """Approximate token count: whitespace-split word count × 1.3."""
    return int(len(text.split()) * 1.3)


# ---------------------------------------------------------------------------
# Windowing (overlap splitting)
# ---------------------------------------------------------------------------

def _window_text(text: str, min_tok: int, max_tok: int, overlap: float) -> list[str]:
    """Split *text* into overlapping windows of max_tok tokens.

    Each window overlaps the previous by *overlap* fraction of max_tok.
    Windows that fall below min_tok are merged forward (or kept if last).
    """
    words = text.split()
    if not words:
        return [text]

    step = max(1, int(max_tok * (1 - overlap) / 1.3))   # words per step
    window_words = max(1, int(max_tok / 1.3))            # words per window

    windows = []
    i = 0
    while i < len(words):
        chunk_words = words[i: i + window_words]
        windows.append(" ".join(chunk_words))
        i += step
        if i >= len(words):
            break

    # Merge tiny trailing window into previous if below min_tok
    if len(windows) > 1 and _approx_tokens(windows[-1]) < min_tok:
        windows[-2] = windows[-2] + " " + windows[-1]
        windows = windows[:-1]

    return windows


# ---------------------------------------------------------------------------
# Heading splitting
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{2,3})\s+(.+)$", re.MULTILINE)


def _split_on_headings(body: str) -> list[tuple[str, str]]:
    """Split *body* on H2/H3 headings.

    Returns list of (heading_text, section_body) tuples.
    A leading intro block before the first heading becomes ("", intro_text).

    H3 headings are qualified with their parent H2 ("Parent > Child") so that
    two identically-named H3s under different H2s (e.g. "Requirements" under
    both "Engineering" and "Outfitting") produce DISTINCT heading_paths — and
    therefore distinct chunk_ids. Without this they collide and the second
    section silently overwrites the first in the index.
    """
    sections: list[tuple[str, str]] = []
    last_end = 0
    last_heading = ""      # qualified heading of the section currently open
    current_h2 = ""        # most recent H2, used to qualify nested H3s
    for m in _HEADING_RE.finditer(body):
        text_before = body[last_end: m.start()].strip()
        if last_end == 0 and text_before:
            sections.append(("", text_before))
        elif last_heading and text_before:
            sections.append((last_heading, text_before))
        elif last_heading:
            sections.append((last_heading, ""))

        level = len(m.group(1))            # 2 for "##", 3 for "###"
        heading_text = m.group(2).strip()
        if level <= 2:
            current_h2 = heading_text
            last_heading = heading_text
        else:
            last_heading = (
                f"{current_h2} > {heading_text}" if current_h2 else heading_text
            )
        last_end = m.end()
    # Trailing section
    tail = body[last_end:].strip()
    if last_heading or tail:
        sections.append((last_heading, tail))
    return sections


# ---------------------------------------------------------------------------
# chunk_page
# ---------------------------------------------------------------------------

def chunk_page(path: Path) -> list[Chunk]:
    """Parse *path* into a list of Chunk objects.

    - Frontmatter defaults applied to every chunk.
    - Inline <!-- tier:N ... --> overrides applied per section.
    - Sections windowed to 128–512 tokens with 15% overlap when over max.
    - Breadcrumb "PageTitle > Heading" prepended to chunk.text.
    - clean_for_embedding applied to chunk.text.
    - kb_path stored with forward slashes (CONTRACTS convention).
    """
    content = path.read_text(encoding="utf-8")
    meta, body = _parse_frontmatter(content)

    # Derive kb_path relative to the path itself (forward-slashes for cross-platform)
    # We store the path as given if it's already relative, otherwise use the name.
    # Callers passing absolute paths get the last three components by convention.
    # For a path like G:\...\kb\engineers\file.md we want kb/engineers/file.md.
    parts = list(path.parts)
    try:
        kb_idx = next(i for i, p in enumerate(parts) if p == "kb")
        kb_path = "/".join(parts[kb_idx:])
    except StopIteration:
        # Fallback: use the filename only (test paths that don't include kb/)
        kb_path = path.name

    # Page-level defaults from frontmatter
    page_title = ""
    for line in body.splitlines():
        stripped = line.lstrip("#").strip()
        if stripped and line.startswith("#"):
            page_title = stripped
            break
    if not page_title:
        page_title = path.stem

    page_source_url: str | None = meta.get("source_url")
    page_source_tier: int = int(meta.get("source_tier", 2))
    page_source_count: int = int(meta.get("source_count", 1))
    page_verified: bool = bool(meta.get("verified", False))
    page_availability: str = str(meta.get("availability") or "live")
    page_changed_note: str | None = meta.get("changed_note") if meta.get("changed_note") else None

    cfg_min = 128
    cfg_max = 512
    cfg_overlap = 0.15
    try:
        from copilot.paths import load_config
        retrieval = load_config().get("retrieval", {})
        cfg_min = int(retrieval.get("chunk_min_tokens", cfg_min))
        cfg_max = int(retrieval.get("chunk_max_tokens", cfg_max))
        cfg_overlap = float(retrieval.get("chunk_overlap", cfg_overlap))
    except Exception:
        pass  # use defaults if config not available

    sections = _split_on_headings(body)
    chunks: list[Chunk] = []

    for heading, section_body in sections:
        if not section_body.strip() and not heading:
            continue

        # Inline override for this section
        overrides = _parse_inline_override(section_body)
        src_tier = overrides.get("source_tier", page_source_tier)
        src_url = overrides.get("source_url", page_source_url)
        verified = overrides.get("verified", page_verified)
        availability = overrides.get("availability", page_availability)

        heading_path = f"{page_title} > {heading}" if heading else page_title

        # Window if needed
        if _approx_tokens(section_body) > cfg_max:
            windows = _window_text(section_body, cfg_min, cfg_max, cfg_overlap)
        else:
            windows = [section_body]

        for w_idx, window in enumerate(windows):
            # Suffix heading_path when a section is split across windows
            if len(windows) > 1:
                h_path = f"{heading_path} [{w_idx + 1}/{len(windows)}]"
            else:
                h_path = heading_path

            breadcrumb = h_path
            # Build embeddable text: breadcrumb + cleaned content
            clean_body = clean_for_embedding(window)
            text = f"{breadcrumb}\n\n{clean_body}".strip()

            chunk = Chunk(
                chunk_id=make_chunk_id(kb_path, h_path),
                text=text,
                kb_path=kb_path,
                heading_path=h_path,
                source_url=src_url,
                source_tier=src_tier,
                source_count=page_source_count,
                verified=verified,
                availability=availability,
                changed_note=page_changed_note,
                score=0.0,
            )
            chunks.append(chunk)

    return chunks
