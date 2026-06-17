---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/imperial_courier.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:26:26Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Imperial Courier

The Imperial Courier is **Gutamaya's fast, low-profile Imperial light combat ship** — the other
Gutamaya small-pad hull alongside the [[ships/imperial-eagle]]. Its calling card is **three Medium
hardpoints on a size-1 airframe** backed by an unusually strong 200 MJ shield: more concentrated,
mid-calibre firepower than any other small-pad ship in the KB, carried on a light, agile hull that
docks anywhere. Unlike its no-gate Imperial Eagle sibling, the Courier **requires an Empire rank
(Master)** to purchase — the more "Imperial" of the Gutamaya small-pad pair.

## Overview

- **Manufacturer:** Gutamaya (an Imperial ship — and, unlike the Imperial Eagle, **rank-gated**)
- **Size class:** 1 (Small landing pad — docks anywhere, including outposts and planetary ports)
- **Role:** Fast light combat / skirmisher / shield-tanky interceptor (bounty hunting, dogfighting)
- **Rank requirement:** Empire rank **Master** (`empireRank` 3 in the Coriolis data) — credits alone
  are not enough; you must reach the third Imperial rank first.
- **Hull cost:** 2,484,137 CR (hull only)
- **Retail cost:** 2,542,931 CR (with stock modules)
- **Crew seats:** 1

## Hull Stats

Source: Coriolis-data ship definition `imperial_courier` (edID 128671223, eddbID 14).

- **Hull mass:** 35 t — **ties the [[ships/adder]] for the joint third-lightest hull in the KB**,
  behind only the [[ships/hauler]] (14 t) and [[ships/sidewinder]] (25 t). The low mass keeps it
  nimble and gives respectable range.
- **Top speed:** 280 m/s · **Boost:** 380 m/s — fast, though not quite the 300/400 of the
  [[ships/imperial-eagle]].
- **Base shield strength:** 200 MJ — **very high for a size-1 hull, second only to the
  [[ships/vulture]]'s 240 MJ among the small-pad ships paged here**. This strong shield (well above
  the Imperial Eagle's 80 or the Viper Mk IV's 150) is the Courier's signature: it fights from behind
  a tough shield rather than relying on armour.
- **Base armour:** 80 — thin. The Courier is a shield-tank, not an armour-tank; with light bulkheads
  it folds quickly once the shield drops.
- **Hull hardness:** 30 (low)
- **Heat capacity:** 230 (mid-pack — comfortably above the [[ships/hauler]]'s KB-low 123)
- **Mass lock factor:** 7
- **Manoeuvrability (deg/s):** pitch 38 · roll 90 · yaw 16. Agile, but its roll of 90 is in the
  mid-tier — short of the [[ships/eagle]]'s class-leading 120 and the roll-100 group
  ([[ships/imperial-eagle]], [[ships/adder]], [[ships/cobra-mk-iii]]).
- **Reserve fuel:** 0.41 t

## Slot Layout

- **Core internals:** Power Plant **4**, Thrusters **3**, Frame Shift Drive **3**, Life Support **1**,
  Power Distributor **3**, Sensors **2**, Fuel Tank **3**. The Courier carries a **bigger core than the
  [[ships/imperial-eagle]]** — a class-4 Power Plant and a class-3 Power Distributor (vs the Imperial
  Eagle's class-3 plant and class-2 distributor) — necessary to power three Medium weapons and the
  heavy shield.
- **Hardpoints:** **3 × Medium** (three weapon mounts) — the **signature**, and the most Medium mounts
  of any small-pad hull in the KB. Concentrated mid-calibre firepower on a size-1 airframe.
- **Utility mounts:** 4 (generous for a small hull — room for chaff, heat sinks, shield boosters and
  point defence; matches the [[ships/vulture]] and [[ships/diamondback-scout]]).
- **Optional internals:** sizes 3, 3, 2, 2, 2, 1, 1, 1 (eight regular slots, top two class-3) plus a
  reserved class-1 **Planetary Approach Suite**. **No Military slot.**
- **Military slots:** none — a notable contrast with the [[ships/imperial-eagle]], which has one
  class-2 Military slot. On the Courier, any hull/module reinforcement must come out of the eight
  regular optionals.

Bulkheads carry `causres 0` on every grade.

## The Gutamaya small-pad pair

- **vs [[ships/imperial-eagle]]:** the two Gutamaya small-pad ships split by philosophy. The
  **Imperial Eagle** is the cheaper (73 k vs 2.48 M CR hull), no-rank-gate light fighter — faster
  (300/400), with 1 Medium + 2 Small mounts and a class-2 Military slot. The **Imperial Courier** is
  the rank-gated step up in firepower and survivability — **three Medium mounts**, a much stronger
  shield (200 vs 80 MJ), a bigger core and four utility slots — but it costs far more, runs slightly
  slower and has no Military slot. Pick the Eagle to start cheap; pick the Courier once you have the
  Empire rank and credits for a serious shield-brawling skirmisher.
- **vs [[ships/viper-mk-iii]]:** the Viper Mk III is the Faulcon DeLacy fast-attack rival — faster
  still (320/400), no rank gate, with 2 Medium + 2 Small mounts and a class-3 Military slot but a thin
  105 MJ shield. The Courier trades a little speed for a far stronger shield and a third Medium mount;
  the Viper is the cheaper, harder-hitting-on-paper interceptor, the Courier the tankier dogfighter.
- **vs [[ships/vulture]]:** the Vulture is the small-pad heavy fighter — two **Large** mounts and a
  240 MJ shield, but a notorious class-4 power-plant bottleneck and a much heavier hull. The Courier
  fields three Medium mounts (lighter calibre, but no power crisis) on a far lighter, rank-gated hull.

## Build notes

The Courier is the small-pad **shield-brawler skirmisher**. Mount three gimballed Medium weapons
(multi-cannons or pulse/burst lasers) and lean on the strong 200 MJ shield with a bi-weave generator
and shield boosters in two of the four utility slots; use the others for a chaff launcher and a heat
sink. The class-4 Power Plant and class-3 Power Distributor give more headroom than the Imperial Eagle,
so sustained fire from three Mediums is viable — but watch the thin 80 armour: once the shield is down
the Courier is fragile, so disengage and let it regenerate rather than trading hull. With no Military
slot, any hull reinforcement competes with cargo/utility internals, so build around the shield.

## Acquisition

Stocked at Imperial shipyards and many others, but **only purchasable once you reach Empire rank
Master** (`empireRank` 3). Its small pad means it can be based out of outposts and planetary ports.
Check Spansh (`spansh.co.uk/stations`) for the nearest source.

[[trunk]]
