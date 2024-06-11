



'''
	python3 status.proc.py shows_v2/recipe/_ops/formulate/**/status_*.py
'''


'''
	from goodest.besties.food_USDA.nature_v2._ops.retrieve import retrieve_parsed_USDA_food
	food_1 = retrieve_parsed_USDA_food ({
		"FDC_ID": 1
	})

	from goodest.shows_v2.recipe._ops.formulate import formulate_recipe
	recipes = formulate_recipe ({
		"natures_with_amounts": [
			[ food_1, 1 ],
			[ ]
		]	
	})
	
	# recipes ["essential nutrients"]
	# recipes ["cautionary ingredients"]
'''

'''
	summary:
		This merges the land measures into 
		the essential_nutrients_recipe measures.
	
	objective:
		merge the land { ingredient } measures into 
		the essential_nutrients_recipe ingredient measures. 
'''



from goodest.shows_v2.recipe.land._ops.formulate import formulate_land_recipe

def formulate_recipe (packet):
	natures_with_amounts = packet ["natures_with_amounts"]

	return {
		'essential nutrients': formulate_land_recipe ({
			"collection": "essential_nutrients",
			"land kind": "essential nutrients",
			
			"natures_with_amounts": natures_with_amounts	
		}),
		'cautionary ingredients': formulate_land_recipe ({
			"collection": "cautionary_ingredients",
			"land kind": "cautionary ingredients",
			
			"natures_with_amounts": natures_with_amounts
		})
	}