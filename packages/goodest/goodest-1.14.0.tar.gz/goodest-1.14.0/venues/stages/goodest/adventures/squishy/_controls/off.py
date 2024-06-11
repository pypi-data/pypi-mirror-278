
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
	
def turn_off_squishy (packet = {}):
	essence = retrieve_essence ()

	rubber = retrieve_path ("open.NFT")
	
	procedure.implicit (
		script = [
			"nft", 
			"-f",
			f"{ open }"
		]
	)

	os.system ("nft list ruleset")

	return;

