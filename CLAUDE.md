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
- `config.py` — user-tunable knobs (see below)
- `original-main.py` — backup of the pre-refactor version

### Control flow

1. Initialization: `clear()`, `change_hat()`
2. Infinite loop:
   - `update_amounts()` — sync global inventory vars from game
   - `plant_decision()` — pick crop based on config/unlock goals/lowest stock
   - `auto_unlocks()` — spend resources on unlocks if affordable
   - `farm_grid(crop_choice, start_x, end_x)` or two drones calling it on split columns
   - Periodic goal status print
   - Final harvest + position reset

### Key design constraints

- **Procedural only** — the game environment does not support Python classes or advanced syntax. No OOP, no dataclasses, no comprehensions that rely on class scope.
- **Global state** — resource counts (`hay`, `wood`, `carrot`, `pumpkin`, `cactus`, `weird_substance`, `fertilizer`, `water`, `power`, `gold`, `loop_counter`) are module-level globals mutated by `update_amounts()`.
- **Data-driven unlock logic** — unlock ordering and prerequisite checks use tuple/dict tables (`UNLOCK_NAMES`, `PREREQUISITES`, `FOCUS_CROP_MAP`) so new tiers can be added without touching control flow.

### config.py knobs

| Variable | Effect |
|---|---|
| `FOCUS_CROP` | Force-plant one crop type (`"Hay"`, `"Wood"`, `"Carrot"`, `"Pumpkin"`, `"Cactus"`, `"Maze"`, `"Sunflower"`, or `None` for dynamic) |
| `PRINT_GOAL_INTERVAL` | Print status every N outer loops; `0`/`None` disables |
| `MIN_PREREQ_STOCK` | Minimum prerequisite resource to hold before advancing to a higher-tier crop (default 100 000) |
| `MIN_POWER_STOCK` | Replenish sunflowers when power drops below this; power doubles drone speed (default 500) |
| `MIN_WEIRD_SUBSTANCE_STOCK` | Run a maze when `Items.Weird_Substance` reaches this level; lower = more frequent runs (default 500) |
| `MIN_GOLD_STOCK` | When `> 0`, prioritize maze runs until this gold target is reached; set before manually buying gold-cost upgrades, reset to `0` when done (default 0) |
| `NUM_DRONES` | Number of parallel drones (1–32); capped to `world_size`; Cactus/Maze/Sunflower always run single-drone; requires Megafarm upgrade (default `32`) |

### Crop farming strategies (inside `farm()`)

- **Hay** — harvest and maintain grassland terrain
- **Wood** — plant trees on a diagonal checkerboard; fill other cells with carrots
- **Carrot** — harvest and replant on soil
- **Pumpkin** — water → plant → fertilize (or `do_a_flip()` if no fertilizer) → wait → harvest
- **Cactus** — phase state machine in `farm_cactus()`; see Scripting gotchas below
- **Maze** — triggered when `weird_substance >= MIN_WEIRD_SUBSTANCE_STOCK` (not by lowest-stock logic); `farm_maze()` calls `clear()`, grows a maze from a bush, left-hand wall-follows to `Entities.Treasure` (step-counter safety valve: `world_size² × 4` max steps), harvests if treasure was reached, then calls `clear()` again to reset the farm; single-use only (no reuse stacking)
- **Sunflower** — `farm_sunflower()` fills the entire grid with sunflowers; Pass 1 scans for the max-petal cell, then harvests it first for the 8× power bonus (requires ≥10 sunflowers on the farm, i.e. world_size ≥ 4); Pass 2 harvests all remaining ready cells and replants

### Items reference

| Item | Obtained from | Notes |
|---|---|---|
| `Items.Hay` | Harvesting grassland | Prerequisite for Wood/Carrot unlocks |
| `Items.Wood` | Harvesting bushes and trees | Diagonal checkerboard farming |
| `Items.Carrot` | Harvesting carrots | Prerequisite for Pumpkin unlocks |
| `Items.Pumpkin` | Harvesting pumpkins | Prerequisite for Cactus/Dinosaur unlocks |
| `Items.Cactus` | Harvesting sorted cacti | Phase state machine; prerequisite for Dinosaur unlock |
| `Items.Weird_Substance` | **Side-effect of `use_item(Items.Fertilizer)`** on any plant | Spent (not grown) — consumed by `farm_maze()` to enter a maze |
| `Items.Gold` | Maze treasure chest | `harvest()` at `Entities.Treasure`; gold = maze area; tracked in global `gold` and `get_amount()`; used by `MIN_GOLD_STOCK` logic |
| `Items.Fertilizer` | Trade (10 pumpkins each) | `use_item(Items.Fertilizer)` grows plant by 2s; each use also generates `Items.Weird_Substance` |
| `Items.Water` | — | `use_item(Items.Water)` waters soil before planting pumpkins |
| `Items.Power` | Harvesting sunflowers | Passive — doubles drone movement speed automatically; no `use_item()` call needed |
| `Items.Bones` | Dinosaurs (not yet implemented) | "The bones of an ancient creature" |

### Unlocks reference

Payment resources match `auto_unlocks()` and `get_next_unlock_goal()`. Tier labels indicate gameplay tier, not necessarily the payment currency.

| Unlock | Paid with | What it enables |
|---|---|---|
| `Unlocks.Loops` | Hay | `while` loops; `True`/`False` |
| `Unlocks.Plant` | Hay | `plant()` function |
| `Unlocks.Hats` | Hay | `change_hat()` and hat bonuses |
| `Unlocks.Speed` | Hay | Drone speed upgrade (repeatable) |
| `Unlocks.Senses` | Hay | `get_pos_x/y()`, `num_items()`, `get_entity_type()`, `get_ground_type()` |
| `Unlocks.Grass` | Wood (Lvl 2+) | Hay yield multiplier: 100%→200%→400%+ |
| `Unlocks.Carrots` | Wood | `till()` + `plant(Entities.Carrot)` |
| `Unlocks.Fertilizer` | Wood | `trade(Items.Fertilizer)` + `use_item(Items.Fertilizer)` |
| `Unlocks.Watering` | Wood | Doubles water regen rate |
| `Unlocks.Variables` | Carrot | Variable assignment (`=`) |
| `Unlocks.Functions` | Carrot | `def` function definitions |
| `Unlocks.Import` | Carrot | `import` statement |
| `Unlocks.Lists` | Carrot | Lists and sets |
| `Unlocks.Sunflowers` | Carrot | `plant(Entities.Sunflower)` → passive `Items.Power` speed boost |
| `Unlocks.Trees` | Hay | `plant(Entities.Tree)` — 5 wood each |
| `Unlocks.Pumpkins` | Carrot | `plant(Entities.Pumpkin)` — initial cost 500 Wood + 200 Carrots |
| `Unlocks.Expand` | Pumpkin | Expands farm grid size |
| `Unlocks.Utilities` | Pumpkin | `min()`, `max()`, `abs()` |
| `Unlocks.Timing` | Pumpkin | `get_time()`, `get_tick_count()` |
| `Unlocks.Costs` | Pumpkin | `get_cost()` |
| `Unlocks.Dictionaries` | Pumpkin | Dict and set data structures |
| `Unlocks.Polyculture` | Pumpkin (Lvl 2: 10,000 Bones) | `get_companion()` — companion planting multiplier (base 5×, upgrades to 10×/20×/…) |
| `Unlocks.Auto_Unlock` | Pumpkin | `unlock()`, `get_cost()`, `num_unlocked()` |
| `Unlocks.Cactus` | Pumpkin | `plant(Entities.Cactus)`, `measure()`, `swap()` |
| `Unlocks.Dinosaurs` | Cactus | `Hats.Dinosaur_Hat` → Bones harvesting |
| `Unlocks.Mazes` | Cactus | Each level doubles maze treasure and `Items.Weird_Substance` cost |

**Wiki pages that are NOT `Unlocks.*` enum values** (tutorial concepts or removed features):
- Move, If, For, Operators — early built-in features, no corresponding enum
- Debug, Debug_2 — `print()`, `quick_print()`, breakpoints, `set_execution_speed()`
- Benchmark — redirects to Timing wiki page
- Multi_Trade — **removed from game**
- Leaderboard — competitive speed-run feature, not a purchasable unlock

### Scripting gotchas

**Grid traversal off-by-one** — `move()` does NOT wrap. Always guard the final step:
```python
for y in range(world_size):
    # ... work ...
    if y < world_size - 1:
        move(North)
```
Same applies to `move(East)` at the end of column loops. `farm_grid()` and `farm_cactus()` both implement these guards correctly.

**Cactus — phase state machine** — `farm_cactus()` advances a global `cactus_phase` (0–4):
- 0: Plant — column-by-column traversal, till to Soil, `plant(Entities.Cactus)`
- 1: Wait — advance only when all `can_harvest()`
- 2: Sort rows ascending — bubble sort each row West→East; smaller values bubble West; smallest ends at x=0
- 3: Sort columns ascending — bubble sort each column South→North; smallest ends at y=0
- 4: Harvest — `goto_sw()` to origin, single `harvest()` cascades through sorted field

Sort swap condition (ascending, smallest at SW origin): `if measure() > measure(East/North): swap(East/North)`.

`goto_sw()` navigates to origin (x=0, y=0) by moving South then West. Avoid nested `while` loops inside `farm_cactus()` — the game environment does not handle them reliably.

**No keyword arguments in function calls** — the game's Python parser rejects keyword arguments entirely. `sorted(list, reverse=True)` causes a parse error ("Expected comma or closing bracket") that prevents the whole script from starting. Use only positional arguments; replace any `sorted(..., reverse=True)` with a manual sort or a different approach. This applies to ALL function calls, not just `sorted()`.

**No ternary expressions** — `x = a if cond else b` causes a parse error ("A BRACKET_CLOSE is expected here") and silently prevents the script from starting. Use a plain `if`/`else` block instead.

**Wood — trees require Soil** — before `plant(Entities.Tree)` always check `if get_ground_type() != Grounds.Soil: till()`. Planting on Grassland fails silently.

**Pumpkin — second harvest sweep** — after the main grid traversal a second full sweep is needed to catch tiles that ripened while the drone worked other cells.

**Mega Farm — multi-drone parallelism** — `farm_grid(crop_choice, start_x, end_x)` wraps the per-cell loop. When `config.NUM_DRONES > 1`, the main loop distributes columns evenly across up to 32 drones: `base = world_size // num_drones` columns per drone, with the first `world_size % num_drones` drones getting one extra column. Spawned drones (0..N-2) handle the first N-1 slices; the main drone handles the final slice. Key constraints:
- `num_drones` is capped at `world_size` — no 0-column slices
- Each drone owns exclusive columns — no shared tiles, no race conditions
- `farm_grid()` calls `update_amounts()` at entry to sync the spawned drone's stale globals copy
- Maze always runs single-drone (sequential wall-following); Cactus and Sunflower both parallelize across drones via strip functions
- `spawn_drone()`, `wait_for()`, `has_finished()` are game-injected APIs (not defined in repo)
