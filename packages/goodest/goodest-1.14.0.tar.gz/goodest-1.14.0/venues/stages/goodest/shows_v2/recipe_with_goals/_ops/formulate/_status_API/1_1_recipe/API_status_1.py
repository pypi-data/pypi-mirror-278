


'''
	python3 status.proc.py shows_v2/recipe_with_goals/_ops/formulate/_status_API/1_1_recipe/API_status_1.py
'''

#----
#
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
from goodest.shows_v2.recipe._ops.retrieve import retrieve_recipe
from goodest.shows_v2.recipe_with_goals._ops.formulate import formulate_recipe_with_goals

#
#
import json
#
#
import rich
#
#----

def add (path, data):
	import pathlib
	from os.path import dirname, join, normpath
	
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
			}
		]	
	})
	
	assert (len (recipe_packet ["not_added"]) == 0)
	recipe_with_goals_packet = formulate_recipe_with_goals ({
		"recipe": recipe_packet ["recipe"],
		"goal_region": "2"
	})
	recipe = recipe_with_goals_packet ["recipe"]
	
	add (
		"status_1.JSON", 
		json.dumps (recipe, indent = 4)
	)
	
	
	vitamin_E = seek_name_or_accepts (
		grove = recipe ["essential nutrients"] ["grove"],
		name_or_accepts = "vitamin e"
	)
	rich.print_json (data = vitamin_E)
	assert (
		vitamin_E ["goal"] ["days of ingredient"] ["mass + mass equivalents"] ["per recipe"] ["fraction string"] == 
		"1800"
	), vitamin_E ["goal"]
	
	vitamin_B3 = seek_name_or_accepts (
		grove = recipe ["essential nutrients"] ["grove"],
		name_or_accepts = "vitamin b3"
	)
	rich.print_json (data = vitamin_B3)
	assert (
		vitamin_B3 ["goal"] ["days of ingredient"] ["mass + mass equivalents"] ["per recipe"] ["fraction string"] == 
		"5625/2"
	), vitamin_B3 ["goal"] ["days of ingredient"] ["mass + mass equivalents"] ["per recipe"] ["fraction string"]
	
checks = {
	'check 1': check_1
}