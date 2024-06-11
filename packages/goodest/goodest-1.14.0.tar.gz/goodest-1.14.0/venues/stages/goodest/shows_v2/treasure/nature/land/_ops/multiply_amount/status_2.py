


'''
	python3 status.proc.py shows_v2/treasure/nature/land/_ops/multiply_amount/status_2.py
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
from fractions import Fraction
import json	
#
#----


def check_1 ():
	nature = food_USDA_nature_v2.create (
		USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	)

	ingredient_scan = nature ["essential nutrients"];
	grove = ingredient_scan ["grove"]
	essential_nutrient_measures = ingredient_scan ["measures"]

	amount = 9;

	'''
		60.018288 = 1351491697361075527451/22517998136852480000
		131.35 = 2627/20
	'''
	mass_and_mass_eq_grams_per_package = Fraction ("47746738154613173415299/112589990684262400000")
	energy_food_calories_per_package = Fraction ("154133/50")
	
	assert (
		ingredient_scan ["measures"] ==
		{
			'mass + mass equivalents': {
				'per recipe': {
					'grams': {
						'scinote string': '4.2408e+2',
						'fraction string': str (mass_and_mass_eq_grams_per_package)
					}
				}
			}, 
			'energy': {
				'per recipe': {
					'food calories': {
						'scinote string': '3.0827e+3',
						'fraction string': str (energy_food_calories_per_package)
					}
				}
			}
		}
	), ingredient_scan ["measures"]

	#print (json.dumps (essential_nutrient_measures, indent = 4))
	#return;

	
	iron_amount_per_package = Fraction ("1461913475040736643/112589990684262400000")
	
	iron = seek_name_or_accepts (
		grove = grove,
		name_or_accepts = "iron"
	)
	assert (
		iron ["measures"] ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"] ==
		str (iron_amount_per_package)
	), iron


	multiply_land_amount (
		land = ingredient_scan,
		amount = amount
	)
	
	'''
		120.036576 = 1351491697361075527451/11258999068426240000
		262.7 = 2627/10
	'''
	assert (
		ingredient_scan ["measures"] ==
		{
			'mass + mass equivalents': {
				'per recipe': {
					'grams': {
						'scinote string': '4.2408e+2',
						'fraction string': str (mass_and_mass_eq_grams_per_package * amount)
					}
				}
			}, 
			'energy': {
				'per recipe': {
					'food calories': {
						'scinote string': '3.0827e+3',
						'fraction string': str (energy_food_calories_per_package * amount)
					}
				}
			}
		}
	), ingredient_scan ["measures"]

	
	iron = seek_name_or_accepts (
		grove = grove,
		name_or_accepts = "iron"
	)
	assert (
		iron ["measures"] ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"] ==
		str (iron_amount_per_package * 9)
	)
	
	print (json.dumps (iron, indent = 4))
	
	return;
	
checks = {
	'check 1': check_1
}