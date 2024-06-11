



'''
	python3 status.proc.py besties/supp_NIH/nature_v2/_status/status_1_info.py
'''

#----
#
import goodest.besties.supp_NIH.nature_v2 as supp_NIH_nature_v2
import goodest.besties.supp_NIH.examples as NIH_examples
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
		NIH_examples.retrieve ("powder/mane_270619.JSON")
	)
	
	def add (path, data):
		this_directory = pathlib.Path (__file__).parent.resolve ()
		example_path = normpath (join (this_directory, path))
		FP = open (example_path, "w")
		FP.write (data)
		FP.close ()
		
	add ("mane_270619_nature.JSON", json.dumps (supp_1, indent = 4))
	
	
	rich.print_json (data = {
		"supp_1:": supp_1
	})
	
	assert (
		supp_1 ["identity"] == {
			"name": "Organic Lion's Mane Mushroom 1 g Unflavored",
			"FDC ID": "",
			"UPC": "8 10014 67049 2",
			"DSLD ID": "270619"
		}
	)
	assert (
		supp_1 ["brand"] == {
			"name": "Nutricost"
		}
	)
	
	return;
	
checks = {
	"check 1": check_1
}