


'''
	python3 status.proc.py besties/supp_NIH/nature_v2/measured_ingredients/_status/status_chia_seeds_214893.py
'''

#----
#
import goodest.besties.supp_NIH.nature_v2 as supp_NIH_nature
from goodest.besties.supp_NIH.nature_v2.measured_ingredients._ops.seek_name import seek_measure_ingredient_by_name
#
import goodest.besties.supp_NIH.examples as NIH_examples
#
#
import json
#
#----

def check_1 ():	
	supp_NIH_example = NIH_examples.retrieve ("other/chia_seeds_214893.JSON")
	measured_ingredients = supp_NIH_nature.create (
		supp_NIH_example,
		return_measured_ingredients_grove = True
	)
	
	measured_ingredient = seek_measure_ingredient_by_name (
		measured_ingredients,
		name = "Phosphorus"
	)
	
	print (json.dumps (measured_ingredient, indent = 4))
	

	
	return;
	
checks = {
	"check 1": check_1
}