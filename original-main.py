clear()
change_hat(Hats.Pumpkin_Hat)

# Decide which crop to grow logic
def plant_decision(hay, wood, carrot, pumpkin):
	decision = None

	if hay <= wood and hay <= carrot and hay <= pumpkin:
		decision = 'hay'
	elif wood < hay and wood < carrot and wood < pumpkin:
		decision = 'wood'
	elif carrot < hay and carrot < wood and carrot < pumpkin:
		decision = 'carrot'
	elif pumpkin < hay and pumpkin < wood and pumpkin < carrot and pumpkin:
		decision = 'pumpkin'
	return decision

# Automatic upgrading logic
def autoUnlocks(hayAmount, woodAmount, carrotAmount, pumpkinAmount):
	grassCost = get_cost(Unlocks.Grass)
	expandCost = get_cost(Unlocks.Expand)
	carrotsCost = get_cost(Unlocks.Carrots)
	treesCost = get_cost(Unlocks.Trees)
	cactusCost = get_cost(Unlocks.Cactus)
	pumpkinsCost = get_cost(Unlocks.Pumpkins)
	wateringCost = get_cost(Unlocks.Watering)

	if woodAmount >= grassCost[Items.Wood]:
		unlock(Unlocks.Grass)
		print("Unlocked the next level of Grass")

	if hayAmount >= treesCost[Items.Hay]:
		unlock(Unlocks.Trees)
		print("Unlocked the next level of Trees")

	if woodAmount >= carrotsCost[Items.Wood]:
		unlock(Unlocks.Carrots)
		print("Unlocked the next level of Carrots")

	if carrotAmount >= pumpkinsCost[Items.Carrot]:
		unlock(Unlocks.Pumpkins)
		print("Unlocked the next level of Pumpkins")

	if pumpkinAmount >= cactusCost[Items.Pumpkin]:
		unlock(Unlocks.Cactus)
		print("Unlocked the next level of Cactus")

	if woodAmount >= wateringCost[Items.Wood]:
		unlock(Unlocks.Watering)
		print("Unlocked the next level of Watering")

	if pumpkinAmount >= expandCost[Items.Pumpkin]:
		unlock(Unlocks.Expand)
		print("Unlocked the next level of Expand")

# Main loop
while True:
	quick_print('----------------------------------------------------------------------------')
	# Initial variables
	worldSize = get_world_size()
	hayAmount = num_items(Items.Hay)
	woodAmount = num_items(Items.Wood)
	carrotAmount = num_items(Items.Carrot)
	pumpkinAmount = num_items(Items.Pumpkin)
	fertilizerAmount = num_items(Items.Fertilizer)
	waterAmount = num_items(Items.Water)
	cropChoice = plant_decision(hayAmount, woodAmount, carrotAmount, pumpkinAmount)

	# Unlock upgrades when possible
	autoUnlocks(hayAmount, woodAmount, carrotAmount, pumpkinAmount)

	for x in range(worldSize):
		for y in range(worldSize):
			# Update amounts
			hayAmount = num_items(Items.Hay)
			woodAmount = num_items(Items.Wood)
			carrotAmount = num_items(Items.Carrot)
			pumpkinAmount = num_items(Items.Pumpkin)
			fertilizerAmount = num_items(Items.Fertilizer)
			waterAmount = num_items(Items.Water)

			if cropChoice == 'hay':
				harvest()
				if get_ground_type() != Grounds.Grassland:
					till()

			elif cropChoice == 'wood':
				harvest()
				evenOrOddX = x % 2
				evenOrOddY = y % 2
				if evenOrOddX == 0 and evenOrOddY == 0:
					plant(Entities.Tree)
				elif evenOrOddX == 1 and evenOrOddY == 1:
					plant(Entities.Tree)
				else:
					if hayAmount <= carrotAmount:
						if get_ground_type() != Grounds.Grassland:
							till()
					else:
						if get_ground_type() != Grounds.Soil:
							till()
						plant(Entities.Carrot)

			elif cropChoice == 'carrot':
				harvest()
				if get_ground_type() != Grounds.Soil:
					till()
				plant(Entities.Carrot)

			elif cropChoice == 'pumpkin':
				if get_entity_type() != Entities.Pumpkin:
					harvest()
				if get_ground_type() != Grounds.Soil:
					till()
				while get_water() < 1:
					use_item(Items.Water)
				plant(Entities.Pumpkin)
				do_a_flip()
				while can_harvest() == False:
					harvest()
					plant(Entities.Pumpkin)
					do_a_flip()

			move(North)
		move(East)

	if cropChoice == 'pumpkin':
		harvest()

	if get_pos_x() != 0 and get_pos_y() != 0:
		clear()
