






'''
	from goodest.shows_v2.recipe_with_goals._ops.for_1_supp import formulate_recipe_with_goals_for_1_supp 
	formulate_recipe_with_goals_for_1_supp ({
		"supp": {
			"emblem": "4"
		},
		"goal": 2
	})
'''

from goodest.adventures.monetary.DB.goodest_tract.goals.retrieve_one import retrieve_one_goal
from goodest.adventures.monetary.DB.goodest_inventory.foods.document.find import find_food
from goodest.shows_v2.recipe_with_goals._ops.formulate import formulate_recipe_with_goals
from goodest.adventures.monetary.DB.goodest_inventory.supps.document.find import find_supp
	
	
def formulate_recipe_with_goals_for_1_supp (packet):
	goal_emblem = packet ["goal"]
	supp_emblem = packet ["supp"] ["emblem"]
	
	if (type (supp_emblem) == str):
		supp_emblem = int (supp_emblem) 
	
	supp_document = find_supp ({
		"filter": {
			"emblem": supp_emblem
		}
	})	

	recipe_with_goals_packet = formulate_recipe_with_goals ({
		"recipe": supp_document ["nature"],
		"goal_region": goal_emblem
	})
	
	# etch_bracket (normpath (join (this_directory, "recipe.JSON")), food_document)
	
	return supp_document
	