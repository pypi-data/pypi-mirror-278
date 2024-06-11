

/*
	// this always returns a string

	import { furnish_array } from '@/grid/furnish/array'
	furnish_array ({ 's': '1' }, [ 's' ], '')
	
	furnish_array ('')
*/


import _get from 'lodash/get'

export function furnish_array () {
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
		
		if (Array.isArray (candidate) === true) {
			return candidate;
		}
		
		console.log (arguments);
		throw new Error (`An array could not be furnished from the preceeding arguments.`)		
	}
	catch (exception) {
		console.log ("exception:", exception)
	}
	
	return []
}