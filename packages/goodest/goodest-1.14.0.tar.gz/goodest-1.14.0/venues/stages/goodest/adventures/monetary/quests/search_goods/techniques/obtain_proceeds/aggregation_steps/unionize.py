
'''

'''
def occur (
	include_food = None,
	include_supp = None,
	include_meals = None
):
	primary = ""

	mods = []
	if (include_food):
		primary = "food"
		mods.append ({
			"$set": { 
			   "food_emblem": "$emblem" 
			} 
		})
	elif (include_supp):
		primary = "supp"
		mods.append ({
			"$set": { 
			   "supp_emblem": "$emblem" 
			} 
		})
	elif (include_meals):
		primary = "meals"
		mods.append ({
			"$set": { 
			   "meals_emblem": "$emblem" 
			} 
		})
		
	if (primary != "supp" and include_supp):
		mods.append ({
			"$unionWith": { 
				"coll": "supp",
				"pipeline": [{ 
					"$set": { 
						"supp_emblem": "$emblem" 
					} 
				}] 
			}
		})
	
	if (primary != "meals" and include_meals):	
		mods.append ({
			"$unionWith": { 
				"coll": "meals",
				"pipeline": [{ 
					"$set": { 
						"meals_emblem": "$emblem" 
					} 
				}] 
			}
		})

		
	return mods;