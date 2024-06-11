


/*
	import { mass_plus_mass_eq } from '@/grid/nature/essential_nutrients/grove/ingredient/mass_plus_mass_eq'
	mass_plus_mass_eq ({ ingredient })
*/

import { fraction_to_float } from '@/grid/Fraction/to_float'

export function mass_plus_mass_eq ({ ingredient }) {
	try {
		return fraction_to_float (
			ingredient ["measures"] ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"],
			false
		)
	}
	catch (ex) {}
	
	return ''
}

