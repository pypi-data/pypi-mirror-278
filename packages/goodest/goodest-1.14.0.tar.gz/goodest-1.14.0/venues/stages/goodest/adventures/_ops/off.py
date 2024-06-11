

'''
	from goodest._ops.off import turn_off
	turn_off ()
'''

#----
#
from goodest._essence import retrieve_essence
#
from goodest.adventures.sanique._ops.off import turn_off_sanique
from goodest.adventures.monetary._ops.off import turn_off_monetary_node
from goodest.adventures.demux_hap._controls.off import turn_off_demux_hap
from goodest.adventures._ops.status import check_status
#
#
import time	
#	
#----

def turn_off ():	
	essence = retrieve_essence ()

	if ("onsite" in essence ["monetary"]):
		turn_off_monetary_node ()	
	
	turn_off_sanique ()
	
	turn_off_demux_hap ()
	
	
	#----
	#
	#	status checks
	#
	#----
	
	
	status = check_status ()
	assert (status ["monetary"] ["local"] == "off"), status
	assert (status ["sanique"] ["local"] == "off"), status