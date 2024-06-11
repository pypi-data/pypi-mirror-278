

#----
#
from goodest._essence import retrieve_essence
from goodest.adventures.sanique.utilities.generate_inventory_paths import generate_inventory_paths
#
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
from sanic_limiter import Limiter, get_remote_address
#from sanic.response import html
#
#
import json
from os.path import exists, dirname, normpath, join
from urllib.parse import unquote
import threading
import time
#
#----

def vue_regions (vue_regions_packet):
	essence = retrieve_essence ()

	app = vue_regions_packet ["app"]
	guest_addresses = vue_regions_packet ["guest_addresses"]
	
	
	front_inventory_paths = generate_inventory_paths (
		essence ["vv_turbo"] ["dist_path"]
	)
	for front_path in front_inventory_paths:
		#print ("front_path:", front_path)
		pass;
	
	the_index = essence ["vv_turbo"] ["dist_path"] + "/index.html"
	the_assets = essence ["vv_turbo"] ["dist_path"] + "/assets"
	
	#
	#	or:
	#		app.static ("/bits", bits_path)
	#
	#
	
	if (essence ["mode"] == "nurture"):
		app.static ("/assets", essence ["vv_turbo"] ["dist_path"] + "/assets", name = "assets")
		
		
		#
		#	get?
		#
		#
		@guest_addresses.route ("/")
		async def home (request):
			return await sanic_response.file (the_index)

		
		@guest_addresses.route ("/front/<encoded_path:path>")
		async def handle_path (request, encoded_path):
			#path = unquote (encoded_path)
			return await sanic_response.file (the_index)
		
	else:
		@guest_addresses.route("/assets/<path:path>")
		async def assets_route (request, path):
			#print (f"address: /assets/{ path }")
			
			#full_path = ""
			try:
				the_path = f"assets/{ path }"	
				if (the_path in front_inventory_paths):
					content_type = front_inventory_paths [ the_path ] ["mime"]
					content = front_inventory_paths [ the_path ] ["content"]
				
					#return sanic_response.raw (content, content_type = content_type)
					
					return sanic_response.raw (
						content, 
						content_type = content_type,
						headers = {
							"Custom-Header-1": "custom",
							"Cache-Control": "private, max-age=31536000",
							#"Expires": "0"
						}
					)
					
			except Exception as E:
				print ("E:", E)
		
			return sanic_response.json ({
				"note": "An anomaly occurred while processing.",
				"the_path": the_path
			}, status = 600)
	
		#
		#	get?
		#
		#
		@guest_addresses.route ("/")
		async def home (request):
			essence = retrieve_essence ()
			#return sanic_response.text ("home")
			
			#
			#	mimetype = vue_dist_inventory [ "index.html" ] ["mime"],
			#
			#
			#return sanic_response.html (the_index)
			return sanic_response.html (front_inventory_paths ["index.html"] ["content"])


		
		@guest_addresses.route ("/front/<encoded_path:path>")
		async def handle_path (request, encoded_path):
			path = unquote (encoded_path)
			return sanic_response.html (front_inventory_paths ["index.html"] ["content"])


	