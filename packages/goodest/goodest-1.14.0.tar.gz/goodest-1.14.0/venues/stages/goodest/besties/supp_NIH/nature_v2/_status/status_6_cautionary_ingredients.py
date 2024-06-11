







'''
	python3 status.proc.py besties/supp_NIH/nature_v2/_status/status_6_cautionary_ingredients.py
'''

#----
#
import goodest.besties.supp_NIH.nature_v2 as supp_NIH_nature_v2
import goodest.besties.supp_NIH.examples as NIH_examples
from goodest.besties.supp_NIH.nature_v2.measured_ingredients._ops.seek_name import seek_measure_ingredient_by_name
#
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
#
#
import rich
#
#
import json
import pathlib
from os.path import dirname, join, normpath
#
#----

def check_1 ():	
	supp_1 = supp_NIH_nature_v2.create (
		NIH_examples.retrieve ("tablets/multivitamin_249664.JSON")
	)
	
	def add (path, data):
		this_directory = pathlib.Path (__file__).parent.resolve ()
		example_path = normpath (join (this_directory, path))
		FP = open (example_path, "w")
		FP.write (data)
		FP.close ()
		
	add ("multivitamin_249664.JSON", json.dumps (supp_1, indent = 4))

	trans_fat = seek_name_or_accepts (
		grove = supp_1 ["cautionary ingredients"] ["grove"],
		name_or_accepts = "trans fat"
	)
	assert (len (trans_fat ["natures"]) == 0)
	
	return;
	
checks = {
	"check 1": check_1
}

