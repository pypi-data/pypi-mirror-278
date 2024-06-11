




'''
	from goodest.adventures.monetary.DB.goodest_inventory.foods.document.find import find_food
	find_food ({
		"filter": {
			"nature.identity.FDC ID": ""
		}
	})
'''



from goodest._essence import retrieve_essence
from goodest.adventures.monetary.DB.goodest_inventory.connect import connect_to_goodest_inventory
from goodest.besties.food_USDA.nature_v2._ops.retrieve import retrieve_parsed_USDA_food
	
import ships.modules.exceptions.parse as parse_exception



	
'''
	FDC_ID = "",
	affiliates = [],
	goodness_certifications = []
'''
def find_food (packet):
	filter = packet ["filter"]

	food = None

	try:
		[ driver, goodest_inventory_DB ] = connect_to_goodest_inventory ()
		food_collection = goodest_inventory_DB ["food"]
	except Exception as E:
		print ("food collection connect:", E)
		raise Exception (E)
	
	try:	
		essence = retrieve_essence ()
		food = food_collection.find_one (filter, {"_id": 0});
		
	except Exception as E:
		print (parse_exception.now (E))
		raise Exception (E)
		
	try:
		driver.close ()
	except Exception as E:
		print (parse_exception.now (E))
		print ("food collection disconnect exception:", E)	
		
	return food;








