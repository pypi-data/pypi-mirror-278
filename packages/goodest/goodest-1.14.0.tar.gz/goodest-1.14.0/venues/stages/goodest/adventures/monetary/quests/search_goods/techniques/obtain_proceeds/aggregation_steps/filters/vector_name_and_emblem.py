

'''
	vector_name_and_emblem.occur (
		kind = "food",
		name = "ASPARAGUS MEDLEY, ASPARAGUS",
		emblem = "31",
		
		direction = "after"
	) 
'''
'''
	Description:
		This is for the collection(s) that
		are chosen in the vector filter.
	
		This filters the document stated
		and documents that have names that are
		(alphabetically) 
			
			> or < 
			
		the document name.
		
				  filter emblem 8
				 |-------|
		[ ] [ ] [8] [ ] [ ]
'''

'''
	Example:
		[food] 4 all american veggie burgers
		[food] 29 asparagus
		[food] 30 asparagus
		[food] 78 asparagus
		[food] 14328 asparagus
		[food] 3193 asparagus
		[food] 31 asparagus medley, asparagus
		
		filter {
			kind = "food",
			name = "asparagus",
			emblem = "14328",
			
			direction = "after"
		}
		
		[food] 3193 asparagus
		[food] 31 asparagus medley, asparagus
'''

'''
	https://www.mongodb.com/docs/manual/reference/operator/aggregation/cond/
	https://www.mongodb.com/docs/manual/reference/operator/aggregation/switch/#mongodb-expression-exp.-switch
'''
def occur (
	name = "",
	emblem = "",
	kind = "",
	
	direction = "after"
):
	if (direction == "after"):
		operator = "$gt"
	else:
		operator = "$lt"
		
	if (kind == "food"):
		emblem_label = "$food_emblem"
	else:
		emblem_label = "$supp_emblem"
	
	return { 
		"$match": { 
			"$or": [
			
				#
				#	allow the treasure if:
				#		document_name > provided_name
				#	
				{
					"$expr": {
						operator : [ "$lower_case_name", name ]
					}
				},
				
				#
				#
				#	allow the treasure if:
				#		document_name == provided_name
				#			and then for that document if:
				#				document_emblem > provided_emblem
				#
				{
					"$expr": {
						"$cond": {
							"if": {
								"$eq": [ "$lower_case_name", name ]
							},
							"then": {
								"$cond": {
									"if": {
										operator : [ emblem_label, emblem ]
									},
									"then": True,
									"else": False
								}
							},
							"else": False
						}
					}
				}
			]
		}
	}
