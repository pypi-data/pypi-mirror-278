

'''
	allow one user:
		iptables -P OUTPUT DROP
		useradd -m -s /bin/bash communicator
		iptables -A OUTPUT -m owner --uid-owner communicator -j ACCEPT
'''

iptables_config = {
	"chains": [{
		"name": "INPUT"
	},{
		"name": "OUTPUT"
	},{
		"name": "FORWARD"
	}]
}


