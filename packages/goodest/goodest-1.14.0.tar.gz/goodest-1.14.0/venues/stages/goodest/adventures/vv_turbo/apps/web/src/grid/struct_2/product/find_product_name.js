
/*
	import { find_product_name } from '@/grid/struct_2/product/find_product_name'
	find_product_name (product)
*/
export function find_product_name (product) {
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