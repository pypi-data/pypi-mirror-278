
'''
	python3 status.proc.py besties/food_USDA/nature_v2/_status_v1/status_2.py
'''

#----
#
import goodest.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import goodest.besties.food_USDA.examples as USDA_examples
import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2
import goodest.mixes.insure.equality as equality
#
import json	
#
#----
	
def check_1 ():
	food_data = USDA_examples.retrieve ("branded/Gardein_f'sh_2663758.JSON")
	nature = food_USDA_nature_v2.create (food_data)
	equality.check (nature ["identity"]["FDC ID"], "2663758")

	assert (
		nature ["measures"]["form"] ==
		{
            "unit": "gram",
            "amount": "288",
            "servings": {
                "listed": {
                    "serving size amount": "96",
                    "serving size unit": "GRM"
                },
                "calculated": {
                    "serving size amount": "96",
                    "servings per package": "3",
                    "foodNutrient per package multiplier": "72/25",
                    "labelNutrient per package multiplier": "3"
                }
            }
        }
	)


	equality.check (True, nature ["measures"]["mass"]["ascertained"])
	equality.check ("288", nature ["measures"]["mass"]["per package"]["grams"]["fraction string"])
	equality.check (False, nature ["measures"]["volume"]["ascertained"])
	equality.check (True, nature ["measures"]["energy"]["ascertained"])
	equality.check ("14976/25",	nature ["measures"]["energy"]["per package"]["food calories"]["fraction string"])
	
	
	
	
checks = {
	'check 1': check_1
}