


#/
#
import law_dictionary
#
#
from goodest.adventures.monetary.DB.goodest_inventory.collect_meals.document.find import find_meal
from goodest.shows_v2.recipe_with_goals._ops.formulate import formulate_recipe_with_goals
from goodest.shows_v2.recipe_with_goals._ops.for_1_food import formulate_recipe_with_goals_for_1_food 
#
#\

def retrieve_meal_quest (packet):

	freight = packet ["freight"]
	
	report_freight = law_dictionary.check (
		return_obstacle_if_not_legit = True,
		allow_extra_fields = True,
		laws = {
			"filters": {
				"required": True,
				"type": dict
			}
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
	
	

	le_meal = {}

	if (type (goal) == int):
		#pass;
		'''
		food = formulate_recipe_with_goals_for_1_food ({
			"food": {
				"emblem": filters ["emblem"]
			},
			"goal": goal
		})
		'''
		
		le_meal = find_meal ({
			"filter": {
				"emblem": filters ["emblem"]
			}
		})
		
	else:
		
		le_meal = find_meal ({
			"filter": {
				"emblem": filters ["emblem"]
			}
		})
			
		'''
		food = find_food ({
			"filter": filters
		})
		'''

	
	
	
	return {
		"label": "finished",
		"freight": le_meal
	}