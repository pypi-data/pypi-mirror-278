


'''
	{
		"freight": {
			"goal": 2,
			"goods": [
				{
					"emblem": 4,
					"FDC_ID": 2677998,
					"kind": "food",
					"packages": 3
				},
				{
					"emblem": 29,
					"FDC_ID": 2390911,
					"kind": "food",
					"packages": 3
				}
			]
		}
	}
'''

#----
#
from goodest.adventures.monetary.DB.goodest_tract.goals.retrieve import retrieve_goals
from goodest.shows_v2.recipe._ops.retrieve import retrieve_recipe
from goodest.adventures.monetary.quests.calculate_recipe import calculate_recipe
from goodest.shows_v2.recipe_with_goals._ops.formulate import formulate_recipe_with_goals
#
#
import law_dictionary
#
#----


def retrieve_recipe_quest (packet):
	freight = packet ["freight"]

	goal = freight ["goal"]
	goods = freight ["goods"]
	
	recipe_packet = calculate_recipe ({
		"IDs_with_amounts": goods	
	})
	assert (len (recipe_packet ["not_added"]) == 0)
	
	print ("""
	
		
		built recipe packet
	
	
	""")
	
	if (type (goal) != int):
		return {
			"label": "finished",
			"freight": recipe_packet ["recipe"]
		}
	
	recipe_with_goals_packet = formulate_recipe_with_goals ({
		"recipe": recipe_packet ["recipe"],
		"goal_region": "2"
	})
	

	return {
		"label": "finished",
		"freight": recipe_with_goals_packet ["recipe"]
	}