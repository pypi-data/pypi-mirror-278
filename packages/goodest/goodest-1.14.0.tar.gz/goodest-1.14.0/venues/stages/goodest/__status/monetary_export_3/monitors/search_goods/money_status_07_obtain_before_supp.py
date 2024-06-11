



'''
	python3 status.proc.py "_status/vows/mongo/vegan_DB_status_2/scan_3/status_7_obtain_before_supp.py"
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
				"food": False,
				"supp": True
			},
			"limit": 10,
			"before": {
				"emblem": 14,
				"kind": "supp",
				"name": "veggie protein unflavored"
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
		
	assert (len (treasures) == 10), len (treasures)
	#rich.print_json (data = treasures)	
	
	this_directory = pathlib.Path (__file__).parent.resolve ()
	the_path = normpath (join (this_directory, "status_07.JSON"))
	etch_bracket (the_path, treasures)
		
	assert (
		[
			{
				"kind": "supp",
				"emblem": 6,
				"lower_case_name": "vegan chia seed oil"
			},
			{
				"kind": "supp",
				"emblem": 9,
				"lower_case_name": "vegan complete vanilla"
			},
			{
				"kind": "supp",
				"emblem": 8,
				"lower_case_name": "vegan evening primrose oil"
			},
			{
				"kind": "supp",
				"emblem": 2,
				"lower_case_name": "vegan multivitamin & mineral supplement with greens"
			},
			{
				"kind": "supp",
				"emblem": 5,
				"lower_case_name": "vegan multivitamin & mineral supplement with greens"
			},
			{
				"kind": "supp",
				"emblem": 15,
				"lower_case_name": "vegan multivitamin & mineral supplement with greens"
			},
			{
				"kind": "supp",
				"emblem": 3,
				"lower_case_name": "vegan plant-based calcium 1,000 mg"
			},
			{
				"kind": "supp",
				"emblem": 7,
				"lower_case_name": "vegan prenatal multivitamin & mineral"
			},
			{
				"kind": "supp",
				"emblem": 10,
				"lower_case_name": "vegan probiotic with fos prebiotics"
			},
			{
				"kind": "supp",
				"emblem": 13,
				"lower_case_name": "vegan smart all-in-one nutritional shake wild berries"
			}
		]
		 == treasures
	), treasures
		
	print ()
	print (count, "documents returned")	

	return;
	
checks = {
	'check 1': check_1
}