

'''
	from goodest.adventures.redis_mix._ops.on import turn_on_redis
	turn_on_redis ()
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


def turn_on_redis (packet = {}):
	return