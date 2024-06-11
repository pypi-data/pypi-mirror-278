

'''
	from goodest.adventures.monetary.moves.URL.retrieve import retreive_monetary_URL
	monetary_URL = retreive_monetary_URL ()
'''

'''
	receive_monetary_URL
'''
from goodest._essence import retrieve_essence

def retreive_monetary_URL (database = ""):
	essence = retrieve_essence ()

	if ("URL" in essence ["monetary"]):
		return essence ["monetary"] ["URL"] + database;

	return "mongodb://" + essence ["monetary"] ["host"] + ":" + essence ["monetary"] ["port"] + "/" + database;