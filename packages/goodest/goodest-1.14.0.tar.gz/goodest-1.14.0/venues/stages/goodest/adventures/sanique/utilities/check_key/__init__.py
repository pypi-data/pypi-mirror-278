
'''
	from goodest.adventures.sanique.utilities.check_key import check_key

	lock_status = check_key (request)
	if (lock_status != "unlocked"):
		return lock_status
'''


from goodest._essence import retrieve_essence

import sanic.response as sanic_response

def check_key (request):
	essence = retrieve_essence ()
	
	opener = request.headers.get ("opener")
	
	if (opener != essence ["sanique"] ["protected_address_key"]):
		return sanic_response.json ({
			"anomaly": "The opener sent is not it."
		}, status = 600)
			
	return "unlocked"