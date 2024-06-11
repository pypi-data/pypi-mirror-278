
import { furnish_string } from 'procedures/furnish/string'
import { furnish_array } from '@/grid/furnish/array'

export const decor = {
	props: [ "treasure" ],
	
	computed: {
		energy () {
			return furnish_string (
				this.treasure, 
				[ 'measures', 'energy', 'per package', 'food calories', 'decimal string' ],
				'not found'
			)
		},
		mass () {
			const mass = furnish_string (
				this.treasure, 
				[ 'measures', 'mass', 'per package', 'grams', 'decimal string' ],
				''
			)
			
			if (mass.length >= 1) {
				return mass + ' grams'
			}
			
			return 'not found'
		},
		volume () {
			const liters = furnish_string (
				this.treasure, 
				[ 'measures', 'volume', 'per package', 'liters', 'decimal string' ],
				''
			)
			if (liters.length >= 1) {
				return liters + ' liters'
			}
			
			return 'not found'
		}
	},
	
	methods: {
		furnish_string,
		furnish_array
	}
}