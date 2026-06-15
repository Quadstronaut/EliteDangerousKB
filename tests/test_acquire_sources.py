"""Roster sanity (A8). Pure data assertions; no network."""
from copilot.acquire_sources import (
    ED_SOURCES,
    VALID_KINDS,
    default_allowlist,
    source_for_url,
)


def test_default_allowlist_is_union_of_source_domains():
    union = []
    for src in ED_SOURCES:
        for dom in src.domains:
            if dom not in union:
                union.append(dom)
    assert default_allowlist() == tuple(union)
    # no duplicates
    assert len(default_allowlist()) == len(set(default_allowlist()))


def test_source_for_url_edsm_tier0():
    src = source_for_url("https://www.edsm.net/api-v1/system")
    assert src is not None
    assert src.key == "edsm"
    assert src.tier == 0


def test_source_for_url_subdomain_match():
    assert source_for_url("https://www.edsm.net/x").key == "edsm"
    assert source_for_url("https://edsm.net/x").key == "edsm"


def test_source_for_url_off_roster_is_none():
    assert source_for_url("https://www.reddit.com/r/Elite") is None
    assert source_for_url("https://evil.example/x") is None
    assert source_for_url("not a url") is None


def test_every_source_has_robots_note_and_valid_kind():
    for src in ED_SOURCES:
        assert src.robots_note.strip(), f"{src.key} missing robots_note"
        assert src.kind in VALID_KINDS, f"{src.key} bad kind {src.kind}"
        assert 0 <= src.tier <= 3, f"{src.key} bad tier {src.tier}"
        assert src.domains, f"{src.key} has no domains"
        assert src.polite_min_interval >= 0


def test_keys_are_unique():
    keys = [s.key for s in ED_SOURCES]
    assert len(keys) == len(set(keys))


def test_reddit_not_in_default_allowlist():
    # Tier-3 corroboration only; deliberately scoped OUT of the fetch allowlist.
    al = default_allowlist()
    assert not any("reddit" in d for d in al)
