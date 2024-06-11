




'''
	python3 status.proc.py shows_v2/treasure/nature/land/grove/_ops/is_story_1/status_1.py
'''

from goodest.shows_v2.treasure.nature.land.grove._ops.nurture import nurture_grove
import goodest.shows_v2.treasure.nature.land.grove._ops.is_story_1 as is_story_1
	
def check_1 ():
	grove = nurture_grove ("essential_nutrients")
	
	story_1_list = is_story_1.generate_list (grove)
	
	assert (is_story_1.check (story_1_list, "carbohydrates") == True)
	assert (is_story_1.check (story_1_list, "protein") == True)

	assert (is_story_1.check (story_1_list, "sugars, added") == False)
	assert (is_story_1.check (story_1_list, "polyunsaturated fat") == False)
	assert (is_story_1.check (story_1_list, "dietary fiber") == False)

checks = {
	'check 1': check_1
}