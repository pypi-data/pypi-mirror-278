






'''
	python3 status.proc.py adventures/monetary/quests/meals/statistics/_status/status_1.py
'''


#----
#
from goodest.adventures.monetary.quests.meals.statistics import formulate_meal_statistics
from goodest.mixes.drives.etch.bracket import etch_bracket
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
#
#
from copy import deepcopy
from fractions import Fraction
import json
import pathlib
from os.path import dirname, join, normpath
#
#----

def check_1 ():
	'''
		protein:
			((2 / 425.00) * 2.2865e+1) + ((1 / 2041.17) * 1.7758e+2) = 0.19459912305197508
	'''
	meal_statistics = formulate_meal_statistics ({
		"IDs_with_amounts": [
			{
				"FDC_ID": "2471166",
				"grams": 1
			},
			{
				"FDC_ID": "2425001",
				"grams": 2
			}
		]	
	})
	
	recipe = meal_statistics ["recipe"]
	
	assert (len (meal_statistics ["not_added"]) == 0), [
		len (meal_statistics ["not_added"])
	]
	
	this_directory = pathlib.Path (__file__).parent.resolve ()
	the_path = normpath (join (this_directory, "status_2_recipe.JSON"))

	etch_bracket (the_path, recipe)
	
	'''
		{
			"info": {
				"includes": [],
				"names": [
					"cholesterol"
				],
				"region": 12
			},
			"measures": {
				"mass + mass equivalents": {
					"per recipe": {
						"grams": {
							"fraction string": "0",
							"scinote string": "0.0000e+0"
						}
					},
					"portion of grove": {
						"fraction string": "0",
						"scinote percentage string": "0.0000e+0"
					}
				}
			},
			"natures": [
				{
					"amount": "10",
					"source": {
						"name": "ORGANIC SOY BEANS",
						"FDC ID": "2025440",
						"UPC": "074873163285",
						"DSLD ID": ""
					},
					"ingredient": {
						"name": "Cholesterol"
					},
					"measures": {
						"mass + mass equivalents": {
							"per package": {
								"listed": [
									"0.000",
									"mg"
								],
								"grams": {
									"scinote string": "0.0000e+0",
									"decimal string": "0.000",
									"fraction string": "0"
								}
							}
						}
					}
				}
			],
			"unites": []
		}
	'''
	cholesterol = seek_name_or_accepts (
		grove = recipe ["essential nutrients"] ["grove"],
		name_or_accepts = "cholesterol"
	)
	assert (
		cholesterol ["measures"] == {
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						"fraction string": "0",
						"scinote string": "0.0000e+0"
					}
				},
				"portion of grove": {
					"fraction string": "0",
					"scinote percentage string": "0.0000e+0"
				}
			}
		}
	), cholesterol
	
	protein = seek_name_or_accepts (
		grove = recipe ["essential nutrients"] ["grove"],
		name_or_accepts = "protein"
	)
	assert (
		protein ["measures"] == {
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						"fraction string": "10955006093578731/56294995342131200",
						"scinote string": "1.9460e-1"
					}
				},
				"portion of grove": {
					"fraction string": "2738751523394682750000/18603305522305598844949",
					"scinote percentage string": "1.4722e+1"
				}
			}
		}
	), protein
	
checks = {
	"check 1 (protein math was checked)": check_1
}

