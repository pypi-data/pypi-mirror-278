






'''
	python3 status.proc.py shows_v2/recipe/_status/status_empty/status_1.py
'''


#----
#
import goodest.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import goodest.besties.food_USDA.examples as USDA_examples	
import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2
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

def check_1 ():
	recipe_1 = formulate_recipe ({
		"natures_with_amounts": []
	})
	
	
	EN_measures = recipe_1 ["essential nutrients"] ["measures"]
	assert ("0" == EN_measures ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"])
	assert ("0" == EN_measures ["energy"] ["per recipe"] ["food calories"] ["fraction string"])
		
	CI_measures = recipe_1 ["cautionary ingredients"] ["measures"]
	assert ("0" == CI_measures ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"])
	assert ("0" == CI_measures ["energy"] ["per recipe"] ["food calories"] ["fraction string"])
	

	
	
	
checks = {
	"check 1": check_1
}