
/*
	import { sort_as_floats } from '@%/glamour/table/sorting/as_float.js'
*/

export function sort_as_floats ({ rows, place, direction }) {
	return rows.sort (function (r1, r2) {
		// console.log ('sort', r1, r2)
		
		function the_variable (original_variable) {
			try {
				const the_float = parseFloat (original_variable [place])
				
				if (typeof the_float === 'number' && isNaN (the_float) === false) {
					return the_float;
				} 
			}
			catch (exception) {}
			
			return ''
		}
		
		r1 = the_variable (r1)
		r2 = the_variable (r2)
		
		if (direction === 'backward') {
			if (r1 === '') {
				return -1
			}
			if (r2 === '') {
				return -1;
			}			
			
			if (r1 > r2) {
				return 1;
			}
			if (r1 < r2) {
				return -1;
			}
			
			return 0
		}
		
	
		if (r1 === '') {
			return 1
		}
		if (r2 === '') {
			return -1;
		}			
		if (r1 > r2) {
			return -1;
		}
		else if (r1 < r2) {
			return 1;
		}
		
		return 0		
	})
} 