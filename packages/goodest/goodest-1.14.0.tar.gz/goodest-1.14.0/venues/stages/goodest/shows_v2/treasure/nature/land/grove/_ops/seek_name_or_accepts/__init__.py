


'''
	"accepts" exists because for example:
			
		example 1:
			B6 is an EN.
			pyridoxine is one form of EN.
			Pyridoxine is not an EN.
			
			https://en.wikipedia.org/wiki/Vitamin_B6
'''

'''
	from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
	B6 = seek_name_or_accepts (
		grove = grove,
		name_or_accepts = "pyridoxine"
	)
'''
from goodest.shows_v2.treasure.nature.land.grove._ops.seek import seek_ingredient_in_grove

def seek_name_or_accepts (
	name_or_accepts = "",
	grove = [],
	return_none_if_not_found = False
):
	name_or_accepts = name_or_accepts.lower ()

	checked = []
	def for_each (entry):		
		accepts = []
		if ("accepts" in entry ["info"]):
			accepts = entry ["info"] ["accepts"]
	
		patterns = [
			* entry ["info"] ["names"],
			* accepts
		]	
		
		checked.append (patterns)
			
		for ingredient_name in patterns:
			#print (f"checking if '{ name_or_accepts }' == '{ ingredient_name.lower ().strip () }'")
		
			if (name_or_accepts == ingredient_name.lower ().strip ()):			
				return True;
			
		return False

	entry = seek_ingredient_in_grove (
		grove = grove,
		for_each = for_each
	)
	if (type (entry) != dict):
		if (return_none_if_not_found):
			return None;
	
		raise Exception (f'''
			
			The "name" or "accepts" "{ name_or_accepts }" was not found.
			
		''')

	return entry