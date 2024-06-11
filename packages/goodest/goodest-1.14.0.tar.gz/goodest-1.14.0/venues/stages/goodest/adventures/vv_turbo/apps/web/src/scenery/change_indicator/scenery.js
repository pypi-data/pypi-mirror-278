

import spinner from './indicators/spinner/indicator.vue'
import action from '@/vendor/scenery/action/scenery.vue'


export const scenery = {
	props: {
		show: {
			type: Boolean,
			default: true
		}
	},
	
	data () {
		return {}
	},
	
	watch: {
		show (show) {
			if (show === false) {}
		} 
	},
	
	components: {
		action,
		spinner
	}
}

