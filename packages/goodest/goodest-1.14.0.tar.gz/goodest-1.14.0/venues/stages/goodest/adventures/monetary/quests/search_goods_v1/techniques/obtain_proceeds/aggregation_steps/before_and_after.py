



def occur (
	reverse = False
):
	if (reverse):
		direction = -1;
	else:
		direction = 1
		
	sortBy = { 
		"lower_case_name": direction,
		"food_emblem": direction,
		"supp_emblem": direction
	}

	return {
		"$setWindowFields": {
			"partitionBy": None,
			"sortBy": sortBy,
			"output": {
				"stats.before": {
					#
					#	This adds 1 for each document in the window
					#
					"$sum": 1,
					"window": {
						#
						#	from the first document in the 
						#	window to 1 before the current document
						#
						"documents": [ "unbounded", -1 ]
					}
				},
				"stats.after": {
					#
					#	This adds 1 for each document in the window
					#
					"$sum": 1,
					"window": {
						#
						#	from the 1 after the current document to the last document in the window
						#
						"documents": [ 1, "unbounded" ]
					}
				}
			}
		}
	}