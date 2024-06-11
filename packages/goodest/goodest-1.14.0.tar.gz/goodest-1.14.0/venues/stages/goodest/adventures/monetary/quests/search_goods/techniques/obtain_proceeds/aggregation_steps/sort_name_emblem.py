


def occur (
	reverse = False
):
	if (reverse):
		direction = -1;
	else:
		direction = 1
		
		
	return {  
		"$sort": { 
			"lower_case_name": direction,
			"food_emblem": direction,
			"supp_emblem": direction,
			"meals_emblem": direction
		}
	}
	
	'''
	return {  
		"$sort": { 
			"lower_case_name": -1,
			"emblem": -1
		}
	}
	return {  
		"$sort": { 
			"lower_case_name": 1,
			"emblem": 1
		}
	}
	'''