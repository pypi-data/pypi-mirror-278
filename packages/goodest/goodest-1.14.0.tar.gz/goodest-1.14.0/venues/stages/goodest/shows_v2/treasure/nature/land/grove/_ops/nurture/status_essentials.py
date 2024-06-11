





'''
	python3 status.proc.py shows_v2/treasure/nature/land/grove/_ops/nurture/status_essentials.py
'''

#----
#
from goodest.shows_v2.treasure.nature.land.grove._ops.nurture import nurture_grove
from goodest.shows_v2.treasure.nature.land.grove._ops.seek import seek_ingredient_in_grove
#
#
import json
#
#----

def check_1 ():
	grove = nurture_grove (
		collection = "essential_nutrients"
	)
	
	protein = seek_ingredient_in_grove (
		grove = grove,
		for_each = lambda entry : True if "protein" in entry ["info"] ["names"] else False
	)
	
	assert (type (protein) == dict), protein
	assert ("protein" in protein ["info"] ["names"])
	
	print ("protein:", protein)
	
	

checks = {
	'check 1': check_1
}