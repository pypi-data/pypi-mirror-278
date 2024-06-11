


import { retrieve_EN_recipe } from '@/fleet/goodest_DB/essential_nutrients/recipe'



import cautionary_ingredients from '@/scenery/nature_cautionary_ingredients/shack.vue'
import change_indicator from '@/scenery/change_indicator/scenery.vue'
import essential_nutrients from '@/scenery/nature_essentials_nutrients/shack.vue'
import router_link_scenery from '@/scenery/router_link/decor.vue'	
import s_button from '@/scenery/button/decor.vue'
import s_food_or_supp_summary from '@/scenery/food_or_supp_summary/decor.vue'

import { cart_system } from '@/warehouses/cart'	

import { append_field } from '@/apps/fields/append'
	
	
	
import _get from 'lodash/get'
	
export const decor = {
	components: {
		cautionary_ingredients,
		
		change_indicator,
		
		s_button,
		
		router_link_scenery,
		
		essential_nutrients,
		s_food_or_supp_summary
	},
	
	data () {
		return {
			recipe: {},
			
			/*
				EN
				list
			*/
			showing: "stats",
			show_recipe: false
		}
	},
	
	methods: {
		_get,
		
		async open_list () {
			console.log ('open_list')
			this.showing = "list"
		},
		
		open_stats () {
			this.showing = "stats"
		},
		
		async open_empty () {
			await append_field ({
				label: "cart",
				field: import ('@/parcels/empty_cart/field.vue')
			})
		},
		async retrieve_recipe () {
			const { 
				status,
				parsed,
				proceeds
			} = await retrieve_EN_recipe ()	
			if (status !== 200) {
				console.error ("The food was not found.");
				
				this.found = false;
				this.show_recipe = true;
				return;
			}
								
			this.recipe = proceeds.freight;
			this.found = true;
			this.show_recipe = true;	
			
		}
	},
	
	async mounted () {		
		this.cart_monitor = cart_system.monitor (({ inaugural, field }) => {
			const warehouse = cart_system.warehouse ()

			console.log ('monitor function', { inaugural, field, warehouse })
			
			this.show_recipe = false;
			
			if (!inaugural) {
				this.retrieve_recipe ()
			}
		})
		
		this.show_recipe = false;
		this.retrieve_recipe ()
	},
	
	beforeUnmount () {
		this.cart_monitor.stop ()
	}
}