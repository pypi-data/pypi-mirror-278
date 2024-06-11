
/*
	import { is_kind } from '@/grid/struct_2/product/is'
	is_kind ("supplement", product)
*/

import { furnish_string } from '@/grid/furnish/string'

export function is_kind (kind, product) {
	if (kind === "supplement") {
		return furnish_string (
			product, 
			[ 'struct_2', 'product', 'DSLD ID' ], 
			''
		).length >= 1
	}
	
	if (kind === "food") {
		return furnish_string (
			product, 
			[ 'struct_2', 'product', 'FDC ID' ], 
			''
		).length >= 1
	}
	
	throw new Error (`Kind ${ kind } was not accounted for.`)
}