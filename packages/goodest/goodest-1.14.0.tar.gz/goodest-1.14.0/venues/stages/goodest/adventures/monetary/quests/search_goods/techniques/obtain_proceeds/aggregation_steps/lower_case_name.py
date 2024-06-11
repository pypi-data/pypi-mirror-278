

def occur ():
	return {
		"$addFields": {
			"lower_case_name": { 
				"$toLower": "$nature.identity.name" 
			}
		}
	}