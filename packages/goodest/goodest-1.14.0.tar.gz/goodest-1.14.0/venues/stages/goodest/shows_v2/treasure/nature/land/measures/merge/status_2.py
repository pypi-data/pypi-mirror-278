








'''
	python3 status.proc.py shows_v2/treasure/nature/land/measures/merge/status_2.py
'''

#----
#
from goodest.shows_v2.treasure.nature.land.measures.merge import merge_land_measures 
#
#
import json	
#
#----

def check_1 ():
	aggregate_measures = {
		"mass + mass equivalents": {
			"per recipe": {
				"grams": {
					"fraction string": "1000"
				}
			}
		},
		"energy": {
			"per recipe": {
				"food calories": {
					"fraction string": "2000"
				}
			}
		}
	}
	
	new_measures = {
		"mass + mass equivalents": {
			"per recipe": {
				"grams": {
					"fraction string": "4000"
				}
			}
		},
		"energy": {
			"per recipe": {
				"food calories": {
					"fraction string": "1"
				}
			}
		}
	}
	
	merge_land_measures (
		aggregate_measures,
		new_measures
	)

	assert (
		aggregate_measures == 
		{
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						"fraction string": "5000",
						'scinote string': '5.0000e+3'
					}
				}
			},
			"energy": {
				"per recipe": {
					"food calories": {
						"fraction string": "2001",
						'scinote string': '2.0010e+3'
					}
				}
			}
		}
	), aggregate_measures

checks = {
	'check 1': check_1
}