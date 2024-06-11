
from goodest.adventures.monetary.DB.goodest_tract.goals.find_ingredient import find_goal_ingredient
	

def find_goal (packet):
	ingredient_names = packet ["ingredient_names"]
	goal_region = packet ["goal_region"]
	
	for ingredient_name in ingredient_names:
		proceeds = find_goal_ingredient ({
			"emblem": goal_region,
			
			#
			#	The ingredient label (e.g. Biotin)
			#
			#
			"label": ingredient_name
		})
		
		if (type (proceeds) == dict):
			return proceeds;

	return None