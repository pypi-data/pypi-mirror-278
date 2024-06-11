






'''
	python3 status.proc.py "search_goods/status_12_meals.py"
	
'''
#/
#
import copy
import rich
#
#
from goodest.adventures.monetary.quests.search_goods import search_goods	
import pathlib
from os.path import dirname, join, normpath	
from goodest.mixes.drives.etch.bracket import etch_bracket
#
#\

def check_1 ():	
	proceeds = search_goods ({
		"filters": {
			"string": "",
			"include": {
				"food": True,
				"supp": True,
				"meals": True
			},
			"limit": 100
		}
	})

	documents = proceeds ["treasures"]

	treasures = []
	count = 0
	for document in documents:
		treasures.append ({
			"kind": document ['nature'] ['kind'], 
			"emblem": document ['emblem'],
			"lower_case_name": document ['lower_case_name']
		})
		
		count += 1

	this_directory = pathlib.Path (__file__).parent.resolve ()
	the_path = normpath (join (this_directory, "status_12.JSON"))
	etch_bracket (the_path, {
		"treasures": treasures
	})

	print ("""
	
		count:
		
	""", count)

	return;
	
checks = {
	'check 1': check_1
}