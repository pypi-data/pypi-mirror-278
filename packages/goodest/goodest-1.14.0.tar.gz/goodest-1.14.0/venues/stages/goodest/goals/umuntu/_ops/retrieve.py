
'''
	from goodest.goals.umuntu._ops.retrieve import retrieve_umutu_goal
	goal = retrieve_umutu_goal ({
		"region": region
	})
'''

from goodest.adventures.monetary.DB.goodest_tract.goals.retrieve_one import retrieve_one_goal

def retrieve_umutu_goal (packet):
	ingredient_doc = retrieve_one_goal ({
		"region": packet ["region"]
	})
	
	return ingredient_doc