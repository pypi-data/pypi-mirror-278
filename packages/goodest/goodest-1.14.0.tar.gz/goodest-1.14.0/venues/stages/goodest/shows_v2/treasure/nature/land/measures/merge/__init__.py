
'''
	from goodest.shows_v2.treasure.nature.land.measures.merge import merge_land_measures 
	merge_land_measures (
		aggregate_measures,
		new_measures
	)
'''

#----
#
import goodest.measures.number.sci_note_2 as sci_note_2
#
#
from fractions import Fraction
#
#----

def merge_land_measures (
	aggregate_measures, 
	new_measures
):
	for measure in new_measures:
		pers = new_measures [ measure ]
		
		for per in pers:
			units = pers [per]
			
			if (per == "portion of grove"):
				continue;
			
			if (per not in [ "per recipe" ]):
				raise Exception (f"The divisor found, '{ per }', was not accounted for.");
			
			for unit in units:
				#print ("unit:", unit)
			
				if (measure not in aggregate_measures):
					aggregate_measures [ measure ] = {}
					aggregate_measures [ measure ] [per] = {}
					aggregate_measures [ measure ] [per] [unit] = {}
					aggregate_measures [ measure ] [per] [unit] ["fraction string"] = "0"

				the_fraction_string = str (
					Fraction (new_measures [ measure ] [per] [unit] ["fraction string"]) + 
					Fraction (aggregate_measures [ measure ] [per] [unit] ["fraction string"])
				)
				
				aggregate_measures [ measure ] [per] [unit] ["fraction string"] = the_fraction_string
				aggregate_measures [ measure ] [per] [unit] ["scinote string"] = sci_note_2.produce (
					Fraction (the_fraction_string)
				)
				