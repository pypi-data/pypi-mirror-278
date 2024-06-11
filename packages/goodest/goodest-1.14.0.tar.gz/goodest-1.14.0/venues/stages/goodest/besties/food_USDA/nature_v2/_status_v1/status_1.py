


'''
	python3 status.proc.py besties/food_USDA/nature_v2/_status_v1/status_1.py
'''


#----
#
from goodest.mixes.insure.override_print import override_print
import goodest.mixes.insure.equality as equality
import goodest.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import goodest.besties.food_USDA.examples as USDA_examples
import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
#
#
import ships
#	
#
import json		
#
#----
	
def check_1 ():
	walnuts_1882785 = USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	assertions_foundational.run (walnuts_1882785)
	nature = food_USDA_nature_v2.create (walnuts_1882785)

	equality.check (nature ["identity"]["FDC ID"], "1882785")

	assert (
		nature ["measures"]["form"] ==
		{
            "unit": "gram",
            "amount": "454",
            "servings": {
                "listed": {
                    "serving size amount": "28",
                    "serving size unit": "g"
                },
                "calculated": {
                    "serving size amount": "28",
                    "servings per package": "227/14",
                    "foodNutrient per package multiplier": "227/50",
                    "labelNutrient per package multiplier": "227/14"
                }
            }
        }
	), nature ["measures"]["form"]


	equality.check (nature ["measures"]["mass"]["ascertained"], True)
	equality.check (
		nature ["measures"]["mass"]["per package"]["grams"]["fraction string"], 
		"454"
	)
	
	equality.check (nature ["measures"]["volume"]["ascertained"], False)
	
	equality.check (nature ["measures"]["energy"]["ascertained"], True)
	equality.check (
		nature ["measures"]["energy"]["per package"]["food calories"]["fraction string"], 
		"154133/50"
	)
	
	protein = seek_name_or_accepts (
		grove = nature ["essential nutrients"]["grove"],
		name_or_accepts = "protein"
	)
	
	'''
	protein = grove_seek_measured_ingredient_name.politely (
		grove = nature ["essential nutrients"]["grove"],
		measured_ingredient_name = "protein"
	)
	'''
	
	'''
	"measures": {
        "mass + mass equivalents": {
            "per recipe": {
                "grams": {
                    "fraction string": "456528486851663599/7036874417766400"
                }
            },
            "portion of grove": {
                "fraction string": "32178219337562192000/210338053544551424737"
            }
        }
    }
	'''
	
	assert (
		protein ["measures"] ["mass + mass equivalents"] ["portion of grove"] ["fraction string"] ==
		"32178219337562192000/210338053544551424737"
	)
	
	
	#ships.show ("protein:", protein)
	
	
checks = {
	'check 1': check_1
}