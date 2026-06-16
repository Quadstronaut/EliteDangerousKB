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

# Cargo Rack (Outfitting)

The **Cargo Rack** is an **optional internal** module that gives your ship cargo capacity —
the tonnes of tradeable commodities, mined ore, mission goods, and limpets you can carry. No
rack, no cargo hold. Group `cr`. Stats below are from the Tier-0 Coriolis module data.

The rack hardware is **massless** in the data model (`mass` 0): fitting a bigger rack costs a
slot, never jump range *while empty*. The **cargo itself weighs 1 t per unit**, so a fully
loaded hold is what drags your jump range down — plan range around loaded mass, not the racks.

## Capacity by class

Standard cargo racks are all **E-rated** and capacity **doubles every class**:

| Class | Rating | Capacity (t) | Cost (CR) |
|---|---|---|---|
| 1 | E | 2 | 1,000 |
| 2 | E | 4 | 3,250 |
| 3 | E | 8 | 10,563 |
| 4 | E | 16 | 34,328 |
| 5 | E | 32 | 111,566 |
| 6 | E | 64 | 362,591 |
| 7 | E | 128 | 1,178,420 |
| 8 | E | 256 | 3,829,866 |

To find a hull's maximum cargo, fill every optional internal with the largest cargo rack each
slot allows and sum the capacities — e.g. the [[ships/type-9-heavy]]'s twin Class-8 slots give
~512 t from those two alone, and the [[ships/panther-clipper-mk-ii]] is the current cargo king.

## Specialised variants

- **Corrosion Resistant Cargo Rack** — needed to carry **corrosive cargo** (Thargoid Sensors,
  Thargoid Probes, certain mission/special commodities) that would damage a standard rack and
  its neighbours over time. Available at **C1** (1 t; plus a free 2 t rating-F variant often
  pre-installed on starter mission ships), **C4** (16 t), **C5** (32 t), and **C6** (64 t). The
  C4–C6 corrosion-resistant racks hold the **same tonnage** as a standard rack of that class, so
  the only cost is needing the specific module rather than a plain rack. Keep at least a small
  one fitted if you haul Thargoid materials for [[ax-thargoid]] / unlock work.
- **Expanded Capacity Cargo Rack** — **C5** and **C6** racks **pre-engineered Grade 5
  "Expanded Capacity"** (blueprint `CargoRack_IncreasedCapacity`). These were a **Community Goal
  reward** (`availability: CG`) and are **not re-engineerable**; they pack more tonnage than a
  standard rack of the same size for haulers who want maximum hold without spending an
  engineering slot.

## Fitting notes

- **Mix sizes to the slots you have:** always fill the largest slots with the biggest racks
  first — two C6 racks (128 t) beat four C4 racks (64 t) for the same slot count.
- **Trade-off vs other optionals:** every slot spent on cargo is a slot not spent on a
  [[outfitting/fuel-scoop]], [[outfitting/shield-generator]], or limpet bay. Dedicated haulers
  go nearly all-cargo; miners reserve slots for [[outfitting/limpet-controllers]] and a
  [[outfitting/refinery]].
- **Corrosive runs:** swap one rack for a Corrosion Resistant rack before picking up Thargoid
  materials, or the cargo degrades.

[[trunk]]
