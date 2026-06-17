---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/standard/frame_shift_drive.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T00:32:57+00:00
source_count: 1
verified: false
availability: live
changed_note: FSD (SCO) Supercruise Overcharge variant added in Update 18 (2024) — now the default drive on new ships. The legacy FSD is still sold.
---

# Frame Shift Drive (Outfitting)

This page is the **module reference** for the Frame Shift Drive core internal — classes, ratings,
optimal mass, fuel-per-jump and cost. For how jump range is *calculated*, engineering, neutron
boosting and the [[outfitting/guardian-fsd-booster|Guardian FSD Booster]], see the mechanics page
[[mechanics/frame-shift-drive]].

The FSD is a mandatory **core internal** sized to the ship. Coriolis lists two parallel lines:
the original **legacy FSD** and the newer **FSD (SCO)** — Supercruise Overcharge — drive.

## Legacy vs SCO — which to buy

**The FSD (SCO) is the current default.** It was added in Update 18 (2024) and ships on every
post-2024 hull. Versus the legacy drive at the same class/rating it has **higher optimal mass**
(so equal or slightly longer jumps) **and** adds the Supercruise Overcharge ability. There is
almost no reason to buy a legacy FSD today; the legacy line is documented here only because it
is still sold and still fitted on older saved builds.

`availability: live` — both lines are currently purchasable.

## Supercruise Overcharge (SCO)

Holding the throttle at maximum in supercruise **overcharges** an SCO drive, pushing in-system
speed far above the normal cap and slashing travel time to distant bodies. The trade-offs:
higher **fuel burn** and **heat** while overcharging, and reduced manoeuvrability at speed. SCO
behaviour is built into the drive — no separate module or engineering is required to use it.

## A-rated module table — Legacy FSD

A-rated gives the best optimal mass (and therefore range) in each class. Legacy tops out at class 7.

| Class | Optimal mass | Max fuel/jump | Power | Cost (CR) |
|---|---|---|---|---|
| 2A | 90 t | 0.9 t | 0.30 | 160,224 |
| 3A | 150 t | 1.8 t | 0.45 | 507,912 |
| 4A | 525 t | 3.0 t | 0.45 | 1,610,080 |
| 5A | 1,050 t | 5.0 t | 0.60 | 5,103,953 |
| 6A | 1,800 t | 8.0 t | 0.75 | 16,179,531 |
| 7A | 2,700 t | 12.8 t | 0.90 | 51,289,112 |

## A-rated module table — FSD (SCO)

SCO adds a class 8 (the only class-8 FSD in the game) and carries higher optimal mass per class.

| Class | Optimal mass | Max fuel/jump | Power | Cost (CR) |
|---|---|---|---|---|
| 2A | 100 t | 1.0 t | 0.30 | 192,269 |
| 3A | 167 t | 1.9 t | 0.45 | 609,494 |
| 4A | 585 t | 3.2 t | 0.45 | 1,932,096 |
| 5A | 1,175 t | 5.2 t | 0.60 | 6,124,743 |
| 6A | 2,000 t | 8.3 t | 0.75 | 19,415,437 |
| 7A | 3,000 t | 13.1 t | 0.90 | 61,546,935 |
| 8A (Mk II) | 4,670 t | 6.8 t | 1.05 | 82,042,060 |

- **Class-5A SCO** (optmass 1,175 t vs the legacy 1,050 t) is the explorer/medium workhorse —
  e.g. the [[ships/mandalay]] runs a class-5 FSD on a light hull for class-leading range.
- **Frame Shift Drive Mk II (SCO)** is the top 8A variant. Its fuel-power exponent (2.5025) is
  lower than the standard SCO line (2.9), giving better range scaling for the heaviest hulls
  (the [[ships/type-9-heavy]], [[ships/panther-clipper-mk-ii]] and other large ships).

## Ratings beyond A

Each class also comes in B/C/D/E. Lower ratings cost far less and weigh differently (D is the
lightest, useful for shaving mass on a budget; B is heaviest/toughest) but give shorter jumps.
For range-focused builds, A-rate the FSD and engineer it — see [[mechanics/frame-shift-drive]].
Stack a [[outfitting/guardian-fsd-booster|Guardian FSD Booster]] on top for a flat per-jump bonus.

[[trunk]]
