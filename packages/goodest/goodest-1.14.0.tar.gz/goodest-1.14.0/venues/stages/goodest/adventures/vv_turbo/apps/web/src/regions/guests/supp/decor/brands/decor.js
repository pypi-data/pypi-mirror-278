

import { find_brand_name } from '@/grid/nature/brand/name'
import { find_nature_name } from '@/grid/nature/identity/name'

import { furnish_string } from '@/grid/furnish/string'
import { furnish_array } from '@/grid/furnish/array'

import { variables } from '@/regions/guests/supp/variables'

export const decor = {
	props: [ 'nature', 'sources' ],

	data () {
		return {
			variables	
		}
	},
	
	methods: {
		
		find_brand_name,
		find_nature_name,
		
		furnish_string,
		furnish_array
	}
}