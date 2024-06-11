







#----
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
#
#
from goodest._essence import retrieve_essence, build_essence
#from .check_key import check_key
#
#----

def addresses_staff_goodest_inventory_recipes (packet):
	
	blueprint = sanic.Blueprint (
		"staff_goodest_inventory_recipes", 
		url_prefix = "/staff/goodest_inventory/recipes"
	)
	
	@blueprint.route ("/insert_1")
	@openapi.parameter ("opener", str, "header")
	async def addresses_staff_goodest_inventory_recipes_insert_1 (request):
		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status
	
		essence = retrieve_essence ()

		#lock_status = check_key (request)
		#if (lock_status != "unlocked"):
		#	return lock_status

		#return sanic.json (essence)
	
	return blueprint