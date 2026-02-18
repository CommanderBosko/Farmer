# Project Overview

This project is an automated farming script for a game. The script, written in Python, automatically decides which crops to plant, harvests them, and unlocks new features based on the resources gathered. The main goal is to efficiently manage the farm to maximize resource production.

# Building and Running

This is a single-file Python script. To run it, you need a Python interpreter and the game environment it's designed to interact with.

```
python main.py
```

**Note:** This script seems to depend on a game-specific API with functions like `get_world_size()`, `plant()`, `harvest()`, `unlock()`, etc. These functions are not defined in the script itself and must be provided by the game environment.

# Development Conventions

The script is written in a procedural style. It uses a main loop to continuously manage the farm. Key logic is separated into functions like `plant_decision` and `autoUnlocks`. There are no specific linting or formatting conventions apparent from this single file, but the code is generally readable.
