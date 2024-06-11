
'''
	python3 status.proc.py besties/food_USDA/nature_v2/_status/status_2_measures.py
'''


import goodest.mixes.insure.equality as equality

import goodest.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import goodest.besties.food_USDA.examples as USDA_examples

import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2

import ships

import json		

import rich

def check_1 ():
	walnuts_1882785 = USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	assertions_foundational.run (walnuts_1882785)
	
	nature = food_USDA_nature_v2.create (walnuts_1882785)
	rich.print_json (data = nature)

	equality.check (nature ["measures"] ["form"] ["unit"], "gram")
	equality.check (nature ["measures"] ["form"] ["amount"], "454")
	
	
	'''
		servings
	'''
	equality.check (
		nature ["measures"] ["form"] ["servings"] ["listed"] ["serving size amount"], 
		"28"
	)
	equality.check (
		nature ["measures"] ["form"] ["servings"] ["listed"] ["serving size unit"], 
		"g"
	)
	equality.check (
		nature ["measures"] ["form"] ["servings"] ["calculated"] ["serving size amount"], 
		"28"
	)
	equality.check (
		nature ["measures"] ["form"] ["servings"] ["calculated"] ["servings per package"], 
		"227/14"
	)
	equality.check (
		nature ["measures"] ["form"] ["servings"] ["calculated"] ["foodNutrient per package multiplier"], 
		"227/50"
	)
	equality.check (
		nature ["measures"] ["form"] ["servings"] ["calculated"] ["labelNutrient per package multiplier"], 
		"227/14"
	)
	
	'''
		mass
	'''
	equality.check (nature ["measures"] ["mass"] ["ascertained"], True)
	equality.check (nature ["measures"] ["mass"] ["per package"] ["grams"] ["fraction string"], "454")
	equality.check (nature ["measures"] ["mass"] ["per package"] ["grams"] ["decimal string"], "454.00")



	

	
checks = {
	'food nature_v2 "measures with mass" check 1': check_1
}

