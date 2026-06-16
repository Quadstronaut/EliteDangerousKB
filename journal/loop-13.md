# Loop 13 journal

## F6 strand — RESOLVED (false positive from a merged page)

- F6 RECOVERY (auto): re-queued stranded source
  https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/meta_alloy_hull_reinforcement_package.json
  (recorded in seen.json but no committed page; purged seen marker so the loop revisits it).

- ROOT CAUSE: the Meta-Alloy HRP source was **merged** into `kb/outfitting/hull-reinforcement.md`
  (whose single `source_url` is the *standard* HRP file), so the guard's `committed_source_urls`
  found no page citing the mahr URL and flagged it stranded. This was a **false positive** — the
  source WAS synthesized, just merged rather than given its own page.

- FIX (this loop, before commit): added the merged-page feeder list
  `source_urls: ["<standard hrp>", "<meta-alloy hrp>"]` to hull-reinforcement.md's frontmatter —
  the exact provenance mechanism the guard reads for merged pages (commit_guard.py K1/C1). Then:
  re-recorded the mahr source in seen.json (page now legitimately cites it), removed the
  auto-re-queued mahr bullet from queue/next-targets.md, and re-ran the index.
  `find_stranded_urls([...]) == []` afterwards; mahr ∈ `committed_source_urls()`.

- TAKEAWAY for future merges: a merged page MUST declare every feeder URL in a single-line
  `source_urls: [...]` flow list, or the F6 guard will treat the merged-away source as stranded.
