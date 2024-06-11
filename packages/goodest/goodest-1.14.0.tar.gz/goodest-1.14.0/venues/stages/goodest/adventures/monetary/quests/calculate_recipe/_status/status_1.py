






'''
	python3 status.proc.py adventures/monetary/quests/calculate_recipe/_status/status_1.py
'''


#----
#
from goodest.adventures.monetary.quests.calculate_recipe import calculate_recipe
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
	received_packet = calculate_recipe ({
		"IDs_with_amounts": [
			{
				"FDC_ID": "2025440",
				"packages": 10
			},
			{
				"DSLD_ID": "69439",
				"packages": 5
			}
		]	
	})
	
	recipe = received_packet ["recipe"]
	
	assert (len (received_packet ["not_added"]) == 0), [
		len (received_packet ["not_added"])
	]
	
	this_directory = pathlib.Path (__file__).parent.resolve ()
	the_path = normpath (join (this_directory, "status_1_recipe.JSON"))

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
	
checks = {
	"check 1": check_1
}

