


'''
	from goodest.adventures.monetary.venture import monetary_venture
	monetary_venture ()
'''

from goodest.adventures.monetary._controls.on import turn_on_monetary_node
from goodest.adventures.monetary._controls.off import turn_off_monetary_node
from goodest.adventures.monetary._controls.status import check_monetary_status

def monetary_venture ():
	return {
		"name": "monetary",
		"kind": "task",
		"turn on": {
			"adventure": turn_on_monetary_node,
		},
		"turn off": turn_off_monetary_node,
		"is on": check_monetary_status
	}