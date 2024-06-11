
'''
	from goodest.adventures.sanique.venture import sanique_venture
	sanique_venture ()
'''

from goodest.adventures.sanique._ops.on import turn_on_sanique
from goodest.adventures.sanique._ops.off import turn_off_sanique
from goodest.adventures.sanique._ops.status import check_sanique_status

def sanique_venture ():
	return {
		"name": "sanique",
		"kind": "task",
		"turn on": {
			"adventure": turn_on_sanique,
		},
		"turn off": turn_off_sanique,
		"is on": check_sanique_status
	}