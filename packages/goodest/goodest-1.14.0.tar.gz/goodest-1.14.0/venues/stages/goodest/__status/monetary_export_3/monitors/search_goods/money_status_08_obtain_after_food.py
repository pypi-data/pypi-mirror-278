



'''
	python3 status.proc.py "search_goods/status_08_obtain_after_food.py"
'''

'''
	[food] 15 vegan bacon {'after': 12, 'before': 23}
	[food] 36 vegan baked ziti with cheeze, vegan cheeze {'after': 11, 'before': 24}
	[food] 13 vegan bread, vegan {'after': 10, 'before': 25}
	[food] 20 vegan chicken noodle soup, vegan chicken noodle {'after': 9, 'before': 26}
	[food] 16 vegan egg {'after': 8, 'before': 27}
	[food] 5 vegan gf vegetable lasagna, vegan gf vegetable {'after': 7, 'before': 28}
	[food] 17 vegan lasagna {'after': 6, 'before': 29}
	[food] 14 vegan mayo spread, vegan mayo {'after': 5, 'before': 30}
	[food] 19 vegan queso party dip, vegan queso {'after': 4, 'before': 31}
	[food] 21 vegan salt & vinegar cashews, vegan salt & vinegar {'after': 3, 'before': 32}
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
				"supp": False
			},
			"limit": 10,
			"before": {
				"emblem": 18,
				"kind": "food",
				"name": "vegan supreme pizza, vegan supreme"
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
		
	assert (len (treasures) == 10), len (treasures)
	
	
	this_directory = pathlib.Path (__file__).parent.resolve ()
	the_path = normpath (join (this_directory, "status_07.JSON"))
	etch_bracket (the_path, treasures)
		
	assert (
		[
		  {
			"kind": "food",
			"emblem": 15,
			"lower_case_name": "vegan bacon"
		  },
		  {
			"kind": "food",
			"emblem": 36,
			"lower_case_name": "vegan baked ziti with cheeze, vegan cheeze"
		  },
		  {
			"kind": "food",
			"emblem": 13,
			"lower_case_name": "vegan bread, vegan"
		  },
		  {
			"kind": "food",
			"emblem": 20,
			"lower_case_name": "vegan chicken noodle soup, vegan chicken noodle"
		  },
		  {
			"kind": "food",
			"emblem": 16,
			"lower_case_name": "vegan egg"
		  },
		  {
			"kind": "food",
			"emblem": 5,
			"lower_case_name": "vegan gf vegetable lasagna, vegan gf vegetable"
		  },
		  {
			"kind": "food",
			"emblem": 17,
			"lower_case_name": "vegan lasagna"
		  },
		  {
			"kind": "food",
			"emblem": 14,
			"lower_case_name": "vegan mayo spread, vegan mayo"
		  },
		  {
			"kind": "food",
			"emblem": 19,
			"lower_case_name": "vegan queso party dip, vegan queso"
		  },
		  {
			"kind": "food",
			"emblem": 21,
			"lower_case_name": "vegan salt & vinegar cashews, vegan salt & vinegar"
		  }
		] == treasures
	), treasures
		
	print ()
	print (count, "documents returned")	

	return;
	
checks = {
	'check 1': check_1
}

