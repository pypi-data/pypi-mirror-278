



/*
	retrieve the mass of effectual mass of an ingredient
	as a float.
*/



/*
	import { retrieve_mass } from '@/grid/struct_2/ingredient/mass'
*/

import { furnish_string } from '@/grid/furnish/string'
import { has_field } from '@/grid/object/has_field'
import { round_quantity } from '@/grid/round_quantity'

export function retrieve_mass ({ ingredient }) {
	// console.log ('retrieve mass', { ingredient })	
	// console.log ('determine mass', ingredient.mass)

	try {
		if (has_field (ingredient, 'mass')) {	
			// console.log ('has mass')
			
			if (has_field (ingredient.mass ['per package'], 'float string grams')) {	
				const mass = ingredient.mass ['per package'] ['float string grams']	
				if (typeof mass === 'string') {
					return [ 
						round_quantity (mass.toString ()),
						"g"
					]
				}
				
			}
			else if (has_field (ingredient.mass ['per package'], 'float grams')) {
				const mass = ingredient.mass ['per package'] ['float grams']	
				if (typeof mass === 'number') {
					return [ 
						round_quantity (mass.toString ()),
						"g"
					]
				}					
			}				
		}
		else if (has_field (ingredient, 'effectual mass')) {
			console.log ('effectual', ingredient ['effectual mass']['per package'])
			
			const { amount, unit } = ingredient ['effectual mass'] ['per package'] ['float']	
			return [ 
				round_quantity (amount.toString ()),
				unit
			]
		}
			
	}
	catch (exception) {
		console.error (exception)
	}
	
	return ''
}