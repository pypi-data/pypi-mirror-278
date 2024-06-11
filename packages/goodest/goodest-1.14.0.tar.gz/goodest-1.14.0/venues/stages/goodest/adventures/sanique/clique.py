

'''
	This is for starting sanique in floating (or implicit) mode.
'''

from goodest.adventures.sanique._ops.on as turn_on_sanique
from goodest.adventures.sanique._ops.off as turn_off_sanique
from goodest.adventures.sanique._ops.sanic.status import check_sanique_status
	
from goodest._essence import prepare_essence
from goodest._essence import run_script_from_file
	
import click
import rich

import time
import os
import pathlib
from os.path import dirname, join, normpath
import sys

def clique ():

	@click.group ("sanique")
	def group ():
		pass


	@group.command ("on")
	def on ():			
		turn_on_sanique ()
		

	@group.command ("off")
	def off ():
		turn_off_sanique ()
		
		
	@group.command ("status")
	def status (essence_path):
		check_sanique_status ()
		

	return group




#



