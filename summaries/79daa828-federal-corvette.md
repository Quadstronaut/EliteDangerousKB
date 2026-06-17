---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/federal_corvette.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:21:19+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Federal Corvette — Coriolis hull data (Tier 0)

Structured JSON parsed directly (no LLM). Key: `federal_corvette`, edID 128049369, eddbID 25.

## Identity
- **Name:** Federal Corvette
- **Manufacturer:** Core Dynamics
- **Class:** 3 → **large landing pad**
- **Requires:** Federal Navy rank **Rear Admiral** (`requirements.federationRank: 12`).

## Hull properties
- **Hull mass:** 900 t
- **Speed / boost:** 200 / 260 m/s
- **Base shield:** 555 MJ · **Base armour:** 370
- **Hardness:** 70 (highest of any KB ship so far) · **Heat capacity:** 333
- **Mass lock:** 24 (very high — strongly mass-locks targets)
- **Manoeuvrability:** pitch 28 / roll 75 / yaw 8 (agile for a large-pad combat hull)
- **Crew seats:** 4 · **fighterHangars: TRUE** (Ship-Launched Fighter bay)
- **Reserve fuel:** 1.13 t
- **Hull cost:** 183,156,068 CR · **Retail:** 187,969,450 CR

## Slot layout (claims)
- **Core internals** (standard `[8,7,6,5,8,8,5]`): Power Plant 8, Thrusters 7, FSD 6,
  Life Support 5, **Power Distributor 8**, Sensors 8, Fuel Tank 5. Class-8 PP + class-8 PD are the
  signature: sustains the heaviest weapon loadout in the game.
- **Hardpoints** (`[4,4,3,2,2,1,1,...]`): **2 × Huge (class-4)** + 1 × Large + 2 × Medium +
  2 × Small = **seven weapon mounts**. First KB ship with Huge (class-4) hardpoints — and it has TWO.
- **Utility mounts:** **8** (eight trailing `0` entries; rule validated against Panther=6, Type-9=4).
- **Optional internals** (`[7,7,7,6,6,5,5, M5, M5, 4,4,3,1, PAS1]`): eleven regular optionals
  (7,7,7,6,6,5,5,4,4,3,1) + **two class-5 Military slots** + class-1 Planetary Approach Suite.
- **Military slots eligible** (per data): mahr, hr, scb, mrp, gsrp, gmrp, ghrp.
- **Bulkheads:** causres 0 on all five grades; hullboost 0.8 / 1.52 / 2.5 / 2.5 / 2.5.

## Currency / availability
- **availability: live.** Current Core Dynamics combat flagship; premier large-pad AX gunship.

## Queue-guess corrections (vs next-targets note)
- It has **two** Huge (class-4) hardpoints, not one.
- **Two** class-5 Military slots (larger than the Alliance trio's class-4, but fewer in count).
- Rank gate confirmed: **Rear Admiral** (`federationRank: 12`).

## Claim count: ~9 (identity, rank gate, mass, shield/armour, hardness, huge hardpoints, military slots, PD8, cost)
obsolete: NO
