

'''
	from goodest.adventures.demux._controls.on import turn_on_demux_hap
'''

import goodest.adventures.demux_hap.SSL as HA_SSL
import goodest.adventures.demux_hap.configs.HTTPS_to_HTTP as HA_HTTPS_to_HTTP

import os

def turn_on_demux_hap ():
	config_path = "/etc/haproxy/haproxy.cfg"
	
	HA_HTTPS_to_HTTP.build (
		SSL_certificate_path = "/etc/haproxy/SSL/certificate.pem",
		config_path = config_path,
		
		to_addresses = [
			"0.0.0.0:8000",
			"0.0.0.0:8000",
			"0.0.0.0:8000",
			"0.0.0.0:8000",
			"0.0.0.0:8000",
			"0.0.0.0:8000",
			"0.0.0.0:8000",
			"0.0.0.0:8000"
		]
	)
	
	#
	#	Check that the config is good
	#
	#
	os.system (f"haproxy -f '{ config_path }' -c")
	#os.system (f"cat '{ config_path }'")
	
	os.system ("service haproxy start")
	#os.system ("service haproxy status")
	
	if (False):
		os.system ("systemctl restart haproxy")
		os.system ("systemctl status haproxy -l --no-pager")