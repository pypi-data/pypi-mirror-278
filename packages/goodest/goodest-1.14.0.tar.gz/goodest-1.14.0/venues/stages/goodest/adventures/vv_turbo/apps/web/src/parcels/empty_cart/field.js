
/*
	import { append_field } from '@/apps/fields/append'
	await append_field ({
		label: "cart",
		field: import ('@/parcels/empty_cart/field.vue')
	})
*/

import s_button from '@/scenery/button/decor.vue'

import { cart_system } from '@/warehouses/cart'	
	

export const field = {
	inject: ['system', 'the_coordinate'],
	
	components: { s_button },
	computed: {},
	data () { return {} },
	
	methods: {
		clicked () {
			console.log ('clicked', this)
			
			cart_system.moves.empty ()
			this.system.moves.close ({
				coord: this.the_coordinate
			})
		}
	},
	mounted () {
		console.log ('empty cart', this.system)
	}
}