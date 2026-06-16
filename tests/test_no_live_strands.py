"""Regression tripwire: no NEW pageless strands sneak into the live tree.

HONESTY (HC-3) — what this test does and does NOT cover
-------------------------------------------------------
This guard covers the ~30 summary-RECONSTRUCTIBLE recorded URLs: the raw source
URLs that can be read back out of ``summaries/*.md`` frontmatter. Each summary
carries exactly one ``source_url:``, so the summaries store is the ONLY place a
RAW recorded URL survives in the tree. There are 30 such files -> 30
reconstructible URLs.

It does NOT cover all 38 ``indexes/seen.json`` keys, and it does not claim to.
seen.json stores ``sha256(url)`` hexdigests, NOT the raw URL, so a seen key
whose URL appears nowhere else in the tree CANNOT be reconstructed here. ~8 of
the 38 keys are exactly that class — pure-navigation / EDSM-variant fetches
that were crawled but never summarised and never paged, so their raw URL exists
NOWHERE in the tree (not in summaries/, not in kb/). Those 8 are out of scope by
construction, not by oversight. The complementary dimension — committed FEEDER
frontmatter (``source_urls:``) — is pinned separately by
``tests/test_kb_feeders.py`` (EXPECTED_FEEDERS). Here we guard the recorded-URL
dimension.

THE BITE (the recorded dissent gen-sonnet-3 wanted closed)
----------------------------------------------------------
A future research loop could quietly GROW the pool of done-but-pageless seen
keys and re-introduce the F6 strand class with no test catching it. This file
pins an explicit, minimal, HAND-WRITTEN allow-list of the URLs that are pageless
*by design* (content-merged into an absorbing page, never their own page). Any
recorded URL that ends up stranded and is NOT on that allow-list fails the gate
and is named in the assertion message.

The allow-list is NOT snapshotted from ``find_stranded_urls`` output (that would
be self-referential and vacuous — a new strand would just be absorbed into the
snapshot). It is written by hand, each entry justified against the body of its
absorbing page, and independently checked for liveness/minimality.
"""
from __future__ import annotations

import pytest

from copilot import commit_guard
from copilot.chunker import _parse_frontmatter
from copilot.paths import repo_root


# ---------------------------------------------------------------------------
# Allow-list: pageless-BY-DESIGN recorded URLs (HAND-WRITTEN literals — I5/T4)
# ---------------------------------------------------------------------------
# Each URL below is a recorded source (it has a summaries/ entry) that has NO kb
# page of its own and is NOT feeder-union-committed (the absorbing page declares
# no ``source_urls:`` list). It is instead CONTENT-MERGED into the body of
# kb/outfitting/mining-tools.md — structurally identical to the named-immune
# kb/ships/python-mk-ii.md (single source_url, multi-fact body). That page's own
# ``source_url`` is mining_laser.json; these five sub-tools live only in its prose.
#
# These are explicit string literals, NOT computed from find_stranded_urls. Each
# carries a comment naming the absorbing page and the body section that absorbs it.
# test_allowlist_minimal_and_live independently verifies every entry is genuinely
# stranded right now, so no dead/bogus entry can hide a future real strand.
ACCEPTED_PAGELESS: frozenset[str] = frozenset(
    {
        # kb/outfitting/mining-tools.md — "## Abrasion Blaster (surface deposits)"
        "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/abrasion_blaster.json",
        # kb/outfitting/mining-tools.md — "## Pulse Wave Analyser (utility — find the rocks)"
        "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/pulse_wave_analyser.json",
        # kb/outfitting/mining-tools.md — "## Seismic Charge Launcher (deep core)"
        "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/seismic_charge_launcher.json",
        # kb/outfitting/mining-tools.md — "## Sub-Surface Displacement Missile (sub-surface)"
        "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/sub_surface_displacement_missile.json",
        # kb/outfitting/mining-tools.md — "Collector Limpets" (body refs: intro + Abrasion + assembly)
        # NOTE: collector_ (internal/), NOT prospector_ — prospector has its own committed page.
        "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/collector_limpet_controllers.json",
    }
)


# ---------------------------------------------------------------------------
# Read-only helper: reconstruct the recorded raw URLs from summaries/ (I7)
# ---------------------------------------------------------------------------

def _reconstruct_recorded_urls() -> set[str]:
    """Walk ``summaries/*.md`` and return the set of recorded raw source URLs.

    Each summary carries exactly one ``source_url:`` frontmatter key — the raw
    URL that was crawled. The summaries store is the ONLY place a raw recorded
    URL survives, so this is the reconstructible-URL universe (~30 of 38 seen
    keys). Read-only: no writes, no network, no seen.json access.
    """
    root = repo_root()
    urls: set[str] = set()
    for summary in sorted((root / "summaries").glob("*.md")):
        meta, _body = _parse_frontmatter(summary.read_text(encoding="utf-8"))
        src = meta.get("source_url")
        if isinstance(src, str) and src:
            urls.add(src)
    return urls


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_recorded_urls_nonvacuous():
    """I1: a run that reconstructs 0 URLs has failed its own purpose. There are
    30 summaries each with one source_url, so >= 30 is the live floor."""
    recorded = _reconstruct_recorded_urls()
    assert len(recorded) >= 30, (
        f"only {len(recorded)} recorded URLs reconstructed from summaries/ "
        "(expected >= 30) — the tripwire would be vacuous"
    )


def test_no_live_strands_outside_allowlist():
    """I2 (the tripwire): every URL currently stranded against the live tree is
    on the hand-written allow-list. A stranded URL NOT on the allow-list is a
    new F6 strand and is named in the failure message."""
    recorded = _reconstruct_recorded_urls()
    stranded = set(
        commit_guard.find_stranded_urls(sorted(recorded), repo_root=repo_root())
    )
    rogue = sorted(stranded - ACCEPTED_PAGELESS)
    assert not rogue, (
        "NEW pageless strand(s) outside the by-design allow-list - a recorded "
        "source has no committed page and no allow-list justification: "
        f"{rogue}"
    )


def test_non_allowlisted_recorded_all_committed():
    """I3 (the complement is fully committed): every recorded URL that is NOT on
    the allow-list has a committed page (own source_url or feeder union), i.e.
    find_stranded_urls(recorded - allow-list) is empty."""
    recorded = _reconstruct_recorded_urls()
    target = sorted(recorded - ACCEPTED_PAGELESS)
    stranded = commit_guard.find_stranded_urls(target, repo_root=repo_root())
    assert stranded == [], (
        "recorded URL(s) outside the allow-list are not committed via the "
        f"union (own source_url OR source_urls feeder): {stranded}"
    )


def test_allowlist_minimal_and_live():
    """I4 (minimality/liveness): every allow-list entry is genuinely stranded
    against the current live tree. No dead/bogus entry that could later mask a
    real strand. Asserted independently of the tripwire's subset/complement
    checks, so the tripwire never becomes self-referential."""
    stranded = set(
        commit_guard.find_stranded_urls(
            sorted(ACCEPTED_PAGELESS), repo_root=repo_root()
        )
    )
    dead = sorted(ACCEPTED_PAGELESS - stranded)
    assert not dead, (
        "allow-list entr(y/ies) are NOT actually stranded (committed elsewhere "
        f"or bogus) — would mask a future real strand: {dead}"
    )
    # And nothing leaks the other way: feeding only the allow-list yields exactly
    # the allow-list (it is closed under find_stranded_urls), so each entry is
    # accounted for, none silently dropped.
    assert stranded == set(ACCEPTED_PAGELESS), (
        f"allow-list is not its own stranded set: extra={sorted(stranded - ACCEPTED_PAGELESS)}, "
        f"missing={sorted(ACCEPTED_PAGELESS - stranded)}"
    )


def test_allowlist_pin_fidelity():
    """I9: the allow-list is EXACTLY the 5 verified-live URLs, and it pins
    collector_ (internal/), NOT prospector_ — prospector has its own committed
    page and must never appear here."""
    assert len(ACCEPTED_PAGELESS) == 5, (
        f"allow-list must hold exactly 5 entries, has {len(ACCEPTED_PAGELESS)}"
    )
    collector = (
        "https://raw.githubusercontent.com/EDCD/coriolis-data/master/"
        "modules/internal/collector_limpet_controllers.json"
    )
    prospector = (
        "https://raw.githubusercontent.com/EDCD/coriolis-data/master/"
        "modules/internal/prospector_limpet_controllers.json"
    )
    assert collector in ACCEPTED_PAGELESS, "collector_limpet_controllers must be pinned"
    assert prospector not in ACCEPTED_PAGELESS, (
        "prospector_limpet_controllers must NOT be pinned — it has its own page"
    )


def test_revert_sensitivity_red_on_dropped_backfill(monkeypatch):
    """I8 / HC-4 (the proof the gate BITES): drop a real committed back-fill —
    here mining-tools.md's own source_url (mining_laser.json) — via monkeypatch,
    and show the tripwire would go RED.

    mining_laser.json is BOTH a recorded URL (it has a summary) AND committed (it
    is the absorbing page's own source_url). It is therefore NOT on the
    by-design allow-list. Removing it from the committed set turns it into a
    stranded URL OUTSIDE the allow-list — exactly the condition
    test_no_live_strands_outside_allowlist guards. We reproduce that test's
    assertion here and confirm it RAISES.

    monkeypatch (a pytest fixture) restores the real function after the test, so
    the live tree and seen.json are never mutated (I7)."""
    mining_laser = (
        "https://raw.githubusercontent.com/EDCD/coriolis-data/master/"
        "modules/hardpoints/mining_laser.json"
    )

    recorded = _reconstruct_recorded_urls()
    assert mining_laser in recorded, (
        "precondition: mining_laser.json must be a recorded (summarised) URL"
    )
    # Sanity: with the real tree it is committed and thus NOT stranded.
    assert mining_laser not in set(
        commit_guard.find_stranded_urls(sorted(recorded), repo_root=repo_root())
    ), "precondition: mining_laser.json must be committed in the live tree"

    # REVERT: monkeypatch committed_source_urls to drop the back-filled URL.
    # find_stranded_urls calls commit_guard.committed_source_urls(...) by name,
    # so patching the module attribute is observed by the guard.
    _real_committed = commit_guard.committed_source_urls

    def _committed_without_mining_laser(**kwargs):
        committed = _real_committed(**kwargs)
        committed.discard(mining_laser)
        return committed

    monkeypatch.setattr(
        commit_guard, "committed_source_urls", _committed_without_mining_laser
    )

    # Now the tripwire's assertion must FAIL: mining_laser becomes a strand that
    # is NOT on the allow-list.
    stranded = set(
        commit_guard.find_stranded_urls(sorted(recorded), repo_root=repo_root())
    )
    rogue = stranded - ACCEPTED_PAGELESS
    assert mining_laser in rogue, (
        "revert did not surface mining_laser.json as a rogue strand — the "
        "tripwire is NOT revert-sensitive (HC-4 BLOCKER)"
    )

    # Demonstrate the tripwire goes RED, executably: the same assertion
    # test_no_live_strands_outside_allowlist makes must raise here.
    with pytest.raises(AssertionError):
        assert not sorted(stranded - ACCEPTED_PAGELESS), (
            f"NEW pageless strand(s) outside the allow-list: "
            f"{sorted(stranded - ACCEPTED_PAGELESS)}"
        )
