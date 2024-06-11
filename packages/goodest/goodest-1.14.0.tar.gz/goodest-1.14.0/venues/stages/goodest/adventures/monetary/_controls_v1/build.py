
'''
	from goodest.adventures.monetary._ops.build import build_monetary
	build_monetary_node ()
'''


'''
	apt update
	apt-get install gnupg curl -y
    curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
	apt update
	apt-get install -y mongodb-org
'''
import goodest.mixes.procedure as procedure
	
import shlex

def build_monetary_node ():
	sequences = [
		"apt update",
		"apt-get install gnupg curl -y",
		"curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor",
		"apt update",
		"apt-get install -y mongodb-org"
	]
	
	for sequence in sequences:
		procedure.implicit (
			script = shlex.split (sequence)
		)
