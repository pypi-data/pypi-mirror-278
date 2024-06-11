




'''
	python3 status.proc.py shows_v2/treasure/nature/land/grove/_ops/seek_uniter/status_1.py
'''

import json
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_uniter import seek_uniter
from goodest.shows_v2.treasure.nature.land.grove._ops.nurture import nurture_grove
	

def check_1 ():	
	uniter = seek_uniter (
		grove = nurture_grove ("essential_nutrients"),
		name_or_accepts = "sugars, added"
	)
	assert ("sugars, total" in uniter ["info"]["names"])
	
	uniter = seek_uniter (
		grove = nurture_grove ("essential_nutrients"),
		name_or_accepts = "dietary fiber"
	)
	assert ("carbohydrates" in uniter ["info"]["names"])
	
def check_2 ():	
	uniter = seek_uniter (
		grove = nurture_grove ("essential_nutrients"),
		name_or_accepts = "calcium"
	)
		
	assert (uniter == None)	
	
checks = {
	'check 1': check_1,
	'check 2': check_2	
}