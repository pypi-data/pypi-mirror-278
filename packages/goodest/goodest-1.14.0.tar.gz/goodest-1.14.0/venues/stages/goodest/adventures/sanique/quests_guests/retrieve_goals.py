
'''
	{
		"freight": {
			"filters": {
				"include": {
					"food": true,
					"supp": true
				},
				"limit": 25,
				"string": ""
			}
		}
	}
'''

#----
#
from goodest.adventures.monetary.DB.goodest_tract.goals.retrieve import retrieve_goals
	
#
#
import law_dictionary
#
#----


def retrieve_goals_quest (packet):
	goals = retrieve_goals ({})

	
	return {
		"label": "finished",
		"freight": goals
	}