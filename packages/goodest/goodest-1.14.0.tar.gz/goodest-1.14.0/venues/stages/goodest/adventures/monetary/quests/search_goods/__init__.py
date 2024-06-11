

'''
	from goodest.adventures.monetary.quests.search_goods import search_goods
	proceeds = search_goods ({
		"filters": {
			"string": "lentils",
			"include": {
				"food": True,
				"supp": False
			},
			"limit": 10
		}
	})
	
	proceeds = search_proceeds ["proceeds"]
'''

#/
#
from .techniques.obtain_proceeds import obtain_proceeds
from .techniques.stats import obtain_stats
from .techniques.limits import obtain_limits
#
#
import rich
#
#\

def search_goods (packet):
	filters = packet ["filters"]

	proceeds = obtain_proceeds (
		filters = filters
	)
	
	documents = proceeds ["documents"]
	
	documents_list = []
	for document in documents:
		del document ["_id"]
		
		documents_list.append (document)
			
	revenue = {
		"treasures": documents_list,
		"exception": {
			"occurred": False
		}
	}
	

	revenue ["stats"] = obtain_stats (	
		documents_list = documents_list
	)
	
	[ prev, next ] = obtain_limits (documents_list)
	revenue ["limits"] = {
		"start": prev,
		"end": next
	}
	
	return revenue
	
	