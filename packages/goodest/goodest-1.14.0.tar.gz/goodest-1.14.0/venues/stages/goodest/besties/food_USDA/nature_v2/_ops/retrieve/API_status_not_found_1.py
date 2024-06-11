
'''
	python3 status.proc.py 
'''

#----
#
import json
#
#
from goodest.besties.food_USDA.nature_v2._ops.retrieve import retrieve_parsed_USDA_food
from goodest._essence import retrieve_essence
#
#----

def check_1 ():
	essence = retrieve_essence ()
	API_USDA_ellipse = essence ['USDA'] ['food']

	out_packet = retrieve_parsed_USDA_food ({
		"USDA API Pass": API_USDA_ellipse,
		"FDC_ID": "1"
	});
	
	assert ("anomaly" in out_packet), out_packet
	assert (out_packet ["anomaly"] == "The USDA API could not find that FDC_ID."), [
		out_packet ["anomaly"]
	]
	
checks = {
	"not found": check_1
}