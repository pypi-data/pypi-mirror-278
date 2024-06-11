
'''
{
    "name": "communicator",
    "UID": 1000,
    "gecos": "",
    "dir": "/home/communicator",
    "shell": "/bin/bash"
  }
'''

'''

'''


import pwd
import rich

def user_roster ():
	users = pwd.getpwall ()
	
	# print ("users:", users)
	# pwd.getpwnam(username)
	
	roster = []	
	for user in users:
		print ("user:", user)
		
		roster.append ({
			"name": user.pw_name,
			"UID": user.pw_uid,
			"gecos": user.pw_gecos,
			"dir": user.pw_dir,
			"shell": user.pw_shell
		})
	
	#user_list = [user.pw_name for user in users]
	
	
	
	return roster

# Usage
roster = user_roster ()

rich.print_json (data = roster)


	
	
