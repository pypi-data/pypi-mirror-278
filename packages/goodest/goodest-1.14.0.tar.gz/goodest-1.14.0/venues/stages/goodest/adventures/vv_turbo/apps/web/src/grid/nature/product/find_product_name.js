
/*
	import { find_product_name } from '@/grid/nature/product/find_product_name'
	find_product_name (nature)
*/
export function find_product_name (nature) {
	try {
		if (typeof nature ["identity"] ["name"] === 'string') {
			return nature ["identity"] ["name"]
		}
	}
	catch (exception) {
		console.warn (exception)
	}
	
	return ''
}