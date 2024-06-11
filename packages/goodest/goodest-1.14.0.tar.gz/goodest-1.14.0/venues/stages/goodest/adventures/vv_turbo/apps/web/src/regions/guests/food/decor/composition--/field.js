

import quantified_grove_table from '@/scenery/struct_2/quantified_grove/table.vue'
import { furnish_string } from '@/grid/furnish/string'

export const field = {
	components: {
		quantified_grove_table
	},
	
	props: [ 
		"product" 
	],
	
	data () {
		return {
			division: "per package"
		}
	},
	
	methods: {
		calculate_mass_2 (product) {
			try {
				console.log ({ product })
				
				var mass = product.struct_2.mass ["of quantified ingredients, with effectuals"][
					"float grams"
				]
				
				return mass
			}
			catch (exception) {
				console.error (exception)
			}
			
			return ''
		},
		
		quantified_grove ({ product }) {
			try {			
				console.log ('quantified grove')	
				console.log ('quantified grove:', product)
				
				return product.struct_2.ingredients ['quantified grove']
			}
			catch (exception) {
				console.error (exception)
			}
			
			return ''
		},
		
		furnish_string,
		mass_in_grams () {}
	}
}