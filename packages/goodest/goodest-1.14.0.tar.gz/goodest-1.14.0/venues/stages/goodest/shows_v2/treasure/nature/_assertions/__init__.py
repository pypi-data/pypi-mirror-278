




'''
	import goodest.shows_v2.treasure.nature._assertions as natures_v2_assertions
	natures_v2_assertions.run (nature)
'''

def are_equal (v1, v2):
	try:
		assert (v1 == v2);
	except Exception as E:
		print ("not equal:", v1, v2)
		raise Exception (E)

	return;


import json
def run (nature):
	assert ("kind" in nature)
	assert ("identity" in nature)
	assert ("brand" in nature)

	assert ("measures" in nature)
	assert ("essential nutrients" in nature)
	assert ("cautionary ingredients" in nature)
	

	#print (json.dumps (nature, indent = 4))
	
	
	

	return;