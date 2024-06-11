
'''
	python3 status.proc.py besties/food_USDA/nature_v2/_status/status_3_measured_ingredients.py
'''

#----
#
import goodest.mixes.insure.equality as equality
import goodest.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import goodest.besties.food_USDA.examples as USDA_examples
import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2
from goodest.besties.food_USDA.nature_v2.measured_ingredients._ops.seek import seek_measured_ingredient

#
#
import ships
#
#
import rich
#
#
import json		
#
#----

def check_1 ():
	walnuts_1882785 = USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	assertions_foundational.run (walnuts_1882785)
	
	measured_ingredients = food_USDA_nature_v2.create (
		walnuts_1882785,
		return_measured_ingredients_list = True
	)
	#rich.print_json (data = nature)

	potassium = seek_measured_ingredient ("Potassium, K", measured_ingredients)
	rich.print_json (data = potassium)
	#equality.check (nature ["measures"] ["form"] ["unit"], "gram")

	equality.check (potassium ["name"], "Potassium, K")
	equality.check (
		potassium ["measures"] ["mass + mass equivalents"] ["per package"] ["grams"] ["fraction string"] , 
		"97383/50000"
	)
	
	equality.check (len (measured_ingredients), 17)

	'''
	[intro] [aggregator] {
	[intro] [aggregator]   "name": "Potassium, K",
	[intro] [aggregator]   "measures": {
	[intro] [aggregator]     "mass + mass equivalents": {
	[intro] [aggregator]       "per package": {
	[intro] [aggregator]         "listed": [
	[intro] [aggregator]           "1947.660",
	[intro] [aggregator]           "mg"
	[intro] [aggregator]         ],
	[intro] [aggregator]         "grams": {
	[intro] [aggregator]           "scinote string": "1.9477e+0",
	[intro] [aggregator]           "decimal string": "1.948",
	[intro] [aggregator]           "fraction string": "97383/50000"
	[intro] [aggregator]         }
	[intro] [aggregator]       }
	[intro] [aggregator]     }
	[intro] [aggregator]   }
	[intro] [aggregator] }
	'''

	
checks = {
	'food nature_v2 "measures with mass" check 1': check_1
}

