

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

//
//
//
import { mass_plus_mass_eq } from '@/grid/nature/essential_nutrients/grove/ingredient/mass_plus_mass_eq'
import { name_0 } from '@/grid/nature/essential_nutrients/grove/ingredient/name_0'
import { biological_activity } from '@/grid/nature/essential_nutrients/grove/ingredient/biological_activity'


import { round_quantity } 		from '@/grid/round_quantity'
import { fraction_to_float } 	from '@/grid/Fraction/to_float'
import { has_field } from '@/grid/object/has_field'

import g_table from '@%/glamour/table/decor.vue'

import { methods } from './fields/methods'
import { markRaw, reactive, h, defineAsyncComponent } from 'vue';

	
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
	
	beforeCreate () {},
	
	data () {
		return {
			columns: [],
			rows: []
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
		
		parsedGrove () {
			if (Array.isArray (this.grove)) {
				return this.grove
			}	
			
			return []
		}
		
		/* linear_grove () {
			if (!Array.isArray (this.grove)) {
				return []
			}

			const grove = cloneDeep (this.grove);			
			sort_grove ({ grove })
			
			return calc_linear_grove ({ 
				grove
			})
		} */
	},
	
	methods,
	
	mounted () {		
		this.columns = this.prepare_columns ()
		this.rows = this.prepare_rows ({
			grove: this.parsedGrove
		})
		
		this.$refs.the_table.column_clicked (
			this.columns [1]
		)
	}
}