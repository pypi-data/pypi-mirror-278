







'''
	python3 insurance.py "besties/food_USDA/nature/form/status_mass_1.py"
'''

import goodest.besties.food_USDA.examples as USDA_examples

from goodest.besties.food_USDA.nature_v2._interpret.packageWeight import calc_package_weight
from goodest.besties.food_USDA.nature_v2.measures.form import calculate_form

import json

def print_dict (dictionary):
	print (json.dumps (dictionary, indent = 4))

def check_1 ():
	USDA_food_data = USDA_examples.retrieve ("branded/beet_juice_2412474.JSON")
	mass_and_volume = calc_package_weight (USDA_food_data)
	
	form = calculate_form (
		servingSize = USDA_food_data ["servingSize"],
		servingSizeUnit = USDA_food_data ["servingSizeUnit"],
		mass_and_volume = mass_and_volume
	)
	
	print_dict (form)

	assert (
		form ==
		{
			"unit": "liter",
			"amount": "473/1000",
			"servings": {
				"listed": {
					"serving size amount": "240",
					"serving size unit": "ml"
				},
				"calculated": {
					"serving size amount": "6/25",
					"servings per package": "473/240",
					"foodNutrient per package multiplier": "473/100",
					"labelNutrient per package multiplier": "473/240"
				}
			}
		}
	)
	
checks = {
	"check 1": check_1
}