






'''
	python3 status.proc.py shows_v2/recipe_with_goals/_ops/formulate/_status_API/1_2_recipe/API_status_1.py
'''

#----
#
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
from goodest.shows_v2.recipe._ops.retrieve import retrieve_recipe
from goodest.shows_v2.recipe_with_goals._ops.formulate import formulate_recipe_with_goals
#
#
import json
from fractions import Fraction
from copy import deepcopy
import pathlib
from os.path import dirname, join, normpath
#
#
import rich
#
#----

def find_grams (measures):
	return Fraction (
		measures ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"]
	)
	
def add (path, data):
	this_directory = pathlib.Path (__file__).parent.resolve ()
	example_path = normpath (join (this_directory, path))
	FP = open (example_path, "w")
	FP.write (data)
	FP.close ()
	

def check_1 ():
	recipe_packet = retrieve_recipe ({
		"IDs_with_amounts": [
			{
				"DSLD_ID": "276336",
				"packages": 10
			},
			{
				"DSLD_ID": "214893",
				"packages": 20
			},
			{
				"FDC_ID": "2412474",
				"packages": 20
			},
			{
				"FDC_ID": "2642759",
				"packages": 20
			},
			{
				"FDC_ID": "2663758",
				"packages": 20
			},
			{
				"FDC_ID": "2664238",
				"packages": 80
			}
		]	
	})
	
	assert (len (recipe_packet ["not_added"]) == 0)
	
	recipe_with_goals_packet = formulate_recipe_with_goals ({
		"recipe": recipe_packet ["recipe"],
		"goal_region": "2"
	})

	add (
		"status_1.JSON", 
		json.dumps (recipe_with_goals_packet ["recipe"], indent = 4)
	)
	
	
	
checks = {
	"check 1": check_1
}