



'''
	from goodest.shows_v2.treasure.nature.land.grove._ops.nurture import nurture_grove
	nurture_grove ("essential_nutrients")
'''



'''
	nurture_grove ("essential_nutrients")
'''


'''
	nurture_grove ("cautionary_ingredients")
'''


#----
#
from goodest.adventures.monetary.DB.goodest_tract._land.retrieve_every import retrieve_every_ingredient
#
#
import json
import copy
#
#----

def nutrient ():
	return {
		"info": {},
		"measures": {},
		"natures": [],
		"unites": []
	}

def nurture_grove (	
	collection = "",
	records = 0
):
	'''
		Pretty sure that this is a modified list
		from the USDA measured ingredients list... etc.?
	'''
	this_grove = []

	added_to_grove_count = 0


	ingredients_DB_list = retrieve_every_ingredient ({
		"collection": collection
	})
	
	
	ingredients_DB_list.sort (key = lambda essential : essential ["region"])
	ingredients_DB_list_size = len (ingredients_DB_list)



	'''
		Add "unites" to each essential.
	'''
	for essential in ingredients_DB_list:		
		this_grove.append ({
			"info": essential,
			"measures": {},
			"natures": [],
			"unites": []
		})
		
	#print_json (data = this_grove)

	'''
		This is a "recursive" loop through 
		the list,
		that constructs this_grove.
	'''
	def find_region (list, region):
		for entry in list:		
			if (entry ["info"] ["region"] == region):
				return entry;
				
			if (len (entry ["unites"]) >= 1):
				found = find_region (entry ["unites"], region)
				if (type (found) == dict):
					return found;
					
		return False
	
	
	'''
	
	'''
	def add_inclusions (entry, the_list):
		nonlocal this_grove;
	
		'''
			This loops through the inclusions
			of a (nature).
			
			If there's a problem here, it probably
			means that the nature that a nature
			points to is now deleted.
			
			for example:
				scene 1:
					nature 43
						includes:
							nature 49
					
				scene 2:
					delete 49
				
				scene 3:
					error can't find 49
		'''
		for region in entry ["info"] ["includes"]:
			physical = find_region (this_grove, region)
			copy_of_physical = copy.deepcopy (physical)
			
			this_grove.remove (physical)
			
			entry ["unites"].append (copy_of_physical)
			
			if (records >= 1):
				print ()
				print ("for:", entry ["info"] ["names"])
				print ("found:", copy_of_physical ["info"] ["names"])
	
	'''
	
	'''
	def build_grove (the_list):
		for entry in the_list:		
			if (len (entry ["info"] ["includes"]) >= 1):
				add_inclusions (entry, the_list)
								
				build_grove (entry ["unites"])
			

	build_grove (this_grove)

	return this_grove