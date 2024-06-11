







'''
	python3 insurance.py shows/ingredient_scan_recipe/formulate/_status/status_food/status_3.py
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
import ships
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


	recipe = formulate_recipe ({
		"natures_with_amounts": [
			[ food_1, 1 ],
			[ food_2, 1 ]
		]
	})
	
	
	protein = seek_name_or_accepts (
		grove = recipe ["essential nutrients"] ["grove"],
		name_or_accepts = "protein"
	)
	
	'''
		grove measures: {
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						"fraction string": "102917049606837137521983/225179981368524800000"
					}
				}
			}
		}

		protein: {
			"measures": {
				"mass + mass equivalents": {
					"per recipe": {
						"grams": {
							"fraction string": "15056569382213862513/225179981368524800"
						}
					},
					"portion of grove": {
						"fraction string": "161898595507675941000/1106634942009001478731"
					}
				}
			}
		}
	'''
	
	'''
		str ((Fraction ("456528486851663599/7036874417766400") + Fraction ("89531560592125469/45035996273704960")) / Fraction ("102917049606837137521983/225179981368524800000"))
			= '161898595507675941000/1106634942009001478731'
	'''
	assert (
		protein ["measures"]["mass + mass equivalents"]["portion of grove"]["fraction string"] ==
		"161898595507675941000/1106634942009001478731"
	), protein
	
	ships.show ("grove measures:", recipe ["essential nutrients"] ["measures"])
	ships.show ("protein:", protein)
	
checks = {
	"check 1": check_1
}