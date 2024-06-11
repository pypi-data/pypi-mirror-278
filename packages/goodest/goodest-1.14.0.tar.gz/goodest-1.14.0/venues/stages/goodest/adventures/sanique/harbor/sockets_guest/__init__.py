

#----
#
from goodest._essence import retrieve_essence
#
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
from sanic_limiter import Limiter, get_remote_address
#from sanic.response import html
#
#
import json
from os.path import exists, dirname, normpath, join
from urllib.parse import unquote
#
#----

def sockets_guest (packet):
	essence = retrieve_essence ()

	