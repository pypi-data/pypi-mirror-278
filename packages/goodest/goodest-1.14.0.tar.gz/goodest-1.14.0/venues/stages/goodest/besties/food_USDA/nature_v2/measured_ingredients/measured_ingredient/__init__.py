
'''
	from goodest.besties.food_USDA.nature_v2.measured_ingredients.measured_ingredient import build_measured_ingredient
	build_measured_ingredient ()
'''

'''
	calculating:
		"mass per package" or "equivalent mass per package"
		
		mass_per_package = nutrient_amount * (100) 
'''

import goodest.measures._interpret.unit_kind
import goodest.measures.number.decimal.reduce as reduce_decimal

from .amount import calc_amount

from fractions import Fraction

'''
	grams or ml:
		https://fdc.nal.usda.gov/fdc-app.html#/food-details/2412474/nutrients
		https://fdc.nal.usda.gov/fdc-app.html#/food-details/1960255/nutrients		
'''

def build_measured_ingredient (
	USDA_food_nutrient,
	mass_and_volume,
	form,

	USDA_label_nutrient = {},
	records = 1
):
	measured_ingredient = {
		"name": USDA_food_nutrient ["nutrient"] ["name"],
		"measures": {}
	}
	
	'''
		
	'''
	measures = calc_amount (
		USDA_food_nutrient,
		mass_and_volume,
		form,

		USDA_label_nutrient = {},
		records = records
	)
	
	if ("mass + mass equivalents" in measures):
		measured_ingredient ["measures"] ["mass + mass equivalents"] = (
			measures ["mass + mass equivalents"]
		)
	
	if ("biological activity" in measures):
		measured_ingredient ["measures"] ["biological activity"] = (
			measures ["biological activity"]
		)
		
	if ("energy" in measures):
		measured_ingredient ["measures"] ["energy"] = (
			measures ["energy"]
		)

	return measured_ingredient