

import click

import O2.sieve.UFW.start as wall_start
import O2.sieve.UFW.install as wall_install
import O2.sieve.UFW.status as wall_status


@click.group ("UFW")
def group ():
	pass

@group.command ("build")
def build ():	
	wall_install.solidly ()
	
@group.command ("start")
def start ():	
	wall_start.solidly ()
	wall_status.show ()
	
@group.command ("status")
def start ():	
	wall_status.show ()	
	
@group.command ("stop")
def stop ():	
	print ("not implemented")
	





#





