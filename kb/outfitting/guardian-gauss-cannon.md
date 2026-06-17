---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/guardian_gauss_cannon.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T00:43:20+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Guardian Gauss Cannon (Outfitting)

The **Guardian Gauss Cannon** is the premier **AX (anti-Xeno) anti-Interceptor weapon** — a
**fixed-mount, charge-fired** hardpoint that deals pure **thermal** damage with very high armour
piercing. It is the workhorse for stripping Thargoid Interceptor hearts. In the Coriolis data it is
group `ggc`, file `hardpoints/guardian_gauss_cannon.json`, flagged `experimental: true`. This page
seeds the KB's **AX-weapon layer**. AX/Thargoid content remains `availability: live` — never present
it as gone.

## What it does

- **100% thermal damage** (`damagedist {T: 1}`) — Gauss cannons bypass much of an Interceptor's
  conventional defence and chew through exposed hearts.
- **Fixed mount only** (`mount: "F"`). There is no gimballed or turreted Gauss; you must aim it.
- **Charge-fired.** The cannon charges before each shot and carries a **clip of 1** — one charged
  shot, then a short reload — so its damage is delivered in deliberate, aimed pulses rather than a
  stream. Plan WEP pips and heat around each shot.
- **High armour piercing** (`piercing: 140`) and a meaningful **breach** chance to damage modules
  behind armour.
- **Range 3000 m**, damage falloff beginning at 1500 m (standard) — engage at mid range.

The two costs of fielding it: a **high distributor draw** (`distdraw`) that empties the WEP
capacitor quickly, and a **high thermal load** (`thermload`) that spikes ship heat — pair it with a
[[outfitting/heat-sink-launcher]] and a strong power distributor.

## Variants and stats

Two sizes — **class 1 (small, rating D)** and **class 2 (medium, rating B)** — each in a **standard**
form and a **pre-engineered reward** form. The reward variants ("Gauss (HCap + RFire)") come
**pre-engineered with Grade 1 High Capacity + Rapid Fire**, cost **0 CR**, and are **locked**: not
re-engineerable, grade cannot be changed, and no experimental effect can be applied. They trade
per-shot damage for a larger clip/ammo reserve and sustained fire.

| Variant | Class | Rating | Dmg/shot | Fire int (s) | Clip / Ammo | Distdraw | Thermload | Power (MW) | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|
| Standard | 1 (Small) | D | 22 | 0.83 | 1 / 80 | 3.8 | 15 | 1.91 | 2 | 167,250 |
| Standard | 2 (Medium) | B | 38.5 | 0.83 | 1 / 80 | 7.2 | 25 | 2.61 | 4 | 543,801 |
| HCap + RFire (reward) | 1 (Small) | D | 9.6 | 1.15 | 2 / 200 | 3.8 | 15 | 1.91 | 2 | 0 |
| HCap + RFire (reward) | 2 (Medium) | B | 18.3 | 1.15 | 2 / 200 | 7.2 | 25 | 2.61 | 4 | 0 |

The medium Gauss is the heavy hitter (38.5 thermal/shot); the small fits ships short on hardpoint
size. The pre-engineered reward variants are valued for their **doubled clip (2) and ammo (200)** —
far more sustained fire before reloading — at lower listed per-shot damage.

## How to fit

- Goes in a **fixed hardpoint** of the matching size (small or medium). Multi-Gauss AX builds mount
  several fixed Gauss and fire them in sync on a charged release.
- **Power your distributor and cool your hull.** The high WEP draw rewards a high-rating power
  distributor; the high heat rewards a [[outfitting/heat-sink-launcher]] for venting between volleys.
- Used against **Thargoid Interceptors** (Cyclops → Hydra) and at AX combat zones, Spire sites and
  Titan wrecks — all `availability: live`.

## Where to get them

The Guardian Gauss Cannon is a **Guardian Technology Broker** unlock (`requirements.horizons: true`):
gather Guardian blueprint fragments and materials at a Guardian Structure site (see Canonn's Guardian
site map), then unlock at a station with a Tech Broker. The cost-0 pre-engineered "HCap + RFire"
variants are reward modules, not standard stock.

## Related AX weapons

The Guardian AX-weapon trio: this Gauss Cannon (long-range thermal, anti-Interceptor specialist),
[[outfitting/guardian-plasma-charger]] (absolute-damage charge burst), and
[[outfitting/guardian-shard-cannon]] (close-range thermal shotgun). The non-Guardian
[[outfitting/ax-multi-cannon]] is the standard kinetic AX workhorse that needs no Guardian unlock.

[[trunk]]
