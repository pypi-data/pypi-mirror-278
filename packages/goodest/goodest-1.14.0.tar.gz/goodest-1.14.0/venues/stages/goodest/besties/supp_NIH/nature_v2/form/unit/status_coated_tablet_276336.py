
'''
	python3 status.proc.py besties/supp_NIH/nature_v2/form/unit/status_coated_tablet_276336.py
'''

import goodest.besties.supp_NIH.nature_v2.form.unit as form_unit
import goodest.besties.supp_NIH.examples as NIH_examples
	
def check_1 ():
	supp_1 = NIH_examples.retrieve ("coated tablets/multivitamin_276336.JSON")
		
	unit = form_unit.calc (
		ingredient_rows = supp_1 ["ingredientRows"],
	
		net_contents = [
			{
				"order": 1,
				"quantity": 90,
				"unit": "Coated Tablet(s)",
				"display": "90 Coated Tablet(s)"
			}
		],
		physical_state = {
			"langualCode": "E0155",
			"langualCodeDescription": "Tablet or Pill"
		},
		serving_sizes = [
			{
				"order": 1,
				"minQuantity": 1,
				"maxQuantity": 1,
				"minDailyServings": 1,
				"maxDailyServings": 1,
				"unit": "Tablet(s)",
				"notes": "",
				"inSFB": True
			}
		]
	)
	
	assert (unit == "Coated Tablet"), unit
	
	return;
	
	
checks = {
	"check 1": check_1
}