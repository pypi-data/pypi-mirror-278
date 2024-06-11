






'''
	python3 status.proc.py shows_v2/recipe/_ops/retrieve/_status/API_status_1.py
'''


#----
#
from goodest.shows_v2.recipe._ops.retrieve import retrieve_recipe
#
#
from copy import deepcopy
from fractions import Fraction
import json
#
#----

def check_1 ():
	received_packet = retrieve_recipe ({
		"IDs_with_amounts": [
			{
				"FDC_ID": "2453050",
				"packages": 10
			},
			{
				"FDC_ID": "2138734",
				"packages": 5
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
	
	
checks = {
	"check 1": check_1
}