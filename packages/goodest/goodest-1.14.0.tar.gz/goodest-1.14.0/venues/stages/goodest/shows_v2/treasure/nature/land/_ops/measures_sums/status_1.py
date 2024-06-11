



'''
	python3 status.proc.py shows_v2/treasure/nature/land/_ops/measures_sums/status_1.py
'''

from goodest.shows_v2.treasure.nature.land._ops.develop import develop_land
from goodest.shows_v2.treasure.nature.land._ops.measures_sums import calc_measures_sums
	
def check_1 ():
	land = develop_land ({
		"collection": "essential_nutrients"
	})
	calc_measures_sums (
		land = land
	)

	return;
	
	
checks = {
	'it does raise an exception': check_1 
}