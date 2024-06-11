


import click

import O2.sieve.clique as sieve

def clique ():
	@click.group ("filter")
	def group ():
		pass

	@click.command ("example")
	def example ():	
		print ("example venue")

	group.add_command (sieve.group)
	group ()




#

