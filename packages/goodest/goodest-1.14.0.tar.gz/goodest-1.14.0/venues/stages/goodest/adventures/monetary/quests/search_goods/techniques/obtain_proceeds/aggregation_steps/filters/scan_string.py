



def occur (
	scan_string = ""
):
	scan_string = scan_string.lower ()

	if (len (scan_string) >= 1):
		return {
			"$match": {
				"lower_case_name": { 
					'$regex' : scan_string, 
					'$options' : 'i'
				}
			}
		}
		
	return None