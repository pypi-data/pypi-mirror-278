
'''
	from goodest.shows_v2.recipe_with_goals._ops.for_1_food import formulate_recipe_with_goals_for_1_food 
	formulate_recipe_with_goals_for_1_food ({
		"food": {
			"emblem": "4"
		},
		"goal": 2
	})
'''


'''
	recipe_packet = formulate_recipe_with_goals ({
		"recipe": formulate_recipe ({
			"natures_with_amounts": [
				[ retrieve_supp ("coated tablets/multivitamin_276336.JSON"), 1 ]
			]	
		}),
		"goal_region": "2"
	})	
'''
from goodest.adventures.monetary.DB.goodest_tract.goals.retrieve_one import retrieve_one_goal
from goodest.adventures.monetary.DB.goodest_inventory.foods.document.find import find_food
from goodest.shows_v2.recipe_with_goals._ops.formulate import formulate_recipe_with_goals
	
	
def formulate_recipe_with_goals_for_1_food (packet):
	goal_emblem = packet ["goal"]
	food_emblem = packet ["food"] ["emblem"]
	
	food_document = find_food ({
		"filter": {
			"emblem": food_emblem
		}
	})
	
	'''
	import pathlib
	from os.path import dirname, join, normpath
	from goodest.mixes.drives.etch.bracket import etch_bracket
	this_directory = pathlib.Path (__file__).parent.resolve ()
	etch_bracket (normpath (join (this_directory, "food.JSON")), food_document)
	'''

	recipe_with_goals_packet = formulate_recipe_with_goals ({
		"recipe": food_document ["nature"],
		"goal_region": goal_emblem
	})
	
	# etch_bracket (normpath (join (this_directory, "recipe.JSON")), food_document)
	
	return food_document
	