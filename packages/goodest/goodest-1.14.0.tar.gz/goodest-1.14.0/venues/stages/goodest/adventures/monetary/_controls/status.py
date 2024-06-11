

'''
	mongod --dbpath ./../_mongo_data --port 39000
'''

'''
	from goodest.adventures.monetary.status import check_monetary_status
	the_monetary_status = find_monetary_status ()
	
	import time
	while True:
		time.sleep (1)
'''

'''	
	mongo_process.terminate ()

	#
	#	without this it might appear as if the process is still running.
	#
	import time
	time.sleep (2)
'''




#----
#
from goodest.adventures.monetary.moves.URL.retrieve import retreive_monetary_URL
from goodest._essence import retrieve_essence
#
#
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import ServerSelectionTimeoutError
import rich
#
#----

def check_monetary_status (
	loop_limit = 1
):
	essence = retrieve_essence ()
	monetary_URL = retreive_monetary_URL ()
	
	print ("checking if can connect to URL:", monetary_URL)	
	

	try:
		client = MongoClient (monetary_URL, serverSelectionTimeoutMS=2000)
		client.server_info ()
		return "on"
		
	except Exception as E:
		print ("mongo connection exception:", E)
	
		pass;

	return "off"
	
	



	

	
