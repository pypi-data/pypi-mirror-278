

from goodest.adventures.monetary.DB.goodest_inventory.collect_meals.document.insert import insert_meal

def insert_meal_quest (packet):
	freight = packet ["freight"]
	proceeds = insert_meal (freight)
	
	return proceeds;