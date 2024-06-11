

'''
	import goodest.besties.food_USDA.deliveries.one.assertions.branded as branded_food_assertions
'''


def run (data):
	#assert ("description" in data)
	assert ("foodNutrients" in data)
	assert ("packageWeight" in data)
	
	
	
	#
	#	
	#
	assert ("ingredients" in data)
	
	#
	#	recommendations
	#
	assert ("servingSize" in data)
	assert ("servingSizeUnit" in data)
	
	#
	#	identity
	#
	assert ("gtinUpc" in data)
	assert ("fdcId" in data)
	#assert ("brandOwner" in data)
	#assert ("brandName" in data)

	return;