


'''
	from goodest.adventures.monetary.DB.goodest_inventory.supps.document.insert import insert_supp
	insert_supp ({
		"DSLD_ID": "",
		"affiliates": [],
		"goodness_certifications": []
	})
'''



from goodest._essence import retrieve_essence
from goodest.adventures.monetary.DB.goodest_inventory.connect import connect_to_goodest_inventory
from goodest.besties.supp_NIH.nature_v2._ops.retrieve import retrieve_parsed_NIH_supp
		
import ships.modules.exceptions.parse as parse_exception


def find_next_emblem (supp_collection):
	count = supp_collection.count_documents ({})

	if (count == 0):
		return 1

	next_emblem = supp_collection.find ().sort ({ 
		"emblem": -1
	}).limit (1).next () ["emblem"] + 1
	
	return next_emblem;
	

	
'''
	DSLD_ID = "",
	affiliates = [],
	goodness_certifications = []
'''
def insert_supp (packet):
	DSLD_ID = packet ["DSLD_ID"]
	affiliates = packet ["affiliates"]
	goodness_certifications = packet ["goodness_certifications"]
	

	try:
		[ driver, goodest_inventory_DB ] = connect_to_goodest_inventory ()
		supp_collection = goodest_inventory_DB ["supp"]
	except Exception as E:
		print ("supp collection connect:", E)
		
	
	try:	
		essence = retrieve_essence ()
		
		print ("essence:", essence)
		
		the_pass = essence ['NIH'] ['supp']
		out_packet = retrieve_parsed_NIH_supp ({
			"DSLD_ID": DSLD_ID,
			"NIH API Pass": the_pass
		})
		


		'''
			This is actually two operations.
				1. find the previous emblem
			
			Multi step insert?
		'''
		next_emblem = find_next_emblem (supp_collection)
		inserted = supp_collection.insert_one ({
			'emblem': next_emblem,
			'nature': out_packet,
			"affiliates": affiliates,
			"goodness certifications": goodness_certifications
		})
		
		inserted_document = supp_collection.find_one ({"_id": inserted.inserted_id })
		
		print ()
		print ("inserted:", inserted_document ["emblem"])

	except Exception as E:
		print (parse_exception.now (E))
		raise Exception (E)
		
	try:
		driver.close ()
	except Exception as E:
		print (parse_exception.now (E))
		print ("food collection disconnect exception:", E)	
		
	return None;








