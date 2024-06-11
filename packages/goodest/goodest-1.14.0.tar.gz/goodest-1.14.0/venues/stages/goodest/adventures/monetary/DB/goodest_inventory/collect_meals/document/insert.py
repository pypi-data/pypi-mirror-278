






'''
	from goodest.adventures.monetary.DB.goodest_inventory.collect_meals.document.insert import insert_meal
	insert_meal ({
		"name": "rice and beans",
		"formulate": {
			"IDs_with_amounts": [
				{
					"FDC_ID": "2471166",
					"grams": 1
				},
				{
					"FDC_ID": "2425001",
					"grams": 2
				}
			]
		}
	})
'''


#/
#
from goodest._essence import retrieve_essence
from goodest.adventures.monetary.DB.goodest_inventory.connect import connect_to_goodest_inventory
from goodest.adventures.monetary.quests.meals.statistics import formulate_meal_statistics
#
#
import ships.modules.exceptions.parse as parse_exception
#
#\

def find_next_emblem (the_collection):
	count = the_collection.count_documents ({})

	if (count == 0):
		return 1

	next_emblem = the_collection.find ().sort ({ 
		"emblem": -1
	}).limit (1).next () ["emblem"] + 1
	
	return next_emblem;
	

	

def insert_meal (packet):
	the_name = packet ["name"]
	formulate = packet ["formulate"]

	try:
		[ driver, goodest_inventory_DB ] = connect_to_goodest_inventory ()
		meals_collection = goodest_inventory_DB ["meals"]
	except Exception as E:
		print ("food collection connect:", E)
		
	
	try:	
		essence = retrieve_essence ()
		next_emblem = find_next_emblem (meals_collection)
		
		meal_statistics = formulate_meal_statistics (formulate)
		
		nature = meal_statistics ["recipe"]
		nature ["kind"] = "meal"
		nature ["identity"] = {
			"name": the_name
		}
		
		inserted = meals_collection.insert_one ({
			'emblem': next_emblem,
			'nature': nature
		})
		
		inserted_document = meals_collection.find_one ({"_id": inserted.inserted_id })
		
		print ()
		print ("inserted emblem #:", inserted_document ["emblem"])

	except Exception as E:
		print (parse_exception.now (E))
	
		raise Exception (E)
		pass;
		
	try:
		driver.close ()
	except Exception as E:
		print (parse_exception.now (E))
		print ("meal collection disconnect exception:", E)	
		
	return None;








