








'''
	python3 status.proc.py shows_v2/treasure/nature/land/measures/merge/status_3.py
'''

#----
#
from goodest.shows_v2.treasure.nature.land.measures.merge import merge_land_measures 
#
#
import json	
#
#----

def empty_aggregate_measures ():
	aggregate_measures = {}
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
						"fraction string": "2000"
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
						"fraction string": "4000",
						'scinote string': '4.0000e+3'
					}
				}
			},
			"energy": {
				"per recipe": {
					"food calories": {
						"fraction string": "2000",
						'scinote string': '2.0000e+3'
					}
				}
			}
		}
	), aggregate_measures

checks = {
	'empty_aggregate_measures': empty_aggregate_measures
}