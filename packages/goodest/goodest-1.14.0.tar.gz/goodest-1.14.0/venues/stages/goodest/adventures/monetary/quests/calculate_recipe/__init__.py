
'''
	This does a retrieve from the monetary node.
'''

'''
	from goodest.adventures.monetary.quests.calculate_recipe import calculate_recipe
	recipe_packet = calculate_recipe ({
		"IDs_with_amounts": [
			{
				"FDC_ID": "",
				"packages": 10
			},
			{
				"FDC_ID": "",
				"packages": 5
			},
			{
				"DSLD_ID": "",
				"packages": 5
			}
		]	
	})
	
	recipe = recipe_packet ["recipe"]
	not_added = recipe_packet ["not_added"]
'''


#----
#
from goodest.adventures.monetary.DB.goodest_inventory.foods.document.find import find_food
from goodest.adventures.monetary.DB.goodest_inventory.supps.document.find import find_supp
#
from goodest.shows_v2.recipe._ops.formulate import formulate_recipe
from goodest.besties.food_USDA.nature_v2._ops.retrieve import retrieve_parsed_USDA_food
from goodest.besties.supp_NIH.nature_v2._ops.retrieve import retrieve_parsed_NIH_supp
from goodest._essence import retrieve_essence	
#
#
from biotech.topics.show.variable import show_variable
#
#
import rich
#
#----
	
def calculate_recipe (packet):
	IDs_with_amounts = packet ["IDs_with_amounts"]
	
	counter = 0
	for good in IDs_with_amounts:
		if ("FDC_ID" in good):
			if (type (good ["FDC_ID"]) == int):
				IDs_with_amounts [counter] ["FDC_ID"] = str (good ["FDC_ID"])
	
		if ("DSLD_ID" in good):
			if (type (good ["DSLD_ID"]) == int):
				IDs_with_amounts [counter] ["DSLD_ID"] = str (good ["DSLD_ID"])
	
		counter += 1
	
	essence = retrieve_essence ()
	API_USDA_pass = essence ['USDA'] ['food']
	API_NIH_pass = essence ['NIH'] ['supp']
	
	not_added = []
	
	natures_with_amounts = []
	for ID_with_amounts in IDs_with_amounts:
		assert ("packages" in ID_with_amounts), ID_with_amounts
		amount_of_packets = ID_with_amounts ["packages"]
		
		if ("FDC_ID" in ID_with_amounts):
			try:				
				food_document = find_food ({
					"filter": {
						"nature.identity.FDC ID": ID_with_amounts ["FDC_ID"]
					}
				})
				food_nature = food_document ["nature"]
				
				natures_with_amounts.append ([
					food_nature,
					amount_of_packets
				])
			except Exception:
				not_added.append (ID_with_amounts)
		
		elif ("DSLD_ID" in ID_with_amounts):
			try:
				supp_document = find_supp ({
					"filter": {
						"nature.identity.DSLD ID": ID_with_amounts ["DSLD_ID"]
					}
				})
				supp_nature = supp_document ["nature"]
			
				natures_with_amounts.append ([
					supp_nature,
					amount_of_packets
				])
			except Exception:
				not_added.append (ID_with_amounts)
		
		else:
			raise Exception (f"""
			
				neither FDC_ID or DSLD_ID was found in natures_with_amount: 
				
				{ natures_with_amount }
				
				""")

	


	recipe = formulate_recipe ({
		"natures_with_amounts": natures_with_amounts	
	})
	
	return {
		"not_added": not_added,
		"recipe": recipe
	};