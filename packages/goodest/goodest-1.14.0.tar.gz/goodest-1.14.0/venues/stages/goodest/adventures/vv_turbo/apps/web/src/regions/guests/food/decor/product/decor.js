
import { find_brand_name } from '@/grid/nature/product/find_brand_name'
import { find_product_name } from '@/grid/nature/product/find_product_name'

import { furnish_string } from '@/grid/furnish/string'
import { furnish_array } from '@/grid/furnish/array'

import s_outer_link from '@/scenery/link/outer/decor.vue'
import goodness_certifications from '@/scenery/treasure/goodness_certifications/money.vue'
	

export const decor = {
	components: {
		goodness_certifications,
		s_outer_link
	},
	props: [ 'product', 'goodness' ],
	methods: {
		furnish_array,
		furnish_string,
		find_product_name,
		find_brand_name,
	},

	computed: {
		FDC_ID_link () { 
			const code = this.furnish_string (this.product, [ "identity", "FDC ID"]);
			
			if (typeof code === 'string' && code.length >= 3) {
				return `https://fdc.nal.usda.gov/fdc-app.html#/food-details/${ code }/nutrients`
			}
			
			return ''
		},
		FDC_ID_code () {
			return furnish_string (this.product, [ "identity", "FDC ID"])
		}
	}
}