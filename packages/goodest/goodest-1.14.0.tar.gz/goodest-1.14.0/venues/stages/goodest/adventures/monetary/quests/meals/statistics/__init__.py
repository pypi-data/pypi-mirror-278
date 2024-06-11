

'''
	[objective]
		[ ] implement DSLD_ID for "form" = "grams"
		[ ] implement DSLD_ID for "form" = "capsules"
'''

'''
	[summary]
		"DSLD_ID" is not implemented

	[DB ops] 		
		modifies: no
		
		This reads the "supp" and "food" collections.
'''



'''
	from goodest.adventures.monetary.quests.meals.statistics import formulate_meal_statistics
	meal_statistics = formulate_meal_statistics ({
		"IDs_with_amounts": [
			{
				"FDC_ID": "2471166",
				"grams": 1
			},
			{
				"FDC_ID": "2425001",
				"grams": 2
			}
		]	
	})
'''

#/
#
from goodest.adventures.monetary.DB.goodest_inventory.foods.document.find import find_food
from goodest.adventures.monetary.DB.goodest_inventory.supps.document.find import find_supp
#
from goodest.shows_v2.recipe._ops.formulate import formulate_recipe
from goodest.besties.food_USDA.nature_v2._ops.retrieve import retrieve_parsed_USDA_food
from goodest.besties.supp_NIH.nature_v2._ops.retrieve import retrieve_parsed_NIH_supp
from goodest._essence import retrieve_essence	
import goodest.measures.number.sci_note_2 as sci_note_2
#
#
from biotech.topics.show.variable import show_variable
#
#
import rich
#
#
from fractions import Fraction
#
#\

def formulate_meal_statistics (packet):
	IDs_with_amounts = packet ["IDs_with_amounts"]
	
	'''
		calculate the grams per package
	'''
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
	added = []
	
	natures_with_amounts = []
	for ID_with_amounts in IDs_with_amounts:
		assert ("grams" in ID_with_amounts), ID_with_amounts
		grams_of_good = ID_with_amounts ["grams"]
		
		if ("FDC_ID" in ID_with_amounts):
			try:				
				food_document = find_food ({
					"filter": {
						"nature.identity.FDC ID": ID_with_amounts ["FDC_ID"]
					}
				})
				food_nature = food_document ["nature"]
				
				mass_per_package_in_grams = Fraction (
					food_nature ["measures"] ["mass"] ["per package"] ["grams"] ["fraction string"]
				)

				amount_of_packets = Fraction (
					Fraction (grams_of_good),
					mass_per_package_in_grams
				)
				
				print ("amount_of_packets:", amount_of_packets)
				
				natures_with_amounts.append ([
					food_nature,
					amount_of_packets
				])
				
				added.append ({
					"nature": food_nature,
					"emblem": food_document ["emblem"],
					"grams": sci_note_2.produce (grams_of_good)
				})				
			except Exception:
				not_added.append (ID_with_amounts)
		
		elif ("DSLD_ID" in ID_with_amounts):
		
			raise Exception ("DSLD_IDs are not currently supported")
		
			'''
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
			'''
		
		else:
			raise Exception (f"""
			
				neither FDC_ID or DSLD_ID was found in natures_with_amount: 
				
				{ natures_with_amount }
				
				""")

	


	recipe = formulate_recipe ({
		"natures_with_amounts": natures_with_amounts	
	})
	
	recipe ["ingredients"] = added;
	recipe ["not_added"] = not_added;
	
	
	return {
		"not_added": not_added,
		"added": added,
		"recipe": recipe
	};
	
	
