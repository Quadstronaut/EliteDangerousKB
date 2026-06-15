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
# Table detection and section splitting (Decision B: KEEP-ATOMIC)
# ---------------------------------------------------------------------------

# A GFM table header row: starts with |, ends with |, contains text cells.
_TABLE_HEADER_RE = re.compile(r"^\|.+\|[ \t]*$", re.MULTILINE)

# A GFM table delimiter row: only |, -, :, spaces, tabs.
_TABLE_DELIM_RE = re.compile(r"^\|[\s|:\-]+\|[ \t]*$", re.MULTILINE)


def _is_table_block(text: str) -> bool:
    """Return True if *text* contains a GFM table (header + delimiter + >=1 data row).

    Detects: a line matching |...| (header), followed by a line matching
    |---|---| (delimiter), followed by at least one more |...| line (data).
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        # Look for a header-like row
        if not (line.strip().startswith("|") and line.strip().endswith("|")):
            continue
        # Next non-empty line should be a delimiter row
        for j in range(i + 1, len(lines)):
            nxt = lines[j]
            if not nxt.strip():
                continue  # skip blanks between header and delim
            if _TABLE_DELIM_RE.match(nxt.strip()):
                # Look for at least one data row after the delimiter
                for k in range(j + 1, len(lines)):
                    data = lines[k]
                    if not data.strip():
                        continue
                    if data.strip().startswith("|") and data.strip().endswith("|"):
                        return True  # header + delim + data found
                    break  # non-pipe line after delim — not a table
            break  # first non-blank after header was not a delimiter
    return False


def _extract_table_blocks(text: str) -> list[tuple[int, int]]:
    """Return list of (start_line, end_line) ranges (inclusive) for each GFM table in *text*.

    A table block is: optional leading blank lines, then header row, delimiter
    row, and contiguous data rows. The range covers header through last data row.
    """
    lines = text.splitlines()
    blocks: list[tuple[int, int]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        # Candidate table header
        if stripped.startswith("|") and stripped.endswith("|"):
            # Scan ahead for delimiter
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and _TABLE_DELIM_RE.match(lines[j].strip()):
                # Found header at i, delimiter at j — collect data rows
                k = j + 1
                while k < len(lines):
                    dline = lines[k].strip()
                    if dline.startswith("|") and dline.endswith("|"):
                        k += 1
                    elif not dline:
                        # blank line — peek ahead to see if more table rows follow
                        # GFM tables end at the first blank line normally, but we
                        # stop here to be conservative (safe for spec).
                        break
                    else:
                        break
                if k > j + 1:  # at least one data row
                    blocks.append((i, k - 1))
                    i = k
                    continue
        i += 1
    return blocks


def _split_section_preserving_tables(
    section_body: str,
    min_tok: int,
    max_tok: int,
    overlap: float,
) -> list[str]:
    """Split *section_body* into windows, keeping any GFM table(s) intact.

    Algorithm:
      1. Find all table blocks in the section (line ranges).
      2. Split the section into non-table prose segments and table segments.
      3. Window each prose segment normally with _window_text.
      4. Emit each table segment as a single chunk (never windowed), even if
         it exceeds max_tok — this is the KEEP-ATOMIC guarantee.
      5. Return segments in their original order.

    If the section contains no table, falls back to _window_text normally.
    """
    if not _is_table_block(section_body):
        if _approx_tokens(section_body) > max_tok:
            return _window_text(section_body, min_tok, max_tok, overlap)
        return [section_body]

    lines = section_body.splitlines(keepends=True)
    table_ranges = _extract_table_blocks(section_body)
    if not table_ranges:
        # Detection said yes but extraction found nothing — fall back.
        if _approx_tokens(section_body) > max_tok:
            return _window_text(section_body, min_tok, max_tok, overlap)
        return [section_body]

    # Build a set of line indices belonging to tables.
    table_line_set: set[int] = set()
    for start, end in table_ranges:
        for li in range(start, end + 1):
            table_line_set.add(li)

    # Walk lines, collecting runs of prose vs table.
    # Each "segment" is (is_table: bool, text: str).
    segments: list[tuple[bool, str]] = []
    prose_buf: list[str] = []

    def _flush_prose():
        if prose_buf:
            segments.append((False, "".join(prose_buf)))
            prose_buf.clear()

    in_table = False
    table_start: int = 0
    for idx, line in enumerate(lines):
        if idx in table_line_set:
            if not in_table:
                _flush_prose()
                in_table = True
                table_start = idx
            # Accumulate table line into the current table segment.
            # We'll emit the whole table when it ends.
        else:
            if in_table:
                # End of current table — find the range and emit.
                # Collect the table lines we just passed.
                for start, end in table_ranges:
                    if start == table_start:
                        table_text = "".join(lines[start: end + 1])
                        segments.append((True, table_text))
                        break
                in_table = False
            prose_buf.append(line)

    if in_table:
        for start, end in table_ranges:
            if start == table_start:
                table_text = "".join(lines[start: end + 1])
                segments.append((True, table_text))
                break
    else:
        _flush_prose()

    # Now emit windows for each segment.
    result: list[str] = []
    for is_table, seg_text in segments:
        if is_table:
            # KEEP-ATOMIC: always emit table as one chunk, regardless of size.
            result.append(seg_text)
        else:
            seg_stripped = seg_text.strip()
            if not seg_stripped:
                continue
            if _approx_tokens(seg_stripped) > max_tok:
                result.extend(_window_text(seg_stripped, min_tok, max_tok, overlap))
            else:
                result.append(seg_stripped)

    return result if result else [section_body]


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
    # For a path like .../kb/engineers/file.md we want kb/engineers/file.md.
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

        # Window if needed, preserving any GFM tables as atomic chunks.
        windows = _split_section_preserving_tables(
            section_body, cfg_min, cfg_max, cfg_overlap
        )

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
