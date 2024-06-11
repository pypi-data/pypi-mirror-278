
'''
	This should not make changes to the grove structure.
	
	The only changes it should make is to the individual
	ingredients.
'''

#----
#
import goodest.besties.supp_NIH.nature_v2.measured_ingredients.measured_ingredient as measured_ingredient_builder
import goodest.besties.supp_NIH.nature_v2.measured_ingredients._ops.seek as seek
#
import goodest.besties.supp_NIH.nature_v2._interpret.ingredientRows.for_each as for_each_IR
#
from goodest.adventures.alerting import activate_alert
#
#
import json
#
#----
	
def find_measured_ingredient (measured_ingredients, name):
	def for_each (
		measured_ingredient, 
		indent = 0, 
		parent_measured_ingredient = None
	):		
		if (measured_ingredient ["name"].lower () == name.lower ()):
			return True
		
		return False;

	measured_ingredient = seek.beautifully (
		measured_ingredients = measured_ingredients,
		for_each = for_each
	)
	
	return measured_ingredient;
	
def build (
	form = {},
	ingredientRows = [],
	records = 0
):
	measured_ingredients = []

	def action (ingredient, indent, parent_ingredient):
		measured_ingredient = measured_ingredient_builder.build (
			form,
			NIH_ingredient = ingredient
		)
	
		if (parent_ingredient == None):
			measured_ingredients.append (measured_ingredient)
		else:
			activate_alert ("info", {
				"inclusionary_ingredient name": parent_ingredient ["name"]
			})
		
			measured_ingredient_parent = find_measured_ingredient (
				measured_ingredients,
				name = parent_ingredient ["name"]
			)
			
			measured_ingredient_parent ["unites"].append (measured_ingredient)

		
		return True;

	ingredient = for_each_IR.start (
		ingredient_rows = ingredientRows,
		action = action
	)
	
	return measured_ingredients