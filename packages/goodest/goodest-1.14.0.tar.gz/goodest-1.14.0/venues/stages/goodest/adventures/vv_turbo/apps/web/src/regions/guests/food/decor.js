
//

import { methods } from './methods'
	
//	
	
import comments from './decor/comments.vue'
import kind from './decor/kind.vue'
import warnings from './decor/warnings.vue'
import zone from './decor/zone.vue'
import affiliates from '@/scenery/treasure/affiliates/decor.vue'


import product_summary from './decor/product/decor.vue'
import brands from './decor/brands/decor.vue'
import references from './decor/references/decor.vue'
import unmeasured_ingredients from './decor/ingredients_unmeasured/decor.vue'

import composition from './decor/composition/decor.vue'


//import composition from './decor/composition/field.vue'
import quantity from './decor/quantity/decor.vue'

// import composition from '@/scenery/struct_2/composition/decor.vue'
import quantity_chooser from '@/scenery/quantity_chooser/decor.vue'
import essential_nutrients from '@/scenery/nature_essentials_nutrients/shack.vue'
import change_indicator from '@/scenery/change_indicator/scenery.vue'

import cautionary_ingredients from '@/scenery/nature_cautionary_ingredients/shack.vue'
	

import _get from 'lodash/get'

export const decor = {
	components: {
		affiliates,
		
		unmeasured_ingredients,
		
		cautionary_ingredients,
		
		change_indicator,
		
		essential_nutrients,
		composition,
		quantity_chooser,
		
		references,
		
		brands,
		product_summary,
		
		comments,
		kind,
		warnings,
		zone
	},
		
	methods,
	
	watch: {
		decor_terrain: {
			deep: true,
			handler () {
				this.change_terrain ()
			}
		}
	},
	
	data () {
		return {
			gt_1000: true,
			decor_terrain: '',
			product: {},
			
			show: false,
			found: false
		}
	},
	
	async created () {
		await this.find ()
	},
	
	mounted () {
		console.log ('mounted:', this.variable)
	}
}