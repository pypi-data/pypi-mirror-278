


/*
	import { biological_activity } from '@/grid/nature/essential_nutrients/grove/ingredient/biological_activity'
	biological_activity ({ ingredient })
*/

/*
	{'biological activity': {'per recipe': {'IU': {'fraction string': '0'}}}}
*/

import { fraction_to_float } from '@/grid/Fraction/to_float'

export function biological_activity ({ ingredient }) {
	try {
		return fraction_to_float (
			ingredient ["measures"] ["biological activity"] ["per recipe"] ["IU"] ["fraction string"],
			false
		)
	}
	catch (ex) {}
	
	return ''
}

