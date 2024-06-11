






'''
	python3 status.proc.py "monitors/search_goods/status_01_obtain.py"
	
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
		
	assert (len (treasures) == 57), len (treasures)
		
	assert (treasures [0] ["stats"] ["after"] == 56), treasures [0]
	assert (treasures [0] ["stats"] ["before"] == 0), treasures [0]
	
	assert (treasures [56] ["stats"] ["after"] == 0), treasures [56]
	assert (treasures [56] ["stats"] ["before"] == 56), treasures [56]
	
	print ()
	print (count, "documents returned")	

	return;
	
checks = {
	'check 1': check_1
}