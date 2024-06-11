

'''
python3 status_api.py "food/USDA/API/one/status/API_STATUS_branded_1.py"
'''


#----
#
import json
#
#
import goodest.besties.food_USDA.deliveries.one as retrieve_1_food
from goodest._essence import retrieve_essence
#
#----
	
def check_branded_1 ():	
	essence = retrieve_essence ()
	API_USDA_ellipse = essence ['USDA'] ['food']
	
	food = retrieve_1_food.presently (
		2642759,
		API_ellipse = API_USDA_ellipse
	)

	
checks = {
	"check branded 1": check_branded_1
}