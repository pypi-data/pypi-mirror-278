



'''
	python3 status.proc.py "search_goods/status_09_obtain_string.py"
'''

#/
#
from goodest.adventures.monetary.quests.search_goods import search_goods	
from goodest.mixes.drives.etch.bracket import etch_bracket
#
#
import copy
import rich
#
#
import pathlib
from os.path import dirname, join, normpath	
#
#\

def check_1 ():
	proceeds = search_goods ({
		"filters": {
			"string": "vegan",
			"include": {
				"food": True,
				"supp": True
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
			"lower_case_name": document ['lower_case_name'],
			"stats": document ["stats"]
		})
		
		count += 1
		
	assert (len (treasures) == 27), len (treasures)
	assert (treasures [0] ["stats"] ["after"] == 26), treasures [0]
	assert (treasures [0] ["stats"] ["before"] == 0), treasures [0]
	assert (treasures [26] ["stats"] ["after"] == 0), treasures [26]
	assert (treasures [26] ["stats"] ["before"] == 26), treasures [26]
		
	print ()
	print (count, "documents returned")	

	return;
	
checks = {
	'check 1': check_1
}