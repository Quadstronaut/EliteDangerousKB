---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/type_10_defender.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:42:17+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Type-10 Defender — Coriolis Tier-0 summary

Structured Coriolis ship definition `type_10_defender` (edID 128785619, eddbID 32). Parsed
directly, no LLM.

## Key claims

- **Manufacturer Lakon, class 3 (large pad), NO rank gate** — there is no `requirements` block in
  the Coriolis data, so it is credits-only (like the Anaconda; unlike the rank-gated Corvette/Cutter).
- **The armour brick of the KB:** `baseArmour 580` (**highest base armour of any KB ship**, above the
  Anaconda's 525) and `hardness 75` (**highest hull hardness in the KB**, above the Corvette/Cutter's
  70). `baseShieldStrength 320` is comparatively LOW — it tanks with hull, not shields.
- **Heaviest hull in the KB:** `hullMass 1200` t (above the Imperial Cutter's 1100). `heatCapacity 335`,
  `masslock 26`.
- **Most weapon mounts in the KB:** hardpoints array `[3,3,3,3,2,2,2,1,1, +8 zeros]` = **4 Large +
  3 Medium + 2 Small = NINE weapon mounts**, but **NO Huge** (max is Large). **8 utility mounts**
  (the 8 trailing zeros).
- **Core internals** (standard `[8,7,7,5,7,4,6]`): Power Plant **8**, Thrusters **7**, FSD **7**,
  Life Support **5**, Power Distributor **7**, Sensors **4**, Fuel Tank **6**.
- **Optional internals** (internal slots): sizes **8,7,6,5,4,4,3,3,2,1** (ten regular) plus **TWO
  class-5 Military slots** plus a reserved class-1 **Planetary Approach Suite**.
- **Manoeuvrability:** speed 179 / boost 219 (slow); pitch 20 / roll 20 / yaw 8 (very sluggish —
  identical airframe figures to the [[ships/type-9-heavy]], its bulk-hauler sibling).
- **Crew 4**, fighter hangar present (`fighterHangars true`). reserveFuel 0.77.
- **Cost:** hull 121,334,619 CR / retail 124,755,342 CR.
- Bulkheads `causres 0` on every grade (no caustic resistance from the hull).

## Military slot eligibility note

The **first** class-5 Military slot is eligible for **Meta-Alloy Hull Reinforcement** (`mahr`) plus
`hr/scb/mrp/gsrp/gmrp/ghrp`; the **second** Military slot is eligible for the same set **except
`mahr`**. So only one Military slot can carry the caustic-resisting Meta-Alloy HRP.

## Currency

availability: **live** — a current AX gunship/platform; AX combat zones, Spire sites and Titan wrecks
all remain accessible. obsolete: NO.
