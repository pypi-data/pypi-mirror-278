






#----
#
from goodest._essence import retrieve_essence, build_essence
from goodest.adventures.monetary.DB.goodest_inventory.foods.document.find import find_food
#
#
import law_dictionary
#
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
#
#
#----

import law_dictionary
	

def addresses_guest_foods (packet):
	app = packet ["app"]

	blueprint = sanic.Blueprint (
		"guest_foods", 
		url_prefix = "/guests/foods"
	)

	@blueprint.route ("/find", methods = [ "patch" ])
	async def address_guest_foods_find (request):
		essence = retrieve_essence ()
		
		try:
			dictionary = request.json
						
		except Exception:
			return sanic.json ({
				"anomaly": "The body could not be parsed."
			})
		
		report_1 = law_dictionary.check (
			return_obstacle_if_not_legit = True,
			allow_extra_fields = False,
			laws = {
				"label": {
					"required": True,
					"type": str
				},
				"freight": {
					"required": True,
					"type": dict
				}
			},
			dictionary = dictionary 
		)
		if (report_1 ["advance"] != True):
			return sanic.json ({
				"obstacle": report_1,
				"obstacle number": 1
			}, status = 600)
		
		
		freight = dictionary ["freight"]
		report_freight = law_dictionary.check (
			return_obstacle_if_not_legit = True,
			allow_extra_fields = True,
			laws = {
				"filters": {
					"required": True,
					"type": dict
				}
			},
			dictionary = freight 
		)
		if (report_freight ["advance"] != True):
			return sanic.json ({
				"obstacle": report_freight,
				"obstacle number": 2
			}, status = 600)
			
		filters = freight ["filters"]
		report_filters = law_dictionary.check (
			return_obstacle_if_not_legit = True,
			allow_extra_fields = True,
			laws = {
				"emblem": {
					"required": True,
					"type": str
				}
			},
			dictionary = filters 
		)
		if (report_filters ["advance"] != True):
			return sanic.json ({
				"obstacle": report_filters,
				"obstacle number": 3
			}, status = 600)
		

		try:
			if ("emblem" in filters):
				filters ["emblem"] = int (filters ["emblem"])
		except Exception:
			return sanic.json ({
				"anomaly": "The emblem couldn't be converted to an integer.",
				"obstacle number": 4
			}, status = 600)
		

		food = find_food ({
			"filter": filters
		})
		
		return sanic.json ({
			"label": "finished",
			"freight": food
		});


	@blueprint.route ("/find_emblem/<emblem>", methods = [ "get" ])
	async def address_recipe_formulate (request, emblem):
		essence = retrieve_essence ()
		
		print ("/find_emblem", emblem)
		
		if (type (emblem) != str):
			return sanic.json ({
				"anomaly": "emblem isn't a string"
			})
			
		try:
			emblem = int (emblem)
		except Exception:
			return sanic.json ({
				"anomaly": "The emblem couldn't be converted to an integer."
			})
		
		'''
		report = law_dictionary.check (
			return_obstacle_if_not_legit = True,
			allow_extra_fields = False,
			laws = {
				"directory_1": {
					"required": False,
					
				}
			},
			dictionary = dictionary
		)
		if (report ["advance"] != True):
			return sanic.json ({
				"obstacle": report
			})
		'''

		food = find_food ({
			"filter": {
				"emblem": emblem
			}
		})
		
		return sanic.json (food);
		
	
	app.blueprint (blueprint)