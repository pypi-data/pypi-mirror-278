
'''
	from goodest.besties.food_USDA.nature_v2._ops.retrieve import retrieve_parsed_USDA_food
	out_packet = retrieve_parsed_USDA_food ({
		"USDA API Pass": 
		"FDC_ID": 1		
	})
'''

#----
#
import goodest.besties.food_USDA.deliveries.one as retrieve_1_food
import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2
#
from goodest.adventures.alerting import activate_alert
from goodest.adventures.alerting.parse_exception import parse_exception
#
import law_dictionary
#
#
import sys
#
#----

def retrieve_parsed_USDA_food (packet):
	'''
		law_dictionary
	'''
	report = law_dictionary.check (	
		return_obstacle_if_not_legit = True,
		allow_extra_fields = False,
		laws = {
			"FDC_ID": {
				"required": True,
				"type": str
			},
			"USDA API Pass": {
				"required": True,
				"type": str
			}
		},
		dictionary = packet
	)
	if (report ["advance"] != True):
		return {
			"anomaly": report ["obstacle"]
		}

	
	FDC_ID = packet ["FDC_ID"]
	USDA_API_Pass = packet ["USDA API Pass"]
	
	activate_alert ("info", "variables passed check", mode = "condensed")

	try:
		activate_alert ("info", 'parsing USDA food data')
		
		food_USDA = retrieve_1_food.presently (
			FDC_ID = FDC_ID,
			API_ellipse = USDA_API_Pass
		)
	except Exception as E:
		activate_alert ("emergency", {
			"exception": parse_exception (E)
		})
		
		try:
			if (str (E) == "The USDA API returned status code 404."):
				return {
					"anomaly": "The USDA API could not find that FDC_ID."
				}
			
		except Exception as E2:
			pass;
		
		return {
			"anomaly": "The food could not be retrieved from the USDA API."
		}
		
		
	try:
		nature = food_USDA_nature_v2.create (food_USDA ["data"])
		return nature
		
	except Exception as E:
		activate_alert ("emergency", {
			'exception': parse_exception (E)
		})
	
		return {
			"anomaly": "The food could not be parsed."
		}
	
	return {
		"anomaly": "An unaccouted for anomaly occurred while parsing and retrieving the food data."
	}