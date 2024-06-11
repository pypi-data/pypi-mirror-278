

'''
	from goodest._ops.status import check_status
	check_status ()
'''
from biotech.topics.show.variable import show_variable

from goodest._essence import retrieve_essence
from goodest.adventures.monetary.moves.URL.retrieve import retreive_monetary_URL

from goodest.adventures.sanique._ops.status import check_sanique_status
from goodest.adventures.monetary._ops.status import check_monetary_status
	
from goodest.mixes.docks.address import find_container_address
	
import rich

def check_status ():	
	essence = retrieve_essence ()

	the_monetary_status = ""
	if ("onsite" in essence ["monetary"]):
		the_monetary_status = check_monetary_status ()
		
	the_sanic_status = check_sanique_status ()
	
	address = find_container_address ()
	
	the_status = {
		"address": address,
		"monetary": {
			"URL": retreive_monetary_URL (),
			"local": the_monetary_status
		},
		"sanique": {
			"port": essence ["sanique"] ["port"],
			"local": the_sanic_status
		}
	}
	
	show_variable ({
		"statuses": the_status
	})
	
	return the_status