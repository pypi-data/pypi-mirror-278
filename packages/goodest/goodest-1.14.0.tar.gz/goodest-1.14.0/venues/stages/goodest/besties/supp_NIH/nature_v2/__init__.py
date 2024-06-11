

'''
	Limitations:
		1. The package mass is not always known.
'''

'''
	Differences from food:
		1a. The ingredients are formatted as a grove
			instead of a list.
			
		1b. The measured ingredients need to be shown
			on the supplement screen.
'''

#----
#
import goodest.besties.supp_NIH.nature_v2.form.unit as form_unit_calculator
import goodest.besties.supp_NIH.nature_v2.form.amount as form_amount_calculator
import goodest.besties.supp_NIH.nature_v2.form.serving_size.amount as serving_size_amount_calculator
import goodest.besties.supp_NIH.nature_v2.measured_ingredients as measured_ingredients_builder
from .land import build_land
#
import goodest.shows_v2.treasure.nature._assertions as natures_v2_assertions
#
#
from fractions import Fraction
import json
import copy
#
#----


def create (
	supp_NIH,
	return_measured_ingredients_grove = False
):
	identity = {
		"name":	supp_NIH ["fullName"],
		"FDC ID": "",
		"UPC": supp_NIH ["upcSku"],
		"DSLD ID": str (supp_NIH ["id"])
	}
	
	nature = {
		"kind": "supp",
		"identity": identity,
		"brand": {
			"name":	supp_NIH ["brandName"]
		},
		"measures": {
			"form": {
				"unit": ""
			},
		}
	}
	
	if ("statements" in supp_NIH):
		nature ["statements"] = supp_NIH ["statements"]
	
	
	''''
		Form
	'''
	assert ("ingredientRows" in supp_NIH)
	assert ("netContents" in supp_NIH)
	assert ("physicalState" in supp_NIH)
	assert ("servingSizes" in supp_NIH)
	net_contents = supp_NIH ["netContents"]	
	physical_state = supp_NIH ["physicalState"]
	serving_sizes = supp_NIH ["servingSizes"]
	servings_per_container = supp_NIH ["servingsPerContainer"]
	ingredientRows = supp_NIH ["ingredientRows"]
	
	form_unit = form_unit_calculator.calc (
		net_contents = net_contents,
		physical_state = physical_state,
		serving_sizes = serving_sizes,
		ingredient_rows = ingredientRows
	)
	form_amount = form_amount_calculator.calc (
		net_contents = net_contents,
		form_unit = form_unit
	)
	
	'''
		Every shape listed might already have this
		in the shape data.
	'''
	serving_size_amount = serving_size_amount_calculator.calc (
		net_contents = net_contents,
		serving_sizes = serving_sizes,
		servings_per_container = servings_per_container,
		form_unit = form_unit,
		ingredientRows = ingredientRows
	)
	nature ["measures"]["form"]["amount per package"] = form_amount;
	nature ["measures"]["form"]["unit"] = form_unit
	nature ["measures"]["form"]["serving size amount"] = serving_size_amount
	
	
	'''
		Is the servings per container an estimate,
		and therefore the nutrient amounts are estimates?
	'''
	if (form_unit == "gram"):
		nature ["measures"]["form"]["amount is an estimate"] = "?"
	
		is_an_estimate = Fraction (form_amount) != (
			Fraction (servings_per_container) *
			Fraction (serving_size_amount)
		)
		if (is_an_estimate):
			nature  ["measures"]["form"]["amount is an estimate"] = "yes"
	
	
	'''
		Measured Ingredients
	'''
	measured_ingredients_grove = measured_ingredients_builder.build (
		ingredientRows = supp_NIH ["ingredientRows"],
		form = nature ["measures"]["form"]
	)
	if (return_measured_ingredients_grove):
		return measured_ingredients_grove;

	nature ["measured ingredients"] = measured_ingredients_grove;
	
	'''
		Unmeasured Ingredients
	'''
	nature ["unmeasured ingredients"] = {
		"list": supp_NIH ["otheringredients"] ["ingredients"]
	}
	

	'''
		Essential Nutrients
	'''
	'''	
		essential nutrients grove steps:
		
			1. build an "essential nutrients grove"
			2. for each nutrient
	'''	
	[ essential_nutrients_land, not_added ] = build_land (
		copy.deepcopy (nature ["measured ingredients"]),
		
		collection = "essential_nutrients",
		identity = nature ["identity"]
	)
	nature ["essential nutrients"] = essential_nutrients_land
	
	'''
		Cautionary Ingredients
	'''
	[ cautionary_ingredients_land, not_added ] = build_land (
		copy.deepcopy (nature ["measured ingredients"]),
		
		collection = "cautionary_ingredients",
		identity = nature ["identity"]
	)
	nature ["cautionary ingredients"] = cautionary_ingredients_land
	
	natures_v2_assertions.run (nature)
	
	return nature