




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


'''
	Increase the first or second number each time.
	The third number is irrelevant.
'''
env = os.environ.copy ()
env ["the_version"] = "1.10.0"

def bun_venture_build ():
	return {
		"name": "bun_turbo_build",
		"kind": "process_identity",
		
		"turn on": {
			"adventure": [ 
				"bun",
				"run",
				"build",
				"--sourcemap",
				"inline"
			],
			
			"Popen": {
				"cwd": cwd,
				"env": env
			},
		}
	}