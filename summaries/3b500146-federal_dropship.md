---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/federal_dropship.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:51:20Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Federal Dropship — Coriolis extract

Tier-0 Coriolis-data ship definition, key `federal_dropship` (edID 128049321, eddbID 9). Parsed
directly, no LLM.

## Key claims

- **Manufacturer:** Core Dynamics. **Size class:** 2 (MEDIUM landing pad).
- **Role:** base medium combat/troop gunship — the first rung of the Core Dynamics
  Dropship → Assault Ship → Gunship trio.
- **Rank gate:** `requirements.federationRank: 3` = Federal Navy rank **Midshipman**.
- **Hull cost:** 13,510,106 CR · **Retail:** 14,314,210 CR.
- **Hull mass:** 580 t (heavy/sluggish). **Speed:** 180 m/s · **Boost:** 300 m/s (slow).
- **Base shield:** 200 MJ · **Base armour:** 300 · **Hardness:** 60 · **Heat capacity:** 331 ·
  **Mass lock:** 14 · **Crew:** 2 · **Reserve fuel:** 0.83 t.
- **Manoeuvrability:** pitch 30 · roll 80 · yaw 14.
- **No fighter hangar** (no Ship-Launched Fighter bay — that is the Gunship's feature).
- **Core internals (standard):** PP6 Thr6 FSD5 LS5 PD6 Sen4 FT4 — `[6,6,5,5,6,4,4]`.
- **Hardpoints:** `[3,2,2,2,2,0,0,0,0]` = **1 Large + 4 Medium = 5 weapon mounts** + 4 utility.
- **Optional internals:** `[6,5,5,4, Mil-c4, Mil-c4, 3,3,2,1, PAS-c1]` = **8 regular** (top class-6)
  + **two class-4 Military slots** + class-1 Planetary Approach Suite.
- Bulkheads `causres 0` on every grade.

## Currency signals

Current live ship in the Coriolis master data; standard Federal Navy rank requirement. No obsolete
mechanics referenced.

## Availability

live — currently purchasable medium combat hull.

OBSOLETE: NO.

Queue-guess reconciliation: class 2 (MEDIUM) CONFIRMED; heavy hull CONFIRMED; slow CONFIRMED;
Military slot present CONFIRMED (TWO class-4); rank gate Midshipman (low-mid) CONFIRMED.
CORRECTION: hardpoints are **1 Large + 4 Medium**, not "2 Large + smaller" — only one Large mount.
No fighter bay (CONFIRMED absent).
