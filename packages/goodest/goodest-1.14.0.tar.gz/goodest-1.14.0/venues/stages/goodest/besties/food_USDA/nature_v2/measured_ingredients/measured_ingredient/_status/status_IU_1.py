


'''
	python3 insurance.py besties/food_USDA/nature/measured_ingredient/status_IU_1.py
'''
from goodest.besties.food_USDA.nature_v2._interpret.packageWeight import calc_package_weight
from goodest.besties.food_USDA.nature_v2.measures.form import calculate_form
from goodest.besties.food_USDA.nature_v2.measured_ingredients.measured_ingredient import build_measured_ingredient

import goodest.besties.food_USDA.examples as USDA_examples

from biotech.topics.show.variable import show_variable

import json

def check_1 ():
	#servings_per_package = "4.035714285714286"
	
	USDA_food = USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	mass_and_volume = calc_package_weight (USDA_food)
	form = calculate_form (
		servingSize = USDA_food ["servingSize"],
		servingSizeUnit = USDA_food ["servingSizeUnit"],
		mass_and_volume = mass_and_volume
	)
	
	'''
		These nutrient levels are actually faked.
		
		
		(454/100) * 5.71 = 25.9234
	'''
	USDA_food_nutrient = {
		"nutrient": {
			"name": "Vitamin D (D2 + D3), International Units",
			"unitName": "IU"
		},
		"amount": 5.71
    }
	USDA_label_nutrient = {
		"value": 1.6
    }

	measured_ingredient = build_measured_ingredient (
		USDA_food_nutrient,
		mass_and_volume,
		form
	)
	
	show_variable ({
		"measured_ingredient": measured_ingredient
	}, mode = "pprint")

	assert (
		measured_ingredient ["measures"] ["biological activity"] ["per package"] ["IU"] ["fraction string"] ==
		"1459357682252203941/56294995342131200"
	)
	assert (
		measured_ingredient ["measures"] ["biological activity"] ["per package"] ["IU"] ["decimal string"] ==
		"25.923"
	)
	assert (
		measured_ingredient ["measures"] ["biological activity"] ["per package"] ["listed"] ==
		[ "25.923", "IU" ]
	)

	return;
	
	
checks = {
	'check 1': check_1
}