# Project State — Farmer Bot

Last updated: 2026-05-28

---

## Current Project State

The bot starts cleanly and runs the full crop progression without warnings. All
primary farming strategies (Hay, Wood, Carrot, Pumpkin, Cactus, Maze, Sunflower)
are implemented. The prerequisite chain (Hay → Wood → Carrot → Pumpkin → Cactus →
Weird_Substance) is enforced correctly. Multi-drone grid splitting is working for
Hay/Wood/Carrot/Pumpkin. The bot can grind gold via `MIN_GOLD_STOCK` for
gold-cost upgrades.

**What works:**
- Full crop cycle: Hay → Wood → Carrot → Pumpkin → Cactus → Maze
- Multi-prerequisites per crop (PREREQUISITES dict is now a list of tuples)
- Sunflower farming for passive power stock maintenance
- Maze farming with threshold trigger and wall-following safety valve
- Gold tracking and MIN_GOLD_STOCK grinding mode
- Multi-drone column splitting (USE_MULTIPLE_DRONES)
- Planting guards on all plant() calls (no occupied-tile spam)
- Broken-pumpkin recovery in the pumpkin wait loop
- Auto-unlock purchasing and ordered unlock goal detection

**What is in progress / partially done:**
- Sunflower 8x petal bonus: simplified to snake traversal (no sorted()); the
  maximum-first harvesting optimization was removed to avoid keyword arguments.
- Dinosaur farming: not yet implemented (Bones item documented but no farm_dinosaur()).

**What is broken / known issues:**
- None blocking. See Known Issues section.

---

## Current Goals

### Short-term (next 1–3 sessions)
1. Recover the sunflower 8x petal bonus using a keyword-argument-free sort (manual selection-sort over a list).
2. End-to-end test the prerequisite chain from a fresh game state.
3. Implement Dinosaur Hat / Bones farming once Cactus prerequisites are stable.

### Long-term
- Full automation through all game tiers including Polyculture companion planting.
- Investigate Leaderboard / Simulation unlocks once gold is farmed.

---

## Recent Decisions

| Date | Decision | Rationale |
|---|---|---|
| 2026-05-28 | No keyword arguments anywhere in main.py | Game parser rejects `func(key=value)` — causes silent script-load failure |
| 2026-05-28 | PREREQUISITES values are lists of tuples | Allows multiple prerequisites per crop without control-flow changes |
| 2026-05-28 | MIN_POWER_STOCK = 5 000 | 50 000 caused excessive sunflower detours; 5 000 is sufficient |
| 2026-05-28 | farm_sunflower() uses snake traversal only | Removed sorted(reverse=True) to comply with keyword-arg restriction |

---

## Known Issues / Tech Debt

- **Sunflower 8x bonus lost** — `sorted(harvestable, reverse=True)` was the mechanism; removed because `reverse=True` is a keyword argument. A manual selection-sort would restore the behavior without violating the parser constraint.
- **No Dinosaur farming** — `Unlocks.Dinosaurs` is purchased via auto_unlocks() but `farm_dinosaur()` does not exist. The bot has no strategy for harvesting Bones.
- **Pumpkin split-grid timing** — with `USE_MULTIPLE_DRONES = True` the two drones farm independent columns; the second pumpkin harvest sweep runs sequentially after both drones finish. This is correct but could miss pumpkins that ripen during the inter-drone delay on large grids.
- **No class/OOP** — the game environment forbids Python classes. All state is module-level globals. This is a hard constraint, not debt.

---

## Next Steps

1. Implement selection-sort in farm_sunflower() to restore max-petal-first harvesting without keyword arguments.
2. Run the bot from a fresh game save and verify Hay → Wood → Carrot prerequisite gating works as expected.
3. Add `farm_dinosaur()` stub and wire it into `plant_decision()` once Cactus farming is confirmed stable.
4. Consider adding a `MIN_BONES_STOCK` config knob in preparation for Polyculture (needs Bones for Polyculture Lvl 2).
