# Loop 15 — Guardian "specials": shield reinforcement, Gauss cannon (AX-weapon seed), FSD booster

Mode: search · 3 Tier-0 Coriolis sources, all `availability: live`, no discards, no escalations.

## What changed
- **NEW** `kb/outfitting/guardian-shield-reinforcement.md` (`gsrp`) — powered optional internal,
  classes 1–5, ratings E/D only. `shieldaddition` = **flat MJ** added to shield strength (the shield
  analogue of the HRP's flat HP); not a multiplier, not active recharge. integrity const 36. D > E in
  MJ at half mass / more power / ~3× cost. C1 E 44 MJ 0.35 MW → C5 D 215 MJ 1.26 MW. Completes the
  **Guardian defensive trio**: gsrp (shields) + ghrp (hull) + gmrp (modules). Guardian Tech Broker
  unlock. source_count 1, verified false.
- **NEW** `kb/outfitting/guardian-gauss-cannon.md` (`ggc`) — **seeds the AX-weapon layer**.
  Fixed-mount only, experimental, **100% thermal** (`damagedist {T:1}`), piercing 140, charge-fired
  clip 1, range 3000. Two sizes: C1 small D (dmg 22) + C2 medium B (dmg 38.5). Plus two pre-engineered
  cost-0 reward variants "Gauss (HCap + RFire)" (G1 High Capacity + Rapid Fire, locked: not
  re-engineerable / grade-changeable / experimental; clip 2 / ammo 200, lower per-shot dmg 9.6/18.3).
  High distdraw + thermload (pair with the heat-sink-launcher). Guardian unlock. source_count 1,
  verified false.
- **NEW** `kb/outfitting/guardian-fsd-booster.md` (`gfsb`) — powered optional internal, classes 1–5,
  single rating H. `jumpboost` = **flat +LY** per jump, stacks additively on the FSD (does not replace
  it). mass const 1.3 t, integrity const 32. C1 +4.0 LY 0.75 MW → C5 +10.5 LY 2.14 MW; diminishing
  class-to-class returns. desc: "…at the cost of overall fuel efficiency." source_count 1, verified
  false.

## Cross-links
- `kb/trunk.md` — 3 new Outfitting bullets + an AX-weapon seed line in the AX/Thargoid section.
- `kb/mechanics/frame-shift-drive.md` — wikilinked to the new booster page; added the Tier-0 booster
  JSON as an independent corroborating source for the "+10.5 ly at class 5" figure → source_count
  2→3, stays verified **true**.
- `kb/outfitting/frame-shift-drive.md` — wikilinked its Guardian FSD Booster prose references.
- `kb/outfitting/hull-reinforcement.md` + `module-reinforcement.md` — added bidirectional
  Guardian-defensive-trio backlinks to the new GSRP page.

## Verify (local council, qwen3-coder:30b + qwen3:8b)
- frame-shift-drive (mechanics) → **verified**, confidence 0.95, escalate false (2/2 support; the
  Tier-0 booster JSON independently confirms +10.5 LY at class 5).
- guardian-shield-reinforcement → skipped (source_count 1, no conflict).
- guardian-gauss-cannon → skipped (source_count 1, no conflict).
- guardian-fsd-booster → skipped (source_count 1, no conflict).

## Path notes
All 3 queue paths resolved first try (gsrp / ggc / gfsb, no 404). Re-fetched `modules/index.js` to
confirm follow-on AX-weapon paths — `require('./x')` with no extension = the `.json` file.

## Follow-ons queued (paths CONFIRMED via index.js)
Guardian Plasma Charger (`gpc`), Guardian Shard Cannon (`gsc`) → complete the Guardian AX-weapon
trio; AX Multi-Cannon (`axmc`) → the standard AX kinetic workhorse. Other AX paths noted for later:
`axmce`, `axmr`, `axmre`, `rfl`, `tbrfl`, `tbem`, `ntp`.
