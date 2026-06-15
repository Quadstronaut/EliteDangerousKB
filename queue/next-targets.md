# Research Queue — next targets

One target per bullet. The orchestrator takes the top 1-3 each loop, dedups against
seen.json, and processes Tier-0 first. Append follow-on targets discovered during synthesis.

- https://www.edsm.net/api-system-v1/stations/outfitting?marketId=3229756160 (tier: 0, type: edsm, note: enumerate Garay Terminal's OUTFITTING module list — corroborate the page's "Outfitting" service claim and document what modules a Farseer visitor can actually buy in-system -> kb/locations/deciat.md "Station Services — large-pad & outfit ports")
- https://raw.githubusercontent.com/EDCD/coriolis-data/master/dist/ships.json (tier: 0, type: coriolis, note: extract the Cobra Mk V hull stats — surfaced as recent stock at Garay Terminal but likely missing a kb/ships/ page; create kb/ships/cobra-mk-v.md from Coriolis fields)

<!-- DONE loop 5: EDSM api-system-v1/stations/shipyard enumerated for Garay Terminal (marketId 3229756160).
     Findings: 17 hulls stocked, incl. recent Type-8 Transporter, Cobra Mk V, Panther Clipper Mk II,
     Type-11 Prospector (confirms current post-2024 roster). Largest: Type-9 Heavy & Panther Clipper Mk II.
     Third independent EDSM endpoint confirming Garay carries a Shipyard -> merged H3 "Garay Terminal —
     shipyard stock" into kb/locations/deciat.md, source_count 2->3, verified true. -->


<!-- DONE loop 4: EDSM api-system-v1/stations enumerated for Deciat (id64 6681123623626).
     Findings: Garay Terminal (Coriolis Starport, marketId 3229756160) is the ONLY large-pad
     orbital port in-system, ~2042 ls, with Market + Shipyard + Outfitting — the restock/outfit/
     shipyard hub for Farseer visitors. Matteucci Dock & Carson Hub are medium-pad Outposts
     (Market+Outfitting, no shipyard); Kirtley Vision/Hasse Point are Planetary Outposts at ~62 ls.
     Merged into kb/locations/deciat.md new H2 "Station Services — large-pad & outfit ports". -->


<!-- DONE loop 3: EDSM Farseer Inc stations/market corroborated -> kb/locations/deciat.md (source_count 2,
     verified) + kb/engineers/felicity-farseer.md aligned. Findings: Farseer Inc market is SELL-ONLY
     (buyPrice 0 / stock 0 across all commodities); Meta-Alloys NOT buyable there (demand 0). Fixed
     stale "Coles Point" ref in felicity-farseer.md -> Witch Head Science Centre ([[locations/hip-23759]]). -->

<!-- DONE loop 2: HIP 23759 stations+market corroborated -> kb/locations/hip-23759.md verified.
     Correction: no "Coles Point" station exists; the Meta-Alloy market is the Witch Head Science
     Centre asteroid base (Meta-Alloys buyPrice ~148,408 cr, BGS-driven stock). -->
