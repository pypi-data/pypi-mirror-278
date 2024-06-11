







'''
	import climate
	smoothie = climate.find ("smoothie")

	URL = smoothie ["protocol"] + smoothie ["domain"] + ":" + smoothie ["ports"][0]
'''

'''
	import climate
	climate.change ("node", {
		"CWD": ""	
	})
'''


import pathlib
from os.path import dirname, join, normpath
import sys
import copy

climate = {

}


def change (field, plant):
	#global CLIMATE;
	climate [ field ] = plant


def find (* positionals):
	if (len (positionals) == 1):
		return copy.deepcopy (climate) [ positionals[0] ]
	
	return copy.deepcopy (climate)
	



#