
'''
	priorities:
		import configs.basic as basic_config
		basic_config.build ({
			
		})
'''

import pathlib
from os.path import dirname, join, normpath
import sys

this_directory = pathlib.Path (__file__).parent.resolve ()
error_log = str (normpath (join (this_directory, "error.log")))
pid_file = str (normpath (join (this_directory, "nginx.pid")))

could_not_connect = '"' + str (normpath (join (this_directory, "could_not_connect.HTML"))) + '"'

def build (parameters):
	to = parameters ["to"]

	b1 = "\u007b"
	b2 = "\u007d"


	'''
		foundations:
			worker_processes 1;
			
			error_log  logs/error.log;
			pid        logs/nginx.pid;
			
			events {
				worker_connections 1024;
			}
	'''
	config = f"""
	
worker_processes 5;

worker_rlimit_nofile 8192;

events {{
	worker_connections 4096;
}}

http {{
	server {{
		listen 80;

		

		location / {{
			error_page 502 { could_not_connect };
			
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_set_header Host $host;

			proxy_pass { to };

			proxy_http_version 1.1;
			proxy_set_header Upgrade $http_upgrade;
			proxy_set_header Connection "upgrade";
		}}
	}}
}}
"""

	return config;