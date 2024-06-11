


	

#/
#
from goodest.besties.food_USDA.nature_v2._ops.retrieve import retrieve_parsed_USDA_food
from goodest.adventures.alerting import activate_alert
#
from goodest.adventures.sanique.utilities.check_key import check_key
#
from goodest._essence import retrieve_essence
#
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
#
#\

def besties__food_USDA__nature_v2__FDC_ID (packet):
	essence = retrieve_essence ()
	USDA_food_ellipse = essence ["USDA"] ["food"]

	app = packet ["app"]
	openapi = packet ["openapi"]
	staff_addresses = packet ["staff_addresses"]

	the_blueprint = sanic.Blueprint (
		"staff_besties_food_USDA", 
		url_prefix = "/staff/besties/food_USDA"
	)

	'''
		 https://sanic.dev/en/plugins/sanic-ext/openapi/decorators.html#ui
	'''
	@the_blueprint.route ('/nature_v2/<FDC_ID>')
	@openapi.parameter ("opener", str, "header")
	@openapi.summary ("Food")
	@openapi.description ("Food parsing route, examples: 2369390")
	async def USDA_food_FDC_ID (request, FDC_ID):
		print ("""
		
			USDA_food_FDC_ID
			
		""")
	
		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status
	
		activate_alert ("info", "/besties/food_USDA/nature_v2/<FDC_ID>")

		

		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status		
	
		try:
			out_packet = retrieve_parsed_USDA_food ({
				"FDC_ID": FDC_ID,
				"USDA API Pass": USDA_food_ellipse
			})

			
			if ("anomaly" in out_packet):
				if (out_packet ["anomaly"] == "The USDA API could not find that FDC_ID."):
					return sanic_response.json (out_packet, status = 604)
			
				return sanic_response.json (out_packet, status = 600)
			
			return sanic_response.json (out_packet)
			
		except Exception as E:
			print (str (E))
			
		return sanic_response.json ({
			"anomaly": "An unaccounted for anomaly occurred."
		}, status = 600)
		
		
	app.blueprint (the_blueprint)