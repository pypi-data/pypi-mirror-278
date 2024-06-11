


'''
	python3 status.proc.py shows_v2/treasure/nature/land/grove/_ops/seek/status_essentials.py
'''

from goodest.shows_v2.treasure.nature.land.grove._ops.nurture import nurture_grove
from goodest.shows_v2.treasure.nature.land.grove._ops.seek import seek_ingredient_in_grove
		
def check_1 ():
	essential_nutrients_grove = nurture_grove ("essential_nutrients")
	
	sodium = seek_ingredient_in_grove (
		grove = essential_nutrients_grove,
		for_each = (
			lambda entry : True if (
				"sodium, na" in list (map (
					lambda name : name.lower (), 
					entry ["info"] ["names"]
				))
			) else False
		)
	)
	
	assert (type (sodium) == dict)

	return;
	
	
checks = {
	'check 1': check_1
}