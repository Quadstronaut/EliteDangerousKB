---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/federal_gunship.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:51:20Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Federal Gunship — Coriolis extract

Tier-0 Coriolis-data ship definition, key `federal_gunship` (edID 128672152, eddbID 10). Parsed
directly, no LLM.

## Key claims

- **Manufacturer:** Core Dynamics. **Size class:** 2 (MEDIUM landing pad).
- **Role:** heavy fighter-bay gunship — the up-armed top variant of the Dropship airframe.
- **Rank gate:** `requirements.federationRank: 7` = Federal Navy rank **Ensign** (higher than the
  Dropship's Midshipman/3).
- **Hull cost:** 34,814,912 CR · **Retail:** 35,814,210 CR.
- **Hull mass:** 580 t (same airframe as the Dropship). **Speed:** 170 m/s · **Boost:** 280 m/s
  (slower than the Dropship's 180/300 — the heaviest-armed, slowest Federal medium).
- **Base shield:** 250 MJ · **Base armour:** 350 · **Hardness:** 60 · **Heat capacity:** 325 ·
  **Mass lock:** 14 · **Crew:** 2 · **Reserve fuel:** 0.82 t.
- **Manoeuvrability:** pitch 25 · roll 80 · yaw 18.
- **Fighter hangar: YES** (`fighterHangars: true`) — carries a Ship-Launched Fighter bay.
- **Core internals (standard):** PP6 Thr6 FSD5 LS5 PD7 Sen5 FT4 — `[6,6,5,5,7,5,4]` (class-7 Power
  Distributor — bigger than the Dropship's PD6, feeds more weapons).
- **Hardpoints:** `[3,2,2,2,2,1,1,0,0,0,0]` = **1 Large + 4 Medium + 2 Small = 7 weapon mounts**
  + 4 utility (the most weapon mounts of the Federal medium line).
- **Optional internals:** `[6,6,5, Mil-c4, Mil-c4, Mil-c4, 2,2,1, PAS-c1]` = **6 regular** (top two
  class-6) + **three class-4 Military slots** + class-1 Planetary Approach Suite.
- Bulkheads `causres 0` on every grade.

## Currency signals

Current live ship in the Coriolis master data; standard Federal Navy rank requirement. No obsolete
mechanics referenced.

## Availability

live — currently purchasable medium combat hull.

OBSOLETE: NO.

Queue-guess reconciliation: class 2 (MEDIUM) CONFIRMED; heavy hull CONFIRMED; slow CONFIRMED;
most weapon mounts of the Federal mediums CONFIRMED (7 vs the Dropship's 5); fighter bay TRUE
CONFIRMED; Military slot CONFIRMED (THREE class-4); rank gate higher than the Dropship CONFIRMED
(Ensign/7 vs Midshipman/3). Note: it trades two regular optionals (6 vs the Dropship's 8) for a
third Military slot plus the fighter bay.
