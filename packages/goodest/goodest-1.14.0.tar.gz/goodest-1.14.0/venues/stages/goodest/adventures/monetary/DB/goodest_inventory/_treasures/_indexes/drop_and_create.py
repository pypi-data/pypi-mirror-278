

'''
	from goodest.adventures.monetary.DB.goodest_inventory._treasures._indexes.drop_and_create import drop_and_create_treasures_indexes
	drop_and_create_treasures_indexes ({
		"collection": "foods"
	})
'''



from goodest.adventures.alerting.parse_exception import parse_exception
from goodest.adventures.alerting import activate_alert
from goodest.adventures.monetary.DB.goodest_inventory.connect import connect_to_goodest_inventory
	
	
def drop_and_create_treasures_indexes (packet):
	collection_name = packet ["collection"]

	[ driver, goodest_inventory_DB ] = connect_to_goodest_inventory ()
	the_collection = goodest_inventory_DB [ collection_name ]

	try:
		proceeds = the_collection.drop_indexes ()
	except Exception as E:
		activate_alert ("emergency", {
			"exception": parse_exception (E)
		})
		
	proceeds = the_collection.create_index ( 
		[( "nature.identity.UPC", 1 )],
		name = "name = nature.identity.UPC"
	)
	
	activate_alert ("info", {
		"proceeds of index create": proceeds
	}, mode = "pprint")
	
	driver.close ()