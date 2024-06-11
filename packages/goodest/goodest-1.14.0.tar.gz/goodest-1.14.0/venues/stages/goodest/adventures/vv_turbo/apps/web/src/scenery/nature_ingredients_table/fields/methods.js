
import cloneDeep from 'lodash/cloneDeep'

import { build_grove } 			from '@/grid/nature/essential_nutrients/grove/sort/cryo/grove-1'
import { sort_grove } 			from '@/grid/nature/essential_nutrients/grove/sort'
import { calc_linear_grove } 	from '@/grid/nature/essential_nutrients/grove/calc_linear_grove'


import { mass_plus_mass_eq } from '@/grid/nature/essential_nutrients/grove/ingredient/mass_plus_mass_eq'
import { name_0 } from '@/grid/nature/essential_nutrients/grove/ingredient/name_0'
import { biological_activity } from '@/grid/nature/essential_nutrients/grove/ingredient/biological_activity'


import { round_quantity } 		from '@/grid/round_quantity'
import { fraction_to_float } 	from '@/grid/Fraction/to_float'
import { has_field } 	from '@/grid/object/has_field'

import { prepare_rows } from './methods_/prepare_rows'
import { prepare_columns } from './methods_/prepare_columns'

export const methods = {
	prepare_rows,
	prepare_columns,

	
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
			return ingredient ["measures"] ["mass + mass equivalents"] ["portion of grove"] ["scinote percentage string"]
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
			return ingredient ["goal"] ["days of ingredient"] ["mass + mass equivalents"] ["per recipe"] ["decimal string"]
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
			
			if (
				has_field (measures, "mass + mass equivalents") === false &&
				has_field (measures, "biological activity") === true
			) {
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
					ingredient ["measures"] ["mass + mass equivalents"] [ per ] ["grams"] ["scinote string"]
				]
				
				return [
					fraction_to_float (
						ingredient ["measures"] ["mass + mass equivalents"] [ per ] ["grams"] ["fraction string"],
						false
					),
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