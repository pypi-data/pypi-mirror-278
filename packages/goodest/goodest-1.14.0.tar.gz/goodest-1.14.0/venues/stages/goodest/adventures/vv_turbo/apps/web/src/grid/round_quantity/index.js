
/*
	import { round_quantity } from '@/grid/round_quantity'
	round_quantity (91.555) // '91.56'
*/

import round from 'lodash/round'

export const round_quantity = function (quantity) {	
	try {
		if (quantity === '') {
			return ''
		}
		
		var rounded_quantity = round (quantity, 2)
		if (isNaN (rounded_quantity)) {
			return ""
		}
		rounded_quantity = rounded_quantity.toString ()

		if (rounded_quantity == "0") {
			return '0.00'
		}
		
		if (rounded_quantity.indexOf (".") == -1) {
			return rounded_quantity + '.00'
		}
		
		var split = rounded_quantity.split ('.')
		
		if (split [1].length == 1) {
			return rounded_quantity + "0"
		}
		
		return rounded_quantity;
	}
	catch (exception) {
		console.error (exception)
	}
	
	return ''
}