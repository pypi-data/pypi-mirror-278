

'''
	from goodest.adventures.monetary.DB.goodest_tract.goals._indexes.create import drop_and_create_goals_indexes
'''

from goodest.adventures.monetary.DB.goodest_tract.connect import connect_to_goodest_tract
from goodest.adventures.alerting.parse_exception import parse_exception
from goodest.adventures.alerting import activate_alert
	
def drop_and_create_goals_indexes ():
	[ driver, goodest_tract_DB ] = connect_to_goodest_tract ()

	try:
		proceeds = goodest_tract_DB ["goals"].drop_indexes ()
	except Exception as E:
		activate_alert ("emergency", {
			"exception": parse_exception (E)
		})
		
	proceeds = goodest_tract_DB ["goals"].create_index ( 
		[( "ingredients.labels", 1 )],
		
		name = "name = ingredients.labels"
	)
	
	activate_alert ("info", {
		"proceeds of index create": proceeds
	}, mode = "pprint")
	
	driver.close ()