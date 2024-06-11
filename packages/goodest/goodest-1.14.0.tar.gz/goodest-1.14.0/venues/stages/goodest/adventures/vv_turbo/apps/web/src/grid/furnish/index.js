

/*
	// this always returns a string

	import { furnish } from '@/grid/furnish'
	
	//
	//	furnish 'number' returns 0 if cannot determine....
	//
	furnish ('number') ({ 's': '1' }, [ 's' ], '')
		
	
*/


import _get from 'lodash/get'



export function furnish (to_furnish) {
	return function () {
		try {
			
			let candidate = undefined;
			if (arguments.length === 3) {
				candidate = _get (
					arguments [0], 
					arguments [1], 
					arguments [2]
				)
			}
			else if (arguments.length === 2) {
				candidate = _get (
					arguments [0], 
					arguments [1], 
					''
				)
			}
			else if (arguments.length === 1) {
				candidate = arguments [0]
			}
			
			if (typeof candidate === to_furnish) {
				return candidate;
			}
			
			console.log (arguments);
			throw new Error (`A ${ to_furnish } could not be furnished from the preceeding arguments.`)		
		}
		catch (exception) {
			console.warn (exception)
		}
		
		if (to_furnish === 'number') {
			return 0
		}
		
		return ''
	}
}