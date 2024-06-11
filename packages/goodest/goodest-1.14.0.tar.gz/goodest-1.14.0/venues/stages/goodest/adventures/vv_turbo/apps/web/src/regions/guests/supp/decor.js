

import { methods } from './methods'

import comments from './decor/comments.vue'
import kind from './decor/kind.vue'
import warnings from './decor/warnings.vue'
import zone from './decor/zone.vue'

import brands from './decor/brands/decor.vue'
import product_summary from './decor/product/decor.vue'

import statements from './decor/statements/decor.vue'
import references from './decor/references/decor.vue'
import films from './decor/films/decor.vue'

import measured_ingredients_table from './decor/measured_ingredients/fountains.vue'
import unmeasured_ingredients from './decor/unmeasured_ingredients/fountain.vue'
import affiliates from '@/scenery/treasure/affiliates/decor.vue'



import composition from '@/scenery/struct_2/composition/decor.vue'
import quantity_chooser from '@/scenery/quantity_chooser/decor.vue'
import essential_nutrients from '@/scenery/nature_essentials_nutrients/shack.vue'
import change_indicator from '@/scenery/change_indicator/scenery.vue'
import cautionary_ingredients from '@/scenery/nature_cautionary_ingredients/shack.vue'
	

export const decor = {
	components: {
		affiliates,
		
		cautionary_ingredients,
		
		change_indicator,
		
		essential_nutrients,
		
		quantity_chooser,
		
		unmeasured_ingredients,
		measured_ingredients_table,
		composition,
		references,
		statements,
		
		brands,
		product_summary,
		
		comments,
		kind,
		warnings,
		zone,
		
		films
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
			
			treasurure: {},
			nature: {},
			
			show: false,
			found: false
		}
	},
	
	async created () {
		await this.find ()
	}
}