
'''
	python3 status.proc.py besties/food_USDA/nature_v2/_status/status_1_description.py
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

	equality.check (nature ["kind"], "food")

	equality.check (nature ["identity"]["name"], "WALNUTS HALVES & PIECES, WALNUTS")
	equality.check (nature ["identity"]["FDC ID"], "1882785")
	equality.check (nature ["identity"]["UPC"], "099482434618")
	equality.check (nature ["identity"]["DSLD ID"], "")
	
	equality.check (nature ["brand"]["name"], "365 WHOLE FOODS MARKET")
	equality.check (nature ["brand"]["owner"], "Whole Foods Market, Inc.")


	#rich.print_json (data = nature)

	
checks = {
	'food nature_v2 "kind, identity, and brand" check 1': check_1
}

