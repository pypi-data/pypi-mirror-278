

'''
	from goodest.adventures.redis_mix._ops.on import turn_off_redis
	turn_off_redis ()
'''

#----
#
#
from goodest._essence import retrieve_essence
#
#
import atexit
import json
import multiprocessing
import subprocess
import time
import os
import shutil
import sys
import time
#
#----


def turn_off_redis (packet = {}):
	return