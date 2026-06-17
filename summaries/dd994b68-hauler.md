---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/hauler.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:12:55Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Hauler — Coriolis Tier-0 extract

Structured Coriolis JSON, parsed directly (no LLM). Key `hauler`, file `hauler.json` (resolved first try).

## Identity
- Name: Hauler — Manufacturer: Zorgon Peterson
- edID 128049261, eddbID 12
- Size class: 1 (Small landing pad)
- Rank requirement: NONE — no `requirements` block (credits only)

## Hull stats
- **Hull mass: 14 t — the NEW LIGHTEST HULL IN THE KB** (undercuts the previous lightest, the
  [[ships/sidewinder]]'s 25 t, by a wide margin)
- Speed 200 / Boost 300 (slow — among the lowest base speeds in the KB)
- Base shield 50 MJ; **base armour 100** (tougher than its tiny mass suggests — more than the
  [[ships/eagle]]'s 40 or the Sidewinder's 60)
- Hardness 20 (low, ties Sidewinder); **heat capacity 123 — the NEW LOWEST in the KB** (below the
  Sidewinder's 140; previous KB min)
- Mass lock 6; manoeuvrability: pitch 36 / roll 100 / yaw 14
- Reserve fuel 0.25 t (tiny); crew 1
- Hull cost 30,308 CR / retail 52,720 CR (cheap — but NOT the cheapest: order is Sidewinder 4,588 <
  Eagle 10,947 < **Hauler 30,308**, so the Hauler is the 3rd-cheapest hull)

## Slots
- Core standard [2,2,2,1,1,1,2]: PP2 Thr2 FSD2 LS1 PD1 Sen1 **FT2** — same shallow small core as the
  Sidewinder but a **bigger class-2 fuel tank** (vs Sidewinder's FT1). FSD is only class 2; the
  Hauler's long-range reputation comes from its **ultra-low 14 t hull mass**, not a big drive.
- Hardpoints [1,0,0] = **1 Small = 1 mount + 2 utility** (the smallest armament of any KB hull)
- Internals [3,3,2,1,1,1,{PAS c1}] = **six regular optionals (top class-3, two class-3)** + class-1
  Planetary Approach Suite. **No Military slot.** Bigger top optionals than the Sidewinder (two
  class-3 vs the Sidewinder's top class-2) — the dedicated-freighter cargo bias.
- Bulkheads causres 0 on all grades.

## Claims
- "Lightest hull in the KB" — TRUE (14 t, new record; displaces Sidewinder 25 t)
- "Lowest heat capacity in the KB" — TRUE (123, new record; below Sidewinder 140)
- "Excellent jump range from a big FSD" — PARTLY: FSD is only class 2; range comes from the 14 t mass
- "Just one Small hardpoint" — TRUE (1 Small + 2 utility)
- "Has a Military slot" — FALSE (none)
- "Cheapest hull" — FALSE (Sidewinder 4,588 and Eagle 10,947 are cheaper; Hauler is 3rd-cheapest)

availability: live · obsolete: NO
