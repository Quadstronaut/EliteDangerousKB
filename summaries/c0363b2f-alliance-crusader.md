---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/alliance_crusader.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:21:19+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Alliance Crusader — Coriolis hull data (Tier 0)

Structured JSON parsed directly (no LLM). Key: `alliance_crusader`, edID 128816581, eddbID 36.

## Identity
- **Name:** Alliance Crusader
- **Manufacturer:** Lakon (Alliance military hull line)
- **Class:** 2 → **medium landing pad**
- **Requires:** Horizons (`requirements.horizons: true`)

## Hull properties
- **Hull mass:** 500 t (heaviest of the Alliance trio: Chieftain 400, Challenger 450)
- **Speed / boost:** 180 / 300 m/s (slowest of the trio)
- **Base shield:** 200 MJ · **Base armour:** 300
- **Hardness:** 65 · **Heat capacity:** 316 · **Mass lock:** 13
- **Manoeuvrability:** pitch 32 / roll 80 / yaw 16 (least agile of the trio)
- **Crew seats:** 4 · **fighterHangars: TRUE** (Ship-Launched Fighter bay)
- **Reserve fuel:** 0.77 t
- **Hull cost:** 22,096,565 CR · **Retail:** 22,866,341 CR

## Slot layout (claims)
- **Core internals** (standard `[6,6,5,5,6,4,4]`): Power Plant 6, Thrusters 6, FSD 5,
  Life Support 5, Power Distributor 6, Sensors 4, Fuel Tank 4 (same core as Chieftain/Challenger).
- **Hardpoints** (`[3,2,2,1,1,1,...]`): 1 × Large + 2 × Medium + 3 × Small = **six weapon mounts**.
- **Utility mounts:** 4 (four trailing `0` entries).
- **Optional internals** (`[6,5,3,3,2,2, M4, M4, M4, 1, PAS1]`): seven regular optionals
  (6,5,3,3,2,2,1) + **three class-4 Military slots** + class-1 Planetary Approach Suite.
- **Military slots eligible** (per data): mahr, hr, scb, mrp, gsrp, gmrp, ghrp.
- **Bulkheads:** causres 0 on all five grades; hullboost 0.8 / 1.52 / 2.5 / 2.5 / 2.5.

## Currency / availability
- **availability: live.** Current, purchasable ship; iconic Alliance AX multicrew platform.

## Queue-guess corrections (vs next-targets note)
- **Crew is 4, not 3** — the Crusader seats a full multicrew complement.
- **Military slots = 3** (same as Chieftain and Challenger), **not 2**.
- It is the **only** Alliance medium with a **fighter hangar** (fighterHangars TRUE) — CONFIRMED.
- It has **six** weapon mounts (1L+2M+3S) — fewer than the Challenger's seven, and only one Large
  (like the Challenger, vs the Chieftain's two).

## Claim count: ~8 (identity, mass, speed, shield/armour, hardpoints, military slots, fighter bay, cost)
obsolete: NO
