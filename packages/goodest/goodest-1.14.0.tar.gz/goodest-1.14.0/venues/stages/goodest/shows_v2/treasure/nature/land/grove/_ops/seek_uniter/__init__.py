
'''
	summary:
		previously: "name_or_accepts" was "name"
'''

'''
	from goodest.shows_v2.treasure.nature.land.grove._ops.seek_uniter import seek_uniter
	uniter = seek_uniter (
		grove = [],
		name_or_accepts = "sugars, total"
	)
'''

from goodest.shows_v2.treasure.nature.land.grove._ops.seek import seek_ingredient_in_grove

def seek_uniter (
	grove = [],
	name_or_accepts = ""
):
	name_or_accepts = name_or_accepts.lower ()

	def retrieve_name_or_accepts (entry):
		accepts = []
		if ("accepts" in entry ["info"]):
			accepts = entry ["info"] ["accepts"]
	
		patterns = [
			* entry ["info"] ["names"],
			* accepts
		]
		
		return patterns
		
		

	def for_each (entry):
		unites = entry ["unites"]
		for entry in unites:
			#names = entry ["info"] ["names"]
			names = retrieve_name_or_accepts (entry)		
					
			for entry_name in names:
				if (name_or_accepts == entry_name.lower ().strip ()):			
					return True;
				
		return False		

	
	return seek_ingredient_in_grove (
		grove = grove,
		for_each = for_each
	)


