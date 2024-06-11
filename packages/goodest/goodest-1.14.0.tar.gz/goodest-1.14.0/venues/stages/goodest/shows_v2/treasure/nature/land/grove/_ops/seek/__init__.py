

'''
	from goodest.shows_v2.treasure.nature.land.grove._ops.seek import seek_ingredient_in_grove
	
	#
	#	This does a lower casing of all the 
	#	names in the essential ingredient names
	#
	sodium = seek_ingredient_in_grove (
		grove = grove,
		for_each = (
			lambda entry : True if (
				"sodium, na" in list (map (
					lambda name : name.lower (), 
					entry ["info"] ["names"]
				))
			) else False
		)
	)
'''

'''
	def for_each (entry):
		names = entry ["info"] ["names"]
		for name in names:
			if (name.lower () == "protein"):
				return True
				
		return False		

	import goodest.shows.ingredient_scan.grove.seek as grove_seek
	protein = grove_seek.beautifully (
		grove = grove,
		for_each = for_each
	)
'''

'''
	description:
		This loops through the entire grove,
		unless True is returned.
'''

'''
	{
		"info": {},
		"natures": [],
		"unites": []
	}
'''

'''
	# recursive
'''

def seek_ingredient_in_grove (
	grove,
	for_each = lambda * p, ** k : None,
	
	story = 1
):
	for entry in grove:
		if (for_each (entry)):
			return entry
		
		if (len (entry ["unites"]) >= 1):
			inner_grove = entry ["unites"]
		
			found = seek_ingredient_in_grove (
				inner_grove,
				for_each = for_each,
				story = story + 1
			);
			if (type (found) == dict):
				return found;
		
		

	return None