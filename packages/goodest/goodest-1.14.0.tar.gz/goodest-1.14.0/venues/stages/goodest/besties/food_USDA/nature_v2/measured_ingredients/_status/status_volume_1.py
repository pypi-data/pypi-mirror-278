
'''
	python3 insurance.py besties/food_USDA/nature/measured_ingredients_list/_status/status_volume_1.py
'''


import goodest.besties.food_USDA.examples as USDA_examples	

import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2
from goodest.besties.food_USDA.nature_v2.measured_ingredients._ops.seek import seek_measured_ingredient

import goodest.mixes.insure.equalities as equalities

import rich

'''
	creates list without raising an exception
'''
def check_1 ():
	measured_ingredients = food_USDA_nature_v2.create (
		USDA_examples.retrieve ("branded/beet_juice_2412474.JSON"),
		return_measured_ingredients_list = True
	)

	#rich.print_json (data = measured_ingredients)

	
checks = {
	'check 1': check_1
}


