import config

# --- Configuration ---
FOCUS_CROP_MAP = {
    "Hay": Items.Hay,
    "Wood": Items.Wood,
    "Carrot": Items.Carrot,
    "Pumpkin": Items.Pumpkin,
}

# --- Global State ---
hay = 0
wood = 0
carrot = 0
pumpkin = 0
fertilizer = 0
water = 0
loop_counter = 0 # New: Global counter for loop iterations

# Map Items enum to readable names for printing
ITEM_NAMES = { # New: Mapping for readable item names
    Items.Hay: "Hay",
    Items.Wood: "Wood",
    Items.Carrot: "Carrot",
    Items.Pumpkin: "Pumpkin",
}


# --- Functions ---

def get_amount(item):
    if item == Items.Hay:
        return hay
    if item == Items.Wood:
        return wood
    if item == Items.Carrot:
        return carrot
    if item == Items.Pumpkin:
        return pumpkin
    return 0

def get_next_unlock_goal():
    unlocks = [
        (Unlocks.Grass, Items.Wood),
        (Unlocks.Trees, Items.Hay),
        (Unlocks.Carrots, Items.Wood),
        (Unlocks.Pumpkins, Items.Carrot),
        (Unlocks.Cactus, Items.Pumpkin),
        (Unlocks.Watering, Items.Wood),
        (Unlocks.Expand, Items.Pumpkin),
    ]

    for unlock_item, required_item in unlocks:
        cost = get_cost(unlock_item)
        if cost and get_amount(required_item) < cost[required_item]:
            return required_item
    return None

def plant_decision():
    if config.FOCUS_CROP and config.FOCUS_CROP in FOCUS_CROP_MAP:
        return FOCUS_CROP_MAP[config.FOCUS_CROP]

    goal = get_next_unlock_goal()
    if goal:
        return goal

    if hay <= wood and hay <= carrot and hay <= pumpkin:
        return Items.Hay
    elif wood < hay and wood < carrot and wood < pumpkin:
        return Items.Wood
    elif carrot < hay and carrot < wood and carrot < pumpkin:
        return Items.Carrot
    elif pumpkin < hay and pumpkin < wood and pumpkin < carrot:
        return Items.Pumpkin
    return None

def auto_unlocks():
    unlocks = [
        (Unlocks.Grass, Items.Wood, wood, "Grass"),
        (Unlocks.Trees, Items.Hay, hay, "Trees"),
        (Unlocks.Carrots, Items.Wood, wood, "Carrots"),
        (Unlocks.Pumpkins, Items.Carrot, carrot, "Pumpkins"),
        (Unlocks.Cactus, Items.Pumpkin, pumpkin, "Cactus"),
        (Unlocks.Watering, Items.Wood, wood, "Watering"),
        (Unlocks.Expand, Items.Pumpkin, pumpkin, "Expand"),
    ]

    for unlock_item, required_item, current_amount, name in unlocks:
        cost = get_cost(unlock_item)
        if cost and current_amount >= cost[required_item]:
            unlock(unlock_item)
            print("Unlocked the next level of " + name)

def update_amounts():
    global hay
    global wood
    global carrot
    global pumpkin
    global fertilizer
    global water
    hay = num_items(Items.Hay)
    wood = num_items(Items.Wood)
    carrot = num_items(Items.Carrot)
    pumpkin = num_items(Items.Pumpkin)
    fertilizer = num_items(Items.Fertilizer)
    water = num_items(Items.Water)

def farm(crop_choice, x, y):
    if crop_choice == Items.Hay:
        harvest()
        if get_ground_type() != Grounds.Grassland:
            till()

    elif crop_choice == Items.Wood:
        harvest()
        if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
            plant(Entities.Tree)
        else:
            if hay <= carrot:
                if get_ground_type() != Grounds.Grassland:
                    till()
            else:
                if get_ground_type() != Grounds.Soil:
                    till()
                plant(Entities.Carrot)

    elif crop_choice == Items.Carrot:
        harvest()
        if get_ground_type() != Grounds.Soil:
            till()
        plant(Entities.Carrot)

    elif crop_choice == Items.Pumpkin:
        if get_entity_type() != Entities.Pumpkin:
            harvest()
        if get_ground_type() != Grounds.Soil:
            till()
        while get_water() < 1:
            use_item(Items.Water)
        plant(Entities.Pumpkin)
        do_a_flip()
        while not can_harvest():
            harvest()
            plant(Entities.Pumpkin)
            do_a_flip()

# --- Main Execution ---

clear()
change_hat(Hats.Pumpkin_Hat)

while True:
    loop_counter += 1

    update_amounts()
    crop_choice = plant_decision()
    auto_unlocks()
    
    # Print goal occasionally based on config
    if config.PRINT_GOAL_INTERVAL and loop_counter % config.PRINT_GOAL_INTERVAL == 0:
        if crop_choice in ITEM_NAMES:
            current_goal_name = ITEM_NAMES[crop_choice]
        else:
            current_goal_name = "Unknown Goal"
        quick_print('----------------------------------------------------------------------------')
        quick_print("Current Goal: " + current_goal_name)
        quick_print('----------------------------------------------------------------------------')
    else:
        quick_print('----------------------------------------------------------------------------')


    world_size = get_world_size()
    for x in range(world_size):
        for y in range(world_size):
            update_amounts()
            farm(crop_choice, x, y)
            move(North)
        move(East)

    if crop_choice == Items.Pumpkin:
        harvest()

    if get_pos_x() != 0 and get_pos_y() != 0:
        clear()
