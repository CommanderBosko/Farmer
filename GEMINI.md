# Project Overview

This project is an automated farming script for a game, designed for efficiency and robustness within a unique execution environment. It automatically decides which crops to plant, harvests them, and strategically manages upgrades.

Key Features and Improvements:
*   **Dynamic Upgrade Prioritization:** The script now prioritizes unlocking upgrades based on the lowest resource cost, rather than a fixed order, ensuring a more adaptive progression.
*   **Resource Prerequisite Safeguard:** A new mechanism ensures that a minimum stock of prerequisite resources (e.g., Carrots for Pumpkins) is maintained before planting higher-tier crops, preventing resource depletion stalls.
*   **Intelligent Pumpkin Farming:** When farming pumpkins, the script will automatically use available fertilizer to speed up growth; otherwise, it performs a 'do_a_flip()' action.
*   **Configurable Behavior:** Key operational parameters, including focus crops and goal printing intervals, are externalized into `config.py` for easy customization without modifying the main script.
*   **Status Feedback:** The script provides periodic updates on its current farming goal, including the specific unlock it's working towards, for better visibility into its operations.

# Building and Running

This is a single-file Python script (`main.py`). To run it, you need a Python interpreter and the game environment it's designed to interact with.

```bash
python main.py
```

**Configuration:**
Customize bot behavior by editing the `config.py` file. Adjust settings like `FOCUS_CROP` for planting priority and `PRINT_GOAL_INTERVAL` for status update frequency, and `MIN_PREREQ_STOCK` for resource safeguarding.

**Note:** This script depends on a game-specific API with functions like `get_world_size()`, `plant()`, `harvest()`, `unlock()`, etc. These functions are not defined in the script itself and must be provided by the game environment.

# Development Conventions

The script is developed in a procedural style, necessitated by the constraints of the execution environment, which does not support Python classes or advanced syntax features. Global variables are used for managing state. The code aims for clarity and maintainability while adhering to these strict compatibility requirements. Data-driven approaches have been used where possible (e.g., for `auto_unlocks` and `PREREQUISITES`) to keep the logic modular.
