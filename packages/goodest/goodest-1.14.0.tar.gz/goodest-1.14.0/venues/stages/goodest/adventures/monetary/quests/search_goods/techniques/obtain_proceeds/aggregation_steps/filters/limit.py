

'''
	https://stackoverflow.com/questions/47821821/fetch-first-n-and-last-n-records-from-mongodb-collection
'''
def occur (limit):
	return {
		"$limit": limit
	}

	'''
	return {
		"$facet": {
			"top 10": [
				{ "$limit": 10 }
			],
			"bottom 10": [
				{ "$limit": 10 }
			]
		}
	}
	'''