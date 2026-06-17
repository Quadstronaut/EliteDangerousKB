---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/mamba.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T05:12:08+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Mamba

The Mamba is **Zorgon Peterson's medium-pad speed-combat hull** — the straight-line "dragster"
of the medium class and the faster sibling of the [[ships/fer-de-lance]] (same manufacturer,
same 250 t airframe, same combat focus). Where the Fer-de-Lance is built to turn and brawl, the
Mamba is built to **close, alpha-strike, and disengage**: it carries the highest base speed of
any medium-pad ship in the KB and a heavy fixed-mount loadout, in exchange for noticeably worse
agility. It shares the Fer-de-Lance's exact core layout — a big class-6 Power Distributor to
feed energy weapons, a weak Frame Shift Drive, and a small fuel tank — so it fights where it
spawns rather than roaming.

## Overview

- **Manufacturer:** Zorgon Peterson
- **Size class:** 2 (Medium landing pad — docks at outposts and all larger ports)
- **Role:** Dedicated combat (bounty hunting, PvP, Conflict Zones) — fast-attack / dragster
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data)
- **Hull cost:** 55,442,918 CR (hull only)
- **Retail cost:** 55,867,040 CR (with stock modules)
- **Crew seats:** 2

## Hull Stats

Source: Coriolis-data ship definition `mamba` (edID 128915979, eddbID 38).

- **Hull mass:** 250 t (identical to the Fer-de-Lance)
- **Top speed:** 310 m/s · **Boost:** 380 m/s — **the fastest base speed of any medium-pad
  (class-2) hull in the KB** (next is the Fer-de-Lance at 260), and the 2nd-highest base speed of
  any ship paged here, behind only the [[ships/viper-mk-iii]] (320). Straight-line pace is the
  Mamba's whole identity.
- **Base shield strength:** 270 MJ (high for a medium, though below the Fer-de-Lance's 300)
- **Base armour:** 230 · **Hull hardness:** 70 (high — a true combat hull, same as the FDL)
- **Heat capacity:** 165 (low — the Mamba runs **hot**, hotter than the Fer-de-Lance's 224;
  a [[outfitting/heat-sink-launcher]] is near-mandatory on an energy build)
- **Mass lock factor:** 12
- **Manoeuvrability (deg/s):** pitch 27 · roll 80 · yaw 10 — **less agile than the
  Fer-de-Lance** (38 / 90 / 12). This is the dragster trade: the Mamba goes faster in a straight
  line but turns worse, so it favours fixed weapons and slashing attack runs over a turning fight.
- **Reserve fuel:** 0.5 t

## Slot Layout

- **Core internals:** Power Plant **6**, Thrusters **5**, Frame Shift Drive **4**,
  Life Support **4**, Power Distributor **6**, Sensors **4**, Fuel Tank **3**. This is the
  **identical core layout to the [[ships/fer-de-lance]]** — a class-6 Power Distributor (sustained
  beam/pulse/multi-cannon fire) bought with a class-4 [[outfitting/frame-shift-drive]] (poor jump
  range) and a class-3 fuel tank (short legs).
- **Hardpoints:** 1 × Huge (class-4) + 2 × Large + 2 × Small (five weapon mounts). Note the
  difference from the Fer-de-Lance, which mounts 1 Huge + 4 Medium: the Mamba swaps those four
  Mediums for **two Large plus two Small**, biasing toward big fixed mounts. The lone Huge slot is
  the family signature.
- **Utility mounts:** 6 (generous — shield boosters, heat sinks, chaff and point defence together).
- **Optional internals:** sizes 5, 4, 3, 2, 2, 1 (six slots) plus a reserved class-1
  **Planetary Approach Suite**. Shallow internals (top slot only class-5) are the cost of the
  combat focus — limited cargo and tight shield/utility space.
- **Military slots:** none.

Bulkheads carry `causres 0` on every grade.

## Mamba vs other medium combat hulls

- **vs [[ships/fer-de-lance]]:** the two Zorgon Peterson combat mediums share a 250 t airframe,
  hardness 70, and an identical core (class-6 PD, class-4 FSD, class-3 tank). The **Fer-de-Lance**
  turns harder (38/90/12 vs 27/80/10), shields better (300 vs 270 MJ), and runs slightly cooler
  (heat capacity 224 vs 165), and it mounts 1 Huge + 4 Medium. The **Mamba** is faster in a
  straight line (310/380 vs 260/350) and mounts 1 Huge + 2 Large + 2 Small. Pick the FDL for a
  turning duel, the Mamba for fixed-weapon firing passes and the ability to dictate range.
- **vs [[ships/python]]:** the Python spreads fire across three Large hardpoints with far deeper
  internals (ten slots) for a multirole/trader build. The Mamba concentrates a Huge mount and
  pace into a dedicated fighter and carries little.
- **vs [[ships/vulture]]:** the Vulture is the small-pad firepower-to-size brawler (two Large on a
  size-1 hull, class-leading roll), power-starved by a class-4 plant. The Mamba is a medium-pad
  step up with a Huge mount, a class-6 distributor, far more shield and speed — at a much higher
  price and a medium pad.

## Build notes

The textbook fit is a Huge **fixed** energy weapon (plasma accelerator, beam, or rail) backed by
the two Large mounts, leaning on the speed to control engagement range rather than out-turning the
target. Pair a Bi-Weave or engineered prismatic shield with heat sinks for the low heat capacity.
Engineer the Power Distributor (at [[engineers/the-dweller]]) and weapons (at Tod "The Blaster"
McQuinn) to sustain the Huge slot's draw.

## Acquisition

Sold at large stations carrying a shipyard. Check Spansh (`spansh.co.uk/stations`) for the nearest
stock. As a high-value combat hull it is most common around higher-population systems.

[[trunk]]
