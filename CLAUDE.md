# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running

```bash
python main.py
```

No build, lint, or test tooling exists. This is a procedural Python script.

## Architecture

This is a farming automation bot for a game. The game injects its own API at runtime — functions like `plant()`, `harvest()`, `unlock()`, `move()`, and enums like `Items`, `Entities`, `Grounds`, `Unlocks`, `Hats` are **not defined in this repo** and must not be imported or stubbed.

### Files

- `main.py` — all logic; entry point is the bottom of the file
- `config.py` — three user-tunable knobs (see below)
- `original-main.py` — backup of the pre-refactor version

### Control flow

1. Initialization: `clear()`, `change_hat()`
2. Infinite loop:
   - `update_amounts()` — sync global inventory vars from game
   - `plant_decision()` — pick crop based on config/unlock goals/lowest stock
   - `auto_unlocks()` — spend resources on unlocks if affordable
   - Nested grid traversal calls `farm(crop_choice, x, y)` for every cell
   - Periodic goal status print
   - Final harvest + position reset

### Key design constraints

- **Procedural only** — the game environment does not support Python classes or advanced syntax. No OOP, no dataclasses, no comprehensions that rely on class scope.
- **Global state** — resource counts (`hay`, `wood`, `carrot`, `pumpkin`, `fertilizer`, `water`, `loop_counter`) are module-level globals mutated by `update_amounts()`.
- **Data-driven unlock logic** — unlock ordering and prerequisite checks use tuple/dict tables (`UNLOCK_NAMES`, `PREREQUISITES`, `FOCUS_CROP_MAP`) so new tiers can be added without touching control flow.

### config.py knobs

| Variable | Effect |
|---|---|
| `FOCUS_CROP` | Force-plant one crop type (`"Hay"`, `"Wood"`, `"Carrot"`, `"Pumpkin"`, or `None` for dynamic) |
| `PRINT_GOAL_INTERVAL` | Print status every N outer loops; `0`/`None` disables |
| `MIN_PREREQ_STOCK` | Minimum prerequisite resource to hold before advancing to a higher-tier crop (default 100 000) |

### Crop farming strategies (inside `farm()`)

- **Hay** — harvest and maintain grassland terrain
- **Wood** — plant trees on a diagonal checkerboard; fill other cells with carrots
- **Carrot** — harvest and replant on soil
- **Pumpkin** — water → plant → fertilize (or `do_a_flip()` if no fertilizer) → wait → harvest

### Scripting gotchas

**Grid traversal off-by-one** — `move()` does NOT wrap. Always guard the final step:
```python
for y in range(world_size):
    # ... work ...
    if y < world_size - 1:
        move(North)
```
Same applies to `move(East)` at the end of column loops. This mistake exists in both the main loop and inside `farm_cactus()`.

**Cactus — phase state machine** — `farm_cactus()` advances a global `cactus_phase` (0–4):
- 0: Plant — column-by-column traversal, till to Soil, `plant(Entities.Cactus)`
- 1: Wait — advance only when all `can_harvest()`
- 2: Sort rows ascending — bubble sort each row West→East; smaller values bubble West; smallest ends at x=0
- 3: Sort columns ascending — bubble sort each column South→North; smallest ends at y=0
- 4: Harvest — `goto_sw()` to origin, single `harvest()` cascades through sorted field

Sort swap condition (ascending, smallest at SW origin): `if measure() > measure(East/North): swap(East/North)`.

`goto_sw()` navigates to origin (x=0, y=0) by moving South then West. Avoid nested `while` loops inside `farm_cactus()` — the game environment does not handle them reliably.

**Wood — trees require Soil** — before `plant(Entities.Tree)` always check `if get_ground_type() != Grounds.Soil: till()`. Planting on Grassland fails silently.

**Pumpkin — second harvest sweep** — after the main grid traversal a second full sweep is needed to catch tiles that ripened while the drone worked other cells.
