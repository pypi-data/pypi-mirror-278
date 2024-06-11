


'''
	python3 status.proc.py shows_v2/treasure/nature/land/_ops/multiply_amount/status_1.py
'''

#----
#
import goodest.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
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
	nature = food_USDA_nature_v2.create (
		USDA_examples.retrieve ("branded/goodest_pizza_2672996.JSON")
	)

	essential_nutrients = nature ["essential nutrients"];
	grove = essential_nutrients ["grove"]
	essential_nutrient_measures = essential_nutrients ["measures"]

	'''
		60.018288 = 1351491697361075527451/22517998136852480000
		131.35 = 2627/20
	'''
	assert (
		essential_nutrients ["measures"] ==
		{
			'mass + mass equivalents': {
				'per recipe': {
					'grams': {
						'scinote string': '3.2967e+1',
						'fraction string': '1484714659522158138277/45035996273704960000'
					}
				}
			}, 
			'energy': {
				'per recipe': {
					'food calories': {
						'scinote string': '1.3135e+2',
						'fraction string': '2627/20'
					}
				}
			}
		}
	), essential_nutrients ["measures"]


	iron = seek_name_or_accepts (
		grove = grove,
		name_or_accepts = "iron"
	)
	assert (
		iron ["measures"] ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"] ==
		"89531560592125469/45035996273704960000"
	)


	multiply_land_amount (
		land = essential_nutrients,
		amount = 2
	)
	
	'''
		120.036576 = 1351491697361075527451/11258999068426240000
		262.7 = 2627/10
	'''
	assert (
		essential_nutrients ["measures"] ==
		{
			'mass + mass equivalents': {
				'per recipe': {
					'grams': {
						'scinote string': '3.2967e+1',
						'fraction string': '1484714659522158138277/22517998136852480000'
					}
				}
			}, 
			'energy': {
				'per recipe': {
					'food calories': {
						'scinote string': '1.3135e+2',
						'fraction string': '2627/10'
					}
				}
			}
		}
	), essential_nutrients ["measures"]

	
	iron = seek_name_or_accepts (
		grove = grove,
		name_or_accepts = "iron"
	)
	assert (
		iron ["measures"] ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"] ==
		"89531560592125469/22517998136852480000"
	)
	
	print (json.dumps (iron, indent = 4))
	
	return;
	
checks = {
	'check 1': check_1
}