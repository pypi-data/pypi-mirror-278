



'''
	python3 status.proc.py shows_v2/recipe/_status/status_foods_and_supps/status_1.py
'''


#----
#
import goodest.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import goodest.besties.food_USDA.examples as USDA_examples	
import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2
#
import goodest.besties.supp_NIH.nature_v2 as supp_NIH_nature_v2
import goodest.besties.supp_NIH.examples as NIH_examples
#
import goodest.mixes.insure.equality as equality
#
from goodest.shows_v2.recipe._ops.formulate import formulate_recipe
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts	
#
#
from copy import deepcopy
from fractions import Fraction
import json
#
#----


def find_grams (measures):
	return Fraction (
		measures ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"]
	)
	

def check_1 ():
	def retrieve_supp (supp_path):
		return supp_NIH_nature_v2.create (
			NIH_examples.retrieve (supp_path) 
		)
	
	def retrieve_food (food_path):
		return food_USDA_nature_v2.create (
			USDA_examples.retrieve (food_path)
		)
	
	print (json.dumps (retrieve_food ("branded/beet_juice_2412474.JSON"), indent = 4))
	
	recipe = formulate_recipe ({
		"natures_with_amounts": [
			[ retrieve_supp ("coated tablets/multivitamin_276336.JSON"), 10 ],
			[ retrieve_supp ("other/chia_seeds_214893.JSON"), 20 ],
			[ retrieve_food ("branded/beet_juice_2412474.JSON"), 20 ],
			[ retrieve_food ("branded/beet_juice_2642759.JSON"), 20 ],
			[ retrieve_food ("branded/Gardein_f'sh_2663758.JSON"), 20 ],
			[ retrieve_food ("branded/impossible_beef_2664238.JSON"), 80 ],
		]
	})
	
	def add (path, data):
		import pathlib
		from os.path import dirname, join, normpath
		this_directory = pathlib.Path (__file__).parent.resolve ()
		example_path = normpath (join (this_directory, path))
		FP = open (example_path, "w")
		FP.write (data)
		FP.close ()
		
	add ("status_1.JSON", json.dumps (recipe, indent = 4))
	
	assert (len (recipe ["essential nutrients"] ["natures"]) == 6)
	

	
checks = {
	"check 1": check_1
}