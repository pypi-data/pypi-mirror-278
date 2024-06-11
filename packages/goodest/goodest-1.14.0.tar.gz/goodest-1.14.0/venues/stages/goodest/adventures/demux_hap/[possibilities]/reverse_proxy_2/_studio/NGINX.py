






def build (
	SSL_CERT 			= "",
	SSL_KEY 			= "",
	
	ACCESS_LOGS 		= "/var/log/nginx/access.log;",
	ERROR_LOGS 			= "/var/log/nginx/error.log;",
	
	HTTPS_ACCESS_LOGS 	= "/LOGS",
	
	PROXY_TO_PORT		= ""
):



	return f"""
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {{
	worker_connections 768;
}}

http {{
	sendfile on;
	tcp_nopush on;
	tcp_nodelay on;
	keepalive_timeout 65;
	types_hash_max_size 2048;

	include /etc/nginx/mime.types;
	default_type application/octet-stream;

	# SSL
	# Dropping SSLv3, ref: POODLE ????
	#--------------------------------------------------------------------
	ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; 
	ssl_prefer_server_ciphers on;
	#--------------------------------------------------------------------

	# LOGS
	#--------------------------------------------------------------------
	access_log { ACCESS_LOGS }
	error_log  { ERROR_LOGS }
	#--------------------------------------------------------------------

	gzip on;

	upstream nodes {{
		#
		# enable sticky session based on IP
		#
		ip_hash;

		server 127.0.0.1:11843;
		
		#server 127.0.0.1:5612;

		# SEND 5x more traffic to this one????
		# server 127.0.0.1:4009 weight=5;
	}}

	#
	#	REDIRECTS HTTP TO HTTPS, OR SOMETHING....
	#
	server {{
		# server_name localhost;

		listen 0.0.0.0:80;
		return 301 https://$host$request_uri;
	}}

	server {{
		# server_name localhost;

		listen 443 ssl default_server;
		listen [::]:443 ssl default_server;

		ssl_certificate     "{ SSL_CERT }";
		ssl_certificate_key "{ SSL_KEY }";

		access_log "{ HTTPS_ACCESS_LOGS }";

		location / {{
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_set_header Host $host;

			proxy_pass http://localhost:11843;

			#
			#	PROXY TO THE "nodes" block
			#
			#proxy_pass http://nodes;


			## proxy_redirect off;

			# enable WebSockets
			proxy_http_version 1.1;
			proxy_set_header Upgrade $http_upgrade;
			proxy_set_header Connection "upgrade";
		}}
		
		location /socket.io {{
			proxy_pass http://localhost:11843/socket.io;
			
			proxy_http_version 1.1;
			proxy_buffering off;
			
			proxy_set_header Upgrade $http_upgrade;
			proxy_set_header Connection "Upgrade";
			proxy_set_header Host $http_host;
			proxy_set_header X-Forwarded-Host $http_host;
			proxy_set_header X-Forwarded-Proto $scheme;
		}}
	}}
}}
	"""