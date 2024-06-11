



import { round_quantity } from '@/grid/round_quantity'
import quantified_grove_table from '@/scenery/struct_2/quantified_grove/table.vue'
import { furnish_string } from '@/grid/furnish/string'

import mass_of_quantified_ingredients from './furniture/mass_of_quantified_ingredients.vue'

export const decor = {
	components: {
		mass_of_quantified_ingredients,
		quantified_grove_table
	},
	
	props: [ 
		"product" 
	],
	
	data () {
		return {
			division: "per package",
			package_mass_as_listed: "unlisted"
		}
	},
	
	watch: {
		product () {
			this.calc_package_mass_as_listed ()
		}
	},
	mounted () {
		this.calc_package_mass_as_listed ()
	},
	
	methods: {
		calc_package_mass_as_listed () {
			const product = this.product;
			
			try {
				this.package_mass_as_listed = product.struct_2.mass ['per package, in grams']				
			}
			catch (exception) {
				
			}
			
			this.package_mass_as_listed = "unlisted"
		},
		quantified_grove ({ product }) {
			try {			
				console.log ('quantified grove')	
				console.log ('quantified grove:', product)
				
				return product.struct_2.ingredients ['quantified grove']
			}
			catch (exception) {
				console.error ("caught exception:", exception.message)
			}
			
			return ''
		},
		
		furnish_string,
		mass_in_grams () {}
	}
}