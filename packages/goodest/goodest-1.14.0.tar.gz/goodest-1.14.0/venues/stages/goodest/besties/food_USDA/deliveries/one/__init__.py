

'''
	import goodest.besties.food_USDA.deliveries.one as retrieve_1_food
	USDA_food = retrieve_1_food.presently (
		FDC_ID,
		API_ellipse = ""
	)
	
	USDA_food_data = USDA_food ["data"]
	USDA_food_source = USDA_food ["source"]
'''

#----
#
import goodest.besties.food_USDA.deliveries.one.assertions.branded as assertions_branded
import goodest.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
#
import goodest.besties.food_USDA.deliveries.source as USDA_source
#
#
from biotech.topics.show.variable import show_variable
#
#
import json
import requests
#
#----

def presently (
	FDC_ID,
	API_ellipse = "",
	kind = "branded"
):
	host = 'https://api.nal.usda.gov'
	path = f'/fdc/v1/food/{ FDC_ID }'
	params = f'?api_key={ API_ellipse }'
	
	address = host + path + params
	
	show_variable ({
		"This ask is on track to be sent.": { 
			"address": address 
		}
	})
	
	r = requests.get (address)
	#show_variable ({
	#	"This response code was received.": r.status_code
	#})
	
	if (r.status_code == 404):
		raise Exception ("The USDA API returned status code 404.")
	
	
	data = json.loads (r.text)

	if (kind == "branded"):
		assertions_branded.run (data)
		
	elif (kind == "foundational"):
		assertions_foundational.run (data)

	return {
		"data": data,
		"source": USDA_source.find (FDC_ID)
	}
	


	#