


'''
	from goodest.shows_v2.treasure.nature.land._ops.multiply_amount import multiply_land_amount
	multiply_land_amount (
		land = land
	)
'''

'''
	ingredient_scan.land.multiply_amount as multiply_land_amount
	multiply_land_amount.smoothly (
		land = land
	)
'''

'''
	Summary:
		This multiplies the amount of all the ingredient measures.
		
		This multiplies the amount of all the land measures.
				
			course 1: 	This multiplies the land measures times the amount
		
			course 2: 	This aggregates the nutrient measures times into
						an empty land measures object.
						
			equality check between "course 1" and "course 2"
'''

#----
#
from goodest.shows_v2.treasure.nature.land.grove._ops.seek import seek_ingredient_in_grove
from goodest.shows_v2.treasure.nature.land.measures.multiply import multiply_land_measures
#
#
import copy
from fractions import Fraction
import json
#
#----

def multiply_land_amount (
	land = None, 
	amount = None
):
	grove = land ["grove"]
	
	original_land_measures = land ["measures"]
	multiply_land_measures (
		amount = amount,
		measures = land ["measures"]
	)
	
	def for_each (entry):
		nonlocal amount;
	
		natures = entry ["natures"]
		if (len (natures) == 1):		
			entry ["natures"] [0] ["amount"] = str (Fraction (amount));
			multiply_land_measures (
				amount = amount,
				measures = entry ["measures"]
			)
			
			measures_to_merge = copy.deepcopy (entry ["measures"]);
			if ("biological activity" in measures_to_merge):
				del measures_to_merge ["biological activity"]
				
		elif (len (natures) == 0):
			pass;
			
		else:
			print (json.dumps (natures, indent = 4))
			raise Exception ("A nature was found that had more than one.")

		return False		

	seek_ingredient_in_grove (
		grove = grove,
		for_each = for_each
	)
	
