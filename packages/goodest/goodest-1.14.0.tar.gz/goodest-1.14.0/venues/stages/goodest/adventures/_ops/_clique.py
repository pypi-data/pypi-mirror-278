

#%%%%
#
#
from ..monetary._controls._clique import monetary_clique
from ..squishy._controls._clique import squishy_clique
from ..demux_hap._controls._clique import demux_hap_clique
#
#
from goodest.adventures.ventures import retrieve_ventures
#
#
import click
#
#%%%%

def adventures_clique ():
	@click.group ("adventures")
	def group ():
		pass


	group.add_command (monetary_clique ())
	group.add_command (squishy_clique ())
	group.add_command (demux_hap_clique ())


	return group




#



