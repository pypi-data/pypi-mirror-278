


'''
	from goodest.shows_v2.treasure.nature.land._ops.develop import develop_land
	land = develop_land ({
		"collection": "essential_nutrients"
	})
'''

'''
	natures:
		This is the amount and identity of the treasures.
	
	measures: 
		These are the sums of the natures.
		
			example, calculated from:
				1.2 packages of sunflower seed + 
				1.6 packages of lentils
	
	grove:
		This is every essential nutrient in the 
		"essential_nutrients" collection.
		
	
'''

from goodest.shows_v2.treasure.nature.land.grove._ops.nurture import nurture_grove
from goodest.shows_v2.treasure.nature.land.measures import build_land_measures_foundation

def develop_land (packet = {}):
	return {
		"natures": [],
		"measures": build_land_measures_foundation (),
		"grove": nurture_grove (packet ["collection"])
	}