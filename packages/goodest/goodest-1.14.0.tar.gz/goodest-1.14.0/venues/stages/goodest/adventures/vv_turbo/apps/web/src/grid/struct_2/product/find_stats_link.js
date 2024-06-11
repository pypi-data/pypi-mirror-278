
/*
	import { find_stats_link } from '@/grid/struct_2/product/find_stats_link'
	find_stats_link ()
*/
import { furnish_string } from '@/grid/furnish/string'
	
	

export function find_stats_link (product, kind) {
	try {
		return `/@/${ furnish_string (kind) }/` + furnish_string (product ['emblem'])
	}
	catch (exception) {
		console.warn (exception)
	}
	
	return ''
}