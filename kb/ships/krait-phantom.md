---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/krait_phantom.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:09:29+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Krait Phantom

The Krait Phantom is a **medium-class multirole / exploration ship** by **Faulcon DeLacy** — the
lighter, explorer-leaning sibling of the combat [[ships/krait-mk-ii|Krait Mk II]]. It drops the
Mk II's third large hardpoint, fighter bay and third crew seat in exchange for **lower hull mass
and a longer jump range**, making it a favourite long-range explorer and a lean medium-pad
multirole hull.

## Overview

- **Manufacturer:** Faulcon DeLacy
- **Size class:** 2 (Medium landing pad — docks at outposts and all larger ports)
- **Role:** Exploration / multirole (long-range explorer, light combat, trade)
- **Hull cost:** 35,741,519 CR (hull only)
- **Retail cost:** 37,472,252 CR (with stock modules)
- **Crew seats:** 2 (pilot + one multicrew seat; **no Ship-Launched Fighter bay**)

## Hull Stats

Source: Coriolis-data ship definition `krait_phantom` (edID 128839281).

- **Hull mass:** 270 t (light — 50 t under the Krait Mk II's 320, for longer jumps)
- **Top speed:** 250 m/s · **Boost:** 350 m/s
- **Base shield strength:** 200 MJ
- **Base armour:** 180 · **Hull hardness:** 55
- **Heat capacity:** 300
- **Mass lock factor:** 14
- **Manoeuvrability (deg/s):** pitch 26 · roll 90 · yaw 10
- **Reserve fuel:** 0.63 t
- **No fighter bay** (`fighterHangars` absent — unlike the Mk II)

## Slot Layout

- **Core internals:** Power Plant **7**, Thrusters **6**, Frame Shift Drive **5**,
  Life Support **4**, Power Distributor **7**, Sensors **6**, Fuel Tank **5**
  (identical core layout to the Krait Mk II).
- **Hardpoints:** **2 × Large + 2 × Medium** (four weapon mounts — one Large fewer than the
  Mk II's 3 L + 2 M).
- **Utility mounts:** 4.
- **Optional internals:** sizes **6, 5, 5, 5, 3, 3, 3, 2, 1** plus a reserved class-1
  **Planetary Approach Suite**. **No Military slots** (like the Mk II).

The optional bank is deep (nine slots) but leaner at the top end than the Mk II's (one class-6
plus three class-5, versus the Mk II's two class-6). Combined with the low hull mass and no
fighter bay, that biases the Phantom toward fuel scoop + Guardian FSD booster + AFMU
exploration fits rather than the Mk II's heavier combat/cargo loadouts.

## Exploration / Build Notes

The Phantom's low mass and class-5 FSD make it a natural long-range explorer:

- Engineer the FSD for Increased Range at [[engineers/felicity-farseer]], add a
  [[outfitting/guardian-fsd-booster]] for +LY per jump and a [[outfitting/fuel-scoop]] for
  unlimited range between scoopable stars.
- The class-7 power distributor and 2 L + 2 M hardpoints still give it credible self-defence and
  light combat capability for a multirole role.
- As a medium-pad hull it docks anywhere with at least a medium pad — handy deep in the black.

It can also run anti-Xeno duty, though with no Military slots and lighter armour (180) it is less
of a tank than the Alliance hulls; AX combat zones, Spire sites and Titan wrecks all remain
**live** if you choose to take it there. Bulkheads give **no caustic resistance** (`causres 0` on
every grade), so fit a Meta-Alloy [[outfitting/hull-reinforcement]] for AX caustic protection.

## Versus the Krait Mk II

Both are class-2 medium-pad Faulcon DeLacy hulls sharing the same core-slot layout; pick by role:

- **Krait Phantom** — the **explorer**: lighter (hull mass 270 vs 320), faster (250 / 350 vs
  240 / 330), no fighter bay, 2-seat crew, and cheaper (≈35.7 M vs ≈44.2 M CR hull). Fewer guns
  (2 L + 2 M vs 3 L + 2 M) and slightly less shield/armour (200 / 180 vs 220 / 220), but the lower
  mass means a longer jump range.
- **[[ships/krait-mk-ii|Krait Mk II]]** — the **combat multirole**: an extra Large hardpoint, a
  Ship-Launched Fighter bay, a third crew seat and a bigger top-end optional bank (two class-6).
  Pick it for firepower and flexibility when jump range matters less.

## Acquisition

Sold at large stations carrying a shipyard. Engineer the FSD for jump range at
[[engineers/felicity-farseer]] (Increased Range). Check Spansh (`spansh.co.uk/stations`) for
nearest stock.

[[trunk]]
