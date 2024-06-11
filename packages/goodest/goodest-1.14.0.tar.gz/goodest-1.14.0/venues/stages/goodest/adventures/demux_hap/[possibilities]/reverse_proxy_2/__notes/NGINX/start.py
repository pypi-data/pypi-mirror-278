
'''
	python3 start.py
'''

'''
	steps:
		-> write config to "/etc/nginx/nginx.conf"
		-> 
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

import os

config_path = "/etc/nginx/nginx.conf"

'''
	80 -> 3000
'''
import configs.HTTP_80 as HTTP_80_config
config = HTTP_80_config.build ({
	"to": "http://localhost:3000"
})

FP = open (config_path, "w")
FP.write (config)
FP.close ()

os.system (f"cat '{ config_path }'")

os.system ("sudo systemctl stop nginx")

os.system ("sudo systemctl enable nginx")
os.system ("sudo systemctl start nginx")

#os.system ("journalctl -xeu nginx.service")

os.system ("systemctl status nginx.service")


