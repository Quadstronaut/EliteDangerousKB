"""
AC-4 corpus invariant: every merged kb page's RECORDED feeder URLs
(source_urls frontmatter) are committed via the union — and the EXPECTED feeder
set (the deliberate mapping from the summaries ledger) is present.

REVERT-SENSITIVITY (AC-4): the expected feeders are pinned here as an explicit
set drawn from summaries/. The invariant is asserted against THAT pinned set, so
removing any merged page's source_urls back-fill leaves a pinned feeder
uncommitted in the union -> find_stranded_urls flags it -> the test FAILS.
A self-referential "gather feeders, assert none stranded" check is NOT enough
(removing a back-fill removes it from both sides); pinning the expected set is
what makes the test bite.
"""
from copilot import commit_guard
from copilot.paths import repo_root


# The deliberate feeder mapping, drawn from the summaries ledger (summaries/),
# verified against the merged-page bodies (NOT a topic-substring guess). Each
# URL here must be committed via the union (own source_url OR a source_urls list).
EXPECTED_FEEDERS: set[str] = {
    # deciat.md (edsm system + 4 station/service endpoints)
    "https://www.edsm.net/api-system-v1/stations?systemName=Deciat",
    "https://www.edsm.net/api-system-v1/stations/market?systemName=Deciat&stationName=Farseer%20Inc",
    "https://www.edsm.net/api-system-v1/stations/shipyard?marketId=3229756160",
    "https://www.edsm.net/api-system-v1/stations/outfitting?marketId=3229756160",
    # hip-23759.md
    "https://www.edsm.net/api-system-v1/stations?systemName=HIP%2023759",
    "https://www.edsm.net/api-system-v1/stations/market?systemName=HIP%2023759&stationName=Witch%20Head%20Science%20Centre",
    # shield-generator.md (bi-weave + prismatic feeders)
    "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/bi_weave_shield_generator.json",
    "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/pristmatic_shield_generator.json",
    # mechanics/frame-shift-drive.md (coriolis FSD module data — also an own source_url)
    "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/standard/frame_shift_drive.json",
}


def _all_feeders() -> list[str]:
    root = repo_root()
    feeders: list[str] = []
    for page in (root / "kb").rglob("*.md"):
        text = page.read_text(encoding="utf-8")
        feeders.extend(commit_guard._read_frontmatter_source_urls(text))
    return feeders


def test_live_kb_expected_feeders_all_committed():
    """The pinned EXPECTED feeder set is committed via the union. Removing any
    merged page's source_urls back-fill strands the feeders it uniquely commits
    and FAILS this test (revert-sensitive)."""
    stranded = commit_guard.find_stranded_urls(
        sorted(EXPECTED_FEEDERS), repo_root=repo_root()
    )
    assert stranded == [], f"expected feeders not committed via union: {stranded}"


def test_live_kb_declared_feeders_all_committed():
    """Corpus consistency: every feeder a page actually DECLARES is also committed
    (no page lists a feeder that nothing commits)."""
    feeders = _all_feeders()
    assert feeders, "no source_urls feeders found in live kb/ — back-fill missing"
    stranded = commit_guard.find_stranded_urls(feeders, repo_root=repo_root())
    assert stranded == [], f"declared feeders not committed via union: {stranded}"


def test_live_kb_merged_pages_declare_expected_feeders():
    """Each known merged page declares its expected feeders inline (revert-
    sensitive at the per-page level)."""
    root = repo_root()
    expect = {
        "locations/deciat.md": {
            "https://www.edsm.net/api-system-v1/stations?systemName=Deciat",
            "https://www.edsm.net/api-system-v1/stations/market?systemName=Deciat&stationName=Farseer%20Inc",
            "https://www.edsm.net/api-system-v1/stations/shipyard?marketId=3229756160",
            "https://www.edsm.net/api-system-v1/stations/outfitting?marketId=3229756160",
        },
        "locations/hip-23759.md": {
            "https://www.edsm.net/api-system-v1/stations?systemName=HIP%2023759",
            "https://www.edsm.net/api-system-v1/stations/market?systemName=HIP%2023759&stationName=Witch%20Head%20Science%20Centre",
        },
        "outfitting/shield-generator.md": {
            "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/bi_weave_shield_generator.json",
            "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/pristmatic_shield_generator.json",
        },
        "mechanics/frame-shift-drive.md": {
            "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/standard/frame_shift_drive.json",
        },
        "engineers/felicity-farseer.md": {
            "https://www.edsm.net/api-system-v1/stations/market?systemName=Deciat&stationName=Farseer%20Inc",
            "https://www.edsm.net/api-system-v1/stations/market?systemName=HIP%2023759&stationName=Witch%20Head%20Science%20Centre",
        },
    }
    for rel, must_have in expect.items():
        text = (root / "kb" / rel).read_text(encoding="utf-8")
        declared = set(commit_guard._read_frontmatter_source_urls(text))
        missing = must_have - declared
        assert not missing, f"{rel} missing expected feeders: {missing}"
