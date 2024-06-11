
'''
	from goodest.shows_v2.treasure.nature.land.measures.multiply import multiply_land_measures
	multiply_land_measures (
		amount = 10,
		measures = measures
	)
'''


from fractions import Fraction

def multiply_land_measures (
	measures = None, 
	amount = None
):


	for measure in measures:
		pers = measures [ measure ]
		
		for per in pers:
			units = pers [per]
		
			if (per == "portion of grove"):
				continue;
		
			if (per not in [ "per package", "per recipe" ]):
				raise Exception (f"The divisor found, '{ per }', was not accounted for.");
			
			for unit in units:
				measures [ measure ] [per] [unit] ["fraction string"] = str (
					Fraction (measures [ measure ] [per] [unit] ["fraction string"]) * Fraction (amount)
				)
				
	return measures;

