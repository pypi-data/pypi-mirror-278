









	

#/
#
from goodest.besties.supp_NIH.nature_v2._ops.retrieve import retrieve_parsed_NIH_supp
from goodest.adventures.alerting import activate_alert
from goodest.adventures.sanique.utilities.check_key import check_key
#
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


def besties__supp_NIH__nature_v2__DSLD_ID (packet):
	essence = retrieve_essence ()
	NIH_supp_ellipse = essence ["NIH"] ["supp"]

	app = packet ["app"]
	openapi = packet ["openapi"]
	staff_addresses = packet ["staff_addresses"]
	
	the_blueprint = sanic.Blueprint (
		"staff_besties_supp_NIH", 
		url_prefix = "/staff/besties/supp_NIH"
	)
	
	@the_blueprint.route ("/nature_v2/<DLSD_ID>")
	@openapi.summary ("Supp")
	@openapi.description ("Supp parsing route, examples: 69439")
	@openapi.parameter ("opener", str, "header")
	async def NIH_supp (request, DLSD_ID):
		print ("""
		
			USDA_food_FDC_ID
			
		""")
	
		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status
	
		data = request.json
	
		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status		
	
		try:
			out_packet = retrieve_parsed_NIH_supp ({
				"DSLD_ID": DLSD_ID,
				"NIH API Pass": NIH_supp_ellipse
			})
			
			if ("anomaly" in out_packet):
				if (out_packet ["anomaly"] == "The NIH API could not find that DLSD_ID."):
					return sanic_response.json (out_packet, status = 604)
			
				return sanic_response.json (out_packet, status = 600)
			
			return sanic_response.json (out_packet)
			
		except Exception as E:
			print (str (E))
			
		return sanic_response.json ({
			"anomaly": "An unaccounted for anomaly occurred."
		}, status = 600)
		
	app.blueprint (the_blueprint)