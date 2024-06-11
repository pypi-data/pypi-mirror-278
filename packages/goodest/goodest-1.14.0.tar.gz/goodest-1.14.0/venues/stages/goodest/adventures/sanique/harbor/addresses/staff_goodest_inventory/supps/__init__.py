







#----
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
#
#
from goodest._essence import retrieve_essence, build_essence
from goodest.adventures.sanique.utilities.check_key import check_key
#
from goodest.adventures.monetary.DB.goodest_inventory.supps.document.insert import insert_supp
#
#----

def addresses_supps (packet):
	app = packet ["app"]
	
	the_blueprint = sanic.Blueprint (
		"staff_supps", 
		url_prefix = "/staff/supps"
	)
	
	@the_blueprint.route ("/insert_1", methods = [ "post" ])
	@openapi.description ("""
	
	{
		"DSLD_ID": "",
		"affiliates": [{
			"name": "Amazon",
			"link": "https://amzn.to/4cFpix6"
		}],
		"goodness_certifications": [{
			"certification": "Certified Vegan Vegan.org"
		}]
	}
	
	USDA:
		https://fdc.nal.usda.gov/fdc-app.html#/
	
	mongo query for affiliates:
		{
			affiliates: { $exists: true, $ne: [] },
			$expr: { $gt: [{ $size: "$affiliates" }, 0] }
		}
	
	""")
	@openapi.parameter ("opener", str, "header")
	@openapi.body ({
		"application/json": {
			"properties": {
				"FDC_ID": { "type": "string" },
				"affiliates": { "type": "array" },
				"goodness_certifications": { "type": "array" }
			}
		}
	})
	async def address_supps_insert (request):
		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status
	
		essence = retrieve_essence ()

		
		try:
			dictionary = request.json
			print ("dictionary:", dictionary)
			
		except Exception:
			return sanic.json ({
				"label": "unfinished",
				"freight": {
					"description": "The body could not be parsed."
				}
			}, status = 600)
		
		proceeds = insert_supp ({
			"DSLD_ID": dictionary ["DSLD_ID"],
			"affiliates": dictionary ["affiliates"],
			"goodness_certifications": dictionary ["goodness_certifications"]
		})
		
		print ("proceeds:", proceeds)
		
		return sanic.json ({
			"label": "finished",
			"freight": {}
		})
		

		#lock_status = check_key (request)
		#if (lock_status != "unlocked"):
		#	return lock_status

		#return sanic.json (essence)
	
	app.blueprint (the_blueprint)