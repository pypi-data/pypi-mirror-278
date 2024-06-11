

/*
	import { fraction_to_float } from '@/grid/Fraction/to_float'
	
	// return a float
	fraction_to_float (Fraction, false)
	
	// return a float string
	fraction_to_float (Fraction)
*/

import { round_quantity } from '@/grid/round_quantity'

export const fraction_to_float = (fraction_string, return_string = true) => {
	if (fraction_string.indexOf ("/") == -1) {
		if (return_string) {
			return round_quantity (fraction_string)
		}
		
		return parseFloat (fraction_string)
	}
	
	var the_split = fraction_string.split ("/")
	if (return_string) {	
		return round_quantity (
			parseFloat (
				the_split [0] /
				the_split [1]
			)
		)
	}
	
	return parseFloat (
		the_split [0] /
		the_split [1]
	)
}