


	
import { inject } from 'vue'
import s_select from '@/scenery/select/decor.vue'

	

export const field = {
	components: {
		s_select
	},
	data () {
		return {
			affiliate_link_option: "yes & no",
			affiliate_link_options: [
				"yes & no",
				"yes",
				"no"
			],
			
			grocery_kind_option: "foods & supps",
			grocery_kind_options: [
				"foods & supps",
				"foods",
				"supps"
			]
		}
	},
	methods: {
		affiliate_link_option_changed (option) {
			console.log (option.value)
			this.affiliate_link_option = option.value;
		},
		grocery_kind_option_changed (option) {
			console.log (option.value)
			this.grocery_kind_option = option.value;
		}
	},
	
	created () {	
		const coodinate = inject ('the_coordinate')
		console.log ("field coordiante:", coodinate)
	
		const system = inject ('system');
		console.log ({ system })
	},
	beforeUnmount () {}	
}