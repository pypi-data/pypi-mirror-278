

'''
	from goodest.adventures.redis_mix._ops.refresh import refresh_redis
	refresh_redis ()
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


def refresh_redis (packet = {}):
	return