
'''
	import legumes.goals.human.FDA as human_FDA_goal
	goal = human_FDA_goal.retrieve ()
'''

'''
	multikey index:
		https://www.mongodb.com/docs/manual/core/indexes/index-types/index-multikey/
'''
def retrieve ():
	return {
	  "label": "FDA goals for the average adult humans",
	  "cautions": [
		"These guidelines have not been checked by any high status nutritionists.",
		"Please consult with your actual physician or nutritionist also."
	  ],
	  "ingredients": [
		{
		  "labels": [
			"Biotin"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/100000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Calcium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "13/10"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"calories"
		  ],
		  "goal": {
			"energy": {
			  "per recipe": {
				"food calories": {
				  "fraction string": "2000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Choline"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "11/20"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Cholesterol"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/10"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Chromium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "7/200000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Copper"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "9/10000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Dietary Fiber"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "28"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Fats"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "78"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Folate",
			"Folic Acid"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "1/2500"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Iodine"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/20000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Iron"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "9/500"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Magnesium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "21/50"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Manganese"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "23/10000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Molybdenum"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "9/200000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Niacin"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "2/125"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Pantothenic Acid"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "1/200"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Phosphorus"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "5/4"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Potassium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "47/10"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Protein"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "50"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Riboflavin"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "13/10000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Saturated Fat"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "20"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Selenium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "11/200000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Sodium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "23/10"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Thiamin"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/2500"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"carbohydrates"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "275"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin A"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "9/10000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin B6"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "17/10000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin B12"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/1250000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin C"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "9/100"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin D"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "1/50000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin E"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/200"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin K"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/25000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Zinc"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "11/1000"
				}
			  }
			}
		  }
		}
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
			  "20",
			  "eternity"
			]
		  ]
		},
		{
		  "label": "exclusions",
		  "includes": [
			"pregnant",
			"breast feeding"
		  ]
		}
	  ],
	  "sources": [
		"https://www.fda.gov/food/new-nutrition-facts-label/daily-value-new-nutrition-and-supplement-facts-labels",
		"https://www.fda.gov/food/nutrition-facts-label/calories-nutrition-facts-label",
		"https://www.fda.gov/media/99069/download",
		"https://www.fda.gov/media/99059/download"
	  ]
	}