

'''
	from goodest.shows_v2.recipe._ops.retrieve import retrieve_recipe
	from goodest.shows_v2.recipe_with_goals._ops.formulate import formulate_recipe_with_goals
	
	recipe_packet = retrieve_recipe ({
		"IDs_with_amounts": [
			{
				"FDC_ID": "",
				"packages": 10
			},
			{
				"FDC_ID": "",
				"packages": 5
			},
			{
				"DSLD_ID": "",
				"packages": 5
			}
		]	
	})
	
	assert (len (recipe_packet ["not_added"]) == 0)
'''

'''
	recipe_with_goals_packet = formulate_recipe_with_goals ({
		"recipe": recipe_packet ["recipe"],
		"goal_region": "2"
	})
	
	recipe = recipe_with_goals_packet ["recipe"]
'''

'''
	The estimate:
		This adds the goals to recipe.
		
		Most likely, it doesn't delete anything.
'''



#----
#
from goodest.shows_v2.recipe._ops.retrieve import retrieve_recipe
#
from .modules.add_goals import add_goals
#
#----


def formulate_recipe_with_goals (packet):

	'''
		step zero: retrieve the recipe without the goals
	'''
	recipe = packet ["recipe"]
	
	if ("goal_region" in packet):	
		goal_region = packet ["goal_region"]
	else:
		goal_region = ""

	if (type (goal_region) == int):
		goal_region = str (goal_region)


	'''
		step 1: access fields of the recipe
	'''
	essential_nutrients = recipe ["essential nutrients"]
	essential_nutrients_grove = essential_nutrients ["grove"]
	cautionary_ingredients = recipe ["cautionary ingredients"]


	''' 
		step 2: 
			If a goal is not asked about, then return the recipe
			without goals.
	'''
	if (
		(type (goal_region) != str) or
		(type (goal_region) == str and len (goal_region) == 0) 
	):
		return {
			"recipe": recipe,
			"note": "goal ingredients not found"
		};

	''' 
		step 3: 
			Add the goals to the essential_nutrients grove 
			of the recipe.
	'''
	add_goals ({
		"recipe": recipe,
		"essential_nutrients_grove": essential_nutrients_grove,
		"goal_region": goal_region,
		"records": 1
	})

	return {
		"recipe": recipe,
		"note": "goal ingredients not found"
	};