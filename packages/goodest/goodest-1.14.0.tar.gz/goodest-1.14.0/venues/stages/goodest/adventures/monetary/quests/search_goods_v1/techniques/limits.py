


'''
	This calculates the next and previous
	items.
'''
def obtain_limits (proceeds):
	prev = {}
	next = {}
	def parse_next_or_prev (treasure):
		return {
			"emblem": treasure ["emblem"],
			"name": treasure ["nature"] ["identity"] ["name"],
			"kind": treasure ["nature"] ["kind"]
		}
		
	if (len (proceeds) == 0):
		pass;
	elif (len (proceeds) == 1):
		prev = parse_next_or_prev (proceeds [0])
		next = parse_next_or_prev (proceeds [0])
	else:
		prev = parse_next_or_prev (proceeds [0])
		next = parse_next_or_prev (proceeds [ len (proceeds) - 1 ])
	
	return [ prev, next ]