---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/imperial_clipper.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:39:15Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Imperial Clipper

The Imperial Clipper is **Gutamaya's fast, elegant large-pad multirole** — the ship that extends the
Imperial/Gutamaya line beyond the small-pad pair ([[ships/imperial-eagle]] + [[ships/imperial-courier]])
up to a large hull. Its calling card is **speed**: at 300 m/s base / 380 m/s boost it is the **joint-fastest
large-pad ship in the KB** (tied with the [[ships/orca]] passenger liner), far quicker than any other
class-3 hull. It pairs that pace with **2 Large +
2 Medium hardpoints** (no Small mounts) and a famous quirk — despite a mid-size feel and handling, it
needs a **Large landing pad**. Buying one requires the Empire rank **Baron**.

## Overview

- **Manufacturer:** Gutamaya (an Imperial ship — rank-gated)
- **Size class:** 3 (Large landing pad only — large orbital and planetary ports; the Clipper's quirk:
  large-pad-restricted despite feeling like a medium)
- **Role:** Fast large-pad multirole (combat, transport, fast courier work, fun fly-by-wire flagship)
- **Rank requirement:** Empire rank **Baron** (`empireRank` 7 in the Coriolis data) — between the
  [[ships/imperial-courier]]'s Master (3) and the [[ships/imperial-cutter]]'s Duke (12).
- **Hull cost:** 21,116,895 CR (hull only)
- **Retail cost:** 22,295,860 CR (with stock modules)
- **Crew seats:** 2 (pilot + one multicrew seat; no Ship-Launched Fighter bay)

## Hull Stats

Source: Coriolis-data ship definition `imperial_clipper` (edID 128049315, eddbID 13).

- **Hull mass:** 400 t — light for a large hull (ties the [[ships/anaconda]]), which helps both speed
  and jump range.
- **Top speed:** 300 m/s · **Boost:** 380 m/s — **joint-fastest of any large-pad ship in the KB**,
  matched only by the [[ships/orca]] (the Saud Kruger liner is the same 300/380). The next-quickest
  large hull is the [[ships/imperial-cutter]] (200/320); the rest — Anaconda (180/240),
  [[ships/federal-corvette]] (200/260), [[ships/type-10-defender]] (179/219), [[ships/type-9-heavy]]
  (130/200), [[ships/panther-clipper-mk-ii]] (181/250) — trail well behind. Straight-line speed is the
  Clipper's signature.
- **Base shield strength:** 180 MJ · **Base armour:** 270 — modest for a large hull; the Clipper is a
  fast skirmisher/transport, not a tank.
- **Hull hardness:** 60
- **Heat capacity:** 304
- **Mass lock factor:** 12
- **Manoeuvrability (deg/s):** pitch 40 · roll 80 · yaw 18 — agile in pitch for a big ship (the
  fly-by-the-seat handling it is loved for), though its roll is large-hull slow.
- **Reserve fuel:** 0.74 t

## Slot Layout

- **Core internals:** Power Plant **6**, Thrusters **6**, Frame Shift Drive **5**, Life Support **5**,
  Power Distributor **6**, Sensors **5**, Fuel Tank **4**. A class-6 power plant and distributor feed the
  weapons; the class-6 thrusters on a light 400 t hull are what make it so fast.
- **Hardpoints:** **2 × Large + 2 × Medium** (four weapon mounts) — **no Small mounts**. All
  medium-or-bigger calibre, the Clipper's signature armament shape; the two Large mounts give it genuine
  punch for a fast multirole.
- **Utility mounts:** 4 (shield boosters, chaff, heat sinks, point defence).
- **Optional internals:** sizes 7, 6, 4, 4, 3, 3, 2, 2, 1 (nine regular slots, **top class-7**) plus a
  reserved class-1 **Planetary Approach Suite**. **No Military slot.**
- **Military slots:** none.

Bulkheads carry `causres 0` on every grade.

## The Gutamaya / Imperial line

- **vs [[ships/imperial-courier]]:** the Courier is the small-pad shield-brawler skirmisher (3 Medium
  mounts, 200 MJ shield, Master rank). The Clipper is the large-pad step up the same Imperial ladder —
  far bigger and faster, with Large mounts and nine optionals, but a higher Baron rank gate and a Large
  pad requirement.
- **vs [[ships/imperial-cutter]]:** the Gutamaya large-pad flagship pair. The **Cutter** is the
  Duke-gated shield-tank/bulk-trader — the highest base shield in the KB (600 MJ), twin class-8
  optionals, but heavy and only the second-fastest large hull (200/320). The **Clipper** is the cheaper,
  lighter, much faster (300/380), lower-gate (Baron) alternative — less tanky and less roomy, but the
  speed king of the large pad. Pick the Clipper for pace and a lower rank; the Cutter for tank and cargo.
- **vs [[ships/anaconda]]:** both light 400 t large hulls, but the Anaconda is the no-gate generalist
  with far more mounts/optionals and the best jump range, while flying slow (180/240). The Clipper trades
  the Anaconda's firepower and internals for raw speed and an easier (rank-only) feel in flight.

## Build notes

The Clipper is the large-pad **speed multirole**. Engineer dirty-drive thrusters to push its already
class-leading pace, arm the 2 Large + 2 Medium mounts with gimballed or fixed weapons to taste, and run a
bi-weave shield with boosters in two of the four utility slots. The light 400 t hull engineers into a
strong jump range — fit a class-5 FSD (Increased Range) at [[engineers/felicity-farseer]] for a fast
long-legged courier/explorer build. With no Military slot, hull reinforcement comes out of the nine
regular optionals, so most builds lean on the shield and speed rather than armour.

## Acquisition

Sold at Imperial shipyards and many large stations, but **only purchasable once you reach Empire rank
Baron** (`empireRank` 7). It needs a **Large landing pad** — no outposts. Check Spansh
(`spansh.co.uk/stations`) for the nearest source.

[[trunk]]
