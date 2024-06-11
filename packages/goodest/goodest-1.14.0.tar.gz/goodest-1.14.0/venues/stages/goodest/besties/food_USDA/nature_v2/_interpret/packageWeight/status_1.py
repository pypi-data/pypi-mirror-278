

'''
	python3 status.proc.py "besties/food_USDA/nature/packageWeight/status_1.py"
'''

from goodest.besties.food_USDA.nature_v2._interpret.packageWeight import calc_package_weight

import goodest.besties.food_USDA.examples as USDA_examples

from biotech.topics.show.variable import show_variable

def check_1 ():
	walnuts_1882785 = USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	mass_and_volume = calc_package_weight (walnuts_1882785)
	
	show_variable ({
		"mass_and_volume": mass_and_volume
	})
	
	assert (mass_and_volume ["mass"]["per package"]["grams"]["fraction string"] == "454")
	assert (mass_and_volume ["mass"]["per package"]["grams"]["decimal string"] == "454.00")	
	
	assert (mass_and_volume ["volume"]["per package"]["liters"]["fraction string"] == "?")
	assert (mass_and_volume ["volume"]["per package"]["liters"]["decimal string"] == "?")

def check_2 ():
	beet_juice_2642759 = USDA_examples.retrieve ("branded/beet_juice_2642759.JSON")
	mass_and_volume = calc_package_weight (beet_juice_2642759)
	
	
	show_variable ({
		"mass_and_volume": mass_and_volume
	})
	
	assert (mass_and_volume ["mass"]["per package"]["grams"]["fraction string"] == "?")
	assert (mass_and_volume ["mass"]["per package"]["grams"]["decimal string"] == "?")	
	
	assert (mass_and_volume ["volume"]["per package"]["liters"]["fraction string"] == "71/200")
	assert (mass_and_volume ["volume"]["per package"]["liters"]["decimal string"] == "0.36")
	
		
	
checks = {
	"check 1": check_1,
	"check 2": check_2	
}