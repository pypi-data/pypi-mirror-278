





'''
	python3 status.proc.py shows_v2/treasure/nature/land/grove/_ops/has_uniters/status_1.py
'''


#----
#
from goodest.shows_v2.treasure.nature.land._ops.add_measured_ingredient import add_measured_ingredient
from goodest.shows_v2.treasure.nature.land._ops.develop import develop_land
#	
from goodest.shows_v2.treasure.nature.land.grove._ops.has_uniters import has_uniters
#
#
import json
#
#----

def check_1 ():	
	land = develop_land ({
		"collection": "essential_nutrients"
	})
	grove = land ["grove"]

	add_measured_ingredient (
		land = land,
		
		amount = "1",
		source = {
			"name":	"",
			"FDC ID": "",
			"UPC": "",
			"DSLD ID": ""
		},
		measured_ingredient = {
			"name": "dietary fiber",
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

	unity = has_uniters (grove, return_problem = True)
	assert ("dietary fiber" in unity ["problem"]["info"]["names"]) 
	
checks = {
	'check 1': check_1
}