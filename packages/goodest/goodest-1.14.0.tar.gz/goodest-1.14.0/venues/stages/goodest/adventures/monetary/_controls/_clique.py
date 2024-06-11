

'''
import goodest.monetary.ingredients.DB.on as ingredient_DB_on
import goodest.monetary.ingredients.DB.off as ingredient_DB_off
import goodest.monetary.ingredients.DB.status as ingredient_DB_status
import goodest.monetary.ingredients.DB.connect as connect_to_ingredient

'''

#----
#
#	local node toggle
#

from .build import build_monetary_node
	
#
#	local or remote 
#
from .status import check_monetary_status
#
from .saves._clique import monetary_saves_clique
#
#
import click
#
#----

def monetary_clique ():
	@click.group ("monetary")
	def group ():
		pass
		
	@group.command ("build")
	#@click.option ('--example-option', required = True)
	def off ():
		build_monetary_node ()


	group.add_command (monetary_saves_clique ())

	return group




#



