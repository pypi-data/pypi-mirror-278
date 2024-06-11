

'''
	HTTP_balancer.build (
		from_port = "80",
		to_addresses = [
			"0.0.0.0:8000",
			"0.0.0.0:8001"
		]
	)
'''


"""
	backend servers
		balance roundrobin
		server server1 0.0.0.0:8000 maxconn 32
		server server2 0.0.0.0:8001 maxconn 32
"""

def build (
	from_port = "80",
	to_addresses = []
):	
	'''
		examples:
			server server1 0.0.0.0:8000 check
			server server1 0.0.0.0:8001 check
	'''
	site_number = 1
	backend_sites = ""
	for to_address in to_addresses:
		name = "site_" + str (site_number)
		backend_sites += f"\tserver { name } { to_address } check\n"
		
		site_number += 1

	#balance = "roundrobin"
	balance = "leastconn"

	config = f"""
global
	daemon
	maxconn 256

defaults
	mode http
	timeout connect 5000ms
	timeout client 50000ms
	timeout server 50000ms

frontend http-in
	bind *:{ from_port }
	default_backend site
	
backend site
	balance { balance }
{ backend_sites }
"""

	return config;