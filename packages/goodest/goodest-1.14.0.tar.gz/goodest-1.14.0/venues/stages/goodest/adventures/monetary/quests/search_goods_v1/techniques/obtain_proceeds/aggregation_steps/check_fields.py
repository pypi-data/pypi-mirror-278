




def occur ():
	return {
		"$match": {
			"$and": [{
				"nature.identity.name": {
					"$exists": True
				},
				"emblem": {
					"$exists": True
				}
			}]
		}
	}