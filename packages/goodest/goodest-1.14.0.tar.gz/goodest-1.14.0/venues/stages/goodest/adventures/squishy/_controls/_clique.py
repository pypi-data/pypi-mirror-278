



#/
#
from .obtain import obtain_squishy
from .on import turn_on_squishy
#
#	
import click
import time
#
#\



def squishy_clique ():

	@click.group ("squishy")
	def group ():
		pass

	@group.command ("obtain")
	def on ():
		build_squishy ()
		return;
	
	@group.command ("on")
	def off ():
		turn_on_squishy ({
			"config": "rubber.NFT"
		})
		return;
		
	@group.command ("off")
	def off ():
		turn_on_squishy ({
			"config": "open.NFT"
		})
		return;
	
	@group.command ("on-docker")
	def on ():
		turn_on_squishy ({
			"config": "docker_bridge_enhanced_on.NFT"
		})
		return;
	
	@group.command ("off-docker")
	def off ():
		turn_on_squishy ({
			"config": "docker_bridge_on.NFT"
		})
		return;


	return group




#


#


#
