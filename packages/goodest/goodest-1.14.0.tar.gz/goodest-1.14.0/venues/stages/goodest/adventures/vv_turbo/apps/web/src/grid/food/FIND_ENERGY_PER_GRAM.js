
/*
"PACKAGE": {
	"MASS": {
		"REPORTED": "4 oz/113 g",
		"SYSTEM INTERNATIONAL": [
			"113",
			"g"
		]
	} 
}

// "MASS": {
//	"SYSTEM INTERNATIONAL": [ 113, "g" ]
// }
"ENERGY": {
    "FOOD CALORIES": {
        "PER PACKAGE": [
            "685.91",
            "FOOD CALORIES"
        ],
        "PER SERVING": [
            "169.96",
            "FOOD CALORIES"
        ]
    }
} 
*/


import { round_quantity } 	from '@/grid/round_quantity'
import _get 		from 'lodash/get'


export function FIND_ENERGY_PER_GRAM (FOOD) {
	try {		
		const ENERGY_PER_PACKAGE 	= _get (FOOD, [ 'ENERGY', 'FOOD CALORIES', 'PER PACKAGE' ], '?')
		const MASS_PER_PACKAGE 		= _get (FOOD, [ 'PACAKGE', 'MASS', 'SYSTEM INTERNATION' ], '?') 
		
		const ENERGY_PER_GRAM = round_quantity (
			ENERGY_PER_PACKAGE [0],
			
		)
		
		
		let ENERGY_PER_G = round_quantity (FOOD['ENERGY'][0] / _get (FOOD, ['PACKAGE MASS', 'G'], '?')) 
		return ENERGY_PER_G + " " + FOOD['ENERGY'][1] + " PER G"
	}
	catch (exception) {
		console.warn ("exception IN @/grid/food/FIND_ENERGY_PER_GRAM")
	}
	
	return "? CALORIES PER GRAM"
}