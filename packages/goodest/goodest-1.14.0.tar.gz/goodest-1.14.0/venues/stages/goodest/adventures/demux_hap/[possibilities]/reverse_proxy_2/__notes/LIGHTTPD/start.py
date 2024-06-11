

'''
	https://www.lighttpd.net/
	
	install:
		dnf install lighttpd
'''

'''
	tutorial:
		https://redmine.lighttpd.net/projects/lighttpd/wiki/TutorialConfiguration
'''

'''
	https://redmine.lighttpd.net/projects/lighttpd/wiki/Docs_SSL
'''

'''
	start:
		#
		#	empty is solid
		#
		lighttpd -tt -f lighttpd.conf
'''

def add_to_system_paths (trails):
	import pathlib
	from os.path import dirname, join, normpath
	import sys
	
	this_directory = pathlib.Path (__file__).parent.resolve ()
	for trail in trails:
		sys.path.insert (0, normpath (join (this_directory, trail)))

add_to_system_paths ([ 
	'structures',
	'structures_pip'
])


import pathlib
from os.path import dirname, join, normpath
import sys
this_directory = pathlib.Path (__file__).parent.resolve ()

config_path = str (normpath (join (this_directory, "lighttpd.conf")))
documents = str (normpath (join (this_directory, "documents")))
error_log = str (normpath (join (this_directory, "error.log")))
access_log = str (normpath (join (this_directory, "access.log")))

config = f"""
server.port = 80

server.document-root = "{ documents }" 

server.modules = ( "mod_scgi", "mod_accesslog", "mod_proxy" )

server.errorlog = "{ error_log }"
accesslog.filename = "{ access_log }"

$HTTP["host"] == "localhost" {{
	proxy.balance = "hash" 
	proxy.server  = ( 
		"" => ( 
			( 
				"host" => "localhost",
				"port" => 5173
			)
		)
	)
}}

"""

print (config)


import os


FP = open (config_path, "w")
FP.write (config)
FP.close ()

script = f"lighttpd -tt -f '{ config_path }'"
os.system (script)


os.system (f"lighttpd -D -f '{ config_path }'")


print ('started?', script)