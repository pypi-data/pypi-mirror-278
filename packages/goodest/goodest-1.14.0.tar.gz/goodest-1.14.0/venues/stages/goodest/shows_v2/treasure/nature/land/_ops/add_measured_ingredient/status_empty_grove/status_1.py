

'''
	python3 status.proc.py shows_v2/treasure/nature/land/_ops/add_measured_ingredient/status_empty_grove/status_1.py
'''

from goodest.shows_v2.treasure.nature.land._ops.add_measured_ingredient import add_measured_ingredient
from goodest.shows_v2.treasure.nature.land._ops.develop import develop_land
	
import json	
	
def check_1 ():
	land = develop_land ({
		"collection": "essential_nutrients"
	})		
	land ["grove"] = []

	added = add_measured_ingredient (
		land = land,
		
		amount = "1",
		source = {
			"name":	"WALNUTS HALVES & PIECES, WALNUTS",
			"FDC ID": "1882785",
			"UPC": "099482434618",
			"DSLD ID": ""
		},
		measured_ingredient = {
			"name": "Potassium, K",
			"measures": {
				"mass + mass equivalents": {
					"per package": {
						"listed": [
							"1947.660",
							"mg"
						],
						"grams": {
							"decimal string": "1.948",
							"fraction string": "97383/50000"
						}
					}
				}
			}
		}
	)
	
	assert (added == False)
		
	print (land ["grove"])
	


	return;
	
	
checks = {
	'check 1': check_1
}