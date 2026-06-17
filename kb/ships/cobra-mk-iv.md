---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/cobra_mk_iv.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T05:39:14+00:00
source_count: 1
verified: false
availability: live
changed_note: "Limited-availability ship — Coriolis flags `horizonsEarlyAdoption`; the Cobra Mk IV was a Horizons pre-order / early-adoption exclusive and is not generally purchasable. Existing owners fly it normally."
---

# Cobra Mk IV

The Cobra Mk IV is **Faulcon DeLacy's heavier, roomier sibling of the iconic
[[ships/cobra-mk-iii]]** — a small-pad multirole that trades the Mk III's signature speed and
agility for more internal capacity and an extra hardpoint. It shares the Mk III's exact core
internals but is heavier, slower and less nimble, with two more optional slots and one more weapon
mount. Its standout fact is **availability**: the Cobra Mk IV was a **Horizons pre-order /
early-adoption exclusive** and is **not generally purchasable** — the Coriolis data flags it
`horizonsEarlyAdoption`. Commanders who hold the entitlement fly it normally; everyone else cannot
buy one.

## Overview

- **Manufacturer:** Faulcon DeLacy
- **Size class:** 1 (Small landing pad — docks anywhere, including outposts and planetary ports)
- **Role:** Multirole (combat, light hauling, exploration) — the heavier Mk III variant
- **Rank requirement:** none — credits only (no rank gate). **BUT** the Coriolis data carries
  `requirements: { horizonsEarlyAdoption: true }` — a **limited-availability flag**, not a rank
  gate (see Availability below).
- **Hull cost:** 623,374 CR (hull only)
- **Retail cost:** 764,720 CR (with stock modules)
- **Crew seats:** 2

## Hull Stats

Source: Coriolis-data ship definition `cobra_mk_iv` (edID 128672262, eddbID 29).

- **Hull mass:** 210 t — **heavier than the Mk III's 180 t** (the roomier-but-bulkier sibling).
- **Top speed:** 200 m/s · **Boost:** 300 m/s — **slower than the Mk III's 280 / 400**; this is the
  core of the Mk III-vs-Mk IV trade.
- **Base shield strength:** 120 MJ — **higher than the Mk III's 80 MJ**.
- **Base armour:** 120 (same as the Mk III) · **Hull hardness:** 35 (same).
- **Heat capacity:** 228
- **Mass lock factor:** 8
- **Manoeuvrability (deg/s):** pitch 30 · roll 90 · yaw 10 — **less agile than the Mk III**
  (40 / 100 / 10).
- **Reserve fuel:** 0.51 t

## Slot Layout

- **Core internals:** Power Plant **4**, Thrusters **4**, Frame Shift Drive **4**, Life Support
  **3**, Power Distributor **3**, Sensors **3**, Fuel Tank **4** — **identical to the
  [[ships/cobra-mk-iii]]'s core**.
- **Hardpoints:** **2 × Medium + 3 × Small (five mounts)** — one more Small than the Mk III's
  2 Medium + 2 Small (four mounts). More guns, but on a slower, heavier platform.
- **Utility mounts:** 2 (same as the Mk III).
- **Optional internals:** sizes 4, 4, 4, 4, 3, 3, 2, 2, 1, 1 (ten regular slots, **top four
  class-4**) plus a reserved class-1 **Planetary Approach Suite** — **two more slots than the
  Mk III's eight** (which has three class-4). The extra internal room is the Mk IV's main draw.
- **Military slots:** none (the same as the Mk III).

Bulkheads carry `causres 0` on every grade.

## Cobra Mk IV vs Cobra Mk III

Both are small-pad Faulcon DeLacy multiroles sharing the same core internals. The **Mk III** is the
lighter, faster, more agile classic (180 t, 280/400, four hardpoints, eight optionals) and is
**freely purchasable** at most shipyards. The **Mk IV** is the heavier, slower variant (210 t,
200/300) that trades that agility for **more capacity** — ten optionals (four class-4), a fifth
(Small) hardpoint and a stronger 120 MJ shield. In practice the Mk IV's slower, less nimble
handling makes it the weaker dogfighter despite the extra gun, so it leans toward hauling and
utility roles. The decisive difference is availability: the Mk III is the one almost anyone can buy;
the Mk IV is a **limited Horizons early-adoption ship** most commanders cannot acquire.

For the modern small-pad multirole with the most mounts and a multicrew cockpit, see the newer
[[ships/cobra-mk-v]] (3 Medium + 2 Small, four utility, three crew seats), which completes the Cobra
line in the KB.

## Availability

The Coriolis data flags the Cobra Mk IV `horizonsEarlyAdoption: true`. Historically it was offered
as a **pre-order / early-adoption bonus for the Horizons season** and was never put on general sale,
so it is **not stocked for purchase** by commanders who lack that entitlement. It is **not removed**
and **not obsolete** — owners who have it fly it normally, and it remains a current ship definition —
but do not plan a build around buying one unless you already hold it. This caveat is the page's
`changed_note`: knowing the Mk IV is restricted prevents the bad decision of shopping for one.

## Acquisition

Not generally purchasable (see Availability) — there is no rank or credit gate, only the Horizons
early-adoption entitlement. Commanders who already own the Cobra Mk IV can swap to it at any
shipyard that lists it. There is no reliable way to acquire it new without the entitlement.

[[trunk]]
