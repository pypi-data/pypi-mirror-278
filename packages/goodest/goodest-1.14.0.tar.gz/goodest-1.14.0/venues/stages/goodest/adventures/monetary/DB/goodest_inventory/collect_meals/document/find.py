







'''
	from goodest.adventures.monetary.DB.goodest_inventory.collect_meals.document.find import find_meal
	le_meal = find_meal ({
		"filter": {
			"nature.identity.FDC ID": ""
		}
	})
'''



#/
#
from goodest._essence import retrieve_essence
from goodest.adventures.monetary.DB.goodest_inventory.connect import connect_to_goodest_inventory
#
#
import ships.modules.exceptions.parse as parse_exception
#
#\


	
'''
	FDC_ID = "",
	affiliates = [],
	goodness_certifications = []
'''
def find_meal (packet):
	filter = packet ["filter"]

	print ("filter:", filter)

	le_meal = None

	try:
		[ driver, goodest_inventory_DB ] = connect_to_goodest_inventory ()
		meals_collection = goodest_inventory_DB ["meals"]
	except Exception as E:
		print ("meals collection connect:", E)
		raise Exception (E)
	
	try:	
		le_meal = meals_collection.find_one (filter, {"_id": 0});
		
	except Exception as E:
		print (parse_exception.now (E))
		raise Exception (E)
		
	try:
		driver.close ()
	except Exception as E:
		print (parse_exception.now (E))
		print ("meals collection disconnect exception:", E)	
		
	return le_meal;








