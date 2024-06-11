







'''
	from goodest.adventures.monetary.DB.goodest_inventory.supps.document.find import find_supp
	find_supp ({
		"filter": {
			"nature.identity.DSLD ID": ""
		}
	})
'''



from goodest._essence import retrieve_essence
from goodest.adventures.monetary.DB.goodest_inventory.connect import connect_to_goodest_inventory
from goodest.besties.supp_NIH.nature_v2._ops.retrieve import retrieve_parsed_NIH_supp
	
import ships.modules.exceptions.parse as parse_exception



	
'''
	DSLD_ID = "",
	affiliates = [],
	goodness_certifications = []
'''
def find_supp (packet):
	filter = packet ["filter"]

	supp = None

	print ('find supp')

	try:
		[ driver, goodest_inventory_DB ] = connect_to_goodest_inventory ()
		collection = goodest_inventory_DB ["supp"]
	except Exception as E:
		print ("supp collection connect:", E)
		raise Exception (E)
	
	try:	
		essence = retrieve_essence ()
		supp = collection.find_one (filter, {"_id": 0});
		
	except Exception as E:
		print ("supp collection retrieval exception:", parse_exception.now (E))
		raise Exception (E)
		
	try:
		driver.close ()
	except Exception as E:
		print (parse_exception.now (E))
		print ("supp collection disconnect exception:", E)	
		
	return supp;








