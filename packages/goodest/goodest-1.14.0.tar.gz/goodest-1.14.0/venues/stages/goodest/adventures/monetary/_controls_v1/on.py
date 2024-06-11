

'''
	mongod --dbpath ./../_mongo_data --port 39000
'''

'''
	from goodest.monetary.node.on import turn_on_monetary_node
	mongo_process = turn_on_monetary_node (
		goodest_essence = goodest_essence,
		
		exception_if_on = True
	)
	
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
from .status import check_monetary_status
#
import goodest.mixes.procedure as procedure
from goodest._essence import retrieve_essence

#----
#
#	indexes
#
#----
from goodest.adventures.monetary.DB.goodest_inventory._treasures._indexes.drop_and_create import drop_and_create_treasures_indexes
	

from goodest.adventures.alerting.parse_exception import parse_exception
from goodest.adventures.alerting import activate_alert	
#
#
from biotech.topics.show.variable import show_variable		
import ships.cycle.loops as cycle_loops	
#
#
import rich
#
#
from fractions import Fraction
import multiprocessing
import subprocess
import time
import os
import atexit
#
#----


def turn_on_the_node (
	exception_if_on = False
):
	essence = retrieve_essence ()

	port = essence ["monetary"] ["onsite"] ["port"]
	dbpath = essence ["monetary"] ["onsite"] ["path"]
	PID_path = essence ["monetary"] ["onsite"] ["PID_path"]
	logs_path = essence ["monetary"] ["onsite"] ["logs_path"]

	os.makedirs (dbpath, exist_ok = True)
	os.makedirs (os.path.dirname (logs_path), exist_ok = True)
	os.makedirs (os.path.dirname (PID_path), exist_ok = True)

	script = [
		"mongod", 

		'--fork',

		'--dbpath', 
		#f"'{ dbpath }'", 
		f"{ dbpath }", 
		
		'--logpath',
		f"{ logs_path }", 
	
		
		'--port', 
		str (port),
		
		'--bind_ip',
		'0.0.0.0',
		
		'--pidfilepath',
		str (PID_path)
	]

	activate_alert ("info", {
		"procedure": script
	})

	mongo_process = procedure.implicit (script)

	the_monetary_status_2 = check_monetary_status (
		loop_limit = 5
	)
	if (the_monetary_status_2 == "on"):
		exception_strand = "The monetary is on"
	
		if (exception_if_on):
			raise Exception (exception_strand)
	
		print (exception_strand)
		return mongo_process

	raise Exception ("A connection to the monetary could not be established.")

def turn_on_monetary_node (
	exception_if_on = False
):
	essence = retrieve_essence ()

	show_variable ("checking if the monetary is already on")

	if (check_monetary_status () != "on"):
		turn_on_the_node (
			exception_if_on = exception_if_on
		)
	else:
		show_variable ("The monetary is already on")
		
	'''
		indexes
	'''
	drop_and_create_treasures_indexes ({
		"collection": "food"
	})
	drop_and_create_treasures_indexes ({
		"collection": "supp"
	})


	

	
	
	


#
#
#