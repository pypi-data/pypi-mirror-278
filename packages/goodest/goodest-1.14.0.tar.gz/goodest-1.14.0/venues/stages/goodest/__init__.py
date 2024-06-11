
'''
	from goodest import build_goodest
	
	goodest = build_goodest ({
		
	})
	
	goodest ["on"] ()
	
	goodest ["retrieve food"] ()
	goodest ["retrieve supp"] ()
	
	goodest ["retrieve recipe"] ()
'''




from goodest._controls._clique import clique

'''

'''
import rich

def build_goodest ():
	def on ():
		return;
	
	return {
		"on": on,
		"off": "",
		
		"retrieve food": "",
		"retrieve supp": "",
		
		"retrieve recipe": ""
	}