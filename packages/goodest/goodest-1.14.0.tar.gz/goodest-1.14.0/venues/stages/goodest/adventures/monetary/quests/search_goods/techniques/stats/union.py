

'''
class aggregate:
	def __init__ (
		DB = None,
		sort_direction = None,
		
		treasures = [],
		
		include_food = None,
		include_supp = None
	):
		return;
'''


'''
	from O2.mongo.goodest_DB.treasure.scan_3.techniques.stats.union import scan_3_union
	scan_3_union.aggregate ()
'''

'''
	https://stackoverflow.com/questions/77688190/is-there-a-mongo-operation-for-getting-the-count-of-documents-in-a-sorted-and-o
'''

def unify_union (
	include_food = None,
	include_supp = None
):
	if (include_food and include_supp):
		mods = [{ 
		   "$set": { 
			   "food_emblem": "$emblem" 
			} 
		},
		{ 
		   "$unionWith": { 
			   "coll": "supp",
			   "pipeline": [{ 
				   "$set": { 
					   "supp_emblem": "$emblem" 
					} 
				}] 
			}
		}]
	elif (include_food and not include_supp):
		mods = [{ 
		   "$set": { 
			   "food_emblem": "$emblem" 
			} 
		}]
	elif (include_supp and not include_food):
		mods = [{ 
		   "$set": { 
			   "supp_emblem": "$emblem" 
			} 
		}]
	else:
		mods = []
		
	return mods;

def aggregate (
	DB = None,
	
	# -1 or 1
	sort_direction = None,
	
	treasures = [],
	
	include_food = None,
	include_supp = None
):
	mods = unify_union (
		include_food = include_food,
		include_supp = include_supp
	)
	
	matches = []
	for treasure in treasures:
		if (treasure ["kind"] == "food"):	
			emblem_name = "food_emblem"
		else:
			emblem_name = "supp_emblem"
		
		matches.append ({
			"$and": [{
				"lower_case_name": {
					"$eq": treasure ["name"].lower ()
				},
				emblem_name: {
					"$eq": treasure ["emblem"]
				}
			}]
		})

	proceeds = DB.food.aggregate ([
		* mods,		
		
		{
			"$match": {
				"$and": [{
					"nature.identity.name": {
						"$exists": True
					},
					"emblem": {
						"$exists": True
					}
				}]
			}
		},
		{
			"$addFields": {
				"lower_case_name": { 
					"$toLower": "$nature.identity.name" 
				}
			}
		},
		{  
			"$sort": { 
				"lower_case_name": sort_direction,
				"food_emblem": sort_direction,
				"supp_emblem": sort_direction
			}
		},
		
		{
			"$setWindowFields": {
				"partitionBy": None,
				"sortBy": { 
					"lower_case_name": sort_direction,
					"food_emblem": sort_direction,
					"supp_emblem": sort_direction
				},
				"output": {
					"stats.before": {
						#
						#	This adds 1 for each document in the window
						#
						"$sum": 1,
						"window": {
							#
							#	from the first document in the 
							#	window to 1 before the current document
							#
							"documents": [ "unbounded", -1 ]
						}
					},
					"stats.after": {
						#
						#	This adds 1 for each document in the window
						#
						"$sum": 1,
						"window": {
							#
							#	from the 1 after the current document to the last document in the window
							#
							"documents": [ 1, "unbounded" ]
						}
					}
				}
			}
		},
		{
			"$match": {
				"$or": matches
			}
		}
	])
	

	'''
	print ("stats?")
	print ({
		"sort_direction": sort_direction,
		
		"name": name,
		"emblem": emblem,
		"kind": kind,
		
		"include_food": include_food,
		"include_supp": include_supp
	})
	'''

	
	counter = 0
	proceeds_list = []
	for proceed in proceeds:
		if (counter == len (treasures)):
			raise Exception (f"Only { len (treasures) } item should have been found.")
	
		proceeds_list.append (proceed)
		
		counter += 1
		
	assert (len (proceeds_list) == len (treasures)), [ len (proceeds_list), len (treasure) ]
	
	if (len (proceeds_list) == 1):
		return proceeds_list [0];
	
	return proceeds_list