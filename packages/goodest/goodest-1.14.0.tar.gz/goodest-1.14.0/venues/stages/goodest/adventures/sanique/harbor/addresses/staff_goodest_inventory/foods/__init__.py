

'''
	objectives:
		[ ] 
'''


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
from goodest.adventures.monetary.DB.goodest_inventory.foods.document.insert import insert_food	
#
#----

def addresses_foods (packet):
	app = packet ["app"]

	the_blueprint = sanic.Blueprint (
		"staff_foods", 
		url_prefix = "/staff/foods"
	)

	@the_blueprint.route ("/insert_1", methods = [ "post" ])
	@openapi.parameter ("opener", str, "header")
	@openapi.description ("""
	
	
	https://www.gs1us.org/tools/gs1-company-database-gepir
	
	This play requires 3 keys.
	
	{
		"FDC_ID": "",
		"affiliates": [{
			"name": "Amazon",
			"link": "https://amzn.to/4cFpix6"
		}],
		"goodness_certifications": []
	}
	
	{
		"FDC_ID": "",
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
	@openapi.body ({
		"application/json": {
			"properties": {
				"FDC_ID": { "type": "string" },
				"affiliates": { "type": "string" },
				"goodness_certifications": { "type": "string" }
			}
		}
	})
	async def address_food_insert (request):
		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status
	
		essence = retrieve_essence ()
		
		print ("""
		
			address_food_insert called
		
		""")
		
		
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
		
		proceeds = insert_food ({
			"FDC_ID": dictionary ["FDC_ID"],
			"affiliates": dictionary ["affiliates"],
			"goodness_certifications": dictionary ["goodness_certifications"]
		})
		
		print ("proceeds:", proceeds)
		
		return sanic.json ({
			"label": "finished",
			"freight": {}
		})
	
		
	app.blueprint (the_blueprint)