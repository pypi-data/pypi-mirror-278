

'''
	from goodest.besties.supp_NIH.nature_v2.measured_ingredients._ops.seek_name import seek_measure_ingredient_by_name
	seek_measure_ingredient_by_name (
		measured_ingredients,
		name
	)
'''

import goodest.besties.supp_NIH.nature_v2.measured_ingredients._ops.seek as seek

def seek_measure_ingredient_by_name (
	measured_ingredients, 
	name
):
	def for_each (
		measured_ingredient, 
		indent = 0, 
		parent_measured_ingredient = None
	):
		return measured_ingredient ["name"] == name

	return seek.beautifully (
		measured_ingredients = measured_ingredients,
		for_each = for_each
	)

