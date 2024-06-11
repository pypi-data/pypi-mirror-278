
import { find_brand_name } from '@/grid/nature/product/find_brand_name'
import { find_product_name } from '@/grid/nature/product/find_product_name'

import { furnish_string } from '@/grid/furnish/string'
import { furnish_array } from '@/grid/furnish/array'

export const decor = {
	props: [ 'product' ],
	methods: {
		furnish_array,
		furnish_string,
		find_product_name,
		find_brand_name
	}
}