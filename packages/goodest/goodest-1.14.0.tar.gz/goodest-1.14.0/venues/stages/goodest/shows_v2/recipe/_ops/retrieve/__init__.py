
'''
	This does a retrieve from the NIH and USDA APIs
'''

'''
	from goodest.shows_v2.recipe._ops.retrieve import retrieve_recipe
	recipe_packet = retrieve_recipe ({
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
	
def retrieve_recipe (packet):
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
				food_nature = retrieve_parsed_USDA_food ({
					"FDC_ID": ID_with_amounts ["FDC_ID"],
					"USDA API Pass": API_NIH_pass
				})
				natures_with_amounts.append ([
					food_nature,
					amount_of_packets
				])
			except Exception:
				not_added.append (ID_with_amounts)
		
		elif ("DSLD_ID" in ID_with_amounts):
			try:
				supp_nature = retrieve_parsed_NIH_supp ({
					"DSLD_ID": ID_with_amounts ["DSLD_ID"],
					"NIH API Pass": API_USDA_pass
				})
			
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

	
	'''
	show_variable ({
		"natures_with_amounts": natures_with_amounts
	})
	'''

	recipe = formulate_recipe ({
		"natures_with_amounts": natures_with_amounts	
	})
	
	
	return {
		"not_added": not_added,
		"recipe": recipe
	};