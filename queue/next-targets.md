# Research Queue — next targets

One target per bullet. The orchestrator takes the top 1-3 each loop, dedups against
seen.json, and processes Tier-0 first. Append follow-on targets discovered during synthesis.

- https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/index.js (tier: 0, type: coriolis, note: enumerate mining-tool module slugs — mining laser, abrasion blaster, seismic charge launcher, sub-surface displacement missile, pulse wave analyser — to seed kb/outfitting/ mining-tool pages now that kb/ships/type-11-prospector.md exists but kb/outfitting/ has no mining tools. Confirm real module JSON paths from the index before fetching, as ships/index.js keys differed from filenames in loops 6-7.)
- https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/index.js (tier: 0, type: coriolis, note: also map standard-module slugs for Frame Shift Drive + FSD(SCO) + fuel scoop to seed kb/outfitting/ core-module pages — supports the new Mandalay explorer and Type-9 Heavy hauler builds. Same path-vs-key caution.)

<!-- DONE loop 8: 3 Coriolis Tier-0 ship hulls created (all current, availability: live):
     (1) kb/ships/type-11-prospector.md — Lakon, class 2/MEDIUM pad, dedicated miner. 320t hull,
     275 MJ shield, 350 armour, hardness 58, PD class 7 (sustains mining tools). 8 hardpoints =
     4 mining-tool-only (3,2,2,1) + 4 general (2,1,1,1); class-5 limpet-only bay + class-5 fighter
     bay; optionals 6,6,6,5,5,4,3,2,1,1. Hull 66.3M CR. Stocked at Garay Terminal (loop 5).
     (2) kb/ships/mandalay.md — Zorgon Peterson, class 2/MEDIUM pad, long-range explorer. Light
     230t hull + class-5 FSD; roll 96 (very nimble); 4M+2S hardpoints; optionals 6,5,4,4,3,3,2,1,1,1.
     Hull 16.5M CR.
     (3) kb/ships/type-9-heavy.md — Lakon, class 3/LARGE pad, bulk hauler. 850t, slow (yaw 8),
     twin class-8 optionals = ~1,580 t theoretical max cargo; 480 armour; 3M+2S hardpoints. Hull
     72.1M CR. Stocked at Garay Terminal (loop 5). All 3 linked in trunk.md Ships section.
     CONFIRMED via ships/index.js: filenames type_11_prospector / mandalay / type_9_heavy all match
     queue paths (no stale-slug 404 this loop). -->


<!-- DONE loop 7: (1) Coriolis Panther Clipper Mk II hull -> kb/ships/panther-clipper-mk-ii.md
     (Zorgon Peterson, class 3/Large pad, 1200t hull, 350 MJ shield, 620 armour, hardness 70,
     PP/Thr C8, FSD C7, twin C8 + twin C7 optionals incl. 2 cargo-restricted = largest cargo ship,
     2L+4M+4S hardpoints, 6 utility, crew 4, fighter hangar). CORRECTION: queue's stale slugs
     panther_clipper_mk_ii.json AND type_8.json both 404; correct Tier-0 paths per ships/index.js
     are ships/panther_clipper.json (key panthermkii) and ships/type_8_transport.json (key
     type_8_transport). (2) Coriolis Type-8 Transporter hull -> kb/ships/type-8-transporter.md
     (Lakon, class 2/Medium pad, 400t hull, 228 MJ shield, 440 armour, FSD C5, C7+3xC6 optionals =
     best medium-pad hauler, 1M+5S hardpoints, 4 utility, crew 1). Both linked in trunk.md. -->


<!-- DONE loop 6: (1) EDSM api-system-v1/stations/outfitting for Garay Terminal (marketId 3229756160).
     653 module SKUs / 107 families. Full core internals to C8; FSD + FSD(SCO) to C7; Shield & Bi-Weave
     to C8; limpets/refinery/AFMU; weapons capped ~C4; NO Guardian modules (expected). Merged H3
     "Garay Terminal — outfitting stock" into kb/locations/deciat.md, source_count 3->4, verified true.
     (2) Coriolis Cobra Mk V hull -> created kb/ships/cobra-mk-v.md. CORRECTION: queue's stale
     dist/ships.json 404s (dist/index.json is build-generated, not committed); correct Tier-0 path is
     ships/<slug>.json (Cobra Mk V = ships/cobra_mk_v.json, export key "cobramkv"). -->


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
