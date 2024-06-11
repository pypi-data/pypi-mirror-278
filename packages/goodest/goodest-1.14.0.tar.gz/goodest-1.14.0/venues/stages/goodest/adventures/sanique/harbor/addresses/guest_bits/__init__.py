

'''
	addresses_bits ({
		"app": ""
	})
'''

#----
#
from goodest._essence import retrieve_essence
#
from goodest.adventures.sanique.utilities.generate_inventory_paths import generate_inventory_paths
#
#
import vegan_bits_1
import vegan_bits_2
import plant_genomes_1
import plant_genomes_2
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
#
#----

def addresses_guest_bits (addresses_packet):
	app = addresses_packet ["app"]
	#
	#	
	essence = retrieve_essence ()
	#bits_inventory_paths_1 = generate_inventory_paths (
	#	essence ["bits"] ["sequences_path"]
	#)
	#
	#

	
	bits_path_1 = vegan_bits_1.sequences ()
	bits_path_2 = vegan_bits_2.sequences ()
	bits_path_3 = plant_genomes_1.sequences ()
	bits_path_4 = plant_genomes_2.sequences ()
	print ("bits_path_4:", bits_path_4)
		
	if (essence ["mode"] == "nurture"):
		app.static ("/bits/1", bits_path_1, name = "bits_path_1")
		app.static ("/bits/2", bits_path_2, name = "bits_path_2")
		app.static ("/bits/3", bits_path_3, name = "bits_path_3")
		app.static ("/bits/4", bits_path_4, name = "bits_path_4")
		return;
		
		
		
	else:
		'''
			bit_path: favicons/favicon-1.ico
		'''
		bits_inventory_paths_1 = generate_inventory_paths (bits_path_1)
		bits_inventory_paths_2 = generate_inventory_paths (bits_path_2)
		bits_inventory_paths_3 = generate_inventory_paths (bits_path_3)
		bits_inventory_paths_4 = generate_inventory_paths (bits_path_4)
		
		print ("bits_inventory_paths_4:", bits_inventory_paths_4)
		for bit_path in bits_inventory_paths_4:
			print ("bit_path:", bit_path)
			pass;
	
		bits_addresses = sanic.Blueprint ("bits", url_prefix = "/bits")

		@bits_addresses.route("/<path:path>")
		async def public_route (request, path):	
			try:
				full_path = path.split ('/', 1) [1]
				bits_number = path.split ('/') [0]

				content_type = False;
				
				if (
					bits_number == "1" and 
					full_path in bits_inventory_paths_1
				):
					content_type = bits_inventory_paths_1 [ full_path ] ["mime"]
					content = bits_inventory_paths_1 [ full_path ] ["content"]
				
				elif (
					bits_number == "2" and 
					full_path in bits_inventory_paths_2
				):
					content_type = bits_inventory_paths_2 [ full_path ] ["mime"]
					content = bits_inventory_paths_2 [ full_path ] ["content"]
				
				elif (
					bits_number == "3" and 
					full_path in bits_inventory_paths_3
				):
					content_type = bits_inventory_paths_3 [ full_path ] ["mime"]
					content = bits_inventory_paths_3 [ full_path ] ["content"]
				
				elif (
					bits_number == "4" and 
					full_path in bits_inventory_paths_4
				):
					content_type = bits_inventory_paths_4 [ full_path ] ["mime"]
					content = bits_inventory_paths_4 [ full_path ] ["content"]
				
				if (type (content_type) == str):
					'''
						possibly: SHA for caching
							maybe better: sequential addresses for caching
					'''						
					return sanic_response.raw (
						content, 
						content_type = content_type,
						headers = {
							"Cache-Control": "private, max-age=31536000",
							"Expires": "0"
						}
					)
				
				return sanic_response.json ({
					"summary": "bits not found"
				}, status = 604)
				
			except Exception as E:
				print ("E:", E)
		
			return sanic_response.text ("An anomaly occurred while processing.", status = 600)	


		app.blueprint (bits_addresses)
