# Loop 18 — AX missile family completed (search mode)

3 new Tier-0 Coriolis outfitting pages, all `availability: live`, source_count 1, verified false.

## Pages

1. **kb/outfitting/ax-missile-rack-enhanced.md** (axmre, `Hpt_ATDumbfireMissile_*_v2`) — v2 upgrade of
   base AX Missile Rack. dmg 77 (Fixed) / 64 (Med Turret) vs base 64/50; shotspeed 1250 vs 750;
   higher power. 4 std variants, no pre-eng reward forms. Dumbfire only, `{X:1,E:1}`.
2. **kb/outfitting/remote-release-flechette-launcher.md** (tbrfl, `Hpt_FlechetteLauncher_*_Medium`) —
   kinetic (`{K:1}`) anti-swarm sibling of the Flak Launcher. dmg 13, ammo 72, piercing 80/70,
   breachdmg 6.5. Class 2 only, Fixed+Turret. Not experimental-flagged.
3. **kb/outfitting/enzyme-missile-rack.md** (tbem, `Hpt_CausticMissile_Fixed_Medium`) — caustic AX
   missile; enzyme DoT degrades Thargoid hull over time (DoT magnitude not in Coriolis data, not
   invented). `{E:1}`, direct dmg 5. Class 2 Medium Fixed only. Base + CG-reward "Caust Enzyme
   (High Cap)" locked variant.

## Edits / links

- Merged bidirectional "Related AX weapons" links + a Flak-vs-Flechette compare section into base
  `ax-missile-rack.md` and `remote-release-flak-launcher.md`.
- trunk.md: +3 Outfitting bullets; AX/Thargoid explosive line extended (enhanced + enzyme), anti-swarm
  line extended (flechette).

## Path notes

All 3 paths resolved first try (no 404); index.js re-fetched to confirm enzyme (`tbem` guess correct)
and nanite torpedo pylon (`ntp` -> `hardpoints/nanite_torpedo_pylon.json`). Follow-on queued: ntp =
LAST AX missile-family weapon. After ntp the AX-weapon line is complete; next coverage = AX-utility
modules (xeno scanner / shutdown field neutraliser / caustic sink launcher).

## Verify

Verify enabled, but all 3 pages are source_count 1 with no CONFLICT markers — none met the council
threshold (source_count >= 2 OR conflict). No escalation. Left verified=false (single Tier-0 source).
