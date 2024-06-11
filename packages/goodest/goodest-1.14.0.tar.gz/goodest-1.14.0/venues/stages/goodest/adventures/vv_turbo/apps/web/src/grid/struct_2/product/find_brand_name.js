

/*

	import { find_brand_name } from '@/grid/struct_2/product/find_brand_name'
	find_brand_name (product)
*/
export function find_brand_name (product) {
	try {
		if (typeof product ["struct_2"]["brand"]["name"] === 'string') {
			return product ["struct_2"]["brand"]["name"]
		}
	}
	catch (exception) {
		console.warn (exception)
	}
	
	return ''
}