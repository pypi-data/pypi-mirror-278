




'''
import goodest.mixes.insure.equality as equality
equality.check (1, 1)
'''

import json
def check (one, two):
	if (one != two):		
		raise Exception (f'''
		
			An inequality was found.
			
			{ one } != { two }
			
		''')

	return