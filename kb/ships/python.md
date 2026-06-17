---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/python.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:58:13+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Python

The Python is a **medium-class multirole ship** by **Faulcon DeLacy** — the classic
workhorse of the medium pad. It pairs three Large hardpoints with deep optional
internals and a no-rank-gate price, making it a long-standing favourite for combat,
trading, and general-purpose flying. Its modern combat-focused stablemate is the
[[ships/python-mk-ii]].

## Overview

- **Manufacturer:** Faulcon DeLacy
- **Size class:** 2 (Medium landing pad — docks at outposts and medium ports)
- **Role:** Multirole (combat, trading, general-purpose)
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data)
- **Hull cost:** 55,324,684 CR (hull only)
- **Retail cost:** 56,978,179 CR (with stock modules)
- **Crew seats:** 2

## Hull Stats

Source: Coriolis-data ship definition `python` (edID 128049339, eddbID 17).

- **Hull mass:** 350 t
- **Top speed:** 230 m/s · **Boost:** 300 m/s
- **Base shield strength:** 260 MJ
- **Base armour:** 260 · **Hull hardness:** 65
- **Heat capacity:** 300
- **Mass lock factor:** 17
- **Manoeuvrability (deg/s):** pitch 29 · roll 90 · yaw 10
- **Reserve fuel:** 0.83 t

## Slot Layout

- **Core internals:** Power Plant **7**, Thrusters **6**, Frame Shift Drive **5**,
  Life Support **4**, Power Distributor **7**, Sensors **6**, Fuel Tank **5**.
- **Hardpoints:** 3 × Large + 2 × Medium (five mounts — three of them Large, heavy
  firepower for a medium hull).
- **Utility mounts:** 4.
- **Optional internals:** sizes 6, 6, 6, 5, 5, 4, 3, 3, 2, 1 (ten slots — three class-6)
  plus a reserved class-1 **Planetary Approach Suite** (planet-landing and SRV capable).
- **Military slots:** none.

The triple class-6 optionals give the Python a large cargo or shield/utility capacity
for a medium ship, while the 3L + 2M hardpoints out-gun most mediums. The class-5 FSD
ceiling keeps base jump range modest — engineer it at [[engineers/felicity-farseer]]
for range. Bulkheads carry `causres 0` on every grade, so for AX work fit a
[[outfitting/hull-reinforcement]] Meta-Alloy package for caustic resistance.

## Python vs Python Mk II

Both are Faulcon DeLacy mediums. The original **Python** leans multirole/trader — three
Large hardpoints and ten optional internals (three class-6). The newer
[[ships/python-mk-ii]] is the Odyssey-era combat refinement (4 × Medium + 2 × Small
hardpoint layout, tuned for gunnery). Pick the base Python for cargo and big-mount
versatility; the Mk II for dedicated medium combat.

## Acquisition

Sold at large stations carrying a shipyard. Check INARA (`inara.cz/elite/ships`) or
Spansh (`spansh.co.uk/stations`) for nearest stock. Common engineers: Felicity Farseer
(FSD), The Dweller (power plant), Tod "The Blaster" McQuinn (weapons).

[[trunk]]
