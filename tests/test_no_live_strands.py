"""
HONESTY STATEMENT (HC-3):

This test covers the ~30 summary-reconstructible RECORDED URLs — specifically,
the source_url from each of the 30 summaries/*.md files. It does NOT cover all
38 keys in indexes/seen.json.

The ~8-key gap: seen.json tracks sha256(url) hexdigests, and the raw URL is
stored NOWHERE in the tree for those ~8 extra keys. They represent pure-nav /
EDSM-variant fetches (e.g. intermediate pagination, variant EDSM API calls) that
were recorded in seen.json but whose raw URLs never made it into a summary file.
Because there is no raw URL to reconstruct, this test cannot evaluate those keys
— it honestly covers only the ~30 URLs reconstructible from summaries/*.md.
"""

from pathlib import Path

import pytest

from copilot.commit_guard import committed_source_urls, find_stranded_urls
from copilot.paths import repo_root

# ---------------------------------------------------------------------------
# ACCEPTED_PAGELESS: explicit, hand-written string literals (HC-5 / I5 / AC-6).
# These 5 URLs are genuinely stranded (no own kb page cites them directly), but
# they are pageless-by-design — their content is merged into the BODY of
# kb/outfitting/mining-tools.md, which uses mining_laser.json as its single
# source_url. That page is structurally identical to kb/ships/python-mk-ii.md:
# one source_url for the absorbing page, multiple tools described in the body.
#
# This allow-list is NOT computed from find_stranded_urls; it is a deliberate,
# minimal, hand-curated set. Each entry has an inline comment that names the
# absorbing page and the body section that absorbs it.
# ---------------------------------------------------------------------------

ACCEPTED_PAGELESS: frozenset[str] = frozenset({
    # Absorbed in kb/outfitting/mining-tools.md § "Abrasion Blaster (surface deposits)"
    "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/abrasion_blaster.json",
    # Absorbed in kb/outfitting/mining-tools.md § "Pulse Wave Analyser (utility — find the rocks)"
    "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/pulse_wave_analyser.json",
    # Absorbed in kb/outfitting/mining-tools.md § "Seismic Charge Launcher (deep core)"
    "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/seismic_charge_launcher.json",
    # Absorbed in kb/outfitting/mining-tools.md § "Sub-Surface Displacement Missile (sub-surface)"
    "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/sub_surface_displacement_missile.json",
    # Absorbed in kb/outfitting/mining-tools.md § "Putting a miner together" (Collector Limpets — internal/)
    "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/collector_limpet_controllers.json",
})


# ---------------------------------------------------------------------------
# Read-only helper (I7 / HC-6): walks summaries/*.md, parses source_url from
# each file's frontmatter, returns the set. No writes, no network.
# ---------------------------------------------------------------------------

def _reconstruct_recorded_urls() -> set[str]:
    """Reconstruct the ~30 recorded URLs by reading summaries/*.md.

    Each summary file carries exactly one ``source_url:`` in its YAML
    frontmatter. Parsing is minimal: strip the value off the ``source_url:``
    line without a full YAML library (matches how _parse_frontmatter works).
    """
    root = repo_root()
    summaries_dir = root / "summaries"
    urls: set[str] = set()
    for md_file in sorted(summaries_dir.glob("*.md")):
        try:
            text = md_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        # Only scan the frontmatter fence (between opening --- and closing ---)
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end == -1:
            continue
        fence = text[3:end]
        for line in fence.splitlines():
            stripped = line.strip()
            if stripped.startswith("source_url:"):
                value = stripped[len("source_url:"):].strip().strip('"').strip("'")
                if value:
                    urls.add(value)
                break  # one source_url per summary; stop after first match
    return urls


# ===========================================================================
# T1 — Non-vacuity (I1 / HC-2a)
# ===========================================================================

def test_recorded_urls_nonvacuous():
    """The reconstructed URL pool must be >= 30; a zero count means the helper
    is broken and the rest of the test suite is vacuous (I1 / HC-2a)."""
    reconstructed = _reconstruct_recorded_urls()
    assert len(reconstructed) >= 30, (
        f"Expected >= 30 reconstructed recorded URLs from summaries/*.md, "
        f"got {len(reconstructed)}. The helper or the summaries/ directory is broken."
    )


# ===========================================================================
# T2/T3 — Tripwire: no live strands outside the allow-list (I2 / HC-2b)
# ===========================================================================

def test_no_live_strands_outside_allowlist():
    """Any stranded URL that is NOT in ACCEPTED_PAGELESS is a real F6 strand.

    This is the tripwire: it fails and names the offending URL(s). It does NOT
    fail for the known-pageless allow-listed entries (those are intentionally
    merged into kb/outfitting/mining-tools.md and do not need their own page).

    Subset invariant (I2): live_stranded(reconstructed) ⊆ ACCEPTED_PAGELESS.
    """
    reconstructed = _reconstruct_recorded_urls()
    assert len(reconstructed) >= 30, f"Non-vacuity guard: only {len(reconstructed)} URLs"

    root = repo_root()
    all_stranded = set(find_stranded_urls(reconstructed, repo_root=root))

    unexpected = all_stranded - ACCEPTED_PAGELESS
    assert not unexpected, (
        f"STRAND DETECTED — the following recorded URL(s) have no committed kb page "
        f"and are NOT in the accepted-pageless allow-list:\n"
        + "\n".join(f"  {u}" for u in sorted(unexpected))
        + "\nEach must either be committed (own source_url or feeder union) or "
          "added to ACCEPTED_PAGELESS with a comment naming the absorbing page."
    )


# ===========================================================================
# T3 — Complement committed (I3 / HC-2b)
# ===========================================================================

def test_non_allowlisted_recorded_all_committed():
    """Every recorded URL that is NOT in ACCEPTED_PAGELESS is committed.

    Complement invariant (I3): find_stranded_urls(reconstructed - ACCEPTED_PAGELESS) == [].
    This is the 'bite' assertion: it is what drives the test RED when a real
    commit or back-fill is reverted.
    """
    reconstructed = _reconstruct_recorded_urls()
    assert len(reconstructed) >= 30, f"Non-vacuity guard: only {len(reconstructed)} URLs"

    non_allowlisted = reconstructed - ACCEPTED_PAGELESS
    root = repo_root()
    stranded = find_stranded_urls(non_allowlisted, repo_root=root)
    assert stranded == [], (
        f"Recorded URLs outside the allow-list that are NOT committed: {stranded}. "
        "Either commit the pages or add them to ACCEPTED_PAGELESS with a comment."
    )


# ===========================================================================
# T4 — Allow-list minimality / liveness (I4)
# ===========================================================================

def test_allowlist_minimal_and_live():
    """Every ACCEPTED_PAGELESS entry is genuinely stranded right now (I4).

    This keeps the allow-list honest: a dead/bogus entry that is NOT actually
    stranded would silently mask a real future strand. The allow-list must
    contain ONLY entries that are currently stranded and pageless-by-design.

    NOTE: This is independent of test_no_live_strands_outside_allowlist — that
    test checks the complement; this one checks the allow-list itself.
    """
    root = repo_root()
    actually_stranded = set(find_stranded_urls(ACCEPTED_PAGELESS, repo_root=root))
    assert actually_stranded == ACCEPTED_PAGELESS, (
        f"ACCEPTED_PAGELESS allow-list integrity failure:\n"
        f"  Dead entries (in allow-list but NOT currently stranded — would mask real strands): "
        f"{ACCEPTED_PAGELESS - actually_stranded}\n"
        f"  Extra stranded (stranded but not yet in allow-list — this should not happen): "
        f"{actually_stranded - ACCEPTED_PAGELESS}"
    )


# ===========================================================================
# T5 — Revert-sensitivity (HC-4 / I8 / AC-3)
# ===========================================================================

def test_revert_sensitivity_red_on_dropped_backfill(monkeypatch):
    """HC-4: dropping a real committed URL makes the tripwire go RED.

    Strategy: monkeypatch committed_source_urls to return the live committed
    set MINUS mining_laser.json's source_url (kb/outfitting/mining-tools.md's
    own source_url). This simulates reverting that page's commit. With
    mining_laser.json removed from the committed set, that URL becomes stranded
    — it is in the reconstructed pool (summaries/ee41feeb-mining-laser.md) but
    no longer committed. It is also NOT in ACCEPTED_PAGELESS (only the 5
    content-merged sub-tools are allow-listed, not the absorbing page itself).

    The test asserts that the tripwire WOULD RAISE, proving AC-3 red-under-revert.
    No files are mutated; the live tree is unchanged (I7 / HC-6).
    """
    MINING_LASER_URL = (
        "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/mining_laser.json"
    )

    # Build the real committed set, then remove mining_laser to simulate a revert.
    real_committed = committed_source_urls(repo_root=repo_root())
    assert MINING_LASER_URL in real_committed, (
        f"Pre-condition failed: {MINING_LASER_URL} should be committed via "
        "kb/outfitting/mining-tools.md source_url — if it is missing the live tree changed."
    )

    simulated_committed = real_committed - {MINING_LASER_URL}

    # Monkeypatch commit_guard.committed_source_urls to return the reduced set.
    import copilot.commit_guard as cg
    monkeypatch.setattr(cg, "committed_source_urls", lambda **kwargs: simulated_committed)

    # Now run the tripwire logic using the patched committed set.
    reconstructed = _reconstruct_recorded_urls()
    assert MINING_LASER_URL in reconstructed, (
        "Pre-condition failed: mining_laser URL must be in the reconstructed pool "
        "(summaries/ee41feeb-mining-laser.md)."
    )

    all_stranded = set(cg.find_stranded_urls(reconstructed, repo_root=repo_root()))
    unexpected = all_stranded - ACCEPTED_PAGELESS

    assert MINING_LASER_URL in all_stranded, (
        "Revert-sensitivity broken: dropping mining_laser.json's committed URL "
        "did NOT cause it to appear as stranded."
    )
    assert MINING_LASER_URL in unexpected, (
        "Revert-sensitivity broken: mining_laser.json URL appeared stranded but "
        "was masked by ACCEPTED_PAGELESS (it should NOT be in the allow-list)."
    )
    # The key assertion: the tripwire condition IS triggered (unexpected is non-empty).
    # This is what would make test_no_live_strands_outside_allowlist go RED.
    assert unexpected, (
        "Revert-sensitivity broken: the tripwire would NOT have fired even after "
        "dropping a real committed URL. The test is vacuous."
    )
