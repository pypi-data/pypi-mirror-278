


'''
	Summary:
		This should be called after all the ingredients have been added
		to the grove.
'''

'''
	from goodest.shows_v2.treasure.nature.land._ops.cultivate import cultivate_land
	cultivate_land (
		land = land
	)
'''


#
#	land
#
from goodest.shows_v2.treasure.nature.land._ops.measures_sums import calc_measures_sums
from goodest.shows_v2.treasure.nature.land._ops.calculate_portions import calculate_portions
from goodest.shows_v2.treasure.nature.land._ops.assertions_one import make_land_assertions_one

#
#	grove
#
from goodest.shows_v2.treasure.nature.land.grove._ops.has_uniters import has_uniters


def cultivate_land (
	land = {}
):
	'''
		This calculate the measure sums (of the supp)
		from the the measures (of the supp ingredients).
		
		?Probably this calculate the food measures also?
	'''
	calc_measures_sums (
		land = land
	)
	
	'''
		This calculate the fractional amounts
		of ingredient measures.
	'''
	calculate_portions (
		land = land
	)
	
	
	'''
		summary:
			This makes sure that the story 2 and above "essentials",
			have a uniter that has "natures".
			
			That is make sure if "added, sugars" is listed,
			that "sugars, total" is listed.
		
		example:
			sugars, total	<- make sure that this exists, if "added sugars" is added.
				added, sugars
	'''
	has_uniters (land ["grove"])

	
	make_land_assertions_one (
		land = land
	)