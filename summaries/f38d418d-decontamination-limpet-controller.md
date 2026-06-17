---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/decontamination_limpet_controller.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:51:43+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Decontamination Limpet Controller — Coriolis Tier-0 summary

Group `dtl`. Optional **internal** module (`Int_DroneControl_Decontamination_*`). Commands a
limpet that **removes caustic chemicals from a ship's hull and applies a small amount of hull
repair**. The sustained, limpet-borne complement to the instant Caustic Sink Launcher. AX kit —
**availability: live**.

## Key claims (parsed directly from JSON)

- Four sizes only: **classes 1, 3, 5, 7** — odd classes only (limpet-controller pattern).
- **All rating E** — a single rating per class, no A–E ladder (unlike the mining Prospector/
  Collector controllers which run A–E).
- `maximum` = **max simultaneous limpets**: C1 = 1, C3 = 2, C5 = 3, C7 = 4.
- `range` = control range in km: C1 0.6 · C3 0.88 · C5 1.3 · C7 2.04 (short — operates on own
  hull or a nearby allied ship).
- In-game description: "Controls a limpet that removes caustic chemicals affecting a ship's hull,
  as well as applying a small amount of hull repair."
- No `time` (limpet-lifetime) field is present in the data for this controller.

| Class | Rating | Max limpets | Range (km) | Mass (t) | Power (MW) | Cost (CR) | Symbol id |
|---|---|---|---|---|---|---|---|
| 1 | E | 1 | 0.6  | 1.3 | 0.18 | 3,600     | y1 |
| 3 | E | 2 | 0.88 | 2   | 0.2  | 16,200    | y2 |
| 5 | E | 3 | 1.3  | 20  | 0.5  | 145,800   | y3 |
| 7 | E | 4 | 2.04 | 128 | 0.97 | 1,312,200 | y4 |

Entities: Caustic Sink Launcher, Heat Sink Launcher, Thargoid caustic damage, Limpet Controllers.
Currency signals: present-tense Coriolis module file; AX caustic-removal kit is current.
Availability: live. OBSOLETE: NO.
