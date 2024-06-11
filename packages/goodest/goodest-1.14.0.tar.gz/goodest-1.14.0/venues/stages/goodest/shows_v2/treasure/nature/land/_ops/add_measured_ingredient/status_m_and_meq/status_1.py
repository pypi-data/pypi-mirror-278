

'''
	python3 status.proc.py shows_v2/treasure/nature/land/_ops/add_measured_ingredient/status_m_and_meq/status_1.py
'''

from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
from goodest.shows_v2.treasure.nature.land._ops.add_measured_ingredient import add_measured_ingredient
from goodest.shows_v2.treasure.nature.land._ops.develop import develop_land
	
import json	
	
def check_1 ():
	land = develop_land ({
		"collection": "essential_nutrients"
	})	

	add_measured_ingredient (
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

	print ("Potassium", json.dumps (land ["grove"], indent = 4))
	Potassium = seek_name_or_accepts (
		grove = land ["grove"],
		name_or_accepts = "potassium, k"
	)
	
	assert (
		Potassium ["natures"] ==
		[
			{
				"amount": "1",
				"source": {
					"name": "WALNUTS HALVES & PIECES, WALNUTS",
					"FDC ID": "1882785",
					"UPC": "099482434618",
					"DSLD ID": ""
				},
				"ingredient": {
					"name": "Potassium, K"
				},
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
		]
	)
	assert (
		Potassium ["measures"] ["mass + mass equivalents"] ==
		{
			"per recipe": {
				"grams": {
					"fraction string": "97383/50000",
					"scinote string": "1.9477e+0",
				}
			}
		}
	), Potassium ["measures"]
	
	assert (
		land ["measures"] ["mass + mass equivalents"] ==
		{
			"per recipe": {
				"grams": {
					"fraction string": "0"
				}
			}
		}
	), land ["measures"]


	return;
	
	
checks = {
	'check 1': check_1
}