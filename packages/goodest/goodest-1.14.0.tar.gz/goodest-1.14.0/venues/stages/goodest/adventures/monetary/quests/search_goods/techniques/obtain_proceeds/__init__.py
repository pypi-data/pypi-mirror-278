


'''
	import goodest.adventures.monetary.quests.search_goods.techniques.obtain_proceeds as obtain_proceeds
	obtain_proceeds.smoothly (
		DB = 
		filters = {
			"string": "lentils",
			"include": {
				"food": True,
				"supp": False
			},
			"limit": 10,
			
			
			#
			#	has either "before" or "after"
			#
			
			"before": {
				"emblem": 32,
				"kind": "food",
				"name": "POMEGRANATE JUICE, POMEGRANATE"
			},
			
			"after": {
				"emblem": 32,
				"kind": "food",
				"name": "POMEGRANATE JUICE, POMEGRANATE"
			},
			
			"format": 1
		}
	)
'''

'''
	[proposals]
		aggregation steps:
			[ ] unionize "food" and "supp" -> "food_emblem" and "supp_emblem"

			[ ] has "nature.identity.name" and "emblem"
			[ ] add "lower_case_name" = "$nature.identity.name".lower ()
			[ ] [filter (if scan string)] by scan string
			[ ] sort by "lower_case_name", then "emblem" in alphabetical order
			
			[ ] add "before" and "after" stats
			[ ] (conditionally) sort by "lower_case_name", then "emblem" in reverse alphabetical order
			
			[ ] [filter (if vector)] by name vector
			[ ] [filter (if vector)] by name and emblem vector									
			
			[ ] limit the documents returned

			[ ] if reversed, forward sort by "lower_case_name", then "emblem"

			[ ] format
'''

#/
#
import goodest.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.spruce.filters as spruce_filters
import goodest.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.affirm.direction as affirm_direction
#
#	aggregation steps
#
#
import goodest.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.unionize as unionize
import goodest.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.check_fields as check_fields
import goodest.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.lower_case_name as lower_case_name
import goodest.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.sort_name_emblem as sort_name_emblem
import goodest.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.filters.scan_string as filter_by_scan_string
import goodest.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.before_and_after as before_and_after
import goodest.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.filters.vector_name as filter_by_vector_name
import goodest.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.filters.vector_name_and_emblem as filter_by_vector_name_and_emblem
import goodest.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.filters.limit as limit_documents
import goodest.adventures.monetary.quests.search_goods.techniques.obtain_proceeds.aggregation_steps.formats.format_1 as format_1
from goodest.adventures.monetary.DB.goodest_inventory.connect import connect_to_goodest_inventory
#
#
import rich
#
#\

	

def obtain_proceeds (
	filters = None
):
	spruce_filters.solid (
		filters = filters, 
		limit_limit = 100
	)
	
	if ("format" not in filters):
		format = 1
	
	direction = affirm_direction.solid (filters = filters)
	is_before = direction ["is_before"]
	is_after = direction ["is_after"]
	if (is_before and is_after):
		raise Exception (f'Vectors "after" and "before" currently cannot both be included.')

	scan_string = filters ["string"]
	limit = filters ["limit"]
	include_food = filters ["include"] ["food"]
	include_supp = filters ["include"] ["supp"]
	
	include_meals = False;
	if ("meals" in filters ["include"]):
		include_meals = filters ["include"] ["meals"]
	
	'''
		join starts from one collection and 
		then adds the other.
	'''
	if (include_food):		
		collection = "food"
	elif (include_supp):
		collection = "supp"
	elif (include_meals):
		collection = "meals"
	else:
		return []
		
		
	#/
	#	direction
	#
	#\
	if (is_before):
		vector_direction = "before"
		reverse = True
	else:
		vector_direction = "after"
		reverse = False
	
	
	ask = []
	unity = unionize.occur (
		include_food = include_food,
		include_supp = include_supp,
		include_meals = include_meals
	)
	for u in unity:
		ask.append (u)
	

	ask.append (check_fields.occur ())
	ask.append (lower_case_name.occur ())

	scan_string_filter = filter_by_scan_string.occur (
		scan_string = scan_string
	);
	if (type (scan_string_filter) == dict):
		ask.append (scan_string_filter)


	ask.append (sort_name_emblem.occur (reverse = False))
	ask.append (before_and_after.occur (reverse = False))

	if (reverse == True):
		ask.append (sort_name_emblem.occur (reverse = reverse))
	
	
	'''
		start from a certain point.
	'''
	if (is_before or is_after):
		if (is_before):
			vector = filters ["before"]
		else:
			vector = filters ["after"]

		vector_kind = vector ["kind"]
		vector_name = vector ["name"].lower ()
		vector_emblem = vector ["emblem"]
		
		if (vector_kind == "food"):
			vector_unique_emblem = "food_emblem"
		else:
			vector_unique_emblem = "supp_emblem"
			
		ask.append (
			filter_by_vector_name_and_emblem.occur (
				kind = vector ["kind"],
				name = vector_name,
				emblem = vector ["emblem"],
				
				direction = vector_direction
			)
		)
	
		ask.append (
			filter_by_vector_name.occur (
				name = vector_name,
				direction = vector_direction
			)
		)
	
	
	
	
	'''
		?? if before, needs to be reverse = True before this line.
	'''
	ask.append (limit_documents.occur (limit))
	if (reverse == True):
		ask.append (sort_name_emblem.occur (reverse = False))

	
	'''
		This step erases fields from the documents
		and prepares the document to only have
		designated fields.
	'''
	ask.append (format_1.occur ())
	

	'''
	rich.print_json (data = {
		"aggregate": ask
	})
	'''


	'''
		This is where the query is actually run.
	'''
	[ driver, goodest_inventory_DB ] = connect_to_goodest_inventory ()
	documents = goodest_inventory_DB [ collection ].aggregate (ask)
	driver.close ()
	
	return {
		"documents": documents,
		"aggregate": ask
	};
	
	
	
	
	
	
	
	#