---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/cargo_rack.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T00:54:21+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Cargo Rack — Tier-0 parse

Group `cr`. Optional-internal storage module. Holds tradeable/mission cargo (1 t per unit).

Key claims (from Coriolis module data):
- **Capacity doubles each class:** C1 2 t · C2 4 · C3 8 · C4 16 · C5 32 · C6 64 · C7 128 ·
  C8 256. Standard racks are all E-rated.
- **Massless** in the data model (`mass` 0) — the rack hardware adds no hull mass; only the
  cargo loaded into it (1 t/unit) affects mass and jump range.
- Cost scales with capacity: C1 1,000 CR … C5 111,566 … C8 3,829,866 CR.
- **Corrosion Resistant Cargo Rack** variants exist for carrying corrosive cargo (Thargoid
  sensors/probes, certain mission goods) that would otherwise damage a normal rack: C1 (1 t,
  6,250 CR; plus a free 2 t rating-F variant), C4 (16 t), C5 (32 t), C6 (64 t). The larger
  corrosion-resistant racks match standard capacity for their class.
- **Expanded Capacity Cargo Rack** (C5, C6) — pre-engineered **Grade 5 "Expanded Capacity"**
  (blueprint `CargoRack_IncreasedCapacity`), a Community-Goal reward (`availability: CG`); not
  re-engineerable. Gives more capacity than a standard rack of the same size.

availability: live. obsolete: NO.
