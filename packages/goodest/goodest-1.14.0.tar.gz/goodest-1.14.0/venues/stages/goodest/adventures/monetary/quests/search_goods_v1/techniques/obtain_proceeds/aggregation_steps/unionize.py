
'''

'''
def occur (
	include_food = None,
	include_supp = None
):
	if (include_food and include_supp):
		mods = [{ 
		   "$set": { 
			   "food_emblem": "$emblem" 
			} 
		},
		{ 
		   "$unionWith": { 
			   "coll": "supp",
			   "pipeline": [{ 
				   "$set": { 
					   "supp_emblem": "$emblem" 
					} 
				}] 
			}
		}]
	elif (include_food and not include_supp):
		mods = [{ 
		   "$set": { 
			   "food_emblem": "$emblem" 
			} 
		}]
	elif (include_supp and not include_food):
		mods = [{ 
		   "$set": { 
			   "supp_emblem": "$emblem" 
			} 
		}]
	else:
		mods = []
		
	return mods;