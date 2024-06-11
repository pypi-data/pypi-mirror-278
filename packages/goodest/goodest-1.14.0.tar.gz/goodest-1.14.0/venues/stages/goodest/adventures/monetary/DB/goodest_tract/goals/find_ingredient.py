
'''
	from goodest.adventures.monetary.DB.goodest_tract.goals.find_ingredient import find_goal_ingredient
	goal_ingredient = find_goal_ingredient ({
		"emblem": "",
		
		#
		#	The ingredient label (e.g. Biotin)
		#
		#
		"label": ""
	})
'''

#----
#
from biotech.topics.show.variable import show_variable
#
#
from goodest.adventures.monetary.DB.goodest_tract.connect import connect_to_goodest_tract
from goodest.adventures.alerting.parse_exception import parse_exception
from goodest.adventures.alerting import activate_alert	
#
#----


def search_for_proceeds (revenue):
	try:
		proceeds = revenue ["nature"] ["ingredients"] [0]
		return proceeds;
	
	except Exception as E:
		pass;
		#activate_alert ("emergency", {
		#	"find ingredient goal proceeds exception": parse_exception (E)
		#})	
			

	return None;

def find_goal_ingredient (packet):

	drive = ""
	try:
		[ driver, goodest_tract_DB ] = connect_to_goodest_tract ()
	except Exception as E:
		activate_alert ("emergency", {
			"find ingredient, driver connect exception": parse_exception (E)
		})
		
		return None;
	
	proceeds = None
	try:
		emblem = int (packet ["emblem"])
		label = packet ["label"]

		query = {
			'emblem': emblem,
			'nature.ingredients.labels': {'$regex': label.lower (), '$options': 'i'}
		}
		revenue = goodest_tract_DB ["goals"].find_one (
			query,
			{ 'nature.ingredients.$': 1, '_id': 0  }
		) 
		
		#activate_alert ("front", {
		#	"query": query,
		#	"revenue": revenue
		#})

		proceeds = search_for_proceeds (revenue)
		
		
	except Exception as E:
		activate_alert ("emergency", {
			"find ingredient exception": parse_exception (E)
		})	
			
		return None;

	try:
		driver.close ()
	except Exception as E:
		activate_alert ("emergency", {
			"find ingredient, driver close exception": parse_exception (E)
		})	
		
		return None;
	
	
	return proceeds;