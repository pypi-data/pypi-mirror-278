
'''
	from goodest.besties.supp_NIH.nature_v2._ops.retrieve import retrieve_parsed_NIH_supp
	out_packet = retrieve_parsed_NIH_supp ({
		"DSLD_ID": 1,
		"NIH API Pass": ""
	})
'''

#----
#
import goodest.besties.supp_NIH.deliveries.one as NIH_API_one
import goodest.besties.supp_NIH.nature_v2 as supp_NIH_nature_v2
#
from goodest.adventures.alerting.parse_exception import parse_exception
from goodest.adventures.alerting import activate_alert
#
import law_dictionary
from biotech.topics.show.variable import show_variable

#
#----

'''
	supplement = NIH_API_one.find (
		dsld_id,
		api_key
	)
	
	NIH_supplement_data = supplement ["data"]
	NIH_supplement_source = supplement ["source"]
'''

def retrieve_parsed_NIH_supp (packet):
	'''
		law_dictionary
	'''
	report = law_dictionary.check (	
		return_obstacle_if_not_legit = True,
		allow_extra_fields = False,
		laws = {
			"DSLD_ID": {
				"required": True,
				"type": str
			},
			"NIH API Pass": {
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

	
	DSLD_ID = packet ["DSLD_ID"]
	NIH_API_Pass = packet ["NIH API Pass"]
	
	
	
	'''
		API Ask
	'''
	try:
		show_variable ('supp_NIH parse?')
	
		supp_NIH = NIH_API_one.find (
			DSLD_ID = DSLD_ID,
			api_key = NIH_API_Pass
		)
	except Exception as E:
		try:
			exc_msg = str (E)
			show_variable ("exception message:", exc_msg)
			
			if (exc_msg == "The NIH API returned status code 404."):
				return {
					"anomaly": "The NIH API could not find that FDC_ID."
				}
			
			exc_type = type (E).__name__
			activate_alert ("exception type", {
				"exception type": exc_type
			})
			
			exc_traceback = sys.exc_info () [2]
	
		except Exception as E2:
			activate_alert ("emergency", {
				"exception": parse_exception (E2)
			})
		
		return {
			"anomaly": "The food could not be retrieved from the NIH API."
		}
		
		
	try:
		nature = supp_NIH_nature_v2.create (supp_NIH ["data"])
		return nature
		
	except Exception as E:
		activate_alert ("emergency", {
			"exception": parse_exception (E)
		})
	
		return {
			"anomaly": "The food could not be parsed."
		}
	
	return {
		"anomaly": "An unaccouted for anomaly occurred while parsing and retrieving the food data."
	}