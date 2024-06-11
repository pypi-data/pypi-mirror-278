

#----
#
from goodest._essence import retrieve_essence, build_essence
from goodest.adventures.sanique.utilities.check_key import check_key
#
from goodest.shows_v2.recipe._ops.retrieve import retrieve_recipe
from goodest.shows_v2.recipe_with_goals._ops.formulate import formulate_recipe_with_goals
#
from goodest.adventures.sanique.quests_staff.insert_meal import insert_meal_quest
#
#
import law_dictionary
import ships.modules.exceptions.parse as parse_exception
#
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
#
#----



quests = {
	"insert meal": insert_meal_quest
}

def addresses_staff (packet):
	app = packet ["app"]
	staff_addresses = packet ["staff_addresses"]

	
	
	@staff_addresses.route ("/", methods = [ "patch" ])
	@openapi.parameter ("opener", str, "header")
	@openapi.description ("""

	{
		"label": "insert meal",
		"freight": {
			"name": "rice and beans",
			"formulate": {
				"IDs_with_amounts": [
					{
						"FDC_ID": "2471166",
						"grams": 1
					},
					{
						"FDC_ID": "2425001",
						"grams": 2
					}
				]
			}
		}
	}
	
	""")
	@openapi.body ({
		"application/json": {
			"properties": {
				"label": { "type": "string" },
				"freight": { "type": "object" }
			}
		}
	})
	async def staff_patches (request):
		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status
	
		essence = retrieve_essence ()


		try:
			dictionary = request.json
			
		except Exception:
			return sanic.json ({
				"label": "unfinished",
				"freight": {
					"description": "The body could not be parsed."
				}
			})

		print ("label:", dictionary ["label"])
		
		
		try:
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
					"label": "unfinished",
					"freight": {
						"description": "The packet check was not passed.",
						"report": report_1
					}
				}, status = 600)
		except Exception:
			return sanic.json ({
				"label": "unfinished",
				"freight": {
					"description": "An exception occurred while running the packet check."
				}
			})
		
		
		try:
			label = dictionary ["label"]		
			if (label not in quests):
				return sanic.json ({
					"label": "unfinished",
					"freight": {
						"description": 'A quest with that "label" was not found.',
						"report": report_1
					}
				}, status = 600)
		except Exception:
			return sanic.json ({
				"label": "unfinished",
				"freight": {
					"description": "An exception occurred while running the packet check."
				}
			})
		
		
		try:
			proceeds = quests [ label ] ({
				"freight": dictionary ["freight"]
			})
		except Exception as E:
			return sanic.json ({
				"label": "unfinished",
				"freight": {
					"description": "An exception occurred while generating the proceeds.",
					"label": label,
					"exception": parse_exception.now (E)
				}
			})	
			
		return sanic.json (proceeds, status = 200)
		
		
		
		

	
	
	
	@staff_addresses.route ("/essence")
	@openapi.parameter ("opener", str, "header")
	async def address_essence (request):
		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status
	
		essence = retrieve_essence ()



		return sanic.json (essence)
		
		
	@staff_addresses.get ('/goals/<region>')
	@openapi.summary ("goals")
	@openapi.description ("goals")
	@openapi.parameter ("opener", str, "header")
	async def goals_by_region (request, region):
		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status
	
		try:
			ingredient_doc = retrieve_one_goal ({
				"region": region
			})
			
			return sanic_response.json (ingredient_doc)
			
		except Exception as E:
			show_variable (str (E))
			
		return sanic_response.json ({
			"anomaly": "An unaccounted for anomaly occurred."
		}, status = 600)
		
	
	'''
		 https://sanic.dev/en/plugins/sanic-ext/openapi/decorators.html#ui
	'''
	@staff_addresses.patch ('/shows_v2/recipe')
	@openapi.summary ("recipe")
	@openapi.description ("""
	
		{ 
			"IDs_with_amounts": [
				{
					"DSLD_ID": "276336",
					"packets": 10
				},
				{
					"DSLD_ID": "214893",
					"packets": 20
				},
				{
					"FDC_ID": "2412474",
					"packets": 20
				}
			] 
		}
		
	""")
	@openapi.body ({
		"application/json": {
			"properties": {
				"IDs_with_amounts": { "type": "list" }
			}
		}
	})
	@openapi.parameter ("opener", str, "header")
	#@doc.produces ({'message': str})
	#@doc.response (200, {"message": "Hello, {name}!"})
	async def recipe (request):
		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status
	
		data = request.json
	
		show_variable ({
			"data": data
		}, mode = "pprint")
	
		try:
			recipe_packet = retrieve_recipe ({
				"IDs_with_amounts": data ["IDs_with_amounts"]
			})
			if (len (recipe_packet ["not_added"]) >= 1):
				not_found_len = len (recipe_packet ["not_added"]);
				assert (type (not_found_len) == int)
			
				not_found_len = str (not_found_len)
			
				return sanic_response.json ({
					"anomaly": f"{ not_found_len } could not be found."
				}, status = 600)
			
			assert (len (recipe_packet ["not_added"]) == 0)
			
			recipe_with_goals_packet = formulate_recipe_with_goals ({
				"recipe": recipe_packet ["recipe"],
				"goal_region": "2"
			})
			
			recipe = recipe_with_goals_packet ["recipe"]	
			
			return sanic_response.json (recipe_with_goals_packet ["recipe"])
			
		except Exception as E:
			print (str (E))
			
		return sanic_response.json ({
			"anomaly": "An unaccounted for anomaly occurred."
		}, status = 600)
		
		
