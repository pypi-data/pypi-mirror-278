



#----
#
from goodest.adventures._ops.on import turn_on
from goodest.adventures._ops.off import turn_off
from goodest.adventures._ops.refresh import refresh
from goodest.adventures._ops.status import check_status
#
#
from ..monetary._ops._clique import monetary_clique
from ..squishy._controls._clique import squishy_clique
from ..demux_hap._controls._clique import demux_hap_clique
#
#
from goodest.adventures.ventures import retrieve_ventures
#
#
import click
#
#----

def ventures_clique ():
	ventures = retrieve_ventures ()

	@click.group ("ventures")
	def group ():
		pass

	
	#
	#	goodest on
	#
	@group.command ("on")
	def on ():		
		ventures ["turn on"] ()

	
	@group.command ("off")
	def off ():
		ventures ["turn off"] ()

	@group.command ("refresh")
	def refresh_op ():
		ventures ["turn off"] ()
		ventures ["turn on"] ()
		
		
	@group.command ("status")
	def status ():
		ventures ["is on"] ()


	return group




#



