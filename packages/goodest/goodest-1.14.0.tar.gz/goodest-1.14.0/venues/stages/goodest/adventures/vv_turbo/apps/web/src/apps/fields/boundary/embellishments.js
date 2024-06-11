

/*
	import boundary from '@/apps/fields/boundary/embellishments.vue'
*/

/*
	https://vuejs.org/guide/components/slots.html#named-slots
*/

import { inject } from 'vue'
import { mapState } from 'pinia'
import color from 'color'

import s_line from '@/scenery/line/decor.vue'
import s_button from '@/scenery/button/decor.vue'
import s_curtain from '@/scenery/curtain/decor.vue'
	
export const embellishments = {
	props: [ 
		"the_coordinate", 
		"close_the_field" 
	],
	
	components: {
		s_line,
		s_curtain,
		s_button
	},
	methods: {
		color
	},
	data () {
		return {}
	},
	created () {},
	mounted () {
		console.log ("mounted")
		
							
		// '-webkit-backdrop-filter': 'blur(5px)',
		// backdropFilter: 'blur(5px)'
		
		// this.$refs.navCanvas.style.backdropFilter = "blur(5px)"

	},
	beforeUnmount () {}
}