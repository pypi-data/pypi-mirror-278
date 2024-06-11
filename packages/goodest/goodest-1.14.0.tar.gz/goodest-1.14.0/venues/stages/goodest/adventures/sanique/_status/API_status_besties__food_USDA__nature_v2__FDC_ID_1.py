

'''
	python3 /goodest/venues/stages/goodest/__status/API/status.proc.py adventures/sanique/_status/API_status_besties__food_USDA__nature_v2__FDC_ID_1.py
'''

#----
#
import json
import requests
#
#
from goodest.adventures.sanique.utilities.retrieve_sanique_URL import retrieve_sanique_URL
from goodest._essence import retrieve_essence
#
#----

def check_1 ():
	essence = retrieve_essence ()

	sanique_URL = retrieve_sanique_URL ()
	full_URL = sanique_URL + "/staff/besties/food_USDA/nature_v2/2369390"

	print ("full_URL:", full_URL)

	response = requests.get (
		full_URL,
		headers = {
			"opener": essence ["sanique"] ["protected_address_key"]
		}
	)	
	
	
	assert (response.status_code == 200), response.status_code
		
	packet = response.json ()
		
	assert ("kind" in packet)	
	assert ("identity" in packet)	
	assert ("brand" in packet)	
	assert ("measures" in packet)	
	assert ("measured ingredients" in packet)	
	assert ("essential nutrients" in packet)	
	assert ("cautionary ingredients" in packet)	
		
	#print (packet)	
		
checks = {
	'check 1': check_1
}