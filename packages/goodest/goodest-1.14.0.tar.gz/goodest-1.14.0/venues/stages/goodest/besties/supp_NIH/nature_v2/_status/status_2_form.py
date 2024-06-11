



'''
	python3 status.proc.py besties/supp_NIH/nature_v2/_status/status_2_form.py
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
		len (supp_1 ["statements"]) == 15
	), len (supp_1 ["statements"])
	
	assert (
		supp_1 ["measures"] ["form"] == {
			"unit": "gram",
			"amount per package": "113",
			"serving size amount": "1",
			"amount is an estimate": "?"
		}
	)
	
	return;
	
checks = {
	"check 1": check_1
}