






'''
	import goodest.besties.supp_NIH.deliveries.one as NIH_API_one
	supplement = NIH_API_one.find (
		dsld_id,
		api_key
	)
	
	NIH_supplement_data = supplement ["data"]
	NIH_supplement_source = supplement ["source"]
'''


'''
	National Institutes of Health, Office of Dietary Supplements. 
	Dietary Supplement Label Database, 2023. https://dsld.od.nih.gov/. 
'''

import goodest.besties.supp_NIH.deliveries.source as NIH_API_source
import goodest.besties.supp_NIH.deliveries.one.assertions as assertions

from biotech.topics.show.variable import show_variable

import requests

import json

def find (
	DSLD_ID,
	api_key
):
	host = 'https://api.ods.od.nih.gov'
	path = f'/dsld/v9/label/{ DSLD_ID }'
	params = f'?api_key={ api_key }'
	
	coordinate = host + path + params
	
	show_variable ({
		"This ask is on track to be sent.": { 
			"address": coordinate 
		}
	})
	
	response = requests.get (coordinate)

	#show_variable ({
	#	"NIH returned response": response.status_code
	#})
	
	nih_supplement_data = json.loads (response.text)


	assertions.check (nih_supplement_data)

	return {
		"data": nih_supplement_data,
		"source": NIH_API_source.find (nih_supplement_data ["id"])
	}