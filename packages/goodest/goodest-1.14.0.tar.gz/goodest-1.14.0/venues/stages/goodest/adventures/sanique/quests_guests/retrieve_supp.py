
import law_dictionary

from goodest.shows_v2.recipe_with_goals._ops.for_1_supp import formulate_recipe_with_goals_for_1_supp 
from goodest.adventures.monetary.DB.goodest_inventory.supps.document.find import find_supp
	

def retrieve_supp_quest (packet):


	freight = packet ["freight"]
	
	report_freight = law_dictionary.check (
		return_obstacle_if_not_legit = True,
		allow_extra_fields = True,
		laws = {
			"filters": {
				"required": True,
				"type": dict
			},
			#"goal": {
			#	"required": True,
			#	"type": int
			#}
		},
		dictionary = freight 
	)
	if (report_freight ["advance"] != True):
		return {
			"label": "unfinished",
			"freight": {
				"obstacle": report_freight,
				"obstacle number": 2
			}
		}
	filters = freight ["filters"]
	goal = freight ["goal"]
	
	
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
		return {
			"label": "unfinished",
			"freight": {
				"obstacle": report_filters,
				"obstacle number": 3
			}
		}
	

	try:
		if ("emblem" in filters):
			filters ["emblem"] = int (filters ["emblem"])
	except Exception:	
		return {
			"label": "unfinished",
			"freight": {
				"description": "The emblem couldn't be converted to an integer.",
				"obstacle number": 4
			}
		}

	
	
	if (type (goal) == int):
		supp = formulate_recipe_with_goals_for_1_supp ({
			"supp": {
				"emblem": filters ["emblem"]
			},
			"goal": goal
		})
	else:
		supp = find_supp ({
			"filter": {
				"emblem": filters ["emblem"]
			}
		})	
		
	return {
		"label": "finished",
		"freight": supp
	}