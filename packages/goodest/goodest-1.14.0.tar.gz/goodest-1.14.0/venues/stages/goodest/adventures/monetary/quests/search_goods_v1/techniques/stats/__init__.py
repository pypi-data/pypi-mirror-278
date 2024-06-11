

'''
	calendar:
	
		[ ] calculate the amounts of {treasures, absorbables} after and before the list
		[ ] calculate the amounts of supps after and before the list
		[ ] calculate the amounts of foods after and before the list
		
		return {
			"amounts": {
				"unlimited": the_supp_count_before + len (proceeds) + the_food_count_before,
				
				"before": 
				"after": 
				
				"returned": len (proceeds)
			}
		}
'''

'''
	return {
		"foods": {
			"after": the_food_count_after,
			"before": the_food_count_before,
			"returned": len (proceeds_foods)
		},
		"supps": {
			"after": the_supp_count_after,
			"before": the_supp_count_before,
			"returned": len (proceeds_supps)
		},
		"amounts": {
			"unlimited": the_supp_count_before + len (proceeds) + the_food_count_before,
			
			"before": the_supp_count_before + the_food_count_before,
			"after": the_supp_count_after + the_food_count_after,
			
			"returned": len (proceeds)
		}
	}
'''

def obtain_stats (
	documents_list
):
	last_index = len (documents_list) - 1
	
	try:
		before = documents_list [ 0 ] ["stats"] ["before"]
	except Exception:
		before = "?"
	
	try:
		after = documents_list [ last_index ] ["stats"] ["after"]
	except Exception:
		after = "?"
	
	return {
		"amounts": {
			"before": before,
			"after": after
		}
	}
		
	
	

		
	