



def build ():
	documents = str (normpath (join (this_directory, "documents")))
	error_log = str (normpath (join (this_directory, "error.log")))
	access_log = str (normpath (join (this_directory, "access.log")))

	config = f"""
server.port = 80

server.document-root = "{ documents }" 

server.modules = ( "mod_scgi", "mod_accesslog", "mod_proxy" )

server.errorlog = "{ error_log }"
accesslog.filename = "{ access_log }"

$HTTP["host"] == "localhost" {{
	proxy.balance = "hash" 
	proxy.server  = ( 
		"" => ( 
			( 
				"host" => "localhost",
				"port" => 5173
			)
		)
	)
}}
	"""
	
	return config;