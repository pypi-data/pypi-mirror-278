




'''
	from goodest.adventures.vv_turbo.venture_build import bun_venture_build
	bun_venture_build ()
'''


'''
	(cd /habitat/venues/stages/goodest/adventures/vv_turbo/ && bun run dev)
'''

import pathlib
from os.path import dirname, join, normpath
import sys
import os

this_directory = str (pathlib.Path (__file__).parent.resolve ())
cwd = str (normpath (join (this_directory, "apps/web")))


def bun_venture_dev ():
	return {
		"name": "bun_turbo_dev",
		"kind": "process_identity",
		
		"turn on": {
			"adventure": [ 
				"bun",
				"run",
				"dev"
			],
			
			"Popen": {
				"cwd": cwd
			},
		}
	}