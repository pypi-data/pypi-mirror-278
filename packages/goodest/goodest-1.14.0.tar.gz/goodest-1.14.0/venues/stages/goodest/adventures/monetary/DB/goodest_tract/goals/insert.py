
'''
	from goodest.adventures.monetary.DB.goodest_tract.goals.insert import insert_goals_document
	insert_goals_document (
		collection = goodest_tract_DB ["goals"],
		document = {}
	)
'''

'''
	itinerary:
		https://www.mongodb.com/docs/manual/core/aggregation-pipeline/
		
		emblem = highest emblem number + 1
'''

from goodest.adventures.monetary.DB.goodest_tract.connect import connect_to_goodest_tract

from biotech.topics.show.variable import show_variable


def insert_goals_document (packet):
	document = packet ["document"]
	
	if ("add_emblem" in packet):
		add_emblem = packet ["add_emblem"]
	else:
		add_emblem = True

	[ driver, goodest_tract_DB ] = connect_to_goodest_tract ()

	collection = goodest_tract_DB ["goals"] 

	exception = ""
	proceeds = ""
	try:
		if (add_emblem):
			result = list (
				collection.aggregate ([
					{
						"$group": {
							"_id": None, 
							"max_emblem": {
								"$max": "$emblem"
							}
						}
					}
				])
			)
			emblem = result[0]['max_emblem'] + 1 if result else 1
						
			proceeds = collection.insert_one ({
				"nature": document,
				"emblem": emblem
			}, { "unique": True })
			
		else:
			proceeds = collection.insert_one (document)
	except Exception as E:
		show_variable ({
			"exception": str (E)
		})
	
	driver.close ()
	
	if (exception):
		raise Exception ("The goal was not added.");
	
	return proceeds;