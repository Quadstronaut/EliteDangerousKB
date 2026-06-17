# Loop 27 — search mode

## Spire-site target blocked → pivot

The queued top target (Thargoid Spire Site, Tier-2 Fandom prose) could not be acquired:

- **elite-dangerous.fandom.com** is Cloudflare-JS-challenged across the whole domain. The Fetcher
  receives a 5.6 KB `"Just a moment..."` interstitial (`__cf_chl_opt` / `cf-chl` managed challenge),
  not the article. Alternate slugs (`Thargoid_Spire`, `Spire_Site`) would hit the same wall — it is
  domain-wide, not a 404.
- The higher-trust fallback **api.canonn.tech** `ConnectTimeout`s (WinError 10060) — host unreachable
  from this environment this loop.

This is a **transient acquisition block, not obsolescence**. The Spire URL was therefore **not
recorded** in `seen.json` (no `record_source`, no `record_discard`) and stays **queued** (re-annotated
`BLOCKED`, demoted below the new reachable targets) for a later loop to retry. Because it was never
recorded, it is outside the F6 recorded-but-pageless strand mechanism — the F6 recovery sweep over the
two fully-processed URLs returned `[]` (parity confirmed).

## Pages written (never-idle pivot → two foundational Tier-0 ship gaps)

Both Tier-0 Coriolis (parsed directly, no LLM), each completing an existing sibling pair:

- **kb/ships/python.md** NEW (`python`, edID 128049339). Faulcon DeLacy, class 2 medium, no rank gate.
  3 Large + 2 Medium hardpoints (5 mounts), 4 utility, ten optionals (three class-6), no Military
  slots. baseShield/baseArmour 260/260, hardness 65, hullMass 350. Bidirectional link ↔
  [[ships/python-mk-ii]].
- **kb/ships/cobra-mk-iii.md** NEW (`cobra_mk_iii`, edID 128049279). Faulcon DeLacy, class 1 small,
  no rank gate. Cheapest hull in the KB (208,372 CR hull). 2 Medium + 2 Small hardpoints (4 mounts),
  2 utility, eight optionals (three class-4). speed 280/boost 400, roll 100 (nimblest in KB),
  hardness 35. Bidirectional link ↔ [[ships/cobra-mk-v]].

## VERIFY

Both pages are `source_count: 1` Tier-0 with no `<!-- CONFLICT -->` markers → no claim meets the
council trigger (`source_count >= 2` OR conflict). No escalation. Both correctly stay
`verified: false` until an independent source corroborates.

## Follow-ons queued (reachable Tier-0, promoted to top)

- Asp Explorer (`ships/asp_explorer.json`) — explorer sibling of the Mandalay.
- Fer-de-Lance (`ships/fer_de_lance.json`) — premier medium combat, one Huge on a medium hull.
- Thargoid Spire Site — stays queued (BLOCKED) for retry.
