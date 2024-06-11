

/*

*/

import s_flip from '@/scenery/flip/decor.vue'

export const decor = {
	components: {
		s_flip
	},
	
	data () {
		return {
			flip: null,
			
			// flip: 'on',
			options: [
				'on',
				'off'
			]
		}
	},
	
	watch: {
		flip () {
			console.log ("flip", this.flip)			
		}
	}
}