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

# Decontamination Limpet Controller (Outfitting)

The **Decontamination Limpet Controller** is an **optional internal** module that commands a
single-use drone (a *limpet*) which **removes caustic chemicals from a ship's hull and applies a
small amount of hull repair**. It is the **sustained, limpet-borne** counterpart to the instant
[[outfitting/caustic-sink-launcher|Caustic Sink Launcher]]: a caustic sink purges all caustic
damage-over-time from *your own* hull in one burst, while a decontamination limpet works the
contamination off over time and can be sent to a **nearby allied ship** as well as your own. In
the Coriolis data it is group `dtl`, file `internal/decontamination_limpet_controller.json`. This
is current, accessible AX kit — **availability: live**.

## What it does

- **Strips caustic contamination over time.** Thargoid caustic clouds, caustic/enzyme missiles
  (see [[outfitting/enzyme-missile-rack]]), and Maelstrom/Titan environments coat the hull in a
  corrosive enzyme that keeps eating armour after you leave the source. A decontamination limpet
  attaches and removes that caustic effect gradually — a sustained counter rather than the
  one-shot purge of a caustic sink.
- **Repairs a little hull, too.** The in-game description notes the limpet *"applies a small
  amount of hull repair"* alongside the decontamination — a minor bonus, not a substitute for a
  dedicated Auto Field-Maintenance Unit or repair-limpet controller.
- **Can be sent to an ally.** Like other limpets it can target a friendly ship in range, so a
  support fitter can decontaminate wingmates diving the same Titan wreck or Maelstrom.
- **Costs a limpet per job.** Each limpet is one cargo unit consumed on use — carry spares.

## Stats (class/rating)

Unlike the mining [[outfitting/limpet-controllers|Prospector and Collector controllers]] (which
run a full A–E rating ladder), the decontamination controller ships in **four sizes only —
classes 1, 3, 5, 7 — all at rating E**. Class sets how many limpets you can run **at once**
(`maximum`) and the control range; mass, power and cost climb steeply with class.

| Class | Rating | Max limpets | Range (km) | Mass (t) | Power (MW) | Cost (CR) |
|---|---|---|---|---|---|---|
| 1 | E | 1 | 0.6  | 1.3 | 0.18 | 3,600     |
| 3 | E | 2 | 0.88 | 2   | 0.2  | 16,200    |
| 5 | E | 3 | 1.3  | 20  | 0.5  | 145,800   |
| 7 | E | 4 | 2.04 | 128 | 0.97 | 1,312,200 |

Symbols `Int_DroneControl_Decontamination_Size{1,3,5,7}_Class1`. There is **no limpet-lifetime
(`time`) field** in the data for this controller, and **no higher ratings** — a low class is the
normal pick, since you rarely need more than one or two decon limpets in flight and the larger
slots are better spent on combat or defence modules.

## Caustic sink vs decontamination limpet

Two different answers to the same Thargoid problem — fit whichever your role wants, or both on a
dedicated AX hull:

- **[[outfitting/caustic-sink-launcher|Caustic Sink Launcher]]** — *utility hardpoint*, instant,
  **self only**. Fires a sink that clears all accumulated caustic DoT in one burst. Best for a
  combat ship that needs to dump caustic *right now* mid-fight. Six sinks before restock.
- **Decontamination Limpet Controller** — *optional internal*, gradual, **self or ally**, plus a
  trickle of hull repair. Best for a support/exploration fitter or a slower diver that has the
  internal slot to spare and wants to keep cleaning over a long exposure.

## How to fit

- Goes in an **optional internal** slot, competing with cargo, fuel, shield and reinforcement
  modules — not a utility mount, so it does **not** contend with the [[outfitting/xeno-scanner]],
  [[outfitting/shutdown-field-neutraliser]] or [[outfitting/caustic-sink-launcher]] for utility
  slots.
- **Carry limpet cargo** — each use consumes one limpet from your hold.
- A **C1 E** controller (1.3 t, 3,600 CR) is enough for self-decon on most builds; size up only
  if you want to run several limpets or reach further to decontaminate allies.

## Related AX utilities

Part of the AX survival kit that keeps a hull alive in Thargoid space:
[[outfitting/caustic-sink-launcher]] (instant self-purge), [[outfitting/heat-sink-launcher]]
(heat venting), [[outfitting/xeno-scanner]] (find the weak points) and
[[outfitting/shutdown-field-neutraliser]] (survive the EMP pulse). See also the mining
[[outfitting/limpet-controllers]] for the Prospector/Collector siblings of this drone family.

[[trunk]]
