
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

def retrieve ():
    return {
		"label": "FDA goals for average adult humans",
		"cautions": [
			"These guidelines have not been checked by any high status nutritionists.",
			"Please consult with your actual physician or nutritionist also."
		],
		
        "ingredients": [
            {
                "goal": [ "2000", "kcal" ],
                "labels": [ "calories" ]
            },
            {
                "goal": [
                    "18",
                    "mg"
                ],
                "labels": [
                    "iron"
                ]
            },
            {
                "goal": [
                    "150",
                    "mcg"
                ],
                "labels": [
                    "iodine"
                ]
            },
            {
                "goal": [
                    "11",
                    "mg"
                ],
                "labels": [
                    "zinc"
                ]
            },
            {
                "goal": [
                    "15",
                    "mg"
                ],
                "labels": [
                    "vitamin e"
                ]
            },
            {
                "goal": [
                    "2.4",
                    "mcg"
                ],
                "labels": [
                    "vitamin b12"
                ]
            },
            {
                "goal": [
                    "1.7",
                    "mg"
                ],
                "labels": [
                    "vitamin b6"
                ]
            },
            {
                "goal": [
                    900,
                    "mcg"
                ],
                "labels": [
                    "vitamin a"
                ]
            },
            {
                "goal": [
                    1.2,
                    "mg"
                ],
                "labels": [
                    "thiamin"
                ]
            },
            {
                "goal": [
                    2300,
                    "mg"
                ],
                "labels": [
                    "sodium"
                ]
            },
            {
                "goal": [
                    55,
                    "mcg"
                ],
                "labels": [
                    "selenium"
                ]
            },
            {
                "goal": [
                    1.3,
                    "mg"
                ],
                "labels": [
                    "riboflavin"
                ]
            },
            {
                "goal": [
                    5,
                    "mg"
                ],
                "labels": [
                    "pantothenic acid"
                ]
            },
            {
                "goal": [
                    16,
                    "mg"
                ],
                "labels": [
                    "niacin"
                ],
                "notes": [
                    "milligrams of niacin equivalents"
                ]
            },
            {
                "goal": [
                    45,
                    "mcg"
                ],
                "labels": [
                    "molybdenum"
                ]
            },
            {
                "goal": [
                    30,
                    "mcg"
                ],
                "labels": [
                    "biotin"
                ]
            },
            {
                "goal": [
                    2300,
                    "mg"
                ],
                "labels": [
                    "chloride"
                ]
            },
            {
                "goal": [
                    0.9,
                    "mg"
                ],
                "labels": [
                    "copper"
                ]
            },
            {
                "goal": [
                    35,
                    "mcg"
                ],
                "labels": [
                    "chromium"
                ]
            },
            {
                "goal": [
                    300,
                    "mg"
                ],
                "labels": [
                    "cholesterol"
                ]
            },
            {
                "goal": [
                    1300,
                    "mg"
                ],
                "labels": [
                    "calcium"
                ]
            },
            {
                "goal": [
                    400,
                    "mcg"
                ],
                "labels": [
                    "folate",
                    "vitamin b9",
                    "folacin",
                    "folic acid"
                ]
            },
            {
                "goal": [
                    420,
                    "mg"
                ],
                "labels": [
                    "magnesium"
                ]
            },
            {
                "goal": [
                    4700,
                    "mg"
                ],
                "labels": [
                    "potassium"
                ]
            },
            {
                "goal": [
                    90,
                    "mg"
                ],
                "labels": [
                    "vitamin c"
                ]
            },
            {
                "goal": [
                    20,
                    "mcg"
                ],
                "labels": [
                    "vitamin d"
                ]
            },
            {
                "goal": [
                    120,
                    "mcg"
                ],
                "labels": [
                    "vitamin k"
                ]
            },
            {
                "goal": [
                    1250,
                    "mg"
                ],
                "labels": [
                    "phosphorous"
                ]
            },
            {
                "goal": [
                    2.3,
                    "mg"
                ],
                "labels": [
                    "manganese"
                ]
            },
            {
                "goal": [
                    50,
                    "g"
                ],
                "labels": [
                    "protein"
                ]
            },
            {
                "goal": [
                    78,
                    "g"
                ],
                "includes": [
                    {
                        "goal": [
                            20,
                            "g"
                        ],
                        "labels": [
                            "saturated fat"
                        ]
                    },
                    {
                        "goal": [],
                        "labels": [
                            "polyunsaturated fat"
                        ]
                    },
                    {
                        "goal": [
                            0,
                            "g"
                        ],
                        "labels": [
                            "trans fat"
                        ]
                    }
                ],
                "labels": [
                    "total fat",
                    "fat"
                ]
            },
            {
                "goal": [
                    275,
                    "g"
                ],
                "includes": [
                    {
                        "goal": [
                            28,
                            "g"
                        ],
                        "labels": [
                            "fiber",
                            "dietary fiber"
                        ]
                    },
                    {
                        "goal": [
                            50,
                            "g"
                        ],
                        "labels": [
                            "sugars",
                            "total sugars"
                        ]
                    }
                ],
                "labels": [
                    "total carbohydrates",
                    "carbohydrates"
                ]
            },
            {
                "goal": [
                    2300,
                    "mg"
                ],
                "labels": [
                    "sodium"
                ]
            }
        ],
        
        "limiters": [
            {
                "includes": [
                    "human"
                ],
                "label": "species"
            },
            {
                "includes": [
                    [
                        "4",
                        "eternity"
                    ]
                ],
                "kind": "slider--integer",
                "label": "age"
            },
            {
                "includes": [
                    "pregnant",
                    "breast feeding"
                ],
                "label": "exclusions"
            }
        ],
		
        "sources": [
            "https://www.fda.gov/food/new-nutrition-facts-label/daily-value-new-nutrition-and-supplement-facts-labels",
            "https://www.fda.gov/media/99069/download",
            "https://www.fda.gov/media/99059/download"
        ]
    }
