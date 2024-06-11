



'''
	summary:
		This builds a land from 
		the measured ingredients.
'''

#----
#
from goodest.shows_v2.treasure.nature.land._ops.develop import develop_land
from goodest.shows_v2.treasure.nature.land._ops.add_measured_ingredient import add_measured_ingredient
from goodest.shows_v2.treasure.nature.land._ops.cultivate import cultivate_land
#
from goodest.shows_v2.treasure.nature.land.grove._ops.nurture import nurture_grove
#
from goodest.adventures.monetary.DB.goodest_tract.connect import connect_to_goodest_tract
from goodest.adventures.monetary.DB.goodest_tract._land.find_name import find_ingredient_by_name
#
#
from ships.flow.simultaneous_v2 import simultaneously_v2
from biotech.topics.show.variable import show_variable
#
#
import rich
#
#
import json	
#
#----

def build_land (
	measured_ingredients = [],
	
	collection = "",
	
	identity = {},
	records = 0
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
	'''
		
	'''
	def move (measured_ingredient):
		if ("name" not in measured_ingredient):
			raise Exception ("A name was not found in", measured_ingredient)
	
		name = measured_ingredient ['name']
		if (records >= 1):
			show_variable (f"measured_ingredient: { name }")
	
		added = add_measured_ingredient (
			#
			#	This is a reference to the land.
			#
			land = land,
			
			amount = 1,
			source = identity,
			measured_ingredient = measured_ingredient,
			
			return_False_if_not_found = True
		)
		
		
		if (added == False):
			not_added.append (measured_ingredient)


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
				
		
		raise Exception ("""
		
			Land essential nutrient additions produced an anomly or anomlies.
			
			'{ json.dumps (problems, indent = 4) }'
					
		""");
	
	
	#rich.print_json (data = {
	#	"land": land
	#})
	#with open ('output.json', 'w') as file:
	#	file.write (json.dumps (land, indent = 4))
		
	cultivate_land (
		land = land
	)
	

	
	
	

	

	return [ land, not_added ];