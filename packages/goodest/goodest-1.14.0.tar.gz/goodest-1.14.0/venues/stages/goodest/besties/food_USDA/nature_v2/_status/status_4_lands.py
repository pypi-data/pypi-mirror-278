
'''
	python3 status.proc.py besties/food_USDA/nature_v2/_status/status_4_lands.py
'''

#----
#
import goodest.mixes.insure.equality as equality
import goodest.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import goodest.besties.food_USDA.examples as USDA_examples
import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2
from goodest.besties.food_USDA.nature_v2.measured_ingredients._ops.seek import seek_measured_ingredient
from goodest._essence import retrieve_essence
#
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
#
#
from biotech.topics.show.variable import show_variable
import ships
#
#
import rich
#
#
import json		
#
#----

def check_1 ():
	walnuts_1882785 = USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	assertions_foundational.run (walnuts_1882785)
	
	nature = food_USDA_nature_v2.create (
		walnuts_1882785
	)
	
	land_essential_nutrients = nature ["essential nutrients"]
	
	'''
		essentials
	'''
	vitamin_D = seek_name_or_accepts (
		grove = nature ["essential nutrients"] ["grove"],
		name_or_accepts = "vitamin d"
	)
	assert (len (vitamin_D ["natures"]) == 1)
	
	
	'''
		cautionaries
	'''
	#show_variable (nature ["cautionary ingredients"])
	trans_fat = seek_name_or_accepts (
		grove = nature ["cautionary ingredients"] ["grove"],
		name_or_accepts = "trans fat"
	)
	assert (len (trans_fat ["natures"]) == 1)

	
checks = {
	'food nature_v2 land essentials': check_1
}



