
'''
	python3 status.proc.py besties/food_USDA/nature_v2/_status_v1/status_2412474.py
'''

#----
#
from goodest.mixes.insure.override_print import override_print
import goodest.mixes.insure.equality as equality
import goodest.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import goodest.besties.food_USDA.examples as USDA_examples
import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2

#
#
from rich import print_json
#
#----
	
def check_1 ():
	beet_juice_2412474 = USDA_examples.retrieve ("branded/beet_juice_2412474.JSON")
	assertions_foundational.run (beet_juice_2412474)
	nature = food_USDA_nature_v2.create (beet_juice_2412474)
	

checks = {
	'check 1': check_1
}