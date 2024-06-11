





'''
	python3 status.proc.py "search_goods/status_04_obtain_after.py"
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
			"after": {
				"emblem": 13,
				"kind": "supp",
				"name": "vegan smart all-in-one nutritional shake wild berries"
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
			"lower_case_name": document ['lower_case_name']
		})
		
		count += 1
		
	assert (len (treasures) == 4), len (treasures)
	rich.print_json (data = treasures)	
		
	assert (
		[
			{
				"kind": "food",
				"emblem": 18,
				"lower_case_name": "vegan supreme pizza, vegan supreme"
			},
			{
				"kind": "food",
				"emblem": 34,
				"lower_case_name": "vegan tofu eggplant green curry with sprouted brown rice, eggplant, mushroom and tofu, vegan tofu eggplant green curry"
			},
			{
				"kind": "supp",
				"emblem": 14,
				"lower_case_name": "veggie protein unflavored"
			},
			{
				"kind": "food",
				"emblem": 2,
				"lower_case_name": "walnuts halves & pieces, walnuts"
			}
		] == treasures
	)	
		
	print ()
	print (count, "documents returned")	

	return;
	
checks = {
	'check 1': check_1
}

