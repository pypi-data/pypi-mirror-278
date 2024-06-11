




import pathlib
from os.path import dirname, join, normpath
import sys
def add_paths_to_system (paths):
	this_directory = pathlib.Path (__file__).parent.resolve ()	
	for path in paths:
		sys.path.insert (0, normpath (join (this_directory, path)))
	

add_paths_to_system ([
	'../../../../stages'
])



#/
#
from goodest._essence import build_essence
#
#
import biotech
#
#
import rich
#
#
import json
import pathlib
from os.path import dirname, join, normpath
import os
import sys
import subprocess
import time
#
#\


def turn_on_stage_physics ():
	this_directory = pathlib.Path (__file__).parent.resolve ()
	os.chdir (this_directory)
	build_essence ()

def retrieve_physics (packet):
	response_packet = {}

	stage_name = "goodest"

	this_directory = pathlib.Path (__file__).parent.resolve ()
	venues = str (normpath (join (this_directory, "../../../../../venues")))
	this_stage = str (normpath (join (venues, f"stages/{ stage_name }")))
	relative_path = str (normpath (join (venues, f"stages/{ stage_name }")))

	module_paths = [
		str (normpath (join (venues, "stages"))),
		str (normpath (join (venues, "stages_pip")))
	]

	if (len (sys.argv) >= 2):
		glob_string = this_stage + '/' + sys.argv [1]
		db_directory = False
	else:
		glob_string = this_stage + '/**/API_status_*.py'
		db_directory = normpath (join (this_directory, "DB"))
		
	return {
		"db_directory": db_directory,
		"glob_string": glob_string,
		"relative_path": relative_path,
		"module_paths": module_paths,
		"venues": venues
	}



turn_on_stage_physics ()	
	
# turn_on ()	
	
physics = retrieve_physics ({})

bio = biotech.on ({
	"glob_string": physics ["glob_string"],
	"module_paths": physics ["module_paths"],
	"relative_path": physics ["relative_path"],
	
	"aggregation_format": 2,
	
	"simultaneous": True,
	"simultaneous_capacity": 10,

	"time_limit": 60,

	"db_directory": physics ["db_directory"]
})


bio ["off"] ()



time.sleep (2)

rich.print_json (data = bio ["proceeds"] ["alarms"])
rich.print_json (data = bio ["proceeds"] ["stats"])