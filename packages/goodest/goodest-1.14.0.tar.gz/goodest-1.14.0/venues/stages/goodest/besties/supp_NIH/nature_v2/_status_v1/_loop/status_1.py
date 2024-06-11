

'''
	status_multivitamin_276336
'''
'''
	python3 insurance.py besties/supp_NIH/nature/_status/_loop/status_1.py
'''

import goodest.besties.supp_NIH.nature_v2 as supp_NIH_nature_v2
import goodest.besties.supp_NIH.examples as NIH_examples

import json

def check_1 ():	
	loop = [
		"coated tablets/multivitamin_276336.JSON",
		"other/chia_seeds_214893.JSON",
		"powder/mane_270619.JSON",
		"powder/nutritional_shake_220884.JSON",
		"powder packets/multivitamin_246811.JSON",
		#"tablets/calcium_261967.JSON",
		#"tablets/multivitamin_249664.JSON",
		#"goodest_capsules/probiotics_248267.JSON"
	]
	
	for supp in loop:
		supp_1 = supp_NIH_nature_v2.create (
			NIH_examples.retrieve (supp)
		)
		

	
	return;
	
checks = {
	"check 1": check_1
}