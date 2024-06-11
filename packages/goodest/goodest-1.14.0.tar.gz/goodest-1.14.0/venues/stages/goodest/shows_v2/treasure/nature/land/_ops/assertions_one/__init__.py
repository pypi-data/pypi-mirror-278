


'''
	This is assertions about the land once 1
	food or supp has been added.
'''

'''
	from goodest.shows_v2.treasure.nature.land._ops.assertions_one import make_land_assertions_one
	make_land_assertions_one (
		land = land
	)
'''

from goodest.shows_v2.treasure.nature.land.grove._ops.assertions import make_grove_assertions
	
def make_land_assertions_one (land):
	assert (len (land ["natures"]) == 1)
	make_grove_assertions (land ["grove"])
