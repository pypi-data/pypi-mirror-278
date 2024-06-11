





'''
	python3 status.proc.py shows_v2/treasure/nature/land/grove/_ops/seek_name_or_accepts/status_essentials_1.py
'''

from goodest.shows_v2.treasure.nature.land.grove._ops.nurture import nurture_grove
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
		
		
def check_1 ():
	essential_nutrients_grove = nurture_grove ("essential_nutrients")
	
	B6 = seek_name_or_accepts (
		grove = essential_nutrients_grove,
		name_or_accepts = "pyridoxine"
	)
	
	print ("B6:", B6)
	
	assert (type (B6) == dict)
	assert ("pyridoxine" in B6 ["info"]["accepts"])
	assert ("Vitamin B6" in B6 ["info"]["names"])

	return;
	
	
checks = {
	'check 1': check_1
}