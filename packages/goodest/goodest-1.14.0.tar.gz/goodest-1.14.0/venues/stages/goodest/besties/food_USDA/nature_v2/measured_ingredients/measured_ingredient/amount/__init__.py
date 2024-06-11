


'''
	To calculate the labelNutrient amount, 
	the labelNutrient name needs to be 
	equated with the foodNutrient name.
	
		This can probably be done with the
		"(essential) relevant nutrients" show.
'''

import goodest.measures._interpret.unit_kind as unit_kind

from .per_package.food_nutrient import calc_food_nutrient
# from .per_package.label_nutrient import calc_label_nutrient

from .biological_activity import calc_biological_activity
from .energy import calc_energy
from .mass import calc_mass

from fractions import Fraction

def calc_amount (
	USDA_food_nutrient,
	mass_and_volume,
	form,

	USDA_label_nutrient = {},
	records = 1
):	
	if (
		mass_and_volume ["mass"]["ascertained"] or
		mass_and_volume ["volume"]["ascertained"]
	):	
		amount_per_package__from_portion = calc_food_nutrient (
			form,
			USDA_food_nutrient
		)
	
		assert ("unitName" in USDA_food_nutrient ["nutrient"])
		unit_name = USDA_food_nutrient ["nutrient"] ["unitName"]
		
		if (unit_kind.calc (unit_name) == "mass"):
			return calc_mass (
				amount_per_package__from_portion,
				unit_name,
				
				USDA_food_nutrient,
				mass_and_volume,
				
				records
			)
		
			
		elif (unit_kind.calc (unit_name) == "biological activity"):
			return calc_biological_activity (
				amount_per_package__from_portion,
				unit_name,
				
				USDA_food_nutrient,
				mass_and_volume,
				
				records
			)
			
		elif (unit_kind.calc (unit_name) == "energy"):		
			return calc_energy (
				amount_per_package__from_portion,
				unit_name,
				
				USDA_food_nutrient,
				mass_and_volume,
				
				records
			)
			
		else:
			raise Exception (f"""
			
				The unit kind of unit '{ unit_name }' was 
				not accounted for.
			
			""")
		
	return {}

