


/*
	import { name_0 } from '@/grid/nature/essential_nutrients/grove/ingredient/name_0'
	name_0 ({ ingredient })
*/

import { fraction_to_float } from '@/grid/Fraction/to_float'

export function name_0 ({ ingredient }) {
	try {
		return ingredient ["info"] ["names"] [0]
	}
	catch (ex) {}
	
	return ''
}

