




'''
	from goodest.adventures.squishy.venture import squishy_venture
	squishy_venture ()
'''

#~~~~
#
from ._controls.on import turn_on_squishy
from ._controls.off import turn_off_squishy
from ._controls.is_on import squishy_is_on
#
#
import pathlib
from os.path import dirname, join, normpath
import sys
import os
#
#~~~~

this_directory = str (pathlib.Path (__file__).parent.resolve ())
cwd = str (normpath (join (this_directory, "apps/web")))



def squishy_venture ():
	return {
		"name": "squishy",
		"kind": "task",
		"turn on": {
			"adventure": turn_on_squishy,
		},
		"turn off": turn_off_squishy,
		"is on": squishy_is_on
	}

