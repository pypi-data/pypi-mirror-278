






'''
	import goodest.mixes.procedure as procedure
	procedure.implicit (
		script = [
		
		]
	)
'''

import rich
	
from fractions import Fraction
import multiprocessing
import subprocess
import time
import os
import atexit

#
#	tethered
#
def explicit (script):
	the_process = subprocess.Popen (script)
	atexit.register (lambda: the_process.terminate ())
	time.sleep (5)
	
	return the_process
	
#
#	floating,
#	untethered
#
def implicit (script):
	the_process = subprocess.Popen (
		script
	)
	return the_process

def go (
	script = []
):
	mongo_process = implicit (script)
