
#----
#
import law_dictionary
#
#
from goodest.adventures.monetary.DB.goodest_inventory.foods.document.find import find_food
from goodest.shows_v2.recipe_with_goals._ops.formulate import formulate_recipe_with_goals
from goodest.shows_v2.recipe_with_goals._ops.for_1_food import formulate_recipe_with_goals_for_1_food 
	
#
#----

def retrieve_food_quest (packet):

	freight = packet ["freight"]
	
	report_freight = law_dictionary.check (
		return_obstacle_if_not_legit = True,
		allow_extra_fields = True,
		laws = {
			"filters": {
				"required": True,
				"type": dict
			},
			#"goal": {
			#	"required": True,
			#	"type": [ int, dict ]
			#}
		},
		dictionary = freight 
	)
	if (report_freight ["advance"] != True):
		return {
			"label": "unfinished",
			"freight": {
				"obstacle": report_freight,
				"obstacle number": 2
			}
		}
	filters = freight ["filters"]
	goal = freight ["goal"]
	
	
	report_filters = law_dictionary.check (
		return_obstacle_if_not_legit = True,
		allow_extra_fields = True,
		laws = {
			"emblem": {
				"required": True,
				"type": str
			}
		},
		dictionary = filters 
	)
	if (report_filters ["advance"] != True):
		return {
			"label": "unfinished",
			"freight": {
				"obstacle": report_filters,
				"obstacle number": 3
			}
		}
	

	try:
		if ("emblem" in filters):
			filters ["emblem"] = int (filters ["emblem"])
	except Exception:	
		return {
			"label": "unfinished",
			"freight": {
				"description": "The emblem couldn't be converted to an integer.",
				"obstacle number": 4
			}
		}
	
	
	'''
	food = find_food ({
		"filter": filters
	})
	recipe_with_goals_packet = formulate_recipe_with_goals ({
		"recipe": food ["nature"],
		"goal_region": "2"
	})	
	recipe = recipe_with_goals_packet ["recipe"]
	'''
	
	
	if (type (goal) == int):
		food = formulate_recipe_with_goals_for_1_food ({
			"food": {
				"emblem": filters ["emblem"]
			},
			"goal": goal
		})
	else:
		food = find_food ({
			"filter": filters
		})

	
	
	
	return {
		"label": "finished",
		"freight": food
	}