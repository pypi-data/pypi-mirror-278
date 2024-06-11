



'''	
	python3 status.proc.py shows_v2/recipe_with_goals/_ops/for_1_supp/_status/status_1.py
'''

from goodest.shows_v2.recipe_with_goals._ops.for_1_supp import formulate_recipe_with_goals_for_1_supp 
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts

import pathlib
from os.path import dirname, join, normpath
from goodest.mixes.drives.etch.bracket import etch_bracket
this_directory = pathlib.Path (__file__).parent.resolve ()


def check_1 ():

	'''
		276336
		8 95634 00002 7
	'''

	supp = formulate_recipe_with_goals_for_1_supp ({
		"supp": {
			"emblem": 2
		},
		"goal": 2
	})
	
	etch_bracket (normpath (join (this_directory, "status_1_supp.JSON")), supp)
	
	
	'''
		The math is not checked.
		However, the consitency against previous results is.
	
		 {
			"days of ingredient": {
				"mass + mass equivalents": {
					"per recipe": {
						"fraction string": "180",
						"decimal string": "180.000"
					}
				}
			}
		}
	'''
	vitamin_e = seek_name_or_accepts (
		grove = supp ["nature"] ["essential nutrients"] ["grove"],
		name_or_accepts = "vitamin e"
	)
	assert (
		vitamin_e ["goal"]["days of ingredient"]["mass + mass equivalents"]["per recipe"]["fraction string"] ==
		"180"
	)
	assert (
		vitamin_e ["goal"]["days of ingredient"]["mass + mass equivalents"]["per recipe"]["decimal string"] ==
		"180.000"
	)
	
checks = {
	'check 1': check_1
}