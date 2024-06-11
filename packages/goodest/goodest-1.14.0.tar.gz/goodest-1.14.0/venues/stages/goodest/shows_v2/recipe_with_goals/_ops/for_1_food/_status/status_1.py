

'''	
	python3 status.proc.py shows_v2/recipe_with_goals/_ops/for_1_food/_status/status_1.py
'''

from goodest.shows_v2.recipe_with_goals._ops.for_1_food import formulate_recipe_with_goals_for_1_food
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts

import pathlib
from os.path import dirname, join, normpath
from goodest.mixes.drives.etch.bracket import etch_bracket
this_directory = pathlib.Path (__file__).parent.resolve ()


def check_1 ():
	food = formulate_recipe_with_goals_for_1_food ({
		"food": {
			"emblem": 4
		},
		"goal": 2
	})
	
	etch_bracket (normpath (join (this_directory, "status_1_food.JSON")), food)
	
	
	'''
		The math is not checked.
		However, the consitency against previous results is.
	
		{
			"days of ingredient": {
				"mass + mass equivalents": {
					"per recipe": {
						"fraction string": "113/400",
						"decimal string": "0.283"
					}
				}
			}
		}
	'''
	dietary_fiber = seek_name_or_accepts (
		grove = food ["nature"] ["essential nutrients"] ["grove"],
		name_or_accepts = "dietary fiber"
	)
	assert (
		dietary_fiber ["goal"]["days of ingredient"]["mass + mass equivalents"]["per recipe"]["fraction string"] ==
		"113/400"
	)
	assert (
		dietary_fiber ["goal"]["days of ingredient"]["mass + mass equivalents"]["per recipe"]["decimal string"] ==
		"0.283"
	)
	
checks = {
	'check 1': check_1
}