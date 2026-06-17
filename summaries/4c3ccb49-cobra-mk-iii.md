---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/cobra_mk_iii.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:58:13+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Cobra Mk III — Coriolis Tier-0 summary

Structured Coriolis ship definition `cobra_mk_iii` (edID 128049279, eddbID 4). Parsed directly, no LLM.

## Key claims

- **Manufacturer Faulcon DeLacy, class 1 (small pad), NO rank gate** — there is no `requirements`
  block in the Coriolis data, so it is credits-only. The iconic affordable jack-of-all-trades; the
  modern small successor is the [[ships/cobra-mk-v]].
- **Cheapest ship in the KB:** hull **208,372 CR** / retail **349,718 CR** — a true starter hull.
- **Fast and very agile:** speed **280** / boost **400** (high), pitch 40 / **roll 100** (the nimblest
  roll of any KB ship so far) / yaw 10. `hullMass 180` t, `masslock 8` (both low).
- **Light defences:** `baseShieldStrength 80`, `baseArmour 120`, `hardness 35` (low — it survives by
  speed, not tanking), `heatCapacity 225`.
- **Weapon mounts:** hardpoints array `[2,2,1,1, +2 zeros]` = **2 Medium + 2 Small = FOUR weapon
  mounts**. **2 utility mounts** (the 2 trailing zeros).
- **Core internals** (standard `[4,4,4,3,3,3,4]`): Power Plant **4**, Thrusters **4**, FSD **4**,
  Life Support **3**, Power Distributor **3**, Sensors **3**, Fuel Tank **4**.
- **Optional internals** (internal slots): sizes **4,4,4,2,2,2,1,1** (eight regular — three class-4)
  plus a reserved class-1 **Planetary Approach Suite**. **NO Military slots.**
- **Crew 2**, no fighter hangar (no `fighterHangars` field). reserveFuel 0.49.
- Bulkheads `causres 0` on every grade.

## Currency

availability: **live** — a current, beginner-favourite small multirole still in regular use. obsolete: NO.
