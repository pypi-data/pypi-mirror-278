










'''
	from goodest.adventures.monetary.DB.goodest_tract.goals.retrieve import retrieve_goals
	ingredient_doc = retrieve_goal ({})
'''

'''
	objective:
		https://www.mongodb.com/docs/manual/core/aggregation-pipeline/
		region = highest region number + 1
'''
from goodest.adventures.monetary.DB.goodest_tract.connect import connect_to_goodest_tract
	
def retrieve_goals (packet = {}):
	[ driver, goodest_tract_DB ] = connect_to_goodest_tract ()
	
	
	found = []
	documents = goodest_tract_DB [ "goals" ].find ({}, {'_id': 0 })
	for document in documents:
		if ("nature" in document):
			found.append (document)

	driver.close ()
	
	return found;
