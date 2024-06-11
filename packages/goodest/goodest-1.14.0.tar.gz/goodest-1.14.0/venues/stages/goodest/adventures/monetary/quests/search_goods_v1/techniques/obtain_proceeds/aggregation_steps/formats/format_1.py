

'''
	https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/
'''
def occur ():	
	return { 
		"$project": {
			"lower_case_name": 1,
			
			"nature.kind": 1,
			"nature.identity": 1,
			
			"emblem": 1,
			"food_emblem": 1,
			"supp_emblem": 1,
			
			"stats": 1
		}
	}