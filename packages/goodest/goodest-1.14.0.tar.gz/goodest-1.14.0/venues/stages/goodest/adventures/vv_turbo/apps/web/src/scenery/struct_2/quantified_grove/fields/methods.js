
import { append_field } from '@/apps/fields/append'
import { round_quantity } from '@/grid/round_quantity'

import { mapState } from 'pinia'
import round from 'lodash/round'
import cloneDeep from 'lodash/cloneDeep'

import { furnish_string } from '@/grid/furnish/string'
import { has_field } from '@/grid/object/has_field'

import { sort_quantified_grove } from '@/grid/struct_2/product/quantified_grove/sort'
	
import { retrieve_mass } from '@/grid/struct_2/ingredient/mass'
export const methods = {		
	round_quantity,
	
	struct_name ({ ingredient }) {
		try {
			return ingredient.name
		}
		catch (exception) {
			console.error (exception)
		}
		
		return ''
	},
	
	/*
	async OPEN_UNREPORTED_field () {
		const { the_coordinate } = await append_field ({
			field: import ('@/parcels/UNREPORTED/field.vue')
		})
	},
	*/
	
	calculate_percentage (ingredient) {
		/*
			"mass": {
				"effectual portion per package": {
					"from quantified ingredients": {
					  "fraction float string": "0.22525726995189502",
					  "fraction string": "24634689961716612000/109362463493309192069",
					  "percentage string": "22.526%"
					}
				  },
			  }
		*/
		try {
			return ingredient ['mass'][
				'effectual portion per package'
			]["from quantified ingredients"]["percentage string"];
		}
		catch (exception) {
			console.info ("The percentage of this ingredient could not be calculated.", ingredient)
		}
		
		return ''
	},
	
	
	determine_mass_in_grams: retrieve_mass,
	
	determine_linear_ingredients () { 
		console.log ('determine_linear_ingredients')
			
		const linear_ingredients = []
		
		
		const quantified_grove = cloneDeep (this.ingredients)
		sort_quantified_grove ({ quantified_grove })
		
		function loop ({ quantified_grove, indent }) {
			for (let s = 0; s <= quantified_grove.length - 1; s++) {
				const ingredient = quantified_grove [s]
				ingredient.indent = indent
				
				linear_ingredients.push (ingredient)
				
				const nested_qg = ingredient ["quantified grove"];
				
				if (
					Array.isArray (nested_qg) &&
					nested_qg.length >= 1
				) {
					loop ({ quantified_grove: nested_qg, indent: (indent + 1) })
				}
			}
		}
		
		loop ({ quantified_grove, indent: 0 })
		
		this.linear_ingredients = linear_ingredients;
	}
}