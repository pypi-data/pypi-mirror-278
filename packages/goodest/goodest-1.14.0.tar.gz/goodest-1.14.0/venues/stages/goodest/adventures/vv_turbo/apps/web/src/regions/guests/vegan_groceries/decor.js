
/*
	https://y-takey.github.io/chartjs-plugin-stacked100/
	https://github.com/nagix/chartjs-plugin-style
	https://nagix.github.io/chartjs-plugin-rough/
	https://github.com/chartjs/chartjs-plugin-annotation
	https://chartjs-plugin-crosshair.netlify.app/samples/
*/

import { methods } from './cycles/methods.js'

// import supplement from './decor/supplement/decor.vue'
// import food from './decor/food/decor.vue'
import search_controls from './decor/search_controls/decor.vue'

import s_button from '@/scenery/button/decor.vue'
import s_food_or_supp_summary from '@/scenery/food_or_supp_summary/decor.vue'
import change_indicator from '@/scenery/change_indicator/scenery.vue'

	
export default {
	components: { 
	
		change_indicator,
		
		s_food_or_supp_summary,
		s_button,
		
		search_controls,
		// supplement,
		// food			
	},

	methods,
	
	data () {
		return {		
			searching: true,
	
			search_string: '',
			previous_search_string: '',

			
			next: false,
			prev: false,
			
			counts: {
				returned: "_",
				unlimited: "_"
			},
			
			amount_after: 0,
			amount_before: 0,
			
			
			message: '',

			treasures: [],
			
			count: "0"
		}
	},

	mounted () {
		this.search ()
	}
}
