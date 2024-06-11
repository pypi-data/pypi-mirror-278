
'''
	import goodest.adventures.monetary.DB.goodest_tract._land.insert_document as _land_insert_document
	_land_insert_document.smoothly (
		collection,
		document = {},
		
		add_region = True
	)
'''

'''
	itinerary:
		https://www.mongodb.com/docs/manual/core/aggregation-pipeline/
		
		region = highest region number + 1
'''

def smoothly (packet):
	document = packet ["document"]

	[ driver, goodest_tract_DB ] = connect_to_goodest_tract ()
	collection = goodest_tract_DB ["goals"]

	if (add_region):
		result = list (
			collection.aggregate ([
				{
					"$group": {
						"_id": None, 
						"max_region": {
							"$max": "$region"
						}
					}
				}
			])
		)
		region = result[0]['max_region'] + 1 if result else 1
		
		print ('region:', region)
		
		proceeds = collection.insert_one ({
			** document,
			"region": region
		})
		
	else:
		proceeds = collection.insert_one (document)
		
	driver.close ()
	
	return proceeds;
