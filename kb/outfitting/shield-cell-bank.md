---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/shield_cell_bank.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T21:07:24+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Shield Cell Bank (Outfitting)

The **Shield Cell Bank** (SCB) is an **optional internal** module that uses pre-charged cells to
**rapidly restore active shields**. It is the active-recovery counterpart to the passive
[[outfitting/shield-generator]]: the generator sets and regenerates the pool slowly, an SCB dumps a
burst of shield MJ back on demand when you take heavy fire. In the Coriolis data it is group `scb`,
file `internal/shield_cell_bank.json`.

## What it does

- **Restores active shields only.** The module's description is explicit: *"No effect on collapsed
  shields."* Once your shields drop (collapse), an SCB does nothing — you must trigger it while the
  shield ring is still up. Timing is the whole skill of using one.
- **Cells are finite uses.** Each module holds a number of **cells** = `clip` (always 1 loaded) +
  `ammo` (reserve). Firing one consumes a cell and restores `shieldreinforcement` MJ over the
  module's `duration`. When the cells are spent the SCB is dead weight until you rearm
  (`ammocost` 300 cr per cell at a station).
- **Spin-up and boot.** Every variant has a **5-second `spinup`** before the heal begins after you
  trigger it, and a **25-second `boot`** delay when the ship powers on or the module is repowered —
  you cannot fire an SCB the instant you flip it on.
- **Heat is the cost.** Each activation dumps a large `thermload` of heat (170 at class 1 up to 800
  at class 8). Spamming cells back-to-back will overheat the ship and start cooking modules, so
  serious builds pair SCBs with **heat sinks** or heat-reducing engineering.

## Cells, heal, and the rating trade

Within a class the ratings do **not** scale in a simple line — they trade cell count against heal
per cell:

- **E and B ratings carry the most cells; A and C fewer; D the fewest** (D is often a single cell).
- **`shieldreinforcement` (heal per cell) rises with both class and rating.** The **A rating gives
  the highest heal per cell** — the best single-press burst recovery. The **B rating gives the
  largest total reservoir** (cells × heal) — more total shield restored across the fight.
- Pick **A** when you want the biggest instant top-up to survive a burst; pick **B** for the most
  total shield healing over a long engagement; **D** is a light, cheap single-cell emergency button.

`duration` is the time over which a cell delivers its reinforcement: ~1 s at class 1 rising to 17 s
at class 8, so small SCBs are near-instant bursts and the largest ones trickle their (larger) heal
out over many seconds.

## Classes and ratings (full table)

"Cells" = `ammo` reserve + 1 loaded. "Pool" = cells × heal/cell (total shield MJ the module can
restore before rearming).

| Class | Rating | Cells | Heal/cell (MJ) | Pool (MJ) | Duration (s) | Mass (t) | Power (MW) | Thermal load | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | E | 4 | 12 | 48 | 1 | 1.3 | 0.41 | 170 | 517 |
| 1 | D | 1 | 12.5 | 12.5 | 1 | 0.5 | 0.55 | 170 | 1,293 |
| 1 | C | 3 | 20 | 60 | 1 | 1.3 | 0.69 | 170 | 3,231 |
| 1 | B | 4 | 24 | 96 | 1 | 2 | 0.83 | 170 | 8,078 |
| 1 | A | 3 | 28 | 84 | 1 | 1.3 | 0.97 | 170 | 20,195 |
| 2 | E | 5 | 14 | 70 | 2 | 2.5 | 0.50 | 240 | 1,448 |
| 2 | D | 3 | 18 | 54 | 2 | 1 | 0.67 | 240 | 3,619 |
| 2 | C | 4 | 23 | 92 | 2 | 2.5 | 0.84 | 240 | 9,048 |
| 2 | B | 5 | 28 | 140 | 2 | 4 | 1.01 | 240 | 22,619 |
| 2 | A | 4 | 32 | 128 | 2 | 2.5 | 1.18 | 240 | 56,547 |
| 3 | E | 5 | 17 | 85 | 2 | 5 | 0.61 | 340 | 4,053 |
| 3 | D | 3 | 23 | 69 | 2 | 2 | 0.82 | 340 | 10,133 |
| 3 | C | 4 | 29 | 116 | 2 | 5 | 1.02 | 340 | 25,333 |
| 3 | B | 5 | 35 | 175 | 2 | 8 | 1.22 | 340 | 63,333 |
| 3 | A | 4 | 41 | 164 | 2 | 5 | 1.43 | 340 | 158,331 |
| 4 | E | 5 | 20 | 100 | 3 | 10 | 0.74 | 410 | 11,349 |
| 4 | D | 3 | 26 | 78 | 3 | 4 | 0.98 | 410 | 28,373 |
| 4 | C | 4 | 33 | 132 | 3 | 10 | 1.23 | 410 | 70,932 |
| 4 | B | 5 | 39 | 195 | 3 | 16 | 1.48 | 410 | 177,331 |
| 4 | A | 4 | 46 | 184 | 3 | 10 | 1.72 | 410 | 443,328 |
| 5 | E | 5 | 21 | 105 | 5 | 20 | 0.90 | 540 | 31,778 |
| 5 | D | 3 | 28 | 84 | 5 | 8 | 1.20 | 540 | 79,444 |
| 5 | C | 4 | 35 | 140 | 5 | 20 | 1.50 | 540 | 198,611 |
| 5 | B | 5 | 41 | 205 | 5 | 32 | 1.80 | 540 | 496,527 |
| 5 | A | 4 | 48 | 192 | 5 | 20 | 2.10 | 540 | 1,241,317 |
| 6 | E | 6 | 20 | 120 | 8 | 40 | 1.06 | 640 | 88,978 |
| 6 | D | 4 | 26 | 104 | 8 | 16 | 1.42 | 640 | 222,444 |
| 6 | C | 5 | 33 | 165 | 8 | 40 | 1.77 | 640 | 556,110 |
| 6 | B | 6 | 39 | 234 | 8 | 64 | 2.12 | 640 | 1,390,275 |
| 6 | A | 5 | 46 | 230 | 8 | 40 | 2.48 | 640 | 3,475,688 |
| 7 | E | 6 | 24 | 144 | 11 | 80 | 1.24 | 720 | 249,137 |
| 7 | D | 4 | 32 | 128 | 11 | 32 | 1.66 | 720 | 622,843 |
| 7 | C | 5 | 41 | 205 | 11 | 80 | 2.07 | 720 | 1,557,108 |
| 7 | B | 6 | 49 | 294 | 11 | 128 | 2.48 | 720 | 3,892,770 |
| 7 | A | 5 | 57 | 285 | 11 | 80 | 2.90 | 720 | 9,731,925 |
| 8 | E | 6 | 28 | 168 | 17 | 160 | 1.44 | 800 | 697,584 |
| 8 | D | 4 | 37 | 148 | 17 | 64 | 1.92 | 800 | 1,743,961 |
| 8 | C | 5 | 47 | 235 | 17 | 160 | 2.40 | 800 | 4,359,903 |
| 8 | B | 6 | 56 | 336 | 17 | 256 | 2.88 | 800 | 10,899,756 |
| 8 | A | 5 | 65 | 325 | 17 | 160 | 3.36 | 800 | 27,249,391 |

Note: the class-8 E variant's `rechargerating` is C (all other variants' recharge rating matches
their module rating) — a Coriolis-recorded quirk of that one SKU.

## How to fit

- SCBs take **optional internal** slots, competing with cargo racks,
  [[outfitting/hull-reinforcement]], fuel tanks, and the like — a shield-tank build trades cargo for
  recovery.
- They draw power and run on the SYS-priority module group; size the **power plant and distributor**
  for the chosen class, and remember the 5 s spin-up / 25 s boot when planning combat timing.
- They are the natural partner to **slow-regen, high-buffer shields**: a
  [[outfitting/shield-generator|Prismatic shield]] (slow passive regen, biggest pool) leans on SCBs
  to recover mid-fight, whereas a Bi-Weave's fast regen needs them less.
- Engineer them (e.g. for reduced thermal load or faster spin-up) on serious combat hulls to make
  cells cheaper to spam; raw SCBs are the baseline.

## Where to get them

Shield Cell Banks are common optional-internal stock at most large outfitting stations, including
**Garay Terminal** in [[locations/deciat]] (stocked to class 8). No Powerplay or unlock requirement.

[[trunk]]
