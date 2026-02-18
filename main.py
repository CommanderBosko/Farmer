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
ITEM_NAMES = {
	Items.Hay: "Hay",
	Items.Wood: "Wood",
	Items.Carrot: "Carrot",
	Items.Pumpkin: "Pumpkin",
}
# New: Map Unlocks enum to readable names
UNLOCK_NAMES = {
	Unlocks.Grass: "Grass",
	Unlocks.Trees: "Trees",
	Unlocks.Carrots: "Carrots",
	Unlocks.Pumpkins: "Pumpkins",
	Unlocks.Cactus: "Cactus",
	Unlocks.Watering: "Watering",
	Unlocks.Expand: "Expand",
}

# New: Prerequisite mapping for stock checks
PREREQUISITES = {
    Items.Wood: (Items.Hay, config.MIN_PREREQ_STOCK),
    Items.Carrot: (Items.Hay, config.MIN_PREREQ_STOCK),
    Items.Pumpkin: (Items.Carrot, config.MIN_PREREQ_STOCK),
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
	unlocks_to_check = [
		(Unlocks.Grass, Items.Wood),
		(Unlocks.Trees, Items.Hay),
		(Unlocks.Carrots, Items.Wood),
		(Unlocks.Pumpkins, Items.Carrot),
		(Unlocks.Cactus, Items.Pumpkin),
		(Unlocks.Watering, Items.Wood),
		(Unlocks.Expand, Items.Pumpkin),
	]

	cheapest_goal = (None, None)
	min_cost = 999999 # Using a large number as the initial minimum

	for unlock_item, required_item in unlocks_to_check:
		cost = get_cost(unlock_item)
		
		# If the unlock is available to be purchased
		if cost:
			required_amount = cost[required_item]
			
			# If we can't afford it yet AND it's the cheapest so far
			if get_amount(required_item) < required_amount and required_amount < min_cost:
				min_cost = required_amount
				cheapest_goal = (required_item, UNLOCK_NAMES[unlock_item])

	return cheapest_goal

def plant_decision():
    # Helper to check prerequisite stock
    def check_stock(crop_to_plant):
        if crop_to_plant in PREREQUISITES:
            prereq_item, required_amount = PREREQUISITES[crop_to_plant]
            if get_amount(prereq_item) < required_amount:
                return prereq_item # Not enough stock, return the prerequisite to plant instead
        return crop_to_plant # Stock is fine, proceed with the original plan

    if config.FOCUS_CROP and config.FOCUS_CROP in FOCUS_CROP_MAP:
        return FOCUS_CROP_MAP[config.FOCUS_CROP] # Focus mode bypasses stock checks

    goal_item, unlock_name = get_next_unlock_goal()
    if goal_item:
        return check_stock(goal_item) # Check stock for the goal item

    # Fallback logic: plant what you have the least of, but check prerequisites
    if hay <= wood and hay <= carrot and hay <= pumpkin:
        return Items.Hay
    elif wood < hay and wood < carrot and wood < pumpkin:
        return check_stock(Items.Wood)
    elif carrot < hay and carrot < wood and carrot < pumpkin:
        return check_stock(Items.Carrot)
    elif pumpkin < hay and pumpkin < wood and pumpkin < carrot:
        return check_stock(Items.Pumpkin)
    
    return None # Should not be reached in normal operation

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
		
		# Use fertilizer if available, otherwise flip
		if fertilizer > 0:
			use_item(Items.Fertilizer)
		else:
			do_a_flip()
		
		while not can_harvest():
			harvest()
			plant(Entities.Pumpkin)
			# Use fertilizer if available, otherwise flip
			if fertilizer > 0:
				use_item(Items.Fertilizer)
			else:
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
		# Get goal info for printing
		goal_item, unlock_name = get_next_unlock_goal()

		if crop_choice in ITEM_NAMES:
			current_goal_name = ITEM_NAMES[crop_choice]
		else:
			current_goal_name = "Unknown Goal"

		status_message = "Current Goal: " + current_goal_name
		# Add unlock name to status if there is one
		if unlock_name and not config.FOCUS_CROP:
			status_message = status_message + " (for upgrading " + unlock_name + ")"

		quick_print('--------------------------------------------------------------------')
		quick_print(status_message)
		quick_print('--------------------------------------------------------------------')
	else:
		quick_print('--------------------------------------------------------------------')


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
