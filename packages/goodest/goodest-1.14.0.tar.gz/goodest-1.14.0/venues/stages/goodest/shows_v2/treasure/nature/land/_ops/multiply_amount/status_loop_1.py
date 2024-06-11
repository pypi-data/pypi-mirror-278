

'''
	python3 status.proc.py shows_v2/treasure/nature/land/_ops/multiply_amount/status_loop_1.py
'''

#----
#
import goodest.besties.food_USDA.examples as USDA_examples	
import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2
import goodest.mixes.insure.equality as equality
#
from goodest.shows_v2.treasure.nature.land._ops.multiply_amount import multiply_land_amount
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
#
#
import json	
#
#----


def check_1 ():
	foods = [
		"branded/beet_juice_2412474.JSON",
		"branded/beet_juice_2642759.JSON",
		"branded/Gardein_f'sh_2663758.JSON",
		"branded/impossible_beef_2664238.JSON",
		"branded/goodest_pizza_2672996.JSON",	
		"branded/walnuts_1882785.JSON"
	]
	
	for food in foods:
		food_data = USDA_examples.retrieve (food)
		nature = food_USDA_nature_v2.create (food_data)
		
		multiply_land_amount (
			land = nature ["essential nutrients"],
			amount = 124892389
		)
		
		#print (json.dumps (nature ["essential nutrients"], indent = 4))
		
	
checks = {
	'check 1': check_1
}