---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/eagle.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T03:59:18Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Eagle (Eagle Mk II) — Coriolis ship summary

Tier-0 Coriolis JSON, parsed directly (no LLM). Key `eagle`, file `ships/eagle.json`
(resolved first try, no 404). edID 128049255, eddbID 7.

## Key claims

- **Identity:** Eagle (Eagle Mk II), manufacturer **Core Dynamics**, size class **1 (small pad)**.
  No `requirements` block = **no rank gate** (credits only).
- **Cost:** hull 10,947 CR / retail 44,800 CR — the **2nd-cheapest hull in the KB**, just above the
  free Sidewinder (hull 4,588 / retail 32,000) and well under the Viper Mk III (hull 96,733).
- **Hull mass:** 50 t (ties the Viper Mk III; heavier than the Sidewinder's 25 t and the Adder's 35 t).
- **Speed/boost:** 240 / 350.
- **Base shield:** 60 MJ · **base armour:** 40 (the **lowest armour of any hull in the KB**, under
  the Sidewinder's 60) · **hardness:** 28 (low).
- **Heat capacity:** 165 · **mass lock:** 6 · **crew:** 1 · **reserve fuel:** 0.34 t.
- **Manoeuvrability:** pitch **50** · roll **120** · yaw 18. **roll 120 is the NEW nimblest roll in
  the KB**, exceeding the prior Sidewinder/Vulture tie at 110. pitch 50 is also the highest in the KB.
- **Core internals** (standard [2,3,3,1,2,2,2]): Power Plant 2, Thrusters **3**, FSD 3, Life Support 1,
  Power Distributor 2, Sensors 2, Fuel Tank 2. Notably the class-3 Thrusters on a 50 t hull drive the
  high roll/pitch.
- **Hardpoints** ([1,1,1,0]): **3 × Small** weapon mounts (the Eagle's signature triple-small) +
  **1 utility** mount.
- **Optional internals** ([3,2,1,1,1,1]): **six** regular optionals (top class-3) + **one class-2
  Military slot** (eligible mahr/hr/scb/mrp/gsrp/gmrp/ghrp) + a reserved class-1 Planetary Approach Suite.
- Bulkheads carry `causres 0` on every grade.

## Currency signals

availability: **live** — the Eagle Mk II is a current, purchasable ship. OBSOLETE: **no**. No
removed/legacy mechanics involved; current-truth Tier-0 hull data.
