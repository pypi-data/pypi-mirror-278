
'''
	from goodest.adventures.ventures import retrieve_ventures
	the_ventures = retrieve_ventures ()

'''

from goodest.adventures.sanique.venture import sanique_venture
from goodest.adventures.squishy.venture import squishy_venture

from goodest.adventures.monetary.venture import monetary_venture
from goodest.adventures.demux_hap.venture import demux_hap_venture
from goodest.adventures.vv_turbo.venture_build import bun_venture_build	
from goodest.adventures.vv_turbo.venture_dev import bun_venture_dev	

from goodest._essence import retrieve_essence

from ventures import ventures_map

def retrieve_ventures ():
	essence = retrieve_essence ()

	return ventures_map ({
		"map": essence ["ventures"] ["path"],
		"ventures": [
			#squishy_venture (),
			sanique_venture (),
			monetary_venture (),
			demux_hap_venture (),
			bun_venture_build (),
			#bun_venture_dev ()
		]
	})