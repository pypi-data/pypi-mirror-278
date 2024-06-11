

'''
	python3 status.proc.py besties/food_USDA/deliveries/one/status/API_status_foundational_1.py
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


def check_foundational_1 ():
	essence = retrieve_essence ()
	API_USDA_ellipse = essence ['USDA'] ['food']
	return;
	
	food = retrieve_1_food.presently (
		2346404,
		API_ellipse = API_USDA_ellipse,
		kind = "foundational"
	)

	
checks = {
	"check foundational 1": check_foundational_1
}