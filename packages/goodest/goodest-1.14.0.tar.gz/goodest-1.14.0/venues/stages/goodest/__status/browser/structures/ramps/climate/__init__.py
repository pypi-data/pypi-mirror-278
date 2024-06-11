
'''
import ramps.climate as climate
this_climate = climate.find ()
'''

'''
	script = 'window.localStorage.setItem ("node address", "' + climate.back_end_address + '")'
	driver.execute_script (script)
'''

def find ():
	environments = {
		"dev": {
			
		},
		"stage": {
			
		}
	}

	class climate:
		def __init__ (this):
			#front_end_address = "https://vegansink.com"
			#front_end_address = "https://127.0.0.1"
			#front_end_address = "https://146.190.63.53"
			#front_end_address = "https://veganmodule.com"
		
			#
			#	the front address
			#
			this.address = "https://0.0.0.0"
			
			this.headless = True
			
			#
			#	localStorage.setItem ("node address", "http://127.0.0.1:48938")
			#
			# this.back_end_address = "http://127.0.0.1:48938"
			# this.back_end_address = "https://veganmodule.com"
			this.back_end_address = "https://0.0.0.0"


	
	return climate ()