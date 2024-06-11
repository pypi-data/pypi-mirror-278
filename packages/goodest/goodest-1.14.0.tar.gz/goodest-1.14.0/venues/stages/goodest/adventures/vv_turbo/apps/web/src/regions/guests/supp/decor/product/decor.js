



import { find_nature_name } from '@/grid/nature/identity/name'

import { furnish_string } from '@/grid/furnish/string'
import { furnish_array } from '@/grid/furnish/array'

import { variables } from '@/regions/guests/supp/variables'
import goodness_certifications from '@/scenery/treasure/goodness_certifications/money.vue'
	
/*

measures	Object { form: {…} }
form	Object { unit: "Coated Tablet", "amount per package": "90", "serving size amount": "1" }
unit	"Coated Tablet"
amount per package	"90"
serving size amount	"1"
*/

export const decor = {
	components: { goodness_certifications },
	
	props: [ 
		'nature', 
		'sources', 
		'goodness', 
		'references' 
	],

	data () {
		return {
			variables
		}		
	},
	
	computed: {
		form () {
			return furnish_string (
				this.nature, 
				[ "measures", "form", "unit"], 
				"not found"
			);
		},
		amount_per_package () {
			return furnish_string (
				this.nature, 
				[ "measures", "form", "amount per package"], 
				"not found"
			);
		}
	},
	
	methods: {
		find_amount_per_package () {
			
		},
		
		find_nature_name,
		
		furnish_string,
		furnish_array
	}
}