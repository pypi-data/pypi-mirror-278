
'''
	python3 status.proc.py besties/food_USDA/nature_v2/_status_v1/status_3.py
'''

from goodest.mixes.insure.override_print import override_print
import goodest.mixes.insure.equality as equality

import goodest.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import goodest.besties.food_USDA.examples as USDA_examples
import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
from rich import print_json
	
def check_1 ():
	walnuts_1882785 = USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	assertions_foundational.run (walnuts_1882785)
	nature = food_USDA_nature_v2.create (walnuts_1882785)
	equality.check (nature ["identity"]["FDC ID"], "1882785")
	
	print_json (data = nature ["essential nutrients"] ["measures"])
	
	energy = seek_name_or_accepts (
		grove = nature ["essential nutrients"] ["grove"],
		name_or_accepts = "energy",
		return_none_if_not_found = True
	)
	
	print_json (data = energy)
	
checks = {
	'check 1': check_1
}