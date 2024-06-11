
'''
	import O2.wall.UFW.start as wall_start
'''	

'''
	This should allow inbound:
		22
		80
		443
'''

import os

def start_scripts (scripts):
	for script in scripts:
		print ()
		print ("script:", script)
		os.system (script)

def solidly ():
	start_scripts ([
		"dnf install ufw -y",
		"ufw allow 443",
		"ufw allow 80",
		"ufw status"
	])

