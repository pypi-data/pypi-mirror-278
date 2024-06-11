







'''
	from goodest.adventures.monetary.DB.goodest_tract.goals.retrieve_one import retrieve_one_goal
	ingredient_doc = retrieve_one_goal ({
		"emblem": ""
	})
'''

'''
	objective:
		https://www.mongodb.com/docs/manual/core/aggregation-pipeline/
		region = highest region number + 1
'''
from goodest.adventures.monetary.DB.goodest_tract.connect import connect_to_goodest_tract
	
def retrieve_one_goal (packet = {}):
	[ driver, goodest_tract_DB ] = connect_to_goodest_tract ()
	
	found = goodest_tract_DB [ "goals" ].find_one ({
		"emblem": int (packet ["emblem"]) 
	}, {'_id': 0 })

	driver.close ()
	
	return found;
