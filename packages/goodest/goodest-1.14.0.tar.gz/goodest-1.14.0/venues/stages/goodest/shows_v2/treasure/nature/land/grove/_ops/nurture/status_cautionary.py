





'''
	python3 status.proc.py shows_v2/treasure/nature/land/grove/_ops/nurture/status_cautionary.py
'''

#----
#
from goodest.shows_v2.treasure.nature.land.grove._ops.nurture import nurture_grove
from goodest.shows_v2.treasure.nature.land.grove._ops.seek import seek_ingredient_in_grove
#			
from biotech.topics.show.variable import show_variable
#
import json
#
#----

def check_1 ():
	grove = nurture_grove (
		collection = "cautionary_ingredients",
	)
	
	trans_fat = seek_ingredient_in_grove (
		grove = grove,
		for_each = lambda entry : True if "trans fat" in entry ["info"] ["names"] else False
	)
	
	assert (type (trans_fat) == dict), trans_fat
	assert ("trans fat" in trans_fat ["info"] ["names"])
	
	show_variable (f"trans fat: { trans_fat }")
	
	

checks = {
	'check 1': check_1
}