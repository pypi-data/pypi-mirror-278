


'''
	python3 insurance.py besties/food_USDA/nature/measured_ingredient/_status/status_mass_1.py
'''
from goodest.besties.food_USDA.nature_v2._interpret.packageWeight import calc_package_weight
from goodest.besties.food_USDA.nature_v2.measures.form import calculate_form
from goodest.besties.food_USDA.nature_v2.measured_ingredients.measured_ingredient import build_measured_ingredient

import goodest.besties.food_USDA.examples as USDA_examples

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
	
	USDA_food_nutrient = {
		"nutrient": {
			"name": "Iron, Fe",
			"unitName": "mg"
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
	
	print ("measured_ingredient", json.dumps (measured_ingredient, indent = 4))

	assert (
		measured_ingredient ["measures"] ["mass + mass equivalents"] ["per package"] ["grams"] ["fraction string"],
		"1459357682252203941/56294995342131200000"
	)
	assert (
		measured_ingredient ["measures"] ["mass + mass equivalents"] ["per package"] ["grams"] ["decimal string"],
		"0.026"
	)
	assert (
		measured_ingredient ["measures"] ["mass + mass equivalents"] ["per package"] ["listed"],
		[ "25.923", "mg" ]
	)

	return;
	
	
checks = {
	'check 1': check_1
}