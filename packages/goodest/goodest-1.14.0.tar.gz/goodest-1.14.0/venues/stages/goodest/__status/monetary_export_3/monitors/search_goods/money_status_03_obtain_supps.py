



'''
	python3 status.proc.py "search_goods/status_03_obtain_supps.py"
'''

#/
#
import copy
from rich import print_json
#
#
from goodest.adventures.monetary.quests.search_goods import search_goods	
#
#\

def check_1 ():
	proceeds = search_goods ({
		"filters": {
			"string": "",
			"include": {
				"food": False,
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
			"lower_case_name": document ['lower_case_name']
		})
		
		count += 1
		
	assert (len (treasures) == 15), len (treasures)
		
	print ()
	print (count, "documents returned")	

	return;
	
checks = {
	'check 1': check_1
}

