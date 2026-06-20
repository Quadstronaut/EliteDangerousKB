---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/asp_scout.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-20T20:56:25+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Asp Scout

The Asp Scout is a **medium-class combat/recon ship** by **Lakon Spaceways** — the cheaper,
lighter budget sibling of the [[ships/asp-explorer]] on the same Asp airframe. Where the Explorer
is the classic roomy long-range explorer, the Scout is the cut-down version: a much lighter hull,
a smaller class-4 Frame Shift Drive, shallower internals and fewer weapon mounts, at roughly 60%
of the Explorer's hull price. It is the budget member of the Asp pair — rarely a first choice
today, but a cheap, no-rank-gate medium-pad platform.

## Overview

- **Manufacturer:** Lakon Spaceways
- **Size class:** 2 (Medium landing pad — docks at outposts and all larger ports)
- **Role:** Light combat / reconnaissance (budget medium multirole)
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data)
- **Hull cost:** 3,819,823 CR (hull only)
- **Retail cost:** 3,961,154 CR (with stock modules)
- **Crew seats:** 2

## Hull Stats

Source: Coriolis-data ship definition `asp_scout` (edID 128672276, eddbID 24).

- **Hull mass:** 150 t (light — about half the Asp Explorer's 280 t)
- **Top speed:** 220 m/s · **Boost:** 300 m/s
- **Base shield strength:** 120 MJ
- **Base armour:** 180 · **Hull hardness:** 52 (low — not a dedicated combat hull)
- **Heat capacity:** 210
- **Mass lock factor:** 8
- **Manoeuvrability (deg/s):** pitch 40 · roll 110 · yaw 15 (a quick roll — nimbler than the
  Explorer's 38/100/10)
- **Reserve fuel:** 0.47 t

## Slot Layout

- **Core internals:** Power Plant **4**, Thrusters **4**, Frame Shift Drive **4**,
  Life Support **3**, Power Distributor **4**, Sensors **4**, Fuel Tank **4**. Note the
  **class-4 FSD** — one size smaller than the Asp Explorer's class-5 drive, so the Scout jumps
  shorter despite its lighter mass. The whole core is one class shallower than the Explorer's
  (which runs class-5 PP/Thr/FSD/Sen/FT).
- **Hardpoints:** 2 × Medium + 2 × Small (four weapon mounts — no Large or Huge). The Explorer
  carries two more Small mounts (six total); the Scout is the lighter-armed of the pair.
- **Utility mounts:** 2 (heat sinks, shield boosters — half the Explorer's four).
- **Optional internals:** sizes 5, 4, 3, 3, 2, 2, 1 (seven slots) plus a reserved class-1
  **Planetary Approach Suite** (planet-landing and SRV capable). One fewer slot than the Explorer,
  and the largest is class-5 rather than class-6 — shallower cargo/fit room.
- **Military slots:** none (same as the Asp Explorer).

Bulkheads carry `causres 0` on every grade, so for any AX detour fit a Meta-Alloy
[[outfitting/hull-reinforcement]] package for caustic resistance.

## Asp Scout vs Asp Explorer

Both are Lakon medium-pad (class-2) hulls with no rank gate, but they split clearly:

| | Asp Scout | Asp Explorer |
|---|---|---|
| Hull cost | 3,819,823 CR | 6,145,793 CR |
| Hull mass | 150 t | 280 t |
| FSD | class 4 | class 5 |
| Speed / boost | 220 / 300 | 250 / 340 |
| Shield / armour | 120 / 180 | 140 / 210 |
| Hardpoints | 2 M + 2 S (4 mounts) | 2 M + 4 S (6 mounts) |
| Utility | 2 | 4 |
| Optionals | 7 (top class-5) | 8 (top class-6) |
| Roll | 110 | 100 |

The **Scout** is the cheaper, lighter, more agile airframe; the **Explorer** is the better-armed,
roomier, longer-legged one (bigger FSD, deeper internals, more mounts and utilities). For long-range
exploration the Explorer's class-5 FSD and class-6 optional win easily; the Scout's only real edges
are price and a slightly quicker roll. Most commanders pick the Explorer — the Scout is a budget
stepping-stone, not the Explorer's combat upgrade.

## Build notes

With only four mounts, two utilities and a class-4 PD/PP core, the Scout is a light skirmisher or
cheap second medium-pad hull rather than a serious combat ship. If you want budget recon, fit a
[[outfitting/frame-shift-drive]] (engineered for range at [[engineers/felicity-farseer]]) and a
Detailed Surface Scanner; the lighter 150 t mass partly offsets the smaller drive. For actual
combat on a medium pad, the dedicated brawlers ([[ships/fer-de-lance]], [[ships/krait-mk-ii]],
the Alliance trio) outclass it.

## Acquisition

Sold at large stations carrying a shipyard; as a long-standing Lakon hull it is fairly widely
stocked. Check Spansh (`spansh.co.uk/stations`) for the nearest source.

[[trunk]]
