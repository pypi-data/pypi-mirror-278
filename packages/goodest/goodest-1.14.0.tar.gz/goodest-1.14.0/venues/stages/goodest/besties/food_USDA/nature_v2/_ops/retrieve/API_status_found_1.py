


'''
	python3 status.proc.py 
'''

#----
#
from goodest.besties.food_USDA.nature_v2._ops.retrieve import retrieve_parsed_USDA_food
import goodest.shows_v2.treasure.nature._assertions as natures_v2_assertions
	
#
from goodest._essence import retrieve_essence
#
#
import rich
#
#
import json
#
#----

def check_1 ():
	essence = retrieve_essence ()
	API_USDA_ellipse = essence ['USDA'] ['food']

	out_packet = retrieve_parsed_USDA_food ({
		"USDA API Pass": API_USDA_ellipse,
		"FDC_ID": "2642759"
	});
		
	natures_v2_assertions.run (out_packet)
	
checks = {
	"not found": check_1
}