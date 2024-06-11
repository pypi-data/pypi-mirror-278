
'''
	from goodest.adventures.sanique.utilities.retrieve_sanique_URL import retrieve_sanique_URL
'''

from goodest._essence import retrieve_essence

def retrieve_sanique_URL ():
	essence = retrieve_essence ()

	return "http://" + essence ["sanique"] ["host"] + ":" + essence ["sanique"] ["port"];