

/*	
	import nature_ingredients_table from '@/scenery/nature_ingredients_table/fountains.vue'
	
	<nature_ingredients_table
		:grove="grove"
	/>
*/


import cloneDeep from 'lodash/cloneDeep'

import { build_grove } 			from '@/grid/nature/essential_nutrients/grove/sort/cryo/grove-1'
import { sort_grove } 			from '@/grid/nature/essential_nutrients/grove/sort'
import { calc_linear_grove } 	from '@/grid/nature/essential_nutrients/grove/calc_linear_grove'

import { mass_plus_mass_eq } from '@/grid/nature/essential_nutrients/grove/ingredient/mass_plus_mass_eq'


import { round_quantity } 		from '@/grid/round_quantity'
import { fraction_to_float } 	from '@/grid/Fraction/to_float'
import { has_field } from '@/grid/object/has_field'

import g_table from '@%/glamour/table/decor.vue'


	
export const fountains = {
	components: { g_table },
	
	props: {
		include_goals: {
			type: Boolean,
			default: false
		},
		
		grove: {
			type: Array,
			default () {
				return []
			}
		},
		
		// EN, CI
		table_kind: {
			type: String,
			default: ""
		},
		
		is_recipe: {
			type: Boolean,
			default: false
		}
	},
	
	computed: {

		
		percent_label () {
			if (this.table_kind === "EN") {
				return "percent of essential nutrient composition"
			}
			else if (this.table_kind == "CI") {
				return "percent of cautionary ingredients composition"
			}
			else {
				return "?"
			}
		},
		
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
				return ingredient ["info"] ["names"] [0];
			}
			catch (ex) {
				console.warn (
					'name not found:', 
					ex
				)				
			}
			
			return ''
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
		
		goal (ingredient) {
			
			try {				
				return ingredient ["goals"] ["days of ingredient"] ["mass + mass equivalents"] ["per recipe"] ["decimal string"]
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
			const per = "per recipe"

			
			try {						
				const measures = ingredient ["measures"]
				// console.log (measures)
				
				if (
					has_field (measures, "mass + mass equivalents") === false &&
					has_field (measures, "biological activity") === true
				) {
					// {'biological activity': {'per recipe': {'IU': {'fraction string': '0'}}}}
					// console.log ("bio activity?")
					
					const per_recipe = measures ["biological activity"]['per recipe']
					if (has_field (per_recipe, "IU")) {
						const amount = fraction_to_float (
							per_recipe ["IU"] ["fraction string"],
							false
						)
						
						return [ `${ amount } IU` ]					
					}
				}
		
				if (has_field (measures, "mass + mass equivalents")) {
					return [
						fraction_to_float (
							ingredient ["measures"] ["mass + mass equivalents"] [ per ] ["grams"] ["fraction string"],
							false
						),
						""
					]
					
					return [
						fraction_to_float (
							ingredient ["measures"] ["mass + mass equivalents"] [ per ] ["grams"] ["fraction string"]
						),
						"grams",
						""
					]
				}
			}
			catch (ex) {
				console.warn ('mass + mass equivalents not found:', ex)
				try {
					console.log (ingredient ["info"] ["names"])
				}
				catch (ex) {}
			}
			
			return ''
		}
	}
}