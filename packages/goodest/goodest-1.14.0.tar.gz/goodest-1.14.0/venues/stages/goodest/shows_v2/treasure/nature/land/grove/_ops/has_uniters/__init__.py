



'''
	from goodest.shows_v2.treasure.nature.land.grove._ops.has_uniters import has_uniters
	has_uniters (grove)
'''

'''
	summary:
		This is meant for checking on 1 food or 1 supplement,
		to assess whether additions need to be made to uniters.
		
		example?
			"carbohydrate" -> "sugars, total" -> "added sugars"
'''

'''
	example:
		['carbohydrates'][][ 2 ]
			['dietary fiber', 'fiber, total dietary'][][ 6 ]
			['sugars, total'][][ 7 ]
				['added sugars', 'sugars, added'][][ 8 ]


		['fats', 'total fat', 'lipids', 'total lipid (fat)'][][ 3 ]
			['monounsaturated fat', 'fatty acids, total monounsaturated'][][ 51 ]
			['polyunsaturated fat', 'fatty acids, total polyunsaturated'][][ 15 ]
			['saturated fat', 'fatty acids, total saturated'][][ 4 ]
			['trans fat', 'fatty acids, total trans'][][ 5 ]

		problems:
			If "added sugars" is included, but "sugars, total" isn't,
			then there's a problem.
			
				"sugars, total" mass = "added sugars" mass
					
					for others this might include "biological activity", etc.
			
			
			If "dietary fiber" is included, but "carbohydrates" isn't,
			then there is a problem, since thusly,
			
				"carbohydrate mass" = "dietary fiber" mass
				
					for others this might include "biological activity", etc.
'''

'''
	objectives:
		Make sure there are no missing intermediaries in the grove.
'''
from goodest.shows_v2.treasure.nature.land.grove._ops.seek import seek_ingredient_in_grove
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_uniter import seek_uniter
import goodest.shows_v2.treasure.nature.land.grove._ops.is_story_1 as is_story_1

from goodest.adventures.alerting import activate_alert
	

import json	
	
def has_uniters (grove, return_problem = False):
	story_1_list = is_story_1.generate_list (grove)

	checked = []

	def for_each (entry):	
		nonlocal return_problem;
	
		name = entry ["info"] ["names"] [0]
		if (is_story_1.check (story_1_list, name) == False):
			uniter = seek_uniter (
				grove = grove,
				name_or_accepts = name
			)		
			assert (type (uniter) == dict)	

			checked.append ([
				name, 
				uniter ["info"] ["names"][0]
			])

			
			if (len (entry ["natures"]) >= 1):
				if (len (uniter ["natures"]) == 0 ):
				
					activate_alert ("emergency", f"""
					
	The uniter '{ uniter ["info"] ["names"] }' is comprised of 
	'{ len (uniter ["natures"]) }' natures.
	
	It unites '{ entry ["info"] ["names"] }' which has 
	'{ len (entry ["natures"]) }' natures.				
					
					""")
					
					'''
						possibly where: {
							"amount": "1",
							"source": {
								"name": "",
								"FDC ID": "",
								"UPC": "",
								"DSLD ID": ""
							},
							"ingredient": {
								"name": "added sugars"
							},
							"measures": {
								"mass + mass equivalents": {
									"per package": {
										"listed": [
											"1947.660",
											"mg"
										],
										"grams": {
											"decimal string": "1.948",
											"fraction string": "97383/50000"
										}
									}
								}
							}
						}
						
						Add the "measures" of "added sugar"
						towards the first story of the grove,
						until a uniter with natures is found.
						
							Therefore, if dietary fiber and carbohydrates
							both do not have natures, then add 
							the "measures" ("mass + mass equivalents")
							of "added "sugars" to "dietary fiber"
							and then to "carbohydrates"
						
								for example:
									This:
										carbs = 0g
											dietary fiber = 0g
												added sugars = 10g
									
									Becomes:
										carbs = 10g
											dietary fiber = 10g
												added sugars = 10g		
								
						
							Alternatively, if carbohydrates has 
							natures and dietary fiber doesn't,
							then perhaps assume that the 
							"measures" of "added sugars" are
							already included in carbohydrates.
							
								for example:
									This:
										carbs = 20g
											dietary fiber = 0g
												added sugars = 10g
									
									Becomes:
										carbs = 20g
											dietary fiber = 10g
												added sugars = 10g	
						
						
						add this: {
							"amount": "1",
							"source": {
								"name": "",
								"FDC ID": "",
								"UPC": "",
								"DSLD ID": ""
							},
							"ingredient": {
								"name": "dietary fiber",
								"added from measures of united": "added sugars"
							},
							"measures": {
								"mass + mass equivalents": {
									"per package": {
										"listed": [
											"1947.660",
											"mg"
										],
										"grams": {
											"decimal string": "1.948",
											"fraction string": "97383/50000"
										}
									}
								}
							}
						}
						
						add this: {
							"amount": "1",
							"source": {
								"name": "",
								"FDC ID": "",
								"UPC": "",
								"DSLD ID": ""
							},
							"ingredient": {
								"name": "carbohydrates",
								"added from measures of united": "added sugars"
							},
							"measures": {
								"mass + mass equivalents": {
									"per package": {
										"listed": [
											"1947.660",
											"mg"
										],
										"grams": {
											"decimal string": "1.948",
											"fraction string": "97383/50000"
										}
									}
								}
							}
						}
					'''
					
					if (return_problem):
						return True
					
					entry_name = entry ["info"] ["names"]
					raise Exception (f"Uniter nature not found for '{ entry_name }'")
					
					
			
	
	problem = seek_ingredient_in_grove (
		grove = grove,
		for_each = for_each
	)
	
	return {
		"checked": checked,
		"problem": problem
	}
