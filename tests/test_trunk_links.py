"""
F4 regression guard — kb/trunk.md is a navigation hub, so every wikilink it
carries MUST resolve to a real kb page. A dangling link from the hub is a
broken table of contents.

This guard is scoped to trunk.md ONLY. The genuinely-dangling cross-page
forward-references that live in *content* pages (kb/outfitting/cargo-rack.md's
[[ax-thargoid]], kb/ships/type-9-heavy.md's [[trailblazers]],
kb/outfitting/mining-tools.md's [[mechanics/powerplay]]) are intentional and are
NOT checked here — they are forward-references to pages the loop has yet to
write, and the spec explicitly puts them out of scope.
"""
import re
from pathlib import Path

import pytest

from copilot.paths import repo_root

# [[target]] or [[target|alias]] — capture the link target before any '|'.
_WIKILINK_RE = re.compile(r"\[\[([^\]\|]+?)(?:\|[^\]]*)?\]\]")


def _kb_dir() -> Path:
    return repo_root() / "kb"


def _resolve(target: str, kb: Path) -> Path | None:
    """Resolve a wikilink target (kb-relative, no extension) to a .md path.

    'ships/python-mk-ii' -> kb/ships/python-mk-ii.md
    'trunk'              -> kb/trunk.md
    Returns the resolved path if it exists, else None.
    """
    target = target.strip()
    candidate = (kb / f"{target}.md").resolve()
    # Containment: never let a crafted '../' target escape kb/.
    kb_resolved = kb.resolve()
    try:
        candidate.relative_to(kb_resolved)
    except ValueError:
        return None
    return candidate if candidate.exists() else None


def test_trunk_md_exists():
    assert (_kb_dir() / "trunk.md").exists(), "kb/trunk.md missing"


def test_every_trunk_wikilink_resolves():
    """Every [[wikilink]] in trunk.md points at an existing kb page."""
    kb = _kb_dir()
    trunk = (kb / "trunk.md").read_text(encoding="utf-8")

    targets = _WIKILINK_RE.findall(trunk)
    assert targets, "trunk.md has no wikilinks — sanity check failed"

    dangling = [t for t in targets if _resolve(t, kb) is None]
    assert not dangling, (
        "trunk.md wikilinks do not resolve to existing kb pages: " + ", ".join(dangling)
    )


def test_trunk_self_backlink_targets_present():
    """The two F4 backlink targets actually carry the [[trunk]] backlink."""
    kb = _kb_dir()
    for rel in ("mechanics/frame-shift-drive.md", "ships/python-mk-ii.md"):
        text = (kb / rel).read_text(encoding="utf-8")
        assert text.rstrip().endswith("[[trunk]]"), (
            f"{rel} must end with a [[trunk]] backlink"
        )


def test_trunk_is_not_verified_sourced_fact():
    """trunk.md is a navigation hub — it must not assert verified:true with a
    single source. F4: set verified:false (or drop the key) — no fabricated 2nd
    source."""
    text = (_kb_dir() / "trunk.md").read_text(encoding="utf-8")
    # Frontmatter is the block between the first two '---' fences.
    fm = text.split("---", 2)[1] if text.startswith("---") else ""
    verified_true = re.search(r"^\s*verified:\s*true\s*$", fm, re.MULTILINE)
    source_count_one = re.search(r"^\s*source_count:\s*1\s*$", fm, re.MULTILINE)
    assert not (verified_true and source_count_one), (
        "trunk.md still asserts verified:true with source_count:1 — a navigation "
        "hub is not a sourced fact page; set verified:false."
    )


def test_dangling_forward_refs_not_in_trunk():
    """The intentional forward-refs must NOT have leaked into trunk.md (they live
    only in their content pages and are out of scope for this guard)."""
    text = (_kb_dir() / "trunk.md").read_text(encoding="utf-8")
    for forward in ("[[ax-thargoid]]", "[[trailblazers]]", "[[mechanics/powerplay]]"):
        assert forward not in text, (
            f"{forward} is an intentional content-page forward-ref; it must not "
            "appear in trunk.md (which would make this guard flag it)."
        )
