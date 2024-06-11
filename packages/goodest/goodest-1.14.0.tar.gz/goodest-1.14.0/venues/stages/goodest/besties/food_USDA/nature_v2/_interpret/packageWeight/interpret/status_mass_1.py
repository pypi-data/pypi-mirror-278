

'''
	python3 insurance.py "besties/food_USDA/interpret/packageWeight/interpret/status_1.py"
'''

'''
	Sometimes when multiple values, one of the values is rounded.
		prefer grams or prefer ounces?
'''

import json

from goodest.besties.food_USDA.nature_v2._interpret.packageWeight.interpret import interpret_amount

from biotech.topics.show.variable import show_variable

def check_1 ():	
	proceeds = interpret_amount ("12 oz")
	calculated = proceeds.calculated;
	listed = proceeds.listed;
	
	show_variable ({
		"calculated": calculated
	})
	
	# 12 * 28.349523125 = 340.1942775
	assert (calculated ['grams'] == '23939044084102737/70368744177664')
	assert (calculated ['pounds'] == '3/4')


def check_2 ():
	proceeds = interpret_amount ("12 oz/340 g")	
	calculated = proceeds.calculated;
	listed = proceeds.listed;
	
	assert (calculated ['grams'] == '340')
	assert (calculated ['pounds'] == '5981343255101440/7979681361367579')	
	
	
def check_3 ():	
	proceeds = interpret_amount ("1 g")
	calculated = proceeds.calculated;
	listed = proceeds.listed;

	show_variable ({
		"calculated": calculated
	})

	assert (calculated ['grams'] == '1')
	
	#
	#	0.002204622621848776 = 1 / 453.59237
	#
	assert (calculated ['pounds'] == '17592186044416/7979681361367579')	

	return
	
	
checks = {
	"check 1": check_1,
	"check 2": check_2,
	"check 3": check_3
}