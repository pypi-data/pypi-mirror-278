



'''
	from goodest.shows_v2.treasure.nature.land.grove._ops.assertions import make_grove_assertions
	make_grove_assertions (grove)
'''


'''
	[{
		"info"
		"measures"
		"natures": []
		"unites"
	}]
'''

def entries_are_formatted_correctly (
	grove,	
	story = 1
):
	for entry in grove:		
		assert ("info" in entry)
		assert ("measures" in entry)
		assert ("natures" in entry)		
		assert ("unites" in entry)
	
		if (len (entry ["unites"]) >= 1):
			grove = entry ["unites"]
		
			entries_are_formatted_correctly (
				grove,
				story = story + 1
			);


def make_grove_assertions (grove):
	entries_are_formatted_correctly (grove)

