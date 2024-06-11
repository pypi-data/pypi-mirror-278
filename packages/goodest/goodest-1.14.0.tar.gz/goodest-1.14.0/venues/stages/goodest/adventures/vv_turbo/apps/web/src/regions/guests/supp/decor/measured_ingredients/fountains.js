

/*	
	import measured_ingredients_table from './fountains.vue'
	
	<measured_ingredients_table
		:grove="measured_ingredients"
	/>
*/


import cloneDeep from 'lodash/cloneDeep'

import { build_grove } from '@/grid/nature/essential_nutrients/grove/sort/cryo/grove-1'
import { sort_grove } from '@/grid/nature/essential_nutrients/grove/sort'
import { calc_linear_grove } from '@/grid/nature/essential_nutrients/grove/calc_linear_grove'
import { mass_plus_mass_eq } from '@/grid/nature/essential_nutrients/grove/ingredient/mass_plus_mass_eq'
import { round_quantity } from '@/grid/round_quantity'
import { fraction_to_float } from '@/grid/Fraction/to_float'

import s_select from '@/scenery/select/decor.vue'


export const fountains = {
	props: [ "grove" ],
	
	components: { s_select },
	
	computed: {
		linear_grove () {
			if (!Array.isArray (this.grove)) {
				return []
			}

			const grove = cloneDeep (this.grove);			
			sort_grove ({ grove })
			
			return calc_linear_grove ({ 
				grove
			})
		}
	},
	
	methods: {
		name_1 (ingredient) {
			try {
				return ingredient ["name"];
			}
			catch (ex) {
				console.warn (
					'name not found:', 
					ex
				)				
			}
			
			return ''
		},
		
		listed_amount (ingredient) {
			try {				
				const listed_measure = ingredient ["listed measure"]
				
				return `${ 
					listed_measure ["operator"] 
				} ${ 
					listed_measure ["amount"] ["decimal string"] 
				} ${
					listed_measure ["unit"]
				}`
			}
			catch (ex) {
				/*
				console.warn (
					'mass + mass eq not found:', 
					ingredient ["essential"]["names"]
				)
				*/				
			}
			
			return ``
		},
		
		portion (ingredient) {
			try {				
				return [
					100 * fraction_to_float (
						ingredient ["measures"] ["mass + mass equivalents"] ["portion of grove"] ["fraction string"],
						false
					),
					"%"
				]
			}
			catch (ex) {
				/*
				console.warn (
					'mass + mass eq not found:', 
					ingredient ["essential"]["names"]
				)
				*/				
			}
			
			return ''
		},
		
		mass_plus_mass_eq (ingredient) {
			try {				
				return [
					fraction_to_float (
						ingredient ["measures"] ["mass + mass equivalents"] ["per package"] ["grams"] ["fraction string"],
						false
					),
					""
				]
			}
			catch (ex) {
				/*
				console.warn (
					'mass + mass eq not found:', 
					ingredient ["essential"]["names"]
				)
				*/				
			}
			
			return ''
		}
	}
}