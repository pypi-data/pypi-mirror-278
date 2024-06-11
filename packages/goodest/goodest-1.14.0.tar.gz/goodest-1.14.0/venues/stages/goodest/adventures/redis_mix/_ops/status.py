

'''
	from goodest.adventures.redis_mix._ops.status import check_redis_status
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


def check_redis_status (packet = {}):
	return