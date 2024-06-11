
'''
	from goodest.adventures.squishy._controls.on import turn_on_squishy
	turn_on_squishy ()
'''

#----
#
import goodest.mixes.procedure as procedure
from goodest.adventures.squishy.configs import retrieve_path
#
from goodest._essence import retrieve_essence
#
#----

import os
	
def turn_on_squishy (packet = {}):
	essence = retrieve_essence ()
	
	config = packet ["config"]
	rules = retrieve_path (config)
	
	procedure.implicit (
		script = [
			"nft", 
			"-f",
			f"{ rules }"
		]
	)

	os.system ("nft list ruleset")

	return;