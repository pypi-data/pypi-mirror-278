

/*
	import { kind } from '@/grid/struct_2/product/kind'
*/

import { is_kind } from '@/grid/struct_2/product/is'

export const kind = (treasure) => {
	if (is_kind ("food", treasure)) {
		return 'food'
	}
	else if (is_kind ("supplement", treasure)) {
		return 'supplement'
	}
	
	return ''
}