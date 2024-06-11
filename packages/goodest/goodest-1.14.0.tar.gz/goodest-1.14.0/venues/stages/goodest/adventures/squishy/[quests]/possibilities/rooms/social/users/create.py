


import subprocess

def create_user (user, the_pass):
    try:
        subprocess.run ([
			'useradd', 
			'-m', 
			user
		])
		
        subprocess.run(['passwd', user], input=the_pass.encode(), check=True)
        
        print(f"User '{username}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating user: {e}")



create_user ("socializer", "socializers_password")
