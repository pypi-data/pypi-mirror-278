













'''
	python3 status.proc.py shows_v2/recipe_with_goals/_ops/formulate/_status/2_food/status_1.py
'''


#----
#
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
from goodest.shows_v2.recipe._ops.retrieve import retrieve_recipe
from goodest.shows_v2.recipe_with_goals._ops.formulate import formulate_recipe_with_goals
from goodest.shows_v2.recipe._ops.formulate import formulate_recipe
#
#
#	foods
#
import goodest.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import goodest.besties.food_USDA.examples as USDA_examples	
import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2
#
#
#	supps
#
import goodest.besties.supp_NIH.nature_v2 as supp_NIH_nature_v2
import goodest.besties.supp_NIH.examples as NIH_examples
import goodest.mixes.insure.equality as equality
#
#	
import rich
#
#
from fractions import Fraction
from copy import deepcopy
import json
#
#----

def find_grams (measures):
	return Fraction (
		measures ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"]
	)
	
def add (path, data):
	import pathlib
	from os.path import dirname, join, normpath
	this_directory = pathlib.Path (__file__).parent.resolve ()
	example_path = normpath (join (this_directory, path))
	FP = open (example_path, "w")
	FP.write (data)
	FP.close ()
	
def retrieve_supp (supp_path):
	return supp_NIH_nature_v2.create (
		NIH_examples.retrieve (supp_path) 
	)

def retrieve_food (food_path):
	return food_USDA_nature_v2.create (
		USDA_examples.retrieve (food_path)
	)

def check_1 ():
	recipe_packet = formulate_recipe_with_goals ({
		"recipe": formulate_recipe ({
			"natures_with_amounts": [
				[ retrieve_food ("branded/Gardein_f'sh_2663758.JSON"), 1 ]
			]	
		}),
		"goal_region": "2"
	})	

	recipe = recipe_packet ["recipe"]

	add (
		"status_1.JSON", 
		json.dumps (recipe, indent = 4)
	)



checks = {
	"check 1": check_1
}