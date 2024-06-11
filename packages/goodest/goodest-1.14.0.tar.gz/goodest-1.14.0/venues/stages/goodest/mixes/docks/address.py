

'''
	from goodest.mixes.docks.address import find_container_address
	address = find_container_address ()
'''

import socket

def find_container_address ():
    return socket.gethostbyname (socket.gethostname ())



