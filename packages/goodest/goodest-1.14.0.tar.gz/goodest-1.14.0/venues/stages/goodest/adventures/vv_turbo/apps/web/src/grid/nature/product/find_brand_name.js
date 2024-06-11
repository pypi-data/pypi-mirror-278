

/*

	import { find_brand_name } from '@/grid/nature/product/find_brand_name'
	find_brand_name (nature)
*/
export function find_brand_name (nature) {
	try {
		if (typeof nature ["brand"] ["name"] === 'string') {
			return nature ["brand"] ["name"]
		}
	}
	catch (exception) {
		console.warn (exception)
	}
	
	return ''
}