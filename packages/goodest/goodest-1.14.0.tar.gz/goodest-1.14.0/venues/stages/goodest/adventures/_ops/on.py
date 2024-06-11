

'''
	from goodest._ops.on import turn_on
	turn_on ()
'''

from goodest.adventures.sanique._ops.on import turn_on_sanique
from goodest.adventures.monetary._ops.on import turn_on_monetary_node
from goodest.adventures.demux_hap._controls.on import turn_on_demux_hap

from goodest._essence import retrieve_essence
from goodest.adventures._ops.status import check_status
	
import rich


def turn_on ():	
	essence = retrieve_essence ()

	turn_on_demux_hap ()
	
	if ("onsite" in essence ["monetary"]):
		turn_on_monetary_node ()
		
	turn_on_sanique ({
		"wait_for_on": "yes"
	})	
	
	
	
	
	#----
	#
	#	status checks
	#
	#----
	status = check_status ()
	
	if ("onsite" in essence ["monetary"]):
		assert (status ["monetary"] ["local"] == "on"), status
	
	assert (status ["sanique"] ["local"] == "on"), status
	
