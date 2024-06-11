

'''
	from goodest.adventures.squishy.configs import retrieve_path
	rubber = retrieve_path ("rubber.NFT")
	open = retrieve_path ("open.NFT")
'''

#----
#
import os
import pathlib
from os.path import dirname, join, normpath
import sys
#
#----

this_directory = pathlib.Path (__file__).parent.resolve ()	
def retrieve_path (config):
	return str (normpath (join (this_directory, config)))