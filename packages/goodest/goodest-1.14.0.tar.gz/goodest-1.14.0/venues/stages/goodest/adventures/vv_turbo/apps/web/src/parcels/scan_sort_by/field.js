


	
import { inject } from 'vue'


export const field = {
	data () {
		return {}
	},
	created () {	
		const coodinate = inject ('the_coordinate')
		console.log ("field coordiante:", coodinate)
	
		const system = inject ('system');
		console.log ({ system })
	},
	beforeUnmount () {}	
}