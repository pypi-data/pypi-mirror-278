
'''

'''

import os

def start_scripts (scripts):
	for script in scripts:
		print ("script:", script)
		os.system (script)

def solidly ():
	start_scripts ([
		"ufw enable"
	])

	return;