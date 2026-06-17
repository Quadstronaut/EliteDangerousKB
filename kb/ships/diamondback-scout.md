---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/diamondback_scout.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T00:00:00+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Diamondback Scout

The Diamondback Scout (DBS) is **Lakon Spaceways' cheap, light small-pad combat/recon ship** — the
budget sibling of the [[ships/diamondback-explorer]]. Where the Explorer is the ranged variant, the
Scout is the nimble entry fighter: more weapon mounts on a lighter, cheaper hull, and it inherits
the Diamondback family's hallmark **cool-running heat capacity**. As a size-1 hull it docks
anywhere, including outposts.

## Overview

- **Manufacturer:** Lakon Spaceways
- **Size class:** 1 (Small landing pad — docks anywhere, including small outposts and planetary ports)
- **Role:** Light combat / reconnaissance (cheap entry combat hull)
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data)
- **Hull cost:** 463,926 CR (hull only)
- **Retail cost:** 564,329 CR (with stock modules)
- **Crew seats:** 1 (single-seat — no multicrew co-pilot, like the DBX)

## Hull Stats

Source: Coriolis-data ship definition (top-level key `diamondback`, file `diamondback_scout.json`;
edID 128671217, eddbID 6).

- **Hull mass:** 170 t (lighter than the DBX's 260 t — cheaper and quicker)
- **Top speed:** 280 m/s · **Boost:** 380 m/s
- **Base shield strength:** 120 MJ
- **Base armour:** 120 · **Hull hardness:** 40 (low — not a heavy combat hull)
- **Heat capacity:** 346 — very high; second only to its [[ships/diamondback-explorer]] sibling
  (351) among ships paged in this KB. This confirms the Diamondback family's famed cool-running
  trait: the Scout, like the Explorer, resists heat far better than rival small hulls.
- **Mass lock factor:** 8
- **Manoeuvrability (deg/s):** pitch 42 · roll 100 · yaw 15 (agile)
- **Reserve fuel:** 0.49 t

## Slot Layout

- **Core internals:** Power Plant **4**, Thrusters **4**, Frame Shift Drive **4**,
  Life Support **2**, Power Distributor **3**, Sensors **2**, Fuel Tank **4**. The class-4
  [[outfitting/frame-shift-drive]] gives modest range — markedly less than the DBX's class-5 FSD,
  which is the deliberate split in the Diamondback pair: the Scout is the cheap fighter, the
  Explorer is the long-range hull.
- **Hardpoints:** 2 × Medium + 2 × Small (four weapon mounts) — one more mount than the DBX's three,
  but no Large slot.
- **Utility mounts:** 4 (heat sinks, shield boosters, chaff, point defence).
- **Optional internals:** sizes 3, 3, 3, 2, 1, 1 (six slots, top class-3) plus a reserved class-1
  **Planetary Approach Suite** (planet-landing and SRV capable). Shallower than the DBX (eight
  slots, top class-4).
- **Military slots:** none (contrast the small-pad [[ships/viper-mk-iii]], which has a class-3
  Military slot).

Bulkheads carry `causres 0` on every grade, so for any AX detour fit a Meta-Alloy
[[outfitting/hull-reinforcement]] package for caustic resistance.

## Diamondback pair: Scout vs Explorer

Both are Lakon small-pad, single-seat, cool-running hulls; the split is combat/recon vs range.

- **Diamondback Scout — cheap combat/recon.** 170 t, hull ~464 k CR, class-4 FSD. More weapon
  mounts (2 Medium + 2 Small = four) and lighter/cheaper, but shallower internals (six, top
  class-3) and lower shield/armour (120/120).
- **[[ships/diamondback-explorer]] — ranged.** 260 t, hull ~1.6 M CR, class-5 FSD. One Large
  mount, deeper internals (eight, top class-4), slightly higher shield/armour (150/150) and the
  KB's highest heat capacity (351). The choice when jump range matters.

Pick the Scout for a cheap, cool, nimble small-pad fighter or scout; the Explorer when you need
range.

## Small-pad combat siblings

- **vs [[ships/viper-mk-iii]]:** the Viper is faster (320/400 vs 280/380) and far lighter/cheaper,
  and it carries a Military reinforcement slot — but it runs hot (heat capacity 195) and has only 2
  utility mounts and lower armour (70). The Scout trades raw speed for the Diamondback's cool
  running, double the utility mounts (4) and more armour.
- **vs [[ships/cobra-mk-iii]]:** same four-mount layout (2 Medium + 2 Small), but the Cobra has
  eight optionals (more cargo/role flexibility) while the Scout brings 4 utility mounts and far
  better heat capacity for a recon/combat lean.
- **vs [[ships/vulture]]:** the Vulture is the dedicated brawler (two Large mounts, high shield);
  the Scout is the cheaper, cooler, more flexible light fighter/scout.

## Build notes

A light combat fit pairs two Medium + two Small weapons (gimballed multi-cannons or pulse lasers),
a shield with boosters in the utility mounts, and the class-4 FSD engineered for range at
[[engineers/felicity-farseer]]. The high heat capacity makes it forgiving when running energy
weapons or scooping between systems on a recon sweep.

## Acquisition

Sold at stations carrying a shipyard; as a long-standing Lakon hull it is widely stocked and, being
small-pad, can be based out of outposts. Check Spansh (`spansh.co.uk/stations`) for the nearest
source, then engineer the FSD at Farseer Inc in [[locations/deciat]].

[[trunk]]
