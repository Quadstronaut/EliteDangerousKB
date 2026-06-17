---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/imperial_eagle.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:12:55Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Imperial Eagle — Coriolis Tier-0 extract

Structured Coriolis JSON, parsed directly (no LLM). Key `imperial_eagle`, file `imperial_eagle.json`
(the queued `empire_eagle.json` 404'd; `ships/index.js` confirms `imperial_eagle: require('./imperial_eagle')`).

## Identity
- Name: Imperial Eagle — **Manufacturer: Gutamaya** (the base [[ships/eagle]] is Core Dynamics; this
  is Gutamaya's Imperial refinement of the same airframe)
- edID 128672138, eddbID 15
- Size class: 1 (Small landing pad)
- **Rank requirement: NONE** — no `requirements` block in the Coriolis data (unlike most Gutamaya
  ships; the Imperial Eagle is buyable for credits without an Empire rank)

## Hull stats
- Hull mass: 50 t (ties the base Eagle / [[ships/viper-mk-iii]])
- Speed 300 / Boost 400 — **faster** than the base Eagle's 240/350
- Base shield 80 MJ — **higher** than the base Eagle's 60
- Base armour 60 — higher than the base Eagle's 40
- Hardness 28 (same as base Eagle); heat capacity 163; mass lock 6
- Manoeuvrability: pitch 40 / **roll 100** / yaw 15 — **lower** than the base Eagle's pitch 50 /
  roll 120. The base Eagle KEEPS the class-leading roll-120 record; the Imperial Eagle does not beat it.
- Reserve fuel 0.37 t; crew 1
- Hull cost 73,023 CR / retail 110,830 CR (more expensive than the base Eagle's 10,947 / 44,800)

## Slots
- Core standard [3,3,3,1,2,2,2]: PP3 Thr3 FSD3 LS1 PD2 Sen2 FT2 — **one bigger power plant** than the
  base Eagle's [2,3,3,1,2,2,2] (class-3 PP vs class-2); otherwise identical core.
- Hardpoints [2,1,1,0] = **1 Medium + 2 Small = 3 mounts + 1 utility** — same 3-mount count as the
  base Eagle but one mount upgraded from Small to **Medium**.
- Internals [3,2,{Military c2},1,1,1,1,{PAS c1}] = six regular optionals (top class-3) + **one class-2
  Military slot** (eligible mahr/hr/scb/mrp/gsrp/gmrp/ghrp) + class-1 Planetary Approach Suite. Same
  internal layout as the base Eagle.
- Bulkheads causres 0 on all grades.

## Claims
- "Faster than the base Eagle (300/400 vs 240/350)" — TRUE
- "Higher base shield (80 vs 60) and armour (60 vs 40)" — TRUE
- "Roll ties/beats the base Eagle's 120" — FALSE (roll 100 < 120; base Eagle stays nimblest)
- "Has a class-2 Military slot like the base Eagle" — TRUE
- "Needs an Empire rank gate" — FALSE (no requirements block)

availability: live · obsolete: NO
