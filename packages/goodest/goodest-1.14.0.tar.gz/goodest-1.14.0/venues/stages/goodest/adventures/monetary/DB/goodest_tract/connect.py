
'''	
	from goodest.adventures.monetary.DB.goodest_tract.connect import connect_to_goodest_tract
	[ driver, goodest_tract_DB ] = connect_to_goodest_tract ()
	driver.close ()
'''

'''
	from goodest.adventures.monetary.DB.goodest_tract.connect import connect_to_goodest_tract
	essential_nutrients_collection = connect_to_goodest_tract () ["essential_nutrients"]	
	essential_nutrients_collection.disconnect ()
'''


'''
	from goodest.adventures.monetary.DB.goodest_tract.connect import connect_to_goodest_tract
	cautionary_ingredients_collection = connect_to_goodest_tract () ["cautionary_ingredients"]	
	cautionary_ingredients_collection.disconnect ()
'''

from goodest.adventures.monetary.moves.URL.retrieve import retreive_monetary_URL
from goodest._essence import retrieve_essence
	
import pymongo

def connect_to_goodest_tract ():
	essence = retrieve_essence ()
	
	#ingredients_DB_name = essence ["monetary"] ["aliases"] ["goodest_tract"]
	ingredients_DB_name = essence ["monetary"] ["databases"] ["goodest_tract"] ["alias"]
	
	monetary_URL = retreive_monetary_URL ()

	driver = pymongo.MongoClient (monetary_URL)

	return [
		driver,
		driver [ ingredients_DB_name ]
	]