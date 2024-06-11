




'''
	python3 status_API.py "supp_NIH/deliveries/one/status/API_status_1.py"
'''


#----
#
import goodest.besties.supp_NIH.deliveries.one as NIH_API_one
from goodest._essence import retrieve_essence
#
#
import json
#
#----

	
def check_branded_1 ():	
	essence = retrieve_essence ()
	API_NIH_ellipse = essence ['NIH'] ['supp']

	supplement = NIH_API_one.find (220884, API_NIH_ellipse)
	
	
checks = {
	"NIH branded 1": check_branded_1
}