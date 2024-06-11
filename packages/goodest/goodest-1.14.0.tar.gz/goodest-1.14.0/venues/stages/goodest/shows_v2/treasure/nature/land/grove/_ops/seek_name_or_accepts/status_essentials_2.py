







'''
	python3 status.proc.py shows_v2/treasure/nature/land/grove/_ops/seek_name_or_accepts/status_essentials_2.py
'''

from goodest.shows_v2.treasure.nature.land.grove._ops.nurture import nurture_grove
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
		
		
def check_1 ():
	essential_nutrients_grove = nurture_grove ("essential_nutrients")
	
	Potassium = seek_name_or_accepts (
		grove = essential_nutrients_grove,
		name_or_accepts = "potassium, k"
	)
	
	print ("Potassium:", Potassium)
	
	assert (type (Potassium) == dict)
	assert ("potassium" in Potassium ["info"]["names"])

	return;
	
	
checks = {
	'check 1': check_1
}