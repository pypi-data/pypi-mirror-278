




'''
	from womb.adventures.sanique.utilities.generate_inventory_paths import generate_inventory_paths
	inventory_paths = generate_inventory_paths (directory)
'''


'''
	https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
'''


import glob
import os

def generate_inventory_paths (directory):
	inventory_glob = directory + "/**/*"
	inventory = glob.glob (directory + "/**/*", recursive = True)
	
	#print ('inventory glob:', inventory_glob)
	
	inventory_partials = {}
	for inventory_path in inventory:
		if (os.path.isfile (inventory_path)):
			FP = open (inventory_path, "rb")
			content = FP.read () 
			FP.close ()
		
			extension = inventory_path.split ('.')[-1].lower ()
			mime = ""
			if (extension == "css"):
				mime = "text/css"
			elif (extension == "js"):
				mime = "text/javascript"
			elif (extension == "html"):
				mime = "text/html"
			
			elif (extension == "ico"):
				mime = "image/x-icon"
			elif (extension == "jpg"):
				mime = "image/jpg"
			elif (extension == "png"):
				mime = "image/png"
			elif (extension == "svg"):
				mime = "image/svg"
				
			else:
				raise Exception (f"Extension '{ extension }' was not accounted for.")
		
			inventory_partials [ inventory_path.split (directory + "/") [1] ] = {
				"path": inventory_path,
				"content": content,
				"extension": extension,
				"mime": mime
			};

	#print ("path inventory size:", len (inventory))

	#for inventory_path in inventory:
	#	print ("inventory_path:", inventory_path)	
		
	return inventory_partials