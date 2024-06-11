

'''
	from goodest.besties.food_USDA.nature_v2._interpret.packageWeight import calc_package_weight
	calc_package_weight ()
'''



'''
	possibilities:
		"quantity per package": {
			"system international": {
				"grams float": "113.0",
				"grams fraction": "113/1",
				"grams e note": "113.00e0",
				"grams base 10": "113.00 * (10^0)"
			},
			"us customary": {
				"pounds float": "0.25"
			}
		}
'''

from .interpret import interpret_amount
from .assertions import establish_assertions

import goodest.measures.number.decimal.reduce as reduce_decimal
	
from fractions import Fraction

def calc_package_weight (usda_food_data):
	assert ("packageWeight" in usda_food_data)
	
	proceeds = {}
	
	interpretations = interpret_amount (usda_food_data ["packageWeight"])
	calculated = interpretations.calculated;

	if ("liters" in calculated):
		proceeds ["volume"] = {
			"ascertained": True,
			"per package": {
				"liters": {
					"fraction string": calculated ["liters"],
					"decimal string": reduce_decimal.start (
						calculated ["liters"],
						partial_size = 2
					)
				}
			}
		}
	else:
		proceeds ["volume"] = {
			"ascertained": False,
			"per package": {
				"liters": {
					"fraction string": "?",
					"decimal string": "?"
				}
			}
		}
		
	if ("grams" in calculated):
		proceeds ["mass"] = {
			"ascertained": True,
			"per package": {
				"grams": {
					"fraction string": calculated ["grams"],
					"decimal string": reduce_decimal.start (
						calculated ["grams"],
						partial_size = 2
					)
				}
			}
		}

	else:
		proceeds ["mass"] = {
			"ascertained": False,
			"per package": {
				"grams": {
					"fraction string": "?",
					"decimal string": "?"
				}
			}
		}
	
	establish_assertions (proceeds)

	return proceeds