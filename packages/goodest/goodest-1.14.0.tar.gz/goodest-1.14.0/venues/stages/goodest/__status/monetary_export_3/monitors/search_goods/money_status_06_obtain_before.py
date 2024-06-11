



'''
	python3 status.proc.py "search_goods/status_06_obtain_before.py"
'''

'''
	[food] 24 orange juice {'after': 27, 'before': 8}
	[food] 33 organic firm tofu vegan {'after': 26, 'before': 9}
	[supp] 4 organic lion's mane mushroom 1 g unflavored {'before': 0, 'after': 13}
	[food] 28 organic soy beans {'after': 25, 'before': 10}
	[supp] 12 organic vegan protein power {'before': 1, 'after': 12}
	[food] 12 pinto beans {'after': 24, 'before': 11}
	[food] 8 plant-based chopped chick'n {'after': 23, 'before': 12}
	[food] 9 plant-based chopped chick'n {'after': 22, 'before': 13}
	[food] 10 plant-based chopped chick'n {'after': 21, 'before': 14}
	[food] 6 plant-based jumbo smart hot dogs {'after': 20, 'before': 15}
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
			"limit": 10,
			"before": {
				"emblem": 37,
				"kind": "food",
				"name": "plant-based original breakfast burrito"
			}
		}
	})

	documents = proceeds ["treasures"]
	
	print ("proceeds:", proceeds)

	treasures = []
	count = 0
	for document in documents:
		print (document)
	
		treasures.append ({
			"kind": document ['nature'] ['kind'], 
			"emblem": document ['emblem'],
			"lower_case_name": document ['lower_case_name']
		})
		
		count += 1
		
	assert (len (treasures) == 10), len (treasures)
	rich.print_json (data = treasures)	
		
	assert (
		[
		  {
			"kind": "food",
			"emblem": 24,
			"lower_case_name": "orange juice"
		  },
		  {
			"kind": "food",
			"emblem": 33,
			"lower_case_name": "organic firm tofu vegan"
		  },
		  {
			"kind": "supp",
			"emblem": 4,
			"lower_case_name": "organic lion's mane mushroom 1 g unflavored"
		  },
		  {
			"kind": "food",
			"emblem": 28,
			"lower_case_name": "organic soy beans"
		  },
		  {
			"kind": "supp",
			"emblem": 12,
			"lower_case_name": "organic vegan protein power"
		  },
		  {
			"kind": "food",
			"emblem": 12,
			"lower_case_name": "pinto beans"
		  },
		  {
			"kind": "food",
			"emblem": 8,
			"lower_case_name": "plant-based chopped chick'n"
		  },
		  {
			"kind": "food",
			"emblem": 9,
			"lower_case_name": "plant-based chopped chick'n"
		  },
		  {
			"kind": "food",
			"emblem": 10,
			"lower_case_name": "plant-based chopped chick'n"
		  },
		  {
			"kind": "food",
			"emblem": 6,
			"lower_case_name": "plant-based jumbo smart hot dogs"
		  }
		] == treasures
	), treasures
		
	print ()
	print (count, "documents returned")	

	return;
	
checks = {
	'check 1': check_1
}