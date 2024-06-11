

import { append_field } from '@/apps/fields/append'

import round from 'lodash/round'
import cloneDeep from 'lodash/cloneDeep'

import { methods } from './fields/methods'

import ingredient_mass from './decor/mass.vue'
// import JOURNAL_BUTTON from '@/decor/JOURNAL_BUTTON/field.vue'	
	
export const table = {
	components: {
		ingredient_mass
	},
	
	props: {
		ingredients: Array,
	},

	
	watch: {
		ingredients () {
			console.log ('ingredients changed')
			
			
		}
	},

	
	data () {
		return {
			linear_ingredients: []
		}
	},

	
	mounted () {
		this.determine_linear_ingredients ()
	},
	
	methods
	
	
}