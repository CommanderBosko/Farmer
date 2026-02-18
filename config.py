# Configuration for the Farmer bot

# Set a focus crop, or set to None for default behavior.
# Possible values: "Hay", "Wood", "Carrot", "Pumpkin", None
FOCUS_CROP = None

# How often to print the current goal (every N loops). Set to 1 to print every loop.
# Set to 0 or None to disable.
PRINT_GOAL_INTERVAL = 1

# The minimum amount of a prerequisite resource to have in stock before
# planting the next tier of crop.
MIN_PREREQ_STOCK = 100000
