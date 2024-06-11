




'''
	Details about this can be found in "goodest.shows_v2.treasure.nature".
'''

'''
	from goodest.besties.food_USDA.nature_v2._ops.retrieve import retrieve_parsed_USDA_food
	out_packet = retrieve_parsed_USDA_food ({
		"FDC_ID": 1
	})
'''

'''
	import goodest.besties.food_USDA.deliveries.one as retrieve_1_food
	import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2
	
	USDA_food = retrieve_1_food.presently (
		FDC_ID,
		API_ellipse = ""
	)
	USDA_food_data = USDA_food ["data"]
	USDA_food_source = USDA_food ["source"]

	nature = food_USDA_nature_v2.create (
		USDA_food_data
	)
'''



#----
#
import goodest.shows_v2.treasure.nature._assertions as natures_v2_assertions
#
from ._interpret.packageWeight import calc_package_weight
from .measures.form import calculate_form
from .measured_ingredients import build_measured_ingredients
from .measured_ingredients._ops.seek import seek_measured_ingredient
from .unmeasured_ingredients import build_unmeasured_ingredients
from .land import build_land
#
#
import copy
from fractions import Fraction
import json
#
#----


def create (
	food_USDA,
	
	return_measured_ingredients_list = False,
	
	records = 0
):
	include_ounces = False
	include_grams = True

	nature = {
		"kind": "food",
		"identity": {
			"name":	food_USDA ["description"],
			"FDC ID": str (food_USDA ["fdcId"]),
			"UPC": food_USDA ["gtinUpc"],
			"DSLD ID": ""
		},
		"brand": {
			"name":	food_USDA ["brandName"],
			"owner": food_USDA ["brandOwner"]
		},
		"measures": {
			"form": {},
			"energy": {
				"ascertained": False,
				"per package": {}
			}
		}
	}
	
	servingSizeUnit = food_USDA ["servingSizeUnit"]

	'''
		treasure exclusive modifications.
	'''
	if (food_USDA ["servingSizeUnit"] == "MLT" and str (food_USDA ["fdcId"]) == "2642759"):
		servingSizeUnit = "mL"
		
	'''
		This calculates the mass and or volume
		from the "packageWeight".
		
		Neither of these are necessary
		for the recipe calculations,
		since supplements don't always
		have these.
	'''
	mass_and_volume = calc_package_weight (food_USDA);
	volume = mass_and_volume ["volume"]
	mass = mass_and_volume ["mass"]
	nature ["measures"]["mass"] = mass
	nature ["measures"]["volume"] = volume

	'''
		{
			"unit": "liter",
			"amount": "473/1000",
			"servings": {
				"listed": {
					"serving size amount": "240",
					"serving size unit": "ml"
				},
				"calculated": {
					"serving size amount": "6/25",
					"servings per package": "473/240"
				}
			}
		}
	'''
	form = calculate_form (
		servingSize = food_USDA ["servingSize"], 
		servingSizeUnit = servingSizeUnit, 
		mass_and_volume = mass_and_volume
	);	
	nature ["measures"] ["form"] = form;
	servings_per_package = form ["servings"]["calculated"]["servings per package"];


	'''
		Measured Ingredients List:
	
			This builds the measured 
			ingredients list.
	'''
	assert ("foodNutrients" in food_USDA)
	measured_ingredients = build_measured_ingredients (
		foodNutrients = food_USDA ["foodNutrients"],
		
		mass_and_volume = mass_and_volume,
		form = form,
		
		records = 0
	)
	nature ["measured ingredients"] = measured_ingredients
	if (return_measured_ingredients_list):
		return nature ["measured ingredients"]
	
	
	
	'''
		Unmeasured Ingredients List:
			# unreported measurements ingredients
	'''
	nature ["unmeasured ingredients"] = build_unmeasured_ingredients (
		food_USDA = food_USDA
	)
	
	
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
	

	'''
		Extract the "energy" or "calories" from the measured_ingredients (list)
		and "energy" to the "measured" section.
	'''
	energy = seek_measured_ingredient ("energy", measured_ingredients)
	assert (type (energy) == dict), energy
	measured_ingredients.remove (energy)
	nature ["measures"]["energy"]["ascertained"] = True
	nature ["measures"]["energy"]["per package"] = energy ["measures"]["energy"]["per package"]
	assert (type (nature ["measures"]["energy"]) == dict)	

	natures_v2_assertions.run (nature)

	return nature