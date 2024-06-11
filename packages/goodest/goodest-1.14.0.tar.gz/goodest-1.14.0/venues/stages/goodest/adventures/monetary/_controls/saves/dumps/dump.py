
#----
#
from goodest._essence import retrieve_essence
import goodest.mixes.procedure as procedure
#
#
import click
import rich
#
#
import pathlib
from os.path import dirname, join, normpath
import sys
import os
import time
#
#----

def dump_node (packet):
	version = packet ["version"]

	essence = retrieve_essence ()
	
	the_dumps_path = essence ["monetary"] ["saves"] ["dumps"] ["path"]
	URL = essence ["monetary"] ["URL"]
	monetary_databases = essence ["monetary"] ["databases"]
	
	already_exists = []
	for monetary_database in monetary_databases:
		database_name = monetary_databases [ monetary_database ] ["alias"]
		database_collections = monetary_databases [ monetary_database ] ["collections"]
		
		for collection in database_collections:
			name = database_name + "." + collection + "." + version + ".dump.gzip"

			dump_path = str (normpath (join (
				the_dumps_path, 
				database_name, 
				collection, 
				name
			)))
			if (os.path.exists (dump_path) == True):
				already_exists.append (dump_path)
				continue;
				
			os.makedirs (
				str (normpath (join (
					the_dumps_path, 
					database_name, 
					collection
				))), 
				exist_ok = True
			)	
				
			process_strand = [
				"mongodump",
				"--uri",
				URL,
				f"--db={ database_name }",
				f"--collection={ collection }",
				#f"--out={ dump_path }",
				"--gzip",
				f"--archive={ dump_path }"
			]
	
			procedure.go (
				script = process_strand
			)
			
			time.sleep (.25)
	
	os.system (f"chmod -R 777 '{ the_dumps_path }'")

	rich.print_json (data = {
		"already_exists": already_exists
	})	