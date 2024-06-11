




'''
	python3 status.proc.py shows/ingredient_scan_recipe/formulate/_status/status_supp/status_1.py
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
	supp_1 = supp_NIH_nature_v2.create (
		NIH_examples.retrieve ("other/chia_seeds_214893.JSON")
	)
	supp_2 = supp_NIH_nature_v2.create (
		NIH_examples.retrieve ("coated tablets/multivitamin_276336.JSON")
	)

	print (json.dumps (supp_1, indent = 4))

	supp_1_1 = deepcopy (supp_1)
	supp_2_1 = deepcopy (supp_2)
	
	supp_1_multiplier = 10
	supp_2_multiplier = 10

	recipe = formulate_recipe ({
		"natures_with_amounts": [
			[ supp_1, supp_1_multiplier ],
			[ supp_2, supp_2_multiplier ]
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
	
	#print (json.dumps (recipe, indent = 4))

	
checks = {
	"check 1": check_1
}