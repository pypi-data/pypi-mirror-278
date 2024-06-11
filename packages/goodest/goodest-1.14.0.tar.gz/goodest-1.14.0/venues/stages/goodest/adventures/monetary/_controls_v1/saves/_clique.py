

#----
#
from goodest._essence import retrieve_essence
import goodest.mixes.procedure as procedure
#
#
import click
import rich
#
#
import pathlib
from os.path import dirname, join, normpath
import sys
import os
import time
#
#----

from .exports.monetary_export import export_documents
from .exports.monetary_import import import_documents

from .dumps.dump import dump_node
from .dumps.restore import restore_node


def monetary_saves_clique ():
	@click.group ("saves")
	def group ():
		pass
	
	
	'''
		mongodump --uri="URL" 
	'''
	@group.command ("dump")
	@click.option (
		'--version',
		required = True
	)
	def clique_dump (version):	
		dump_node ({
			"version": version
		})
		
	@group.command ("restore")
	@click.option (
		'--version',
		required = True
	)
	@click.option (
		'--drop', 
		help = "drop the current documents in the collection", 
		is_flag = True
	)
	def clique_restore (version, drop):	
		restore_node ({
			"version": version,
			"drop": drop
		})	
		
	'''
		itinerary:
			[ ] goodest_1 adventures monetary saves export --version 2
					[ ] { database }.{ collection }.{ version }.JSON
	'''
	@group.command ("export")
	@click.option (
		'--version',
		required = True
	)
	def save (version):	
		export_documents ({
			"version": version
		})
	
	'''
		goodest_1 adventures monetary saves import --version 2 --drop
	'''
	@group.command ("import")
	@click.option ('--version', required = True)
	@click.option (
		'--drop', 
		help = "drop the current documents in the collection", 
		is_flag = True
	)
	def insert (version, drop):
		import_documents ({
			"version": version,
			"drop": drop			
		})
		

	return group




#



