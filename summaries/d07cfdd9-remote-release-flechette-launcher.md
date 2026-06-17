---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/remote_release_flechette_launcher.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:20:16+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Remote Release Flechette Launcher (tbrfl) — Coriolis Tier-0 summary

Group `tbrfl`, file `hardpoints/remote_release_flechette_launcher.json`, symbol
`Hpt_FlechetteLauncher_*_Medium`. The **kinetic** sibling of the explosive
[[outfitting/remote-release-flak-launcher|Remote Release Flak Launcher]] (`rfl`) — the other
remote-detonation anti-swarm weapon. AX/Thargoid content → `availability: live`.

## Key claims (parsed directly from JSON)

- **100% kinetic** damage `damagedist {K:1}` — fires flechette (shrapnel) rounds, NOT explosive
  (this is the key contrast with the flak launcher's `{E:1}`).
- **NOT flagged `experimental`** in the data (no `experimental: true` key) — unlike the AX missile/MC lines.
- **2 variants**, Class 2 (Medium) only, rating B, Fixed + Turret:
  - xy — Medium Fixed, dmg 13, piercing **80**, ammo 72, clip 1, reload 2, cost 353,761
  - yF — Medium Turret, dmg 13, piercing **70**, ammo 72, clip 1, reload 2, cost 1,279,200
- Constants: power 1.20, mass 4, integrity 51, fireint 2.0, thermload 3.6, shotspeed 550, distdraw 0.24,
  **breachdmg 6.5** (breachmin/max 1) — notable module-breach damage on penetration.

## Diffs vs Remote Release Flak Launcher (rfl)

- **Kinetic (`K:1`) vs flak's explosive (`E:1`)** — shrapnel cloud, not a blast burst.
- **More ammo**: 72 vs flak's 32; **lower per-hit dmg**: 13 vs flak's 34.
- **Higher piercing**: 80/70 vs flak's 60; plus **breachdmg 6.5** (flak had no breach damage).
- Shared: Class 2 only, rating B, Fixed+Turret, mass 4, power 1.20, shotspeed 550, fireint 2.0,
  reload 2, clip 1, thermload 3.6 → both are single-shot remote-detonation anti-swarm weapons.

availability=live, obsolete=NO. claims=5. Tier-0 structured, no LLM.
