---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/viper.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T00:00:00+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Viper Mk III

The Viper Mk III is **Faulcon DeLacy's fast-attack small-pad interceptor** — the iconic cheap, fast
budget bounty-hunter. Its signature is raw speed on a featherweight 50 t hull: 320 m/s base / 400
boost, the fastest base speed of any ship paged in this KB. It is also the **cheapest hull in the
KB** (96,733 CR), making it the classic first dedicated combat ship. The trade-offs are thin armour,
a hot-running heat capacity, and short legs — but it carries a class-3 Military slot uncommon on so
small a hull.

## Overview

- **Manufacturer:** Faulcon DeLacy
- **Size class:** 1 (Small landing pad — docks anywhere, including outposts and planetary ports)
- **Role:** Fast-attack combat (bounty hunting, interception, Conflict Zones)
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data)
- **Hull cost:** 96,733 CR (hull only — the cheapest ship in the KB)
- **Retail cost:** 142,931 CR (with stock modules)
- **Crew seats:** 1

## Hull Stats

Source: Coriolis-data ship definition `viper` (= the Mk III; the Mk IV is a separate hull). edID
128049273, eddbID 22.

- **Hull mass:** 50 t — by far the lightest hull in the KB (next-lightest are the Cobra Mk III at
  180 t and the Diamondback Scout at 170 t). The low mass is the basis of its speed.
- **Top speed:** 320 m/s · **Boost:** 400 m/s — the **highest base speed of any ship paged here**
  (the Cobra Mk III matches the 400 boost but only 280 base).
- **Base shield strength:** 105 MJ
- **Base armour:** 70 · **Hull hardness:** 35 (low — it survives by speed, not by tanking)
- **Heat capacity:** 195 — low; the Viper runs hot, the opposite of the cool-running Diamondbacks
  (346/351). Manage heat with a [[outfitting/heat-sink-launcher]] when running energy weapons.
- **Mass lock factor:** 7
- **Manoeuvrability (deg/s):** pitch 35 · roll 90 · yaw 15
- **Reserve fuel:** 0.41 t

## Slot Layout

- **Core internals:** Power Plant **3**, Thrusters **3**, Frame Shift Drive **3**,
  Life Support **2**, Power Distributor **3**, Sensors **3**, Fuel Tank **2**. A small core capped
  at class-3, and a tiny class-2 fuel tank — the Viper has short legs and is built for short,
  intense engagements close to home, not roaming.
- **Hardpoints:** 2 × Medium + 2 × Small (four weapon mounts) — the same layout as the
  [[ships/cobra-mk-iii]].
- **Utility mounts:** 2 (chaff, heat sinks, a shield booster or point defence — choose carefully).
- **Optional internals:** sizes 3, 3, 2, 1, 1, 1 (six slots) plus **one class-3 Military slot**
  (eligible Meta-Alloy / standard Hull Reinforcement, Module Reinforcement, Shield Cell Bank or a
  Guardian reinforcement package) and a reserved class-1 **Planetary Approach Suite**. The Military
  slot is notable on so cheap and small a hull — it lets the Viper carry a reinforcement module
  without spending a normal optional.
- **Military slots:** one (class 3).

Bulkheads carry `causres 0` on every grade.

## Small-pad combat siblings

- **vs [[ships/vulture]]:** the Vulture is the step-up brawler — two Large hardpoints, a high base
  shield (240) and best-in-KB roll, but it is far heavier, pricier (~4.9 M CR) and power-constrained.
  The Viper is the fast, cheap interceptor: lighter, quicker, and a fraction of the cost, but with
  four smaller mounts (2 Medium + 2 Small) and thin armour.
- **vs [[ships/cobra-mk-iii]]:** the same four-mount hardpoint layout, but the Viper is faster
  (320 vs 280 base), lighter (50 vs 180 t) and cheaper, and it adds a class-3 Military slot the
  Cobra lacks. The Cobra has eight optionals and 2 utility — more cargo/role flexibility and a
  multirole bent — while the Viper is the pure fast fighter.
- **vs [[ships/diamondback-scout]]:** the Scout matches the four-mount layout but runs far cooler
  (heat capacity 346 vs 195), carries 4 utility mounts (vs 2) and more armour; the Viper answers
  with greater speed, lower price and a Military slot.

## Build notes

The textbook fit is two Medium + two Small weapons (gimballed multi-cannons or pulse/burst lasers
to spare the class-3 distributor), a fast-charging shield, and chaff plus a heat sink in the two
utility mounts. Engineer Dirty Drive Tuning on the thrusters to push the already-high speed, and put
a Hull or Module Reinforcement in the Military slot to offset the thin armour. Engineer the FSD at
[[engineers/felicity-farseer]] if you want to extend its short legs.

## Acquisition

Widely stocked — sold at most stations with a shipyard and one of the first combat ships many
commanders buy. Check Spansh (`spansh.co.uk/stations`) for nearest stock.

[[trunk]]
