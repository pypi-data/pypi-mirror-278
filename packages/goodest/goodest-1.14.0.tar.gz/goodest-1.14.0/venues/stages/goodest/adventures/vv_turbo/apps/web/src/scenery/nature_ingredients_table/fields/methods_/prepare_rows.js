
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

import { markRaw, reactive, h, defineAsyncComponent } from 'vue';

import name_component from './../../components/name.vue'
import percent_component from './../../components/the_percent.vue'
import mass_component from './../../components/mass.vue'

export function prepare_rows ({ grove }) {
	// const grove = this.parsedGrove;
	
	if (!Array.isArray (grove)) {
		return []
	}
	const linear_grove = calc_linear_grove ({ 
		grove: cloneDeep (grove)
	})
	
	const rows = []
	for (let s = 0; s < linear_grove.length; s++) {
		const ingredient = linear_grove [s];
		
		rows.push ({
			'1': {
				'component': markRaw (name_component),
				'props': {
					'name': this.name_1 (ingredient),
					'indent': ingredient.indent
				}
			},
			'2':  {
				'component': markRaw (mass_component),
				'props': {
					'the_string': this.mass_plus_mass_eq (ingredient) [0]
				}
			},
			'3':  {
				'component': markRaw (percent_component),
				'props': {
					'percent': this.portion (ingredient)
				}
			},
			'4': this.goal (ingredient)
		})
	}

	
	return rows;
}