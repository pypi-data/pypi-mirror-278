








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

def addresses_guest_supps (packet):
	app = packet ["app"]

	blueprint = sanic.Blueprint (
		"guest_supps", 
		url_prefix = "/guests/supps"
	)

	@blueprint.route ("/find")
	#@openapi.parameter ("opener", str, "header")
	async def address_recipe_formulate (request):
		essence = retrieve_essence ()

		#lock_status = check_key (request)
		#if (lock_status != "unlocked"):
		#	return lock_status

		#return sanic.json (essence)
	
	
	app.blueprint (blueprint)