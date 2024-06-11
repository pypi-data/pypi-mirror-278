
/*
	new one is "find_product_name"
*/

/*
	import { find_name } from '@/grid/struct_2/product/find_name'
	find_name (product)
*/
export function find_name (product) {
	try {
		if (typeof product ["struct_2"] ["product"] ["name"] === 'string') {
			return product ["struct_2"] ["product"] ["name"]
		}
	}
	catch (exception) {
		console.warn (exception)
	}
	
	return ''
}