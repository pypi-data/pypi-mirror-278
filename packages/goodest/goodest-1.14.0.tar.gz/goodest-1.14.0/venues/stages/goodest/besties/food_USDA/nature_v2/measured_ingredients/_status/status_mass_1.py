
'''
	python3 status.proc.py besties/food_USDA/nature_v2/measured_ingredients/_status/status_mass_1.py
'''



import goodest.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import goodest.besties.food_USDA.examples as USDA_examples
	
import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2
from goodest.besties.food_USDA.nature_v2.measured_ingredients._ops.seek import seek_measured_ingredient

import goodest.mixes.insure.equalities as equalities

import rich

import json	

def check_1 ():
	walnuts_1882785 = USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	assertions_foundational.run (walnuts_1882785)
	
	measured_ingredients = food_USDA_nature_v2.create (
		walnuts_1882785,
		return_measured_ingredients_list = True
	)
	
	rich.print_json (data = {
		"measured ingredients": measured_ingredients
	})
	
	
	Potassium = seek_measured_ingredient ("Potassium, K", measured_ingredients)
	equalities.check ([
		[
			Potassium ["measures"] ["mass + mass equivalents"]["per package"][
				"grams"
			]["fraction string"],
			"97383/50000"
		],
		[
			Potassium ["measures"] ["mass + mass equivalents"]["per package"][
				"grams"
			]["decimal string"],
			"1.948"
		]
	], effect = "exception")
	
	Energy = seek_measured_ingredient ("Energy", measured_ingredients)
	equalities.check ([
		[
			Energy ["measures"] ["energy"]["per package"][
				"food calories"
			]["fraction string"],
			"154133/50"
		],
		[
			Energy ["measures"] ["energy"]["per package"][
				"food calories"
			]["decimal string"],
			"3082.660"
		]
	], effect = "exception")
	
	vitamin_d = seek_measured_ingredient ("Vitamin D (D2 + D3), International Units", measured_ingredients)
	
	assert (
		vitamin_d == 
		{
			"name": "Vitamin D (D2 + D3), International Units",
			"measures": {
				"biological activity": {
					"per package": {
						"listed": [
							"0.000",
							"IU"
						],
						"IU": {
							"decimal string": "0.000",
							"fraction string": "0"
						}
					}
				}
			}
		}
	
	)
	
	print (Potassium)
	
	
	
checks = {
	'check 1': check_1
}


