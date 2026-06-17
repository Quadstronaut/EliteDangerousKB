---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/federal_assault_ship.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:59:43Z
source_count: 1
verified: false
availability: live
changed_note: ""
---

# Federal Assault Ship — Coriolis Tier-0 extract

**Key:** `federal_assault_ship` (file resolved first try, 3762 bytes, no 404). edID 128672145, eddbID 8.

## Identity / class
- Name: Federal Assault Ship; manufacturer: **Core Dynamics**.
- `class: 2` = **MEDIUM landing pad**.
- Rank gate: `requirements.federationRank: 5` = **Federal Navy CHIEF PETTY OFFICER**. Sits BETWEEN the
  base [[ships/federal-dropship]] (Midshipman/3) and the heavy [[ships/federal-gunship]] (Ensign/7).
  QUEUE-GUESS "Petty Officer/4 or Chief Petty Officer/5" → CONFIRMED (rank 5).

## Hull / flight
- `hullMass: 480` — **LIGHTER than both Federal-medium siblings (each 580)**. QUEUE-GUESS "~580, same
  airframe" → **WRONG**: the Assault Ship is a 480 t hull, 100 t lighter than the Dropship/Gunship.
- `speed: 210` / `boost: 350` — **FASTEST of the Federal medium trio** (Dropship 180/300, Gunship
  170/280). QUEUE-GUESS "expect FASTER than both siblings" → CONFIRMED.
- `baseShieldStrength: 200` (ties the Dropship; below the Gunship's 250).
- `baseArmour: 300` (ties the Dropship; below the Gunship's 350).
- `hardness: 60` (same across the trio).
- `heatCapacity: 286` — **LOWER than both siblings** (Dropship 331, Gunship 325): runs hotter.
- `masslock: 14`; `crew: 2`; `reserveFuelCapacity: 0.72`.
- Maneuver: `pitch 38 / roll 90 / yaw 19` — **MOST AGILE of the Federal medium trio** (Dropship
  30/80/14, Gunship 25/80/18). QUEUE-GUESS "the most agile of the trio" → CONFIRMED.
- **NO `fighterHangars` key → NO SLF bay** (matches the Dropship; the Gunship is the only trio member
  with a fighter bay). QUEUE-GUESS "expect NONE" → CONFIRMED.

## Core internals (standard slots)
- `standard: [6,6,5,5,6,4,4]` = PP6 Thr6 FSD5 LS5 PD6 Sen4 FT4 — **IDENTICAL core layout to the
  Dropship** (the Gunship steps PD up to 7 and Sensors to 5).

## Hardpoints
- `hardpoints: [3,3,2,2,0,0,0,0]` = **2 LARGE + 2 MEDIUM = 4 weapon mounts** + **4 utility**.
- QUEUE-GUESS "a mid count between the Dropship's 5 and Gunship's 7" → **WRONG**: only 4 mounts,
  FEWER than both siblings — BUT it is the only Federal medium with **TWO Large** hardpoints (the
  Dropship and Gunship each carry a single Large + four Mediums). The Assault Ship trades mount COUNT
  for bigger Large mounts and agility — a true "assault" skirmisher profile.

## Optional internals
- `internal: [5, 5, 4, Mil-c4, Mil-c4, 3, 2, 2, 1, PAS-c1]` = **SEVEN regular** (top two class-5) +
  **TWO class-4 Military** slots + class-1 Planetary Approach Suite.
- Sits between siblings: Dropship 8 regular / 2 Military; Gunship 6 regular / 3 Military; Assault Ship
  7 regular / 2 Military. QUEUE-GUESS Military "~2" → CONFIRMED (two class-4).
- Both Military slots eligible: mahr/hr/scb/mrp/gsrp/gmrp/ghrp.

## Costs
- `hullCost: 19,111,109` / `retailCost: 19,814,210` (between the Dropship ~14.3 M and Gunship ~35.8 M).

## Bulkheads
- causres 0 across all five grades (Lightweight → Reactive Surface), standard Coriolis pattern.

availability: **live** (currently purchasable). obsolete: NO.
