# Configuration for the Farmer bot

# Set a focus crop, or set to None for default behavior.
# Possible values: "Hay", "Wood", "Carrot", "Pumpkin", "Cactus", "Maze", "Sunflower", None
# WARNING: FOCUS_CROP bypasses prerequisite stock checks entirely.
# If planting a crop that requires prerequisites (e.g. Pumpkin requires Carrot),
# you must pre-stock those prerequisites manually before enabling this mode.
FOCUS_CROP = None

# How often to print the current goal (every N loops). Set to 1 to print every loop.
# Set to 0 or None to disable.
PRINT_GOAL_INTERVAL = 1

# The minimum amount of a prerequisite resource to have in stock before
# planting the next tier of crop.
MIN_PREREQ_STOCK = 100000

# Minimum power to keep on hand. When power drops below this the bot will
# switch to sunflower farming until it's replenished. Power doubles drone
# speed (1 power consumed per 30 actions), so keeping it stocked is worth
# the brief detour. Requires Unlocks.Sunflowers to be purchased first.
MIN_POWER_STOCK = 5000

# Weird_Substance threshold for triggering maze farming. The bot will run a
# maze (clearing the current farm) only when this much WS is stockpiled.
# Maze cost = world_size * 2^(maze_level-1), so 500 comfortably covers any
# level. Lower this for more frequent maze runs; raise it to prioritize crops.
MIN_WEIRD_SUBSTANCE_STOCK = 500

# Gold target. When > 0, the bot will prioritize maze runs (as soon as one
# maze worth of WS is available) until gold reaches this amount. Set this
# before manually purchasing gold-cost upgrades (Top Hat, Megafarm, Debug_2,
# Simulation, Leaderboard), then reset to 0 when done.
MIN_GOLD_STOCK = 0

# Enable multi-drone farming (requires Mega Farm unlock purchased with Gold).
# Set to False to fall back to single-drone if issues arise.
USE_MULTIPLE_DRONES = True
