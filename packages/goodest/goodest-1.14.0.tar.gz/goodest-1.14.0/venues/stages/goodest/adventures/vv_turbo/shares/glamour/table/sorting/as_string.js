
/*
	import { sort_as_strings } from '@%/glamour/table/sorting/as_string.js'
*/

export function sort_as_strings ({ rows, place, direction }) {
	
	return rows.sort (function (r1, r2) {
		r1 = r1 [ place ]
		r2 = r2 [ place ]
		
		// console.log ({ r1, r2 })
		
		function the_string (variable) {
			if (typeof variable === 'string') {
				return variable
			}
			
			return variable.props.name;
		}
		
		r1 = the_string (r1).toLowerCase ()
		r2 = the_string (r2).toLowerCase ()
		
		if (direction === 'backward') {
			if (r1 > r2) {
				return 1;
			}
			return -1;
		}
		
		if (r1 > r2) {
			return -1;
		}
		return 1;
	})
}