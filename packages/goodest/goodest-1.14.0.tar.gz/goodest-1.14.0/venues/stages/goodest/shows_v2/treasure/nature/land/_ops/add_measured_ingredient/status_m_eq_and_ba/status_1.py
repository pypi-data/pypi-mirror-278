
'''
	python3 status.proc.py shows_v2/treasure/nature/land/_ops/add_measured_ingredient/status_m_eq_and_ba/status_1.py

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
		
		amount = 10,
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
	
	add_measured_ingredient (
		land = land,
		
		amount = 10,
		source = {
			"name":	"WALNUTS HALVES & PIECES, WALNUTS",
			"FDC ID": "1882785",
			"UPC": "099482434618",
			"DSLD ID": ""
		},
		measured_ingredient = {
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

	Potassium = seek_name_or_accepts (
		grove = land ["grove"],
		name_or_accepts = "potassium, k"
	)
	assert (len (Potassium ["natures"]) == 1)
	assert (
		Potassium ["natures"][0] ==
		{
			"amount": "10",
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
	)
	
	
	assert (
		Potassium ["measures"]["mass + mass equivalents"] ==
		{
			"per recipe": {
				"grams": {
					"scinote string": "1.9477e+1",
					"fraction string": "97383/5000"
				}
			}
		}
	), Potassium ["measures"]["mass + mass equivalents"]


	Vitamin_D = seek_name_or_accepts (
		grove = land ["grove"],
		name_or_accepts = "Vitamin D (D2 + D3), International Units"
	)
	assert (len (Vitamin_D ["natures"]) == 1)
	assert (
		Vitamin_D ["natures"][0] ==
		{
			"amount": "10",
			"source": {
				"name": "WALNUTS HALVES & PIECES, WALNUTS",
				"FDC ID": "1882785",
				"UPC": "099482434618",
				"DSLD ID": ""
			},
			"ingredient": {
				"name": "Vitamin D (D2 + D3), International Units",
			},
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
	), Vitamin_D ["natures"]
	assert (
		Vitamin_D ["measures"]["biological activity"] ==
		{
			"per recipe": {
				"IU": {
					"scinote string": "0.0000e+0",
					"fraction string": "0"
				}
			}
		}
	), Vitamin_D ["measures"]["biological activity"]
	
	
	'''
		The land measures might not yet be updated.
	'''
	'''
	assert (
		land ["measures"] ["mass + mass equivalents"] ==
		{
			"per recipe": {
				"grams": {
					"scinote string": "0.0000e+0",
					"fraction string": "0"
				}
			}
		}
	), land ["measures"] ["mass + mass equivalents"]
	'''
	

	return;
	
	
checks = {
	'check 1': check_1
}