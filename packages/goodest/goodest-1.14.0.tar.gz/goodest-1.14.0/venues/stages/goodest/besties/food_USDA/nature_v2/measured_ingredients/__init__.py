

from .measured_ingredient import build_measured_ingredient

def build_measured_ingredients (
	foodNutrients = [],
	mass_and_volume = {},
	form = {},
	
	records = 0
):
	measured_ingredients_list = []

	for USDA_food_nutrient in foodNutrients:
		measured_ingredient = build_measured_ingredient (
			USDA_food_nutrient,
			mass_and_volume,
			form,
			
			records = 0
		)
	
		measured_ingredients_list.append (measured_ingredient)

	
	return measured_ingredients_list