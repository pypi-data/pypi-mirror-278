





'''
	python3 insurance.py shows/ingredient_scan_recipe/formulate/_status/status_food/status_2.py
'''


#----
#
import goodest.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import goodest.besties.food_USDA.examples as USDA_examples	
import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2
import goodest.mixes.insure.equality as equality
#
from goodest.shows_v2.recipe._ops.assertions.ingredient import ingredient_assertions
from goodest.shows_v2.recipe._ops.formulate import formulate_recipe
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts	
#
#
from copy import deepcopy
from fractions import Fraction
import json
#
#----

def find_grams (measures):
	return Fraction (
		measures ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"]
	)

def check_1 ():
	food_1 = food_USDA_nature_v2.create (
		USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	)
	food_2 = food_USDA_nature_v2.create (
		USDA_examples.retrieve ("branded/goodest_pizza_2672996.JSON")
	)

	food_1_1 = deepcopy (food_1)
	food_2_1 = deepcopy (food_2)

	food_1_mass_and_mass_eq_grams = Fraction ("47746738154613173415299/112589990684262400000")
	food_1_energy_food_calories = Fraction ("154133/50")
	food_1_multiplier = 10

	food_2_mass_and_mass_eq_grams = Fraction ("1484714659522158138277/45035996273704960000")
	food_2_energy_food_calories = Fraction ("2627/20")
	food_2_multiplier = 100
		
	assert (
		food_1 ["essential nutrients"] ["measures"] ==
		{
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						"fraction string": str (food_1_mass_and_mass_eq_grams),
						'scinote string': '4.2408e+2'
					}
				}
			},
			"energy": {
				"per recipe": {
					"food calories": {
						"fraction string": str (food_1_energy_food_calories),
						'scinote string': '3.0827e+3'
					}
				}
			}
		}
	), food_1 ["essential nutrients"] ["measures"]
	assert (
		food_2 ["essential nutrients"] ["measures"] ==
		{
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						'scinote string': '3.2967e+1',
						"fraction string": str (food_2_mass_and_mass_eq_grams)
					}
				}
			},
			"energy": {
				"per recipe": {
					"food calories": {
						'scinote string': '1.3135e+2',
						"fraction string": str (food_2_energy_food_calories)
					}
				}
			}
		}
	), food_2 ["essential nutrients"] ["measures"]


	recipe = formulate_recipe ({
		"natures_with_amounts": [
			[ food_1, food_1_multiplier ],
			[ food_2, food_2_multiplier ]
		]
	})
	assert (
		recipe ["essential nutrients"] ["measures"] ==
		{
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						"fraction string": str (
							(food_1_mass_and_mass_eq_grams * food_1_multiplier) +
							(food_2_mass_and_mass_eq_grams * food_2_multiplier)							
						),
						'scinote string': '7.5375e+3'
					}
				}
			},
			"energy": {
				"per recipe": {
					"food calories": {
						"fraction string": str (
							(food_1_energy_food_calories * food_1_multiplier) +
							(food_2_energy_food_calories * food_2_multiplier)							
						),
						'scinote string': '4.3962e+4'
					}
				}
			}
		}
	), recipe ["essential nutrients"] ["measures"]
	
	
	'''
	assert_ingredient ("protein")
	assert_ingredient ("carbohydrates")
	assert_ingredient ("Cholesterol")
	assert_ingredient ("Sodium, Na")
	'''
	
	ingredient_assertions (
		"carbohydrates",
		
		recipe,
		
		food_1_1,
		food_2_1,
		
		food_1_multiplier,
		food_2_multiplier,
		
		food_1,
		food_2
	)
	ingredient_assertions (
		"Cholesterol",
		
		recipe,
		
		food_1_1,
		food_2_1,
		
		food_1_multiplier,
		food_2_multiplier,
		
		food_1,
		food_2
	)
	ingredient_assertions (
		"protein",
		
		recipe,
		
		food_1_1,
		food_2_1,
		
		food_1_multiplier,
		food_2_multiplier,
		
		food_1,
		food_2
	)
	
checks = {
	"check 1": check_1
}