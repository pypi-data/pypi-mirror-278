





'''
	python3 status.proc.py "search_goods/status_11_pomegranate.py"
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
			"string": "",
			"include": {
				"food": True,
				"supp": True
			},
			"limit": 10,
			"after": {
				"emblem": 32,
				"kind": "food",
				"name": "POMEGRANATE JUICE, POMEGRANATE"
			}
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
		
	assert (len (treasures) == 10), len (treasures)
	assert (treasures [0] ["stats"] ["after"] == 32), treasures [0]
	assert (treasures [0] ["stats"] ["before"] == 24), treasures [0]
	assert (treasures [9] ["stats"] ["after"] == 23), treasures [9]
	assert (treasures [9] ["stats"] ["before"] == 33), treasures [9]
		
	print ()
	print (count, "documents returned")	

	return;
	
checks = {
	'check 1': check_1
}