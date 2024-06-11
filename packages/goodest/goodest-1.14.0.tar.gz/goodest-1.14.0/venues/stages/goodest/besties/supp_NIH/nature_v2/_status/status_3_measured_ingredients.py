



'''
	python3 status.proc.py besties/supp_NIH/nature_v2/_status/status_3_measured_ingredients.py
'''

#----
#

#
import goodest.besties.supp_NIH.nature_v2 as supp_NIH_nature_v2
import goodest.besties.supp_NIH.examples as NIH_examples
from goodest.besties.supp_NIH.nature_v2.measured_ingredients._ops.seek_name import seek_measure_ingredient_by_name
#
#
import rich
#
#
import json
import pathlib
from os.path import dirname, join, normpath
#
#----

def check_1 ():	
	supp_1 = supp_NIH_nature_v2.create (
		NIH_examples.retrieve ("tablets/multivitamin_249664.JSON")
	)
	
	def add (path, data):
		this_directory = pathlib.Path (__file__).parent.resolve ()
		example_path = normpath (join (this_directory, path))
		FP = open (example_path, "w")
		FP.write (data)
		FP.close ()
		
	add ("multivitamin_249664.JSON", json.dumps (supp_1, indent = 4))
	
	rich.print_json (data = {
		"supp_1:": supp_1
	})
	
	measured_ingredients = supp_1 ["measured ingredients"]
	Vitamin_E = seek_measure_ingredient_by_name (
		measured_ingredients,
		name = "Vitamin E"
	)
	
	assert (Vitamin_E == {
		"name": "Vitamin E",
		"alternate names": [],
		"measures": {
			"biological activity": {
				"per package": {
					"listed operator": "=",
					"listed": [
						"50.000",
						"IU"
					],
					"IU": {
						"decimal string": "50.000",
						"fraction string": "50"
					}
				}
			}
		},
		"listed measure": {
			"amount": {
				"fraction string": "50",
				"decimal string": "50.000"
			},
			"unit kind": "biological activity",
			"unit": "IU",
			"operator": "="
		},
		"unites": []
	})
	
	return;
	
checks = {
	"check 1": check_1
}