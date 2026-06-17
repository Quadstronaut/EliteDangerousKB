# Research Queue — next targets

One target per bullet. The orchestrator takes the top 1-3 each loop, dedups against
seen.json, and processes Tier-0 first. Append follow-on targets discovered during synthesis.

- https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/diamondback_explorer.json (tier: 0, type: coriolis-ship, note: BUDGET EXPLORER GAP — rounds out the explorer line now that [[ships/asp-explorer]] + [[ships/mandalay]] are both paged. The Diamondback Explorer (DBX) is the iconic cheap, cold-running long-range explorer (famously low heat for fuel-scooping near hot stars). Tier-0 Coriolis JSON, parse directly (no LLM): extract name/manufacturer (Lakon)/class (expect 1 = SMALL pad — the only small-pad explorer of the trio)/hullMass/reserveFuel/speed-boost/baseShield/baseArmour/hardness/masslock/heatCapacity (note its LOW heat reputation)/core-standard array/hardpoints array (count Large/Med/Small + utility = trailing zeros)/internal array (optionals + PAS, likely NO Military)/costs. Write -> kb/ships/diamondback-explorer.md NEW (source_type: coriolis, tier 0, verified false, availability: live). Cross-link [[ships/asp-explorer]] + [[ships/mandalay]] (explorer siblings — add a 3-way "budget vs roomy vs max-range" compare), [[engineers/felicity-farseer]] (FSD), [[outfitting/fuel-scoop]] + [[outfitting/guardian-fsd-booster]], [[outfitting/frame-shift-drive]], and [[trunk]] Ships. CONFIRM filename via ships/index.js if diamondback_explorer.json 404s — Coriolis key likely "diamondback_explorer" or "dbx".)

- https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/vulture.json (tier: 0, type: coriolis-ship, note: SMALL-PAD COMBAT GAP — the combat-line companion to the just-paged [[ships/fer-de-lance]]. The Vulture is the iconic Core Dynamics small-pad heavy fighter: TWO Large hardpoints on a size-1 hull (huge firepower-to-size ratio) at the cost of a notoriously power-starved distributor/power-plant. Tier-0 Coriolis JSON, parse directly: extract name/manufacturer (Core Dynamics)/class (expect 1 = SMALL pad)/hullMass/speed-boost/baseShield/baseArmour/hardness/masslock/core-standard array (note the small PP/PD — the famous power bottleneck)/hardpoints array (expect 2 Large = [3,3,...] + utility trailing zeros)/internal array (shallow optionals + PAS, likely NO Military)/costs. Write -> kb/ships/vulture.md NEW (source_type: coriolis, tier 0, verified false, availability: live). Cross-link [[ships/fer-de-lance]] (medium combat step up) + the combat hulls + [[engineers/the-dweller]] (power plant — the Vulture's defining engineering need) + [[trunk]] Ships. CONFIRM filename via ships/index.js if vulture.json 404s — Coriolis key likely "vulture".)

<!-- DONE loop 28: PAGED THE TWO QUEUED FOUNDATIONAL TIER-0 SHIP GAPS (Asp Explorer + Fer-de-Lance).
     2 new Tier-0 Coriolis ship pages (both availability: live, source_count 1, verified false):
     (1) kb/ships/asp-explorer.md NEW (KEY "asp", NOT "asp_explorer" — asp_explorer.json 404'd 14 bytes;
     ships/index.js confirmed `asp: require('./asp').asp`, so file is ships/asp.json). edID 128049303,
     eddbID 3. Lakon, class 2 (MEDIUM pad), NO requirements block = NO rank gate (credits only). hullMass
     280 (light → strong range), speed 250/boost 340, baseShield 140, baseArmour 210, hardness 52 (low),
     heatcap 272, masslock 11, crew 2, pitch 38/roll 100/yaw 10, reservefuel 0.63, hull 6,145,793 / retail
     6,661,154 (cheap mid-game). Core standard [5,5,5,4,4,5,5]: PP5 Thr5 FSD5 LS4 PD4 Sen5 FT5 (class-5
     FSD on a light hull = its long range; modest class-4 PD = explorer not gunship). Hardpoints
     [2,2,1,1,1,1 + 4 zeros] = **2 Medium + 4 Small = 6 weapon mounts** + **4 utility**, NO Large/Huge.
     Optionals 6,5,3,3,3,2,2,1 (EIGHT, top class-6) + class-1 PAS. NO Military. Bulkheads causres 0 all
     grades. Bidirectional explorer-sibling link to [[ships/mandalay]] (added an Asp predecessor sentence
     to the Mandalay intro). The cheaper, roomier classic vs the Mandalay's lighter max-range modern hull.
     (2) kb/ships/fer-de-lance.md NEW (fer_de_lance.json resolved FIRST TRY, no 404). edID 128049351,
     eddbID 11. Zorgon Peterson, class 2 (MEDIUM pad), NO requirements block = NO rank gate. hullMass 250,
     speed 260/boost 350, baseShield **300 (high for a medium)**, baseArmour 225, **hardness 70 (combat
     hull)**, **heatcap 224 (LOW — runs hot)**, masslock 12, crew 2, pitch 38/roll 90/yaw 12, reservefuel
     0.67, hull 51,242,363 / retail 51,567,040. Core standard [6,5,4,4,6,4,3]: PP6 Thr5 **FSD4 (weak jump)**
     LS4 **PD6 (large — feeds energy weapons)** Sen4 **FT3 (small tank)**. Hardpoints [4,2,2,2,2 + 6 zeros]
     = **1 Huge (class-4) + 4 Medium = 5 weapon mounts** + **6 utility (generous)**. Optionals 5,4,4,2,1,1
     (SIX only, top class-5 — shallow) + class-1 PAS. NO Military. Bulkheads causres 0 all grades.
     QUEUE-GUESS CORRECTION: the queue guessed a "weak power-distributor" tradeoff — WRONG, the PD is a
     large class-6; the real tradeoffs are the class-4 FSD (poor range), class-3 fuel tank (short legs)
     and the shallow 6-slot internals. CONFIRMED: 1 Huge on a medium hull. Cross-linked [[ships/python]]
     (3 Large multirole contrast) + [[ships/krait-mk-ii]] + [[engineers/the-dweller]] (PD) + the combat
     hulls + [[trunk]] Ships.
     PATH NOTE: the Asp 404 reconfirmed the require('./key').key → ships/<key>.json mapping; always probe
     index.js when a "<name>_<suffix>.json" guess 404s (the iconic ships often use the short bare key).
     trunk.md: +2 Ships bullets (Asp after Mandalay in the explorer line; FDL after Krait Phantom).
     NEXT: queued two reachable Tier-0 ship gaps at the TOP so the next loop progresses regardless of the
     still-blocked Spire Site — Diamondback Explorer (budget cold-running explorer, completes the
     Asp/Mandalay/DBX explorer trio) + Vulture (Core Dynamics small-pad heavy fighter, 2 Large on a size-1
     hull, the combat-line companion to the FDL). The Spire Site stays queued (BLOCKED) for retry. -->


- https://elite-dangerous.fandom.com/wiki/Thargoid_Spire_Site (tier: 2, type: wiki-prose, status: BLOCKED loop 27 — Fandom is Cloudflare-JS-challenged (whole domain returns a "Just a moment..." interstitial via the Fetcher, NOT a 404) AND api.canonn.tech ConnectTimeouts (host unreachable from this env). RETRY a later loop; if Fandom stays blocked, try a non-Fandom prose source or re-probe the Canonn API (it has been intermittently up). note: PIVOT — the whole AX HULL line is now complete (medium Chieftain/Challenger/Crusader + Krait pair, large-pad trinity Corvette/Anaconda/Cutter + the Type-10 Defender armour brick), so move from AX *ships* to AX *SITE mechanics*. Target the Thargoid Spire Site (a.k.a. Spire/Robigo-style Maelstrom spire) — CURRENT, availability: live (the war narrative ended but Spire sites are accessible). This is Tier-2 PROSE: fetch via Fetcher, then SUMMARIZE via mcp__ollama-tools__summarize_text qwen3-coder:30b with the fact-extraction prompt (key claims, named entities, currency signals, OBSOLETE yes/no, per-claim availability). Extract: what a Spire site IS, how to find/approach one, the loot/objective loop (Thargoid materials, e.g. Titan Drive Component etc.), hazards (caustic, heat, Thargoid defenders), and which AX kit applies. Write -> kb/ax-thargoid/sites/thargoid-spire-site.md NEW (source_type: wiki, tier 2, verified false, availability: live). CONFIRM the slug if it 404s — try "Thargoid_Spire", "Spire_Site", or the Canonn structured API (api.canonn.tech, Tier-0 JSON: system/bodyName/lat-long/type) as a higher-trust fallback. Cross-link the AX weapon/utility/defence outfitting line + the AX hulls (esp. [[ships/type-10-defender]] as the durable site-runner) + [[trunk]] AX/Thargoid section. After this, AX site coverage could extend to Titan wrecks / AX combat-zone tactics, or Canonn structured site listings.)

<!-- DONE loop 27: SPIRE-SITE TARGET BLOCKED -> PIVOTED TO TWO FOUNDATIONAL TIER-0 SHIP GAPS.
     The queued Thargoid Spire Site (Tier-2 Fandom prose) could NOT be acquired this loop:
     elite-dangerous.fandom.com is Cloudflare-JS-challenged across the WHOLE domain (the Fetcher
     gets a 5.6KB "Just a moment..." interstitial, not the article — so alternate slugs would not
     help) AND the higher-trust fallback api.canonn.tech ConnectTimeouts (host unreachable from this
     env). This is a transient ACQUISITION block, NOT obsolescence/404 -> the target was NOT
     recorded in seen.json (neither record_source nor record_discard) and stays QUEUED (re-annotated
     BLOCKED, demoted below the new reachable targets) so a later loop retries it.
     To stay productive (never-idle mandate), pivoted to two reachable Tier-0 Coriolis ship gaps,
     each COMPLETING AN EXISTING SIBLING PAIR (mirrors the krait/cobra base+variant pattern):
     (1) kb/ships/python.md NEW (python, edID 128049339, eddbID 17). Faulcon DeLacy, class 2 (MEDIUM
     pad), NO requirements block = NO rank gate (credits only). hullMass 350, speed 230/boost 300,
     baseShield 260, baseArmour 260 (symmetrical), hardness 65, heatcap 300, masslock 17, crew 2, NO
     fighter bay, pitch 29/roll 90/yaw 10, reservefuel 0.83, hull 55,324,684 / retail 56,978,179.
     Core standard [7,6,5,4,7,6,5]: PP7 Thr6 FSD5 LS4 PD7 Sen6 FT5. Hardpoints [3,3,3,2,2,+4 zeros] =
     **3 Large + 2 Medium = 5 mounts (three Large — heavy for a medium)** + **4 utility**. Optionals
     6,6,6,5,5,4,3,3,2,1 (TEN, three class-6) + class-1 PAS. NO Military slots. Bulkheads causres 0
     all grades. Bidirectional sibling link to [[ships/python-mk-ii]] (added a "modern combat
     refinement of the classic Python" line to the Mk II intro). The classic medium workhorse;
     Mk II is the combat refinement.
     (2) kb/ships/cobra-mk-iii.md NEW (cobra_mk_iii, edID 128049279, eddbID 4). Faulcon DeLacy, class
     1 (SMALL pad), NO rank gate. **CHEAPEST hull in the KB: hull 208,372 / retail 349,718.** hullMass
     180, speed 280/boost 400 (fast), baseShield 80, baseArmour 120, hardness 35 (low), heatcap 225,
     masslock 8, crew 2, NO fighter bay, pitch 40/**roll 100 (nimblest roll in KB)**/yaw 10,
     reservefuel 0.49. Core standard [4,4,4,3,3,3,4]: PP4 Thr4 FSD4 LS3 PD3 Sen3 FT4. Hardpoints
     [2,2,1,1,+2 zeros] = **2 Medium + 2 Small = 4 mounts** + **2 utility**. Optionals 4,4,4,2,2,2,1,1
     (EIGHT, three class-4) + class-1 PAS. NO Military slots. Bulkheads causres 0 all grades.
     Bidirectional sibling link to [[ships/cobra-mk-v]] (turned its "classic Cobra line" mention into a
     [[ships/cobra-mk-iii]] wikilink). The iconic cheap/fast/agile starter; Mk V is the modern
     successor.
     PATH NOTES: BOTH Coriolis filenames resolved FIRST TRY, no 404 — ships/python.json (key python) and
     ships/cobra_mk_iii.json (key cobra_mk_iii). URL format confirmed from cobra-mk-v frontmatter:
     raw.githubusercontent.com/EDCD/coriolis-data/master/ships/<key>.json (no dist/ prefix). trunk.md:
     +2 Ships bullets (python after python-mk-ii, cobra-mk-iii after... before cobra-mk-v).
     NEXT: queued two more reachable Tier-0 ship gaps at the TOP so the next loop progresses regardless
     of the Spire block — Asp Explorer (explorer sibling of Mandalay) + Fer-de-Lance (premier medium
     combat, one Huge on a medium). The Spire Site stays queued (blocked) for retry. -->


<!-- DONE loop 26: COMPLETED THE LARGE-PAD AX LINE — added the dedicated AX ARMOUR BRICK, finishing
     the whole AX-hull roster (medium trio + Krait pair + large trinity + this). 1 new Tier-0 Coriolis
     ship page (availability: live, source_count 1, verified false):
     kb/ships/type-10-defender.md NEW (type_10_defender, edID 128785619, eddbID 32). Lakon, class 3
     (LARGE pad), **NO requirements block = NO rank gate** (credits only, like the Anaconda). hullMass
     **1200 (HEAVIEST hull in KB**, above Cutter 1100), speed 179/boost 219 (slow), baseShield **320
     (LOW — armour-tank, not shield-tank)**, baseArmour **580 (HIGHEST armour in KB**, above Anaconda
     525), hardness **75 (HIGHEST hardness in KB**, above Corvette/Cutter 70), heatcap 335, masslock 26,
     crew 4, fighterHangars TRUE, pitch 20/roll 20/yaw 8 (**very sluggish — IDENTICAL airframe figures
     to the Type-9 Heavy**), reservefuel 0.77, hull 121,334,619 / retail 124,755,342. Core standard
     [8,7,7,5,7,4,6]: PP8 Thr7 FSD7 LS5 PD7 Sen4 FT6. Hardpoints [3,3,3,3,2,2,2,1,1 + 8 zeros] = **4
     Large + 3 Medium + 2 Small = NINE weapon mounts (MOST in KB)**, **NO Huge** + **8 utility**.
     Optionals 8,7,6,5,4,4,3,3,2,1 = TEN regular + **TWO class-5 Military** + class-1 PAS. Bulkheads
     causres 0 all grades.
     QUEUE-GUESS RESULTS: class 3 + no rank gate + very high armour + 8 utility + big hardpoint count +
     Military slots ALL CONFIRMED. CORRECTION: **NO Huge hardpoint** (queue asked "Huge?") — max mount
     is Large; firepower comes from COUNT (9 mounts) not a Huge slot. Military slots = 2 class-5 (NOT
     unknown). NOTABLE: only the FIRST of the 2 Military slots is eligible for Meta-Alloy HRP (mahr);
     the second slot's eligible set omits mahr.
     PATH NOTE: ships/type_10_defender.json resolved FIRST TRY, no 404 (the feared type_9_heavy-style
     suffix did not apply here). trunk.md: +1 Ships bullet + extended the large-pad line from "trinity"
     to "trinity plus the dedicated armour brick" (and softened the Corvette's "heaviest AX gunship" to
     "highest-firepower AX gunship" since the Type-10 is now the heaviest hull). Type-9 Heavy page:
     added a bidirectional airframe-sibling link (same Lakon airframe, combat variant).
     ROSTER SUMMARY (large-pad AX): Corvette = firepower king (2 Huge, Rear Admiral); Anaconda = no-gate
     generalist (best range); Cutter = shield-tank (600 MJ, Duke); Type-10 = armour brick (580 armour /
     75 hardness / 9 mounts, no Huge, no gate). NEXT: PIVOT from AX ships to AX SITE MECHANICS — queued
     the Thargoid Spire Site (Tier-2 wiki prose, summarize via qwen3-coder:30b; Canonn structured API as
     a higher-trust fallback). After that: Titan wrecks / AX combat-zone tactics. -->


<!-- DONE loop 25: COMPLETED THE LARGE-PAD COMBAT TRINITY (Corvette/Anaconda/Cutter). 2 new Tier-0
     Coriolis ship pages (both availability: live, source_count 1, verified false):
     (1) kb/ships/anaconda.md NEW (anaconda, edID 128049363, eddbID 2). MANUFACTURER CORRECTION:
     **Faulcon DeLacy, NOT Lakon** (queue guess was wrong). class 3 (LARGE pad), **NO requirements
     block = NO rank gate** (credits only — the trinity's only no-gate hull). hullMass 400 (LIGHT —
     basis of best-in-trinity jump range), speed 180/boost 240 (slow), baseShield 350, baseArmour
     **525 (HIGHEST armour in KB)**, hardness 65, heatcap 334, masslock 23, crew 4, fighterHangars
     TRUE, pitch 25/roll 60/yaw 10 (sluggish), reservefuel 1.07, hull 142,456,440 / retail
     146,969,451. Core standard [8,7,6,5,8,8,5]: PP8 Thr7 FSD6 LS5 PD8 Sen8 FT5 (class-8 PP + PD;
     Sensors 8 recorded verbatim, flag for corroboration). Hardpoints [4,3,3,3,2,2,1,1 + 8 zeros] =
     **1 Huge + 3 Large + 2 Medium + 2 Small = EIGHT weapon mounts (most of trinity)** + **8 utility**.
     Optionals 7,6,6,6,5,5,5,4,4,4,2,1 = TWELVE regular + **ONE class-5 Military** + class-1 PAS.
     QUEUE-GUESS CORRECTIONS: manufacturer Faulcon DeLacy (NOT Lakon); Military slots = 1 class-5 (NOT
     0, NOT Corvette's 2). Bulkheads causres 0 all grades. CONFIRMED: 1 Huge, 8 utility, no rank gate.
     (2) kb/ships/imperial-cutter.md NEW (imperial_cutter, edID 128049375, eddbID 26). Gutamaya, class
     3 (LARGE pad), requires empireRank 12 = **DUKE** (CONFIRMED). hullMass **1100 (HEAVIEST in KB)**,
     speed 200/boost 320, baseShield **600 (HIGHEST shield in KB)**, baseArmour 400, hardness 70,
     heatcap 327, masslock **27 (HIGHEST in KB)**, crew 4, fighterHangars TRUE, pitch 18/roll 45/yaw 8
     (**LEAST AGILE in KB**), reservefuel 1.16, hull 200,493,413 / retail 208,969,451. Core standard
     [8,8,7,7,7,7,6]: PP8 Thr8 FSD7 LS7 PD7 Sen7 FT6 (**first KB ship with class-8 Thrusters**).
     Hardpoints [4,3,3,2,2,2,2 + 8 zeros] = **1 Huge + 2 Large + 4 Medium = SEVEN weapon mounts, NO
     Small** + **8 utility**. Optionals 8,8,6,6,6,5,5,4,3,1 = TEN regular (**TWO class-8** — huge
     cargo/shield) + **TWO class-5 Military** + class-1 PAS. QUEUE-GUESS CORRECTION: hardpoints are 1
     Huge + 2 Large + 4 Medium (queue guessed "Large/Medium/Small" — there are **NO Small mounts**).
     Bulkheads causres 0 all grades.
     PATH NOTES: BOTH filenames resolved FIRST TRY, no 404 — ships/anaconda.json (key anaconda) and
     ships/imperial_cutter.json (key imperial_cutter). trunk.md: +2 Ships bullets + rebuilt the
     large-pad line in the AX/Thargoid section into the full trinity. Corvette page: turned its plain
     "Imperial Cutter" + "Anaconda" mentions into bidirectional wikilinks.
     TRINITY SUMMARY: Anaconda = no-gate generalist (most mounts/optionals, best range, cheapest/
     lightest, 1 Military); Corvette = firepower king (2 Huge, more agile, 2 Military, Rear Admiral);
     Cutter = shield-tank/trader (600 MJ shield, 2 class-8 optionals, least agile, 2 Military, Duke).
     NEXT: EXTEND large-pad AX to the dedicated AX BRICK — the Type-10 Defender (Lakon flying fortress,
     no rank gate, heavy armour + many utility/hardpoints). Queued as concrete Tier-0 URL. After that,
     AX coverage could finally pivot to Spire/Titan SITE mechanics or AX combat-zone tactics. -->


<!-- DONE loop 24: COMPLETED THE ALLIANCE AX TRIO + PIVOTED TO LARGE-PAD AX. 2 new Tier-0 Coriolis
     ship pages (both availability: live, source_count 1, verified false):
     (1) kb/ships/alliance-crusader.md NEW (alliance_crusader, edID 128816581, eddbID 36). Lakon/
     Alliance, class 2 (medium pad), requires Horizons. hullMass 500 (heaviest of the trio), speed
     180/boost 300 (SLOWEST), baseShield 200, baseArmour 300, hardness 65, heatcap 316, masslock 13,
     crew 4, fighterHangars TRUE (only Alliance medium with an SLF bay), pitch 32 / roll 80 (least
     agile) / yaw 16, reservefuel 0.77, hull cost 22,096,565 / retail 22,866,341. Core: PP6 Thr6 FSD5
     LS5 PD6 Sen4 FT4 (SAME core as Chieftain/Challenger). Hardpoints 1L+2M+3S (SIX mounts) + 4
     utility. Optionals 6,5,3,3,2,2,1 (seven regular) + THREE class-4 MILITARY slots (mahr/hr/scb/mrp/
     gsrp/gmrp/ghrp) + class-1 PAS. Bulkheads causres 0 all grades.
     QUEUE-GUESS CORRECTIONS: crew = 4 (NOT 3); Military slots = 3 (SAME as the other two, NOT 2).
     fighter bay TRUE confirmed. It's the multicrew gunship: only fighter bay + crew 4, but slowest/
     least agile + fewest weapon mounts (6 vs Challenger's 7, both have only 1 Large). Cross-linked
     [[ships/alliance-chieftain]] + [[ships/alliance-challenger]] (turned the challenger's "not yet
     paged" note into a wikilink; added the trio line to the chieftain intro) + full AX line +
     [[ships/federal-corvette]] as the large-pad step up. ALLIANCE TRIO NOW COMPLETE.
     (2) kb/ships/federal-corvette.md NEW (federal_corvette, edID 128049369, eddbID 25). Core
     Dynamics, class 3 (LARGE pad), requires Federal Navy rank REAR ADMIRAL (federationRank 12).
     hullMass 900, speed 200/boost 260, baseShield 555, baseArmour 370, HARDNESS 70 (highest in KB),
     heatcap 333, masslock 24 (very high), crew 4, fighterHangars TRUE, pitch 28 / roll 75 / yaw 8,
     reservefuel 1.13, hull cost 183,156,068 / retail 187,969,450. Core: PP8 Thr7 FSD6 LS5 PD8 Sen8
     FT5 (class-8 PP + class-8 PD = signature). Hardpoints 2 HUGE (class-4) + 1L + 2M + 2S (SEVEN
     mounts) + 8 UTILITY. First KB ship with Huge hardpoints — and it has TWO. Optionals 7,7,7,6,6,5,
     5,4,4,3,1 (ELEVEN) + TWO class-5 MILITARY slots (bigger than the Alliance class-4, but only 2) +
     class-1 PAS. Bulkheads causres 0 all grades.
     QUEUE-GUESS CORRECTIONS: TWO Huge mounts (not one); 8 utility (validated zeros-in-hardpoints-
     array rule vs Panther=6/Type-9=4); 2 class-5 Military slots. Cross-linked the AX line as the
     large-pad platform + contrasted vs medium [[ships/alliance-challenger]]/[[ships/krait-mk-ii]].
     PATH NOTES: BOTH filenames resolved FIRST TRY, no 404 — ships/alliance_crusader.json (key
     alliance_crusader) and ships/federal_corvette.json (key federal_corvette). trunk.md: +2 Ships
     bullets + extended the AX-hulls line with the Crusader (medium) and the Corvette (large-pad step
     up). DATA NOTE: Coriolis lists Corvette Sensors at class 8 (standard[5]=8) — recorded verbatim
     per Tier-0 trust; flag for corroboration (source_count 1, verified false).
     NEXT: CONTINUE LARGE-PAD AX — the Anaconda (Lakon do-everything flagship, 1 Huge, NO rank gate,
     best jump range) + the Imperial Cutter (Gutamaya shield-tank flagship, Duke rank gate) complete
     the large-pad combat trinity (Corvette/Anaconda/Cutter). Both queued as concrete Tier-0 URLs.
     After those, AX coverage could move to Spire/Titan SITE mechanics or AX combat-zone tactics. -->


<!-- DONE loop 23: COMPLETED THE QUEUED AX-HULL PAIR — the tankier Alliance sibling + the explorer
     Krait sibling. 2 new Tier-0 Coriolis ship pages (both availability: live, source_count 1,
     verified false):
     (1) kb/ships/alliance-challenger.md NEW (alliance_challenger, edID 128816588). Lakon/Alliance,
     class 2 (medium pad), requires Horizons. hullMass 450, speed 204/boost 310, baseShield 220,
     baseArmour 300, HARDNESS 65, heatcap 316, masslock 13, crew 2, NO fighter bay, pitch 32 / roll
     90 / yaw 16, reservefuel 0.77, hull cost 29,569,804 / retail 30,472,252. Core: PP6 Thr6 FSD5 LS5
     PD6 Sen4 FT4 (SAME core layout as the Chieftain). Hardpoints 1L+3M+3S (SEVEN mounts) + 4 utility.
     Optionals 6,6,3,3,2,2,1 (seven regular, incl TWO class-6) + THREE class-4 MILITARY slots (eligible
     mahr/hr/scb/mrp/gsrp/gmrp/ghrp) + class-1 PAS. Bulkheads causres 0 all grades.
     QUEUE-GUESS CORRECTIONS: Military slots = 3 (SAME as Chieftain, NOT "more"); hardness = 65 (SAME,
     NOT higher). It IS the tank: heavier/more armour/more shield/deeper optionals than the Chieftain,
     but SLOWER (204 vs 230) and less agile (roll 90/pitch 32 vs 92/39). More total mounts (7 vs 6) but
     FEWER Large (1L vs 2L). Cross-linked [[ships/alliance-chieftain]] (bidirectional sibling note added
     to chieftain intro) + full AX weapon/utility/defence line. Noted the Alliance Crusader as the
     un-paged third sibling (now queued).
     (2) kb/ships/krait-phantom.md NEW (krait_phantom, edID 128839281). Faulcon DeLacy, class 2 (medium
     pad), NO requirements block in data (no Horizons gate recorded). hullMass 270 (50t under Mk II's
     320), speed 250/boost 350, baseShield 200, baseArmour 180, hardness 55, heatcap 300, masslock 14,
     crew 2, NO fighter bay (fighterHangars absent), pitch 26 / roll 90 / yaw 10, reservefuel 0.63, hull
     cost 35,741,519 / retail 37,472,252. Core: PP7 Thr6 FSD5 LS4 PD7 Sen6 FT5 (IDENTICAL core to Mk II).
     Hardpoints 2L+2M (FOUR mounts, one Large fewer than Mk II's 5) + 4 utility. Optionals 6,5,5,5,3,3,
     3,2,1 (NINE) + class-1 PAS. NO Military slots. Bulkheads causres 0 all grades.
     QUEUE-GUESS CORRECTION: the Phantom does NOT have "an extra/larger optional internal" — both Krait
     hulls have NINE optionals and the Mk II's top end is actually BIGGER (two class-6 vs Phantom's one).
     The Phantom's longer range comes from LOWER HULL MASS (270 vs 320) + dropped fighter bay, not bigger
     internals. crew 2 (vs Mk II's 3) CONFIRMED; fighter bay ABSENT CONFIRMED. Cross-linked
     [[ships/krait-mk-ii]] (bidirectional sibling note added to mk-ii intro) + [[engineers/felicity-farseer]]
     + [[outfitting/guardian-fsd-booster]] + [[outfitting/fuel-scoop]] for the explorer fit.
     PATH NOTES: BOTH filenames resolved FIRST TRY, no 404 — ships/alliance_challenger.json (key
     alliance_challenger) and ships/krait_phantom.json (key krait_phantom). trunk.md: +2 Ships bullets +
     extended the "AX hulls" line in the AX/Thargoid section (now Chieftain/Challenger pair + Krait Mk II/
     Phantom pair).
     NEXT: complete the Alliance AX trio with the Alliance Crusader (multicrew/fighter-bay sibling), then
     PIVOT TO LARGE-PAD AX with the Federal Corvette (Core Dynamics flagship; first KB ship with a Huge
     class-4 hardpoint, rank-gated). Both queued as concrete Tier-0 URLs. After those, large-pad AX could
     extend to the Anaconda, or AX coverage could move to Spire/Titan site mechanics. -->


<!-- DONE loop 22: PIVOTED FROM AX MODULES TO AX HULLS — added the two iconic medium-pad AX
     platforms that carry the now-complete AX weapon/utility/defence line. 2 new Tier-0 Coriolis
     ship pages (both availability: live, source_count 1, verified false):
     (1) kb/ships/alliance-chieftain.md NEW (alliance_chieftain, edID 128816574). Lakon/Alliance,
     class 2 (medium pad), requires Horizons. hullMass 400, speed 230/boost 330, baseShield 200,
     baseArmour 280, HARDNESS 65 (high), heatcap 289, masslock 13, crew 2, NO fighter bay
     (fighterHangars absent), roll 92 (very agile), pitch 39 / yaw 16, reservefuel 0.77, hull cost
     18,612,476 / retail 19,382,252. Core: PP6 Thr6 FSD5 LS5 PD6 Sen4 FT4. Hardpoints 2L+1M+3S
     (six mounts) + 4 utility. Optionals 6,5,4,2,2,1 + THREE class-4 MILITARY slots + class-1 PAS.
     DEFINING TRAIT = the 3 Military slots (eligible per data: mahr/hr/scb/mrp/gsrp/gmrp/ghrp) — the
     AX-defence reinforcement modules go here without costing cargo/utility internals. Bulkheads
     causres 0 on ALL grades (no caustic res from hull; fit Meta-Alloy HRP). Cross-linked the full AX
     weapon line + AX utility trio + decon limpet + the Military-eligible defence modules + a vs-Krait
     compare section.
     (2) kb/ships/krait-mk-ii.md NEW (krait_mkii, edID 128816567). Faulcon DeLacy, class 2 (medium
     pad). hullMass 320, speed 240/boost 330, baseShield 220, baseArmour 220, hardness 55, heatcap
     300, masslock 16, crew 3, fighterHangars TRUE (SLF bay), roll 90 / pitch 26 / yaw 10, reservefuel
     0.63, hull cost 44,160,710 / retail 45,814,205. Core: PP7 Thr6 FSD5 LS4 PD7 Sen6 FT5 (big class-7
     PP + PD). Hardpoints 3L+2M (five mounts — heavier than Chieftain) + 4 utility. Optionals
     6,6,5,5,4,3,3,2,1 + class-1 PAS. NO Military slots (key contrast w/ Chieftain). Bulkheads causres
     0. Cross-linked AX weapon/utility line + a vs-Chieftain compare section.
     PATH NOTES: BOTH filenames resolved FIRST TRY, no 404 — ships/alliance_chieftain.json (key
     alliance_chieftain) and ships/krait_mkii.json (key krait_mkii; the "kraitmkii" guess mapped to
     krait_mkii.json). trunk.md: +2 Ships bullets + new "AX hulls" line in the AX/Thargoid section.
     NEXT: complete the Alliance AX trio (Alliance Challenger = tankiest sibling) + the Krait Phantom
     (explorer sibling of the Mk II) — both queued as concrete Tier-0 URLs. After those, AX-hull
     coverage could extend to a large-pad AX platform (Anaconda / Federal Corvette) or Spire/Titan
     site mechanics. -->


<!-- DONE loop 21: COMPLETED THE AX-UTILITY MODULE LINE — added the AX LIMPET leg, the last
     AX-utility module. 1 new Tier-0 Coriolis outfitting page (availability: live, source_count 1,
     verified false): kb/outfitting/decontamination-limpet-controller.md NEW (grp dtl, symbol
     Int_DroneControl_Decontamination_Size{1,3,5,7}_Class1). It is an OPTIONAL INTERNAL (not a
     utility hardpoint like the caustic sink) commanding a limpet that removes CAUSTIC chemicals
     from the hull over time + applies a SMALL amount of hull repair; can target self OR a nearby
     allied ship. The sustained limpet-borne complement to [[outfitting/caustic-sink-launcher]]
     (sink = instant, self-only, utility mount; decon limpet = gradual, self/ally, internal slot,
     +minor repair). DATA: 4 sizes ONLY — classes 1/3/5/7, ALL rating E (no A–E ladder, unlike the
     mining prospector/collector controllers). maximum (= max simultaneous limpets): C1 1 / C3 2 /
     C5 3 / C7 4. range (km): 0.6 / 0.88 / 1.3 / 2.04 (short — own hull or nearby ally). mass: 1.3
     / 2 / 20 / 128 t. power: 0.18 / 0.2 / 0.5 / 0.97 MW. cost: 3,600 / 16,200 / 145,800 / 1,312,200
     CR. ids y1-y4. NO `time` (limpet-lifetime) field in this controller's data. Where: standard
     module, AX/rescue supply. PATH NOTE: internal/decontamination_limpet_controller.json resolved
     FIRST TRY (1957 bytes, no 404) — loop-19 path note confirmed, require('./x')=.json holds.
     trunk.md: +1 Outfitting bullet + extended the AX-utilities line in the AX/Thargoid section.
     Bidirectional link added to [[outfitting/limpet-controllers]] (turned the "decontamination"
     out-of-scope mention into a wikilink). With this, the WHOLE AX outfitting line (weapons +
     defence + utilities) is complete. NEXT: pivot to AX HULLS — the platforms that carry this kit.
     Queued the Alliance Chieftain (iconic medium AX combat ship) + Krait Mk II (heavier AX
     multirole), both Tier-0 Coriolis ships/, to tie the AX module line to concrete builds. -->


<!-- DONE loop 20: COMPLETED THE AX-UTILITY TRIO — the survival/targeting kit that turns any hull
     into a Thargoid-capable ship. 3 new Tier-0 Coriolis outfitting pages (all availability: live,
     source_count 1, verified false), all class-0 utility mounts:
     (1) kb/outfitting/caustic-sink-launcher.md NEW (grp csl, single variant id 4A rating I, symbol
     Hpt_CausticSinkLauncher_Turret_Tiny). The caustic analogue of the Heat Sink Launcher — fires a
     caustic sink that instantly purges accumulated caustic DoT (Thargoid clouds / enzyme missiles /
     Titan-Maelstrom). NO class/rating ladder (one size). KEY: clip 1 + ammo 5 = SIX sinks (vs heat
     sink's 4). ammocost 10, fireint 5.0, reload 10, power 0.6, eps 0.4, distdraw 2, mass 1.7,
     integ 45, cost 50,000, passive 1. Where: Human Tech Broker / AX supply. Cross-linked
     [[outfitting/heat-sink-launcher]].
     (2) kb/outfitting/xeno-scanner.md NEW (grp xs). IDs Thargoid type + reveals subsystems/weak
     points (mandatory to target Interceptor hearts). 3 variants, all class 0, shared scantime 10s /
     angle 23 / boot 2s. RANGE is the differentiator: xs base rating E 500m (power 0.2, mass 1.3,
     integ 56, cost 365,698) / 3y Enhanced Xeno Scanner (Mk2) rating C 2000m (power 0.8, same mass/
     integ, cost 745,948 — the practical default) / 4B Pulse Wave Xeno Scanner rating C 1000m but
     heavier (mass 3, integ 100, power 1.0, cost 850,000). Symbols XenoScanner_Basic / XenoScannerMk2_
     Basic / XenoScanner_Advanced.
     (3) kb/outfitting/shutdown-field-neutraliser.md NEW (grp sfn). Counters the Thargoid EMP
     shutdown-field pulse that disables ship systems. 2 variants, both class 0, shared cooldown 10 /
     duration 1 / passive 1. Sn base rating F range 3000m (power 0.2, activepower 0.25, mass 1.3,
     integ 35, cost 63,000) / 4E "Thargoid Pulse Neutraliser" V2 rating E (power 0.4, activepower 0.33,
     mass 3, integ 70, cost 150,000) — its range field is 0 in Coriolis data (recorded verbatim, NOT
     invented). activepower (draw while firing) is distinct from passive power. Symbols
     AntiUnknownShutdown_Tiny / _Tiny_V2.
     trunk.md: +3 Outfitting bullets + new "AX utilities" line in the AX/Thargoid section (scanner /
     shutdown neutraliser / caustic sink trio). Bidirectional AX-utility cross-links across all 3 new
     pages + [[outfitting/heat-sink-launcher]]. PATH NOTES: all 3 hardpoints/*.json (caustic_sink_
     launcher, xeno_scanner, shutdown_field_neutraliser) resolved first try, no 404 — index.js keys
     csl/xs/sfn confirmed last loop. NEXT: decontamination_limpet_controller (dtl, internal/) = the AX
     LIMPET line (sustained caustic removal, self/ally) — queued. After that the core AX-utility set is
     complete; AX coverage could then move to AX hull/build guidance or Spire/Titan site mechanics. -->


<!-- DONE loop 19: COMPLETED THE ENTIRE AX-WEAPON LINE — the last AX missile/torpedo-family weapon.
     1 new Tier-0 Coriolis outfitting page (availability: live, source_count 1, verified false):
     kb/outfitting/nanite-torpedo-pylon.md NEW (grp ntp, symbol Hpt_ATVentDisruptorPylon_Fixed_*).
     The SEEKING anti-Thargoid torpedo (missile "S" — distinct from the dumbfire axmr/axmre "D"). The
     internal symbol "ATVentDisruptorPylon" reveals the mechanism: a guided torpedo carrying a NANITE
     payload aimed at Thargoid caustic/cooling VENTS, not conventional hull damage. KEY DATA FACT:
     damage 0 with damagedist {E:1} — the data carries NO direct hull damage and NO payload magnitude,
     so no numeric effect was invented (same discipline as enzyme-missile-rack's DoT). 2 variants only,
     both Fixed, rating I, single-shot clip 1: 4Q Medium (class 2, ammo 64, power 0.4, mass 3, integ 50,
     cost 843,170) / 4R Large (class 3, ammo 125, power 0.7, mass 5, integ 80, cost 1,627,419). Constants:
     reload 3, fireint 2.0, shotspeed 1000, thermload 35 (high), breachdmg 0, distdraw 0. NO Small, NO
     Turret, NO pre-eng reward variant. Source: Human Tech Broker / AX war-effort supply (no Guardian
     unlock). trunk.md: +1 Outfitting bullet + AX/Thargoid explosive line extended (now lists the seeking
     nanite torpedo alongside axmr/axmre/enzyme). Bidirectional "Related AX weapons" backlinks added to
     ax-missile-rack.md, ax-missile-rack-enhanced.md, enzyme-missile-rack.md. PATH NOTE: ntp resolved
     first try (hardpoints/nanite_torpedo_pylon.json), no 404. NEXT COVERAGE = AX-UTILITY MODULES: paths
     resolved this loop via index.js and queued as concrete URLs — csl (caustic_sink_launcher), xs
     (xeno_scanner), sfn (shutdown_field_neutraliser); dtl (decontamination_limpet_controller, internal/)
     still open after. After ntp the AX-WEAPON line is COMPLETE; AX coverage now shifts to utilities. -->


<!-- DONE loop 18: completed the AX MISSILE family (3 new Tier-0 Coriolis outfitting pages, all
     availability: live, source_count 1, verified false):
     (1) kb/outfitting/ax-missile-rack-enhanced.md NEW (grp axmre, symbol Hpt_ATDumbfireMissile_*_v2).
     The v2 UPGRADE of base axmr (done L17). damagedist {X:1,E:1}, dumbfire only (missile "D"). KEY
     DIFFS vs base: dmg 77 (Fixed) / 64 (Med Turret) vs base 64/50; shotspeed 1250 (vs 750, 1.67x);
     power 1.30/1.72/1.85 (vs 1.20/1.62/1.75). 4 std variants only — NO pre-eng reward variants (base
     had 2). Lower nominal ratings (Fixed Med D / Turret Med E / Fixed Lrg B / Turret Lrg D). Med+Lrg,
     Fixed+Turret. ammo 64/128, clip 8/12, piercing 60, fireint 2.0, reload 5. NOTE file OMITS the
     falloff field base carried. Human Tech Broker. Bidirectional links added to base ax-missile-rack.md.
     (2) kb/outfitting/remote-release-flechette-launcher.md NEW (grp tbrfl, symbol
     Hpt_FlechetteLauncher_*_Medium). KINETIC sibling of the Flak Launcher (rfl, done L17) — the OTHER
     remote-detonation anti-swarm weapon. damagedist {K:1} (100% kinetic shrapnel, NOT explosive).
     NOT experimental-flagged. Class 2 (Med) ONLY, rating B, Fixed+Turret. dmg 13, ammo 72 (vs flak 32),
     piercing 80(F)/70(T) (vs flak 60), breachdmg 6.5 (flak had none), clip 1, reload 2, fireint 2.0,
     shotspeed 550, power 1.20, mass 4. 2 variants (xy Med F B 353761 / yF Med T B 1279200). NO pre-eng.
     Added a "Flak vs Flechette" compare section to both pages. AX war-effort supply / Human Tech Broker.
     (3) kb/outfitting/enzyme-missile-rack.md NEW (grp tbem, symbol Hpt_CausticMissile_Fixed_Medium).
     The CAUSTIC AX missile = "Caustic Missile" internally; caustic enzyme DoT degrades Thargoid hull
     over time (DoT magnitude NOT in Coriolis data — did not invent). damagedist {E:1}, low direct
     damage 5. experimental:true. Class 2 Med FIXED ONLY (no Turret/Small/Large). clip 8, ammo 64,
     reload 5, fireint 2.0, piercing 60, shotspeed 750, thermload 1.5, power 1.20, cost 480501. Base
     variant xt + 1 pre-eng CG-reward variant 5Z "Caust Enzyme (High Cap)" (G5 HighCapacity, locked:
     not reeng/gradechange, no experimental; stored clip 7/ammo 40).
     trunk.md: +3 Outfitting bullets; AX/Thargoid section explosive line extended (enhanced + enzyme),
     anti-swarm line extended (flechette). PATH NOTES: all 3 paths resolved first try (axmre/tbrfl/tbem),
     no 404 — index.js keys confirmed this loop; enzyme guess was correct. Follow-on queued: ntp (nanite
     torpedo pylon, path CONFIRMED via index.js) = LAST AX missile-family weapon. After ntp the entire
     AX-weapon line is complete; next coverage = AX-utility modules (xeno scanner / shutdown field
     neutraliser / caustic sink launcher). -->


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
