
'''
from goodest.besties.food_USDA.nature_v2.measured_ingredients._ops.seek import seek_measured_ingredient
potassium = seek_measured_ingredient ("Potassium, K", measured_ingredients)
'''

#import goodest.besties.food_USDA.nature.measured_ingredients_list.for_each as mil_for_each

from ..for_each import for_each_measured_ingredient

def seek_measured_ingredient (name, measured_ingredients_list):
	name = name.lower ()

	def action (ingredient):
		nonlocal name;
		
		#print ("ingredient:", ingredient)
	
		if (ingredient ["name"].lower () == name):
			return False
			
		return True

	return for_each_measured_ingredient (
		measured_ingredients_list = measured_ingredients_list,
		action = action
	)
	
