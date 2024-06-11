



'''
	python3 status.proc.py "search_goods/status_02_obtain_foods.py"
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
				"food": True,
				"supp": False
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
		
	assert (len (treasures) == 42), len (treasures)
		
	assert (treasures [0] ["stats"] ["after"] == 41), treasures [0]
	assert (treasures [0] ["stats"] ["before"] == 0), treasures [0]
	
	assert (treasures [41] ["stats"] ["after"] == 0), treasures [41]
	assert (treasures [41] ["stats"] ["before"] == 41), treasures [41]	
		
	print ()
	print (count, "documents returned")	

	return;
	
checks = {
	'check 1': check_1
}