


import { RouterLink } 	from 'vue-router'

import { append_field } from '@/apps/fields/append'
import { open_physics } from '@/parcels/physics/open.js'

	
import mobile_top_nav from './navs/mobile_top/field.vue'
import top_nav from './navs/top/field.vue'


export const decor = {
	props: [ "open_menu" ],
	components: {		
		mobile_top_nav,
		top_nav,
		RouterLink
	},
	methods: {
		async open_options () {			
			await open_physics ()
		}
	},
	
	data () {
		return {	
			focused: false
		}
	}
}