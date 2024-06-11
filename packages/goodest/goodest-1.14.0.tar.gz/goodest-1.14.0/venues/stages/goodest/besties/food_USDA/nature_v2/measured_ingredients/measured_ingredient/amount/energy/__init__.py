


import goodest.measures._interpret.unit_kind as unit_kind
import goodest.measures.mass.swap as mass_swap
import goodest.measures.number.decimal.reduce as reduce_decimal
import goodest.measures.energy.swap as energy_swap


from biotech.topics.show.variable import show_variable


from fractions import Fraction

def calc_energy (
	amount_per_package__from_portion,
	unit_name,		
			
	USDA_food_nutrient,
	mass_and_volume,
	
	records = 1
):
	energy__from_portion = amount_per_package__from_portion
	
	'''
	difference = abs (
		biological_activity__from_portion -
		label_nutrient_amount
	)
	assert (difference <= 1)
	'''
	if (records >= 1):
		show_variable ({
			"energy__from_portion:": energy__from_portion
		})
	
	food_calories_per_package__from_portion = Fraction (energy_swap.start ([ 
		energy__from_portion, 
		unit_name 
	], "food calories"))
	
	'''
	joules_package__from_portion = Fraction (energy_swap.start ([ 
		energy__from_portion, 
		unit_name 
	], "joules"))
	
	"joules": {
		"decimal string": reduce_decimal.start (
			joules_package__from_portion, 
			partial_size = 3
		),
		"fraction string": str (joules_package__from_portion)
	} 
	'''
	
	return {
		"energy": {
			"per package": {
				"listed": [ 
					reduce_decimal.start (
						energy__from_portion, 
						partial_size = 3
					), 
					unit_name 
				],
				"food calories": {
					"decimal string": reduce_decimal.start (
						food_calories_per_package__from_portion, 
						partial_size = 3
					),
					"fraction string": str (food_calories_per_package__from_portion)
				}				
			}
		}
	}