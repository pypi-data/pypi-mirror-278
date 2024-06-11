

'''
	vector_name_and_emblem.occur (
		name = "ASPARAGUS MEDLEY, ASPARAGUS",
		direction = "after"
	) 
'''

'''
	Description:
		This is for the collection(s) that
		aren't chosen in the vector filter.
		
		This filters the document stated
		and documents that have names that are
		(alphabetically) 
		
			>= or <= 
			
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
		[supp] 78 asparagus
		[food] 14328 asparagus
		[food] 3193 asparagus
		[food] 31 asparagus medley, asparagus
		
		filter {
			name = "asparagus",
			direction = "after"
		}
		
		[food] 29 asparagus
		[food] 30 asparagus
		[supp] 78 asparagus
		[food] 14328 asparagus
		[food] 3193 asparagus
		[food] 31 asparagus medley, asparagus
'''

def occur (
	name = "",
	direction = "after"
):
	if (direction == "after"):
		operator = "$gte"
	else:
		operator = "$lte"

	return { 
		"$match": { 
			"$or": [
			
				#
				#	allow the treasure if:
				#		document_name > provided_name
				#	
				{
					"$expr": {
						operator : [ 
							"$lower_case_name", 
							name
						]
					}
				}
			]
		}
	}




