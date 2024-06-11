

'''
	from goodest._ops.refresh import refresh
	refresh ()
'''

#----
#
from goodest.adventures.sanique._ops.refresh import refresh_sanique
#	
from goodest._essence import retrieve_essence
from goodest.adventures._ops.status import check_status
#
import rich
#
#----

def refresh ():	
	essence = retrieve_essence ()

	#if ("onsite" in essence ["monetary"]):
	#	turn_on_monetary_node ()
		
	refresh_sanique ()	
		
	check_status ()
		
