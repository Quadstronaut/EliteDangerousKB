# Research Queue — next targets

One target per bullet. The orchestrator takes the top 1-3 each loop, dedups against
seen.json, and processes Tier-0 first. Append follow-on targets discovered during synthesis.

- https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/ax_missile_rack_enhanced.json (tier: 0, type: coriolis, note: Enhanced AX Missile Rack -> kb/outfitting/ax-missile-rack-enhanced.md (new) OR merge into ax-missile-rack.md. The upgraded axmr (done L17, dumbfire X+E, base done). PATH per index.js key axmre -> hardpoints/ax_missile_rack_enhanced.json. Parse damage/ammo/clip/damagedist/class+rating + note what "enhanced" changes vs base (likely shotspeed/dmg, maybe seeking). CONFIRM path via modules/index.js if 404.)
- https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/remote_release_flechette_launcher.json (tier: 0, type: coriolis, note: Remote Release Flechette Launcher -> kb/outfitting/remote-release-flechette-launcher.md (new). Sibling of the Flak Launcher (rfl, done L17) — the OTHER anti-swarm remote-detonation weapon; flechette rounds vs Thargoid swarms/scouts. PATH per index.js key tbrfl -> hardpoints/remote_release_flechette_launcher.json. Parse damage/ammo/damagedist/class+rating + remote-detonation note. CONFIRM path via index.js if 404.)
- https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/enzyme_missile_rack.json (tier: 0, type: coriolis, note: Enzyme Missile Rack -> kb/outfitting/enzyme-missile-rack.md (new). Caustic/enzyme AX missile that degrades Thargoid hull over time; distinct from the standard AX Missile Rack. PATH per index.js key tbem -> resolve filename via modules/index.js FIRST (enzyme_missile_rack.json is a guess; AX guns have had stale-slug 404s — check index.js require('./x')=.json before fetching). Parse damage/ammo/damagedist/class+rating + the enzyme DoT note. Sibling ntp = nanite torpedo pylon, also open.)

<!-- DONE loop 17: completed the standard (non-Guardian) AX-weapon line — 3 new Tier-0 Coriolis
     outfitting pages (all availability: live, source_count 1, verified false):
     (1) kb/outfitting/ax-multi-cannon-enhanced.md NEW (grp axmce, symbol Hpt_ATMultiCannon_*_V2 /
     Gimbal). The UPGRADE of base axmc (done L16). damagedist {X:1,K:1} (AX+kinetic, same as base).
     KEY DIFFS vs base: (a) ADDS GIMBAL mount — base is Fixed+Turret only, enhanced is Fixed+Gimbal+
     Turret; (b) shotspeed 4000 (2.5x base 1600) — far better hit rate on strafing Thargoids; (c)
     Lrg Fixed dmg 7.3 (vs base 6.1). NO Small (Med/Lrg only) — CORRECTS the L16 queue guess that
     said "adds Small mounts". ammo 2100, clip 100(F/G)/90(T), range 4000/falloff 2000, reload 4, low
     heat 0.10-0.28, power 0.46-0.69. 6 std variants (4W Med F D 3.9 / 4X Med G E 3.7 / 4Y Med T E 2.0
     / 4Z Lrg F B 7.3 / 5A Lrg G C 6.3 / 5B Lrg T D 3.9). 2 pre-eng gimbal reward variants "AX MC
     (OC, Auto-Load)" (5y Med E, 5z Lrg C): G5 Overcharged + Auto-Loader exp, NOT reeng/gradechange,
     canApplyExperimental TRUE. Where: Human Tech Broker (AX-weapon line). Also EDITED base
     ax-multi-cannon.md: fixed the wrong "Small mounts" Enhanced callout -> now correct (gimbal +
     2.5x shotspeed) + linked to new page; added a "Related AX weapons" section.
     (2) kb/outfitting/ax-missile-rack.md NEW (grp axmr, symbol Hpt_ATDumbfireMissile_*). The
     EXPLOSIVE AX leg. damagedist {X:1,E:1} (AX+explosive). DUMBFIRE ONLY (missile "D") — CORRECTS
     the queue note's "dumbfire/seeking"; no seeking variant in this file. 64 dmg/missile (Med F & both
     Lrg; Med T 50), piercing 60 (HIGH), falloff 10000 (full dmg to 10km), shotspeed 750, fireint 2.0,
     reload 5. Fixed+Turret, Med(2)+Lrg(3). ammo 64(M)/128(L), clip 8/12. 4 std variants (x4 Med F B /
     x5 Med T B / x6 Lrg F A / x7 Lrg T A). 2 pre-eng fixed reward variants "AX MRack (HCap+RFire)"
     (5w Med E, 5x Lrg C cost 0=CG reward): G5 HighCapacity+RapidFire, dmg 71.5, fireint 3.045,
     reload 7.85, NOT reeng/gradechange, canApplyExperimental FALSE.
     (3) kb/outfitting/remote-release-flak-launcher.md NEW (grp rfl, symbol Hpt_FlakMortar_*). The
     ANTI-SWARM support weapon — remote-detonated flak clears Thargoid Swarm clouds + Scout packs.
     damagedist {E:1} (100% explosive area burst). NOT flagged experimental in data. Class 2 (Medium)
     ONLY, rating B, Fixed+Turret. dmg 34, ammo 32, clip 1, reload 2, fireint 2.0, piercing 60,
     falloff 100000, shotspeed 550, thermload 3.6, power 1.2, mass 4. 2 variants (x8 Med F B cost
     261800 / x9 Med T B cost 1259200). NO Small/Large, NO pre-eng variant. It's a HARDPOINT weapon
     (not a utility — distinct from Point Defence). Where: AX war-effort supply chain, no Guardian unlock.
     trunk.md: +3 Outfitting bullets; AX/Thargoid section reworked into kinetic (axmc + enhanced) /
     explosive (axmr) / Guardian trio / anti-swarm (rfl) groupings. Bidirectional "Related AX weapons"
     links added across the new pages + base axmc.
     PATH NOTES: all 3 hardpoints/*.json (ax_multi_cannon_enhanced, ax_missile_rack,
     remote_release_flak_launcher) resolved first try, no 404 — index.js keys axmce/axmr/rfl confirmed.
     Follow-ons queued (paths via index.js, require('./x')=.json): Enhanced AX Missile Rack (axmre ->
     ax_missile_rack_enhanced), Remote Release Flechette Launcher (tbrfl ->
     remote_release_flechette_launcher), Enzyme Missile Rack (tbem -> CONFIRM filename via index.js).
     Remaining AX path still open: ntp (nanite torpedo pylon). -->


<!-- DONE loop 16: completed the Guardian AX-weapon trio + seeded the standard AX kinetic line.
     3 new Tier-0 Coriolis outfitting pages (all availability: live, source_count 1, verified false):
     (1) kb/outfitting/guardian-plasma-charger.md NEW (grp gpc, symbol Hpt_Guardian_PlasmaLauncher_*).
     CHARGE-UP weapon: hold to spin a plasma orb, release fires a burst expending up to the full clip
     of 15 rounds. 100% ABSOLUTE damage (damagedist A:1 — ignores all resistances). Fixed + Turret,
     Small/Medium/Large (C1/C2/C3) — fuller ladder than fixed-only Gauss. dmg/round 2-7, piercing
     65->95, range 3000 (C1/C3) / 3500 (C2), high distdraw 0.68->2.6, MODEST thermload 4.2->6.4 (much
     cooler than Gauss). clip 15 / ammo 200 / reload 3 / fireint 0.2 / shotspeed 1200 / falloff 1000.
     Pre-eng cost-0 "Plasma Charger (OC+Foc)" = C1 Fixed D + C2 Fixed B, G1 Overcharged+Focused, locked.
     Guardian Tech Broker unlock.
     (2) kb/outfitting/guardian-shard-cannon.md NEW (grp gsc, symbol Hpt_Guardian_ShardCannon_*).
     SHOTGUN: 12 shards/shot (roundspershot 12) + jitter 5; 100% THERMAL (damagedist T:1). SHORT range
     — range==falloff==1700 (full dmg to 1700 then hard cut). Fixed+Turret, C1/C2/C3. dmg/shard
     1.1-5.2 (x12 = 13.2-62.4/shot point-blank), piercing 30->60, VERY LOW thermload 0.6-2.2 (best
     sustained DPS of the trio). clip 5 / ammo 180 / reload 5 / fireint 0.6 / shotspeed 1133. Note C2
     Fixed is rating A (trio's only base-A). Pre-eng cost-0: "Shard (OC+Foc+SPen)" C1 Fixed D + C2
     Fixed A (G1 LongRange+Focused + Super Penetrator exp, canApplyExperimental TRUE); "Shard (Long
     Range)" C2 Fixed A (G5 LongRange, CG reward, locked). Guardian Tech Broker unlock.
     (3) kb/outfitting/ax-multi-cannon.md NEW (grp axmc, symbol Hpt_ATMultiCannon_*). The STANDARD
     non-Guardian AX kinetic workhorse — NO Guardian unlock (entry AX weapon). damagedist {X:1,K:1}
     = AX + kinetic split. Sustained auto-fire: clip 100 (fixed)/90 (turret), HUGE ammo 2100. Long
     range 4000 / falloff 2000. VERY low heat (thermload 0.1-0.3) + low power (0.46-0.64). Medium +
     Large ONLY (no Small in base line), Fixed + Turret. dmg 1.7-6.1, piercing 17 (M)/33 (L),
     shotspeed 1600, reload 4. Enhanced variant (axmce) noted as follow-on (adds Small + better stats).
     trunk.md: +3 Outfitting bullets; AX/Thargoid section reworked into "AX weapons" (trio + axmc) +
     "AX defence" (Guardian defensive trio). Bidirectional "Related AX weapons" links added across all
     4 weapon pages (gauss <-> plasma <-> shard <-> axmc).
     PATH NOTES: all 3 hardpoints/*.json (guardian_plasma_charger, guardian_shard_cannon,
     ax_multi_cannon) resolved first try, no 404 — index.js keys gpc/gsc/axmc confirmed last loop.
     Follow-ons queued (paths via index.js, require('./x')=.json): Enhanced AX MC (axmce ->
     ax_multi_cannon_enhanced), AX Missile Rack (axmr -> ax_missile_rack; enhanced axmre), Remote
     Release Flak Launcher (rfl -> remote_release_flak_launcher, anti-swarm utility). Remaining AX
     paths still open: tbrfl (flechette), tbem (enzyme missile), ntp (nanite torpedo). -->


<!-- DONE loop 15: completed the Guardian "specials" layer — 3 new Tier-0 Coriolis pages (all availability: live):
     (1) kb/outfitting/guardian-shield-reinforcement.md NEW (grp gsrp). POWERED optional internal, classes 1-5,
     ratings E/D only. shieldaddition = FLAT MJ added to shield strength (shield analogue of the HRP's flat HP);
     NOT a multiplier (unlike shield-booster) and not active recharge (unlike SCB). integrity const 36. D > E in
     MJ at half mass / more power / ~3x cost. C1 E 44 MJ 0.35 MW -> C5 D 215 MJ 1.26 MW. Completes the Guardian
     defensive TRIO: gsrp (shields) + ghrp (hull) + gmrp (modules). Guardian Tech Broker unlock. source_count 1,
     verified false. Bidirectional trio links added to hull-reinforcement.md + module-reinforcement.md.
     (2) kb/outfitting/guardian-gauss-cannon.md NEW (grp ggc) -> SEEDS THE AX-WEAPON LAYER. Fixed-mount only,
     experimental, 100% THERMAL (damagedist T:1), piercing 140, charge-fired clip 1, range 3000. Two sizes:
     C1 small D (dmg 22) + C2 medium B (dmg 38.5). Plus two pre-engineered cost-0 reward variants "Gauss
     (HCap + RFire)" (G1 High Capacity + Rapid Fire, locked: not re-eng/grade-change/experimental; clip 2 ammo
     200, lower per-shot dmg 9.6/18.3). High distdraw + thermload (pair w/ heat-sink-launcher). Guardian unlock.
     source_count 1, verified false.
     (3) kb/outfitting/guardian-fsd-booster.md NEW (grp gfsb). POWERED optional internal, classes 1-5, single
     rating H. jumpboost = FLAT +LY per jump, stacks additively on the FSD (does NOT replace it). mass const 1.3t,
     integrity const 32. C1 +4.0 LY 0.75 MW -> C5 +10.5 LY 2.14 MW; diminishing class-to-class returns. desc:
     "...at the cost of overall fuel efficiency." INDEPENDENTLY corroborates mechanics/frame-shift-drive.md's
     "+10.5 ly at class 5" claim -> that page source_count 2->3, stays verified true; bidirectional wikilinks
     added there + on outfitting/frame-shift-drive.md. source_count 1, verified false.
     trunk.md updated: 3 new Outfitting bullets + AX-weapon seed line in the AX/Thargoid section.
     PATH NOTES: all 3 queue paths resolved first try (gsrp/ggc/gfsb, no 404). modules/index.js re-fetched to
     confirm follow-on AX-weapon paths. Follow-ons queued (paths CONFIRMED via index.js, require('./x')=.json):
     Guardian Plasma Charger (gpc), Guardian Shard Cannon (gsc) -> complete the Guardian AX-weapon trio; AX
     Multi-Cannon (axmc) -> the standard AX kinetic workhorse. Other AX paths noted: axmce, axmr, axmre, rfl,
     tbrfl, tbem, ntp. -->


<!-- DONE loop 14: completed the Guardian AX outfitting layer + the heat-management utility.
     2 MERGES + 1 new Tier-0 Coriolis page (all availability: live):
     (1) kb/outfitting/hull-reinforcement.md MERGED Guardian Hull Reinforcement (grp ghrp) as a full
     H2 + table. POWERED (unlike std/Meta-Alloy HRP, 0 power): C1 D 0.56MW -> C5 D 1.46MW. causres 0.05
     (5% FLAT, MORE than Meta-Alloy's 3%) + thermres 0.02 (2%); explres/kinres 0. HIGHEST raw HP of all
     3 HRP lines (C5 488/450 D/E vs std 390/360 vs MA 351/324). Classes 1-5, E/D only, Guardian unlock.
     Independent Tier-0 file -> source_count 2->3, stays verified TRUE.
     (2) kb/outfitting/module-reinforcement.md MERGED Guardian Module Reinforcement (grp gmrp) as a full
     H2 + table. POWERED (std MRP 0 power): C1 D 0.34MW -> C5 D 0.88MW. SAME protection fractions as std
     MRP (D 0.60 / E 0.30) -> independent Tier-0 corroboration of the protection mechanic -> source_count
     1->2, verified false->TRUE. ~10% larger integrity pools than std (C5 385/424 vs 350/385) + Thargoid
     disruption resistance. Classes 1-5, E/D only, Guardian unlock.
     (3) kb/outfitting/heat-sink-launcher.md NEW (grp hs). UTILITY mount, class 0 rating I, passive,
     0.2MW. Single size (no class/rating ladder). clip 1 + ammo 3 reserve = 4 sinks; duration 10s cooling,
     fireint 5s, reload 10s, ammocost 25cr, mass 1.3t, cost 3500. Sirius variant (id 5W): mass 0.65t,
     cost 0 (Powerplay reward), pre-eng G1 Expanded Heat Sink Capacity (Misc_HeatSinkCapacity), NOT
     re-engineerable/grade-changeable/experimental. source_count 1, verified false. Forward-linked from
     shield-cell-bank.md ("heat sinks" plain ref -> [[wikilink]]).
     PATH NOTES: queue's guardian_hull_reinforcement.json AND guardian_module_reinforcement.json both
     404'd (14-byte "404: Not Found"); modules/index.js gave the correct keys/paths:
     ghrp=internal/guardian_hull_reinforcement_package.json, gmrp=internal/guardian_module_reinforcement_package.json
     (the _package suffix was missing). heat_sink_launcher.json resolved first try. Follow-ons queued
     (paths pre-confirmed via index.js): Guardian Shield Reinforcement (gsrp), Guardian Gauss Cannon
     (ggc, seeds AX weapons), Guardian FSD Booster (gfsb). -->


<!-- DONE loop 13: completed the module-protection / shield-recovery layer. 2 new Tier-0 Coriolis pages
     + 1 MERGE (all availability: live):
     (1) kb/outfitting/shield-cell-bank.md NEW (grp scb). Active-recharge: restores ACTIVE shields only
     ("no effect on collapsed shields"). Cells = clip(1) + ammo(reserve); E & B ratings carry the most
     cells, A & C fewer, D fewest (often 1). shieldreinforcement (MJ/cell) rises w/ class+rating: A =
     highest heal/cell (burst), B = largest total pool (cells x heal). spinup 5s + boot 25s (all);
     thermload 170->800 by class (heat is the cost; pair w/ heat sinks). Full C1-8 E/D/C/B/A table
     (cells/heal/pool/duration/mass/power/thermload/cost). Quirk: C8 E rechargerating=C. source_count 1,
     verified false. Forward-linked from shield-generator.md (Prismatic SCB ref now a wikilink).
     (2) kb/outfitting/module-reinforcement.md NEW (grp mrp). Optional internal, NO power draw, classes
     1-5, ratings E & D ONLY. protection = fraction of penetrating module dmg absorbed (E 0.30 / D 0.60);
     integrity = pool size. E = high capacity/low absorb (heavier, cheaper); D = low capacity/high absorb
     (half mass, ~3x cost). Stacking -> diminishing returns toward a cap. The 3rd tank leg: shields ->
     hull(HRP) -> modules(MRP). source_count 1, verified false.
     (3) kb/outfitting/hull-reinforcement.md MERGED Meta-Alloy HRP (grp mahr) as a full H2 + table.
     causres = 3% FLAT all class/rating (only HRP w/ caustic res); explres/kinres/thermres = 0 (gives up
     conventional resists); slightly LESS raw HP than standard (C5 324/351 vs 360/390). Classes 1-5 E/D,
     no power. Confirms the existing causres-0 cross-ref -> source_count 1->2, verified false->TRUE
     (independent Tier-0 file corroborates). Also wikilinked "Module Reinforcement Packages" -> new page.
     PATH NOTES: all 3 internal/*.json (shield_cell_bank, module_reinforcement_package,
     meta_alloy_hull_reinforcement_package) resolved first try, no 404. Follow-ons queued: Guardian HRP,
     Guardian MRP, Heat Sink Launcher (the latter directly referenced by the new SCB page). -->


<!-- DONE loop 12: completed the defence trio. 1 MERGE + 2 new Tier-0 Coriolis pages (all availability: live):
     (1) kb/outfitting/shield-generator.md — MERGED Prismatic Shield Generator (grp psg) as a full H2 +
     3-way "which to fit" section. Powerplay reward (Aisling Duval), A-rating ONLY across C1-8, optmul
     1.5 (highest of any line; std A 1.2, Bi-Weave 0.9), minmul 1.0 / maxmul 2.0. Heavy power (C5 5.46MW
     vs std 5A 3.64MW) + slow regen (1.0 MJ/s thru C6) => leans on Shield Cell Banks. source_count 2->3,
     stays verified true (independent Tier-0 module file; shared multiplier mechanic corroborated).
     changed_note added: Prismatic now an Aisling Duval PP2.0 reward, module unchanged.
     (2) kb/outfitting/shield-booster.md — UTILITY mount (class 0, passive), NOT internal. Path is
     hardpoints/shield_booster.json key sb (queue's internal/ path was wrong; index.js confirmed). Ratings
     E-A => +4/8/12/16/20% shieldboost. Base resists 0 (engineering only). Diminishing-returns falloff on
     stacking noted (JSON stores single-module value). source_count 1, verified false.
     (3) kb/outfitting/hull-reinforcement.md — optional internal grp hr, classes 1-5, E & D ratings ONLY.
     Flat armour HP (C1 80/110 -> C5 360/390); D = more HP at half E's mass for ~3x cost. Resists scale
     +0.5%/class (exp/kin/therm). causres 0 => NO caustic protection; points to Meta-Alloy HRP (mahr) for
     AX. source_count 1, verified false.
     PATH NOTES: Coriolis filename for Prismatic is the MISSPELLED internal/pristmatic_shield_generator.json
     (typo upstream). shield_booster is under hardpoints/ not internal/. hull_reinforcement_package path OK.
     Follow-ons queued: shield_cell_bank (scb), module_reinforcement_package (mrp), meta_alloy_hrp (mahr). -->


<!-- DONE loop 11: 2 new Tier-0 Coriolis outfitting pages (all availability: live):
     (1) kb/outfitting/shield-generator.md — MERGED standard (grp sg) + Bi-Weave (grp bsg).
     Core concept documented: shield strength is a MULTIPLIER on ship base shield, interpolated
     by hull mass across minmass/optmass/maxmass; MJ is ship-specific, never a module constant.
     Standard ratings E-A set optmul (A 1.2 / E 0.8); CLASS 1 HAS NO B RATING (only E/D/C/A).
     Full class/rating table C1-C8. Bi-Weave is C-rating-only, optmul 0.9, regen 1.8-5.8 (1.8-2.4x
     standard) — trades MJ for recharge. Uniform resists exp +0.5/kin +0.4/therm -0.2. Both
     stocked to C8 at Garay Terminal (loop 6). source_count 2, verified false.
     (2) kb/outfitting/cargo-rack.md — grp cr, all E-rated, capacity DOUBLES per class (C1 2t ->
     C8 256t). MASSLESS rack (mass 0); cargo itself 1t/unit drives loaded jump range. Variants:
     Corrosion Resistant (C1/C4/C5/C6, for Thargoid/corrosive cargo; C4-C6 match standard cap) +
     Expanded Capacity (C5/C6, pre-eng G5 CargoRack_IncreasedCapacity, CG reward, not re-eng).
     Both linked in trunk.md Outfitting. Follow-ons queued: prismatic_shield_generator (merge into
     shield-generator.md), shield_booster, hull_reinforcement_package (complete the defence trio).
     PATH NOTE: internal/shield_generator.json, bi_weave_shield_generator.json, cargo_rack.json all
     resolved first try (no 404). -->


<!-- DONE loop 10: completed the mining loop with 2 new Tier-0 Coriolis pages (all availability: live):
     (1) kb/outfitting/limpet-controllers.md — merged Prospector + Collector controllers.
     Prospector (group pc): class sets simultaneous limpets C1=1/C3=2/C5=4/C7=8; A-rated range
     C1 7km -> C7 11.9km; reports composition + yield bonus. Collector (group cc): class max
     C1=1/C3=2/C5=3/C7=4; `time` field = limpet lifetime sec (A 720 longest, E 300); autonomous
     fragment/canister scoop. Build advice: 1 small Prospector, large-class Collector.
     (2) kb/outfitting/refinery.md — group rf, classes 1-4, MASSLESS (no mass field). `bins` =
     concurrent ore types; A-rated bins C1 4/C2 6/C3 8/C4 10. Sits at end of mining loop.
     Both linked into trunk.md Outfitting section; mining-tools.md back-linked (plain refs ->
     [[wikilinks]]). PATH NOTE held: internal/*.json paths all resolved first try (no 404).
     Follow-ons queued: shield_generator + bi_weave_shield_generator + cargo_rack. -->


<!-- DONE loop 9: seeded kb/outfitting/ (was empty) with 3 Tier-0 Coriolis module pages, all availability: live:
     (1) kb/outfitting/mining-tools.md — full mining toolkit: Pulse Wave Analyser (utility C0, A-E),
     Mining Laser (C1/C2 D, 500m; + Powerplay "Mining Lance" Zemina Torval 2000m; + pre-eng V1),
     Abrasion Blaster (C1 D, 1000m; + LR 4180m), Sub-Surface Displacement Missile (C1/C2 B, 3000m;
     + "Extraction Missile"), Seismic Charge Launcher (C2 B, deep core). Three extraction methods
     (surface/sub-surface/core) explained; build-a-miner section links type-11-prospector.
     (2) kb/outfitting/frame-shift-drive.md — module reference: legacy FSD (C2-7) vs FSD(SCO)
     Supercruise Overcharge (C2-8, the current default since Update 18 2024). A-rated optmass/maxfuel/
     cost tables both lines; class-8 only exists as SCO; "FSD Mk II (SCO)" 8A top variant
     (fuelpower 2.5025). Cross-links mechanics/frame-shift-drive for jump-range theory (no dup).
     (3) kb/outfitting/fuel-scoop.md — massless optional; KGBFOAM scoopable stars; A-rated scoop-rate
     table 1A 42 -> 8A 1680. All 3 linked in new trunk.md "Outfitting" section.
     PATH FIX (carry-forward): modules/index.js require('./x') with NO extension = .json file, not .js.
     The .js URLs all 404'd; refetched correct .json paths. -->


<!-- DONE loop 8: 3 Coriolis Tier-0 ship hulls created (all current, availability: live):
     (1) kb/ships/type-11-prospector.md — Lakon, class 2/MEDIUM pad, dedicated miner. 320t hull,
     275 MJ shield, 350 armour, hardness 58, PD class 7 (sustains mining tools). 8 hardpoints =
     4 mining-tool-only (3,2,2,1) + 4 general (2,1,1,1); class-5 limpet-only bay + class-5 fighter
     bay; optionals 6,6,6,5,5,4,3,2,1,1. Hull 66.3M CR. Stocked at Garay Terminal (loop 5).
     (2) kb/ships/mandalay.md — Zorgon Peterson, class 2/MEDIUM pad, long-range explorer. Light
     230t hull + class-5 FSD; roll 96 (very nimble); 4M+2S hardpoints; optionals 6,5,4,4,3,3,2,1,1,1.
     Hull 16.5M CR.
     (3) kb/ships/type-9-heavy.md — Lakon, class 3/LARGE pad, bulk hauler. 850t, slow (yaw 8),
     twin class-8 optionals = ~1,580 t theoretical max cargo; 480 armour; 3M+2S hardpoints. Hull
     72.1M CR. Stocked at Garay Terminal (loop 5). All 3 linked in trunk.md Ships section.
     CONFIRMED via ships/index.js: filenames type_11_prospector / mandalay / type_9_heavy all match
     queue paths (no stale-slug 404 this loop). -->


<!-- DONE loop 7: (1) Coriolis Panther Clipper Mk II hull -> kb/ships/panther-clipper-mk-ii.md
     (Zorgon Peterson, class 3/Large pad, 1200t hull, 350 MJ shield, 620 armour, hardness 70,
     PP/Thr C8, FSD C7, twin C8 + twin C7 optionals incl. 2 cargo-restricted = largest cargo ship,
     2L+4M+4S hardpoints, 6 utility, crew 4, fighter hangar). CORRECTION: queue's stale slugs
     panther_clipper_mk_ii.json AND type_8.json both 404; correct Tier-0 paths per ships/index.js
     are ships/panther_clipper.json (key panthermkii) and ships/type_8_transport.json (key
     type_8_transport). (2) Coriolis Type-8 Transporter hull -> kb/ships/type-8-transporter.md
     (Lakon, class 2/Medium pad, 400t hull, 228 MJ shield, 440 armour, FSD C5, C7+3xC6 optionals =
     best medium-pad hauler, 1M+5S hardpoints, 4 utility, crew 1). Both linked in trunk.md. -->


<!-- DONE loop 6: (1) EDSM api-system-v1/stations/outfitting for Garay Terminal (marketId 3229756160).
     653 module SKUs / 107 families. Full core internals to C8; FSD + FSD(SCO) to C7; Shield & Bi-Weave
     to C8; limpets/refinery/AFMU; weapons capped ~C4; NO Guardian modules (expected). Merged H3
     "Garay Terminal — outfitting stock" into kb/locations/deciat.md, source_count 3->4, verified true.
     (2) Coriolis Cobra Mk V hull -> created kb/ships/cobra-mk-v.md. CORRECTION: queue's stale
     dist/ships.json 404s (dist/index.json is build-generated, not committed); correct Tier-0 path is
     ships/<slug>.json (Cobra Mk V = ships/cobra_mk_v.json, export key "cobramkv"). -->


<!-- DONE loop 5: EDSM api-system-v1/stations/shipyard enumerated for Garay Terminal (marketId 3229756160).
     Findings: 17 hulls stocked, incl. recent Type-8 Transporter, Cobra Mk V, Panther Clipper Mk II,
     Type-11 Prospector (confirms current post-2024 roster). Largest: Type-9 Heavy & Panther Clipper Mk II.
     Third independent EDSM endpoint confirming Garay carries a Shipyard -> merged H3 "Garay Terminal —
     shipyard stock" into kb/locations/deciat.md, source_count 2->3, verified true. -->


<!-- DONE loop 4: EDSM api-system-v1/stations enumerated for Deciat (id64 6681123623626).
     Findings: Garay Terminal (Coriolis Starport, marketId 3229756160) is the ONLY large-pad
     orbital port in-system, ~2042 ls, with Market + Shipyard + Outfitting — the restock/outfit/
     shipyard hub for Farseer visitors. Matteucci Dock & Carson Hub are medium-pad Outposts
     (Market+Outfitting, no shipyard); Kirtley Vision/Hasse Point are Planetary Outposts at ~62 ls.
     Merged into kb/locations/deciat.md new H2 "Station Services — large-pad & outfit ports". -->


<!-- DONE loop 3: EDSM Farseer Inc stations/market corroborated -> kb/locations/deciat.md (source_count 2,
     verified) + kb/engineers/felicity-farseer.md aligned. Findings: Farseer Inc market is SELL-ONLY
     (buyPrice 0 / stock 0 across all commodities); Meta-Alloys NOT buyable there (demand 0). Fixed
     stale "Coles Point" ref in felicity-farseer.md -> Witch Head Science Centre ([[locations/hip-23759]]). -->

<!-- DONE loop 2: HIP 23759 stations+market corroborated -> kb/locations/hip-23759.md verified.
     Correction: no "Coles Point" station exists; the Meta-Alloy market is the Witch Head Science
     Centre asteroid base (Meta-Alloys buyPrice ~148,408 cr, BGS-driven stock). -->
