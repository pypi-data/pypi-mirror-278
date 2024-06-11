
'''
	python3 insurance.py besties/supp_NIH/nature/form/amount/status_214893.py
'''


import goodest.besties.supp_NIH.nature_v2.form.amount as form_amount

def check_1 ():	
	amount = form_amount.calc (
		net_contents = [
			{
				"order": 1,
				"quantity": 16,
				"unit": "Oz(s)",
				"display": "16 Oz(s)"
			},
			{
				"order": 2,
				"quantity": 454,
				"unit": "Gram(s)",
				"display": "454 Gram(s)"
			}
		],
		form_unit = "gram"
	)

	assert (amount == "454")

	return;
	
checks = {
	"check 1": check_1
}