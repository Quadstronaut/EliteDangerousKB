---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/standard/frame_shift_drive.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T00:32:57+00:00
source_count: 1
verified: false
availability: live
changed_note: FSD (SCO) Supercruise Overcharge variant added in Update 18 (2024); now the default drive on new ships. Legacy FSD still sold.
---

# Frame Shift Drive (Coriolis module def)

Core internal. Powers supercruise and hyperspace jumps. The Coriolis def contains BOTH the
legacy FSD line and the newer **FSD (SCO)** Supercruise Overcharge line. Group `fsd`.

Key claims (from Coriolis JSON):
- **Legacy FSD:** classes **2–7**, ratings E–A. A-rated has the best optimal mass per class
  (e.g. 5A optmass 1050 t, maxfuel 5.0 t/jump; 7A optmass 2700 t). No class-8 legacy FSD.
- **FSD (SCO):** classes **2–8**, all ratings. Higher optimal mass than legacy at the same
  class/rating (e.g. 5A SCO optmass **1175** vs 1050 legacy; 6A SCO optmass 2000 vs 1800),
  so SCO drives generally jump slightly farther AND add Supercruise Overcharge boost.
- **Class 8 exists only as SCO** (8E optmass 2800 → 8A "Mk II (SCO)" optmass 4670). The
  "Frame Shift Drive Mk II (SCO)" 8A is the top variant (fuelpower 2.5025, fuelmul 0.011).
- A-rated SCO costs scale steeply (5A ≈ 6.1M CR, 7A ≈ 61.5M CR, 8A Mk II ≈ 82M CR).
- SCO behaviour: holding throttle overcharges the drive in supercruise for much higher in-system
  speed, at higher fuel use and heat. SCO is now the default fit on post-2024 ships.
- Pre-engineered "V1" variants exist for both legacy (5A) and SCO (every class) at cost 0/None.

availability: live. obsolete: NO.
