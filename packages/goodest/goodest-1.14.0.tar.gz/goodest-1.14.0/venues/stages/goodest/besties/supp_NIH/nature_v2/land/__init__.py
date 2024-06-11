
'''
	import goodest.besties.supp_NIH.nature.ingredient_scan as calculate_ingredient_scan
	calculate_ingredient_scan.eloquently (
		measured_ingredients_grove
	)
'''

#----
#
from goodest.shows_v2.treasure.nature.land._ops.develop import develop_land
from goodest.shows_v2.treasure.nature.land._ops.add_measured_ingredient import add_measured_ingredient
from goodest.shows_v2.treasure.nature.land._ops.cultivate import cultivate_land
from goodest.adventures.alerting import activate_alert
#
import goodest.besties.supp_NIH.nature_v2.measured_ingredients._ops.seek as seek
#
#
from ships.flow.simultaneous_v2 import simultaneously_v2
from biotech.topics.show.variable import show_variable
#
#
import json
#
#----

def build_land (
	measured_ingredients = [],
	collection = "",
	identity = {},
	records = 1
):
	land = develop_land ({
		"collection": collection 
	})
	
	grove = land ["grove"]
	natures = land ["natures"]
		
	natures.append ({
		"amount": "1",
		"identity": identity
	})	
	
	not_added = []
	
	def move (measured_ingredient):
		activate_alert ("info", {
			"measured_ingredient": measured_ingredient ["name"]
		})

		found = add_measured_ingredient (
			#
			#	This is a reference to the land.
			#
			land = land,
			
			amount = 1,
			source = identity,
			measured_ingredient = measured_ingredient,
			
			return_False_if_not_found = True
		)
		if (not found):
			not_added.append (measured_ingredient ["name"])


		return ""


	proceeds = simultaneously_v2 (
		items = measured_ingredients,
		capacity = 100,
		move = move
	)
	if (len (proceeds ["anomalies"]) != 0):
		problems = []
		for anomaly in proceeds ["anomalies"]:
			problems.append (
				proceeds ["results"] [ anomaly ]
			)
				
		problems_string = json.dumps (problems, indent = 4)
		
		raise Exception (f"""
		
			Land essential nutrient additions produced an anomly or anomlies.
			
			'{ problems_string }'
					
		""");
	
	cultivate_land (
		land = land
	)
	
	return [ land, not_added ];