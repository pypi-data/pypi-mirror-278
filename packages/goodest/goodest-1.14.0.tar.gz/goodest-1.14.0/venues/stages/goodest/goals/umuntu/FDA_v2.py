
'''
	import legumes.goals.human.FDA as human_FDA_goal
	goal = human_FDA_goal.retrieve ()
'''

'''
	https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx
'''

'''
	https://www.fda.gov/food/nutrition-facts-label/daily-value-nutrition-and-supplement-facts-labels
'''

#
#	 of 4 or more years
#

'''
{
	"labels": [ "Added sugars" ],
	"goal": {
		"mass + mass equivalents": {
			"per day": {
				"grams": {
					"fraction string": "50/1"
				}
			}
		}
	}
},
'''

'''
	equivalents:
		{
			"labels": [ "Folate", "Folic Acid" ],
			"goal": [ "400", "mcg", "DFE" ],
		}
		
		{
			"labels": [ "Niacin" ],
			"goal": [ "16", "mg", "NE" ],
		}
		
		{
			"labels": [ "Vitamin A" ],
			"goal": [ "900", "mcg", "RAE" ],
		}
		
		{
			"labels": [ "Vitamin E" ],
			"goal": [ "15", "mg", "alpha-tocopherol" ],
		}
'''

def retrieve ():
	return {
		"label": "FDA goals for average adult humans",
		"cautions": [
			"These guidelines have not been checked by any high status nutritionists.",
			"Please consult with your actual physician or nutritionist also."
		],
		"ingredients": [
			
			{
				"labels": [ "Biotin" ],
				"goal": [ "30", "mcg" ],
			},
			{
				"labels": [ "Calcium" ],
				"goal": [ "1300", "mg" ],
			},
			{
				"labels": [ "calories" ],
				"goal": [ "2000", "kcal" ],
			},
			{
				"labels": [ "Choline" ],
				"goal": [ "550", "mg" ],
			},
			{
				"labels": [ "Cholesterol" ],
				"goal": [ "300", "mg" ],
			},
			{
				"labels": [ "Chromium" ],
				"goal": [ "35", "mcg" ],
			},
			{
				"labels": [ "Copper" ],
				"goal": [ "0.9", "mg" ],
			},
			{
				"labels": [ "Dietary Fiber" ],
				"goal": [ "28", "g" ],
			},
			{
				"labels": [ "Fat" ],
				"goal": [ "78", "g" ],
			},
			{
				"labels": [ "Folate", "Folic Acid" ],
				"goal": [ "400", "mcg", "DFE" ],
			},
			{
				"labels": [ "Iodine" ],
				"goal": [ "150", "mcg" ],
			},
			{
				"labels": [ "Iron" ],
				"goal": [ "18", "mg" ],
			},
			{
				"labels": [ "Magnesium" ],
				"goal": [ "420", "mg" ],
			},
			{
				"labels": [ "Manganese" ],
				"goal": [ "2.3", "mg" ],
			},
			{
				"labels": [ "Molybdenum" ],
				"goal": [ "45", "mcg" ],
			},
			{
				"labels": [ "Niacin" ],
				"goal": [ "16", "mg", "NE" ],
			},
			{
				"labels": [ "Pantothenic Acid" ],
				"goal": [ "5", "mg" ],
			},
			{
				"labels": [ "Phosphorus" ],
				"goal": [ "1250", "mg" ],
			},
			{
				"labels": [ "Potassium" ],
				"goal": [ "4700", "mg" ],
			},
			{
				"labels": [ "Protein" ],
				"goal": [ "50", "g" ],
			},
			{
				"labels": [ "Riboflavin" ],
				"goal": [ "1.3", "mg" ],
			},
			{
				"labels": [ "Saturated Fat" ],
				"goal": [ "20", "g" ],
			},
			{
				"labels": [ "Selenium" ],
				"goal": [ "55", "mcg" ],
			},
			{
				"labels": [ "Sodium" ],
				"goal": [ "2300", "mg" ],
			},
			{
				"labels": [ "Thiamin" ],
				"goal": [ "1.2", "mg" ],
			},
			{
				"labels": [ "Total carbohydrate" ],
				"goal": [ "275", "g" ],
			},
			{
				"labels": [ "Vitamin A" ],
				"goal": [ "900", "mcg", "RAE" ],
			},
			{
				"labels": [ "Vitamin B6" ],
				"goal": [ "1.7", "mg" ],
			},
			{
				"labels": [ "Vitamin B12" ],
				"goal": [ "2.4", "mcg" ],
			},
			{
				"labels": [ "Vitamin C" ],
				"goal": [ "90", "mcg" ],
			},
			{
				"labels": [ "Vitamin D" ],
				"goal": [ "20", "mcg" ],
			},
			{
				"labels": [ "Vitamin E" ],
				"goal": [ "15", "mg", "alpha-tocopherol" ],
			},
			{
				"labels": [ "Vitamin K" ],
				"goal": [ "120", "mcg" ],
			},
			{
				"labels": [ "Zinc" ],
				"goal": [ "11", "mg" ],
			},
		],
		"limiters": [
			{
				"label": "species",
				"includes": [
					"human"
				]               
			},
			{
				"kind": "slider--integer",
				"label": "age",
				"includes": [
					[
						"4",
						"eternity"
					]
				],
			},
			{
				"label": "exclusions",
				"includes": [
					"pregnant",
					"breast feeding"
				],
			}
		],
		"sources": [
			"https://www.fda.gov/food/new-nutrition-facts-label/daily-value-new-nutrition-and-supplement-facts-labels",
			"https://www.fda.gov/food/nutrition-facts-label/calories-nutrition-facts-label",
			"https://www.fda.gov/media/99069/download",
			"https://www.fda.gov/media/99059/download"
		]
	}
