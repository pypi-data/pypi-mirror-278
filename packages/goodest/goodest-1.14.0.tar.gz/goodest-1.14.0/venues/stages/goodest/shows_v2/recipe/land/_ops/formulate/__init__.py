



'''
	from goodest.shows_v2.recipe.land._ops.formulate import formulate_land_recipe
	recipes = formulate_land_recipe ({
		"collection": "essential_nutrients",
		"land kind": "essential nutrients",
		
		"natures_with_amounts": [
			[ nature_1, amount_1 ],
			[ nature_2, amount_2 ]
		]		
	})
'''

'''
	Goals:
		Figure out what "land kind" is.
'''

#----
#
from goodest.shows_v2.treasure.nature.land._ops.develop import develop_land
from goodest.shows_v2.treasure.nature.land._ops.multiply_amount import multiply_land_amount
from goodest.shows_v2.treasure.nature.land._ops.calculate_portions import calculate_portions
#
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
from goodest.shows_v2.treasure.nature.land.grove._ops.seek import seek_ingredient_in_grove
#
from goodest.shows_v2.treasure.nature.land.measures.merge import merge_land_measures 
#
from goodest.adventures.alerting.parse_exception import parse_exception
from goodest.adventures.alerting import activate_alert
#
#
import json
import copy
#
#----

def formulate_land_recipe (packet):
	natures_with_amounts = packet ["natures_with_amounts"]
	collection = packet ["collection"]
	land_kind = packet ["land kind"]

	land_recipe = develop_land ({
		"collection": collection
	})
	
	
	
	for nature_with_amounts in natures_with_amounts:
		nature_amount = nature_with_amounts [1];
		land_treasure = copy.deepcopy (
			nature_with_amounts [0] [ land_kind ]
		)
	
		land_treasure_measures = land_treasure ["measures"]
		land_treasure_grove = land_treasure ["grove"]
	
		land_recipe ["natures"].append (
			land_treasure ["natures"] [0]
		)
		
		'''
			This multiplies the land measures 
			and the land grove measures, then
			adds them to the land_recipe measures.
		'''
		multiply_land_amount (
			amount = nature_amount,
			land = land_treasure
		)
		merge_land_measures (
			land_recipe ["measures"],
			land_treasure ["measures"]
		)
		
		
		'''
			objective:
				for each in the land grove:
					1. merge the treasure measures into the land_recipe ingredient measures
					2. append the treasure nautres to the land_recipe ingredient natures
		'''
		def for_each (treasure_ingredient):
			land_recipe_grove_ingredient = seek_name_or_accepts (
				grove = land_recipe ["grove"],
				name_or_accepts = treasure_ingredient ["info"] ["names"] [0]
			)
			merge_land_measures (
				land_recipe_grove_ingredient ["measures"],
				treasure_ingredient ["measures"]
			)
			
			assert (len (treasure_ingredient ["natures"]) <= 1);
			
			if (len (treasure_ingredient ["natures"]) == 1):
				land_recipe_grove_ingredient ["natures"].append (
					treasure_ingredient ["natures"] [0]
				) 
					
			return False		
		
		seek_ingredient_in_grove (
			grove = land_treasure ["grove"],
			for_each = for_each
		)
		
	calculate_portions (
		land = land_recipe
	)
	
	return land_recipe