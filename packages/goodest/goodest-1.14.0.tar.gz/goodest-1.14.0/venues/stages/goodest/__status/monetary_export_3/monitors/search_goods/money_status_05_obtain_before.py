





'''
	python3 status.proc.py "search_goods/status_05_obtain_before.py"
'''

#/
#
import copy
import rich
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
			"limit": 100,
			"before": {
				"emblem": 30,
				"kind": "food",
				"name": "asparagus"
			}
		}
	})

	documents = proceeds ["treasures"]

	treasures = []
	count = 0
	for document in documents:
		#print ()
		#print (document)
	
		treasures.append ({
			"kind": document ['nature'] ['kind'], 
			"emblem": document ['emblem'],
			"lower_case_name": document ['lower_case_name']
		})
		
		count += 1
		
	assert (len (treasures) == 3), len (treasures)
	rich.print_json (data = treasures)	
		
	assert (
		[
			{
				"kind": "food",
				"emblem": 4,
				"lower_case_name": "all american veggie burgers"
			},
			{
				'kind': 'food', 
				'emblem': 49, 
				'lower_case_name': 'almond butter, creamy'
			},
			{
				"kind": "food",
				"emblem": 29,
				"lower_case_name": "asparagus"
			}
		] == treasures
	), treasures
		
	print ()
	print (count, "documents returned")	

	return;
	
checks = {
	'check 1': check_1
}