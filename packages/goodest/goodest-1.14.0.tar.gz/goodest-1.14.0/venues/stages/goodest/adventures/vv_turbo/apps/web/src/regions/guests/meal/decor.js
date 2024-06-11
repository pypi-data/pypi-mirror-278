


import { retrieve_EN_recipe } from '@/fleet/goodest_DB/essential_nutrients/recipe'


import cautionary_ingredients from '@/scenery/nature_cautionary_ingredients/shack.vue'
import change_indicator from '@/scenery/change_indicator/scenery.vue'
import essential_nutrients from '@/scenery/nature_essentials_nutrients/shack.vue'
import router_link_scenery from '@/scenery/router_link/decor.vue'	
import s_button from '@/scenery/button/decor.vue'
import s_food_or_supp_summary from '@/scenery/food_or_supp_summary/decor.vue'

import { cart_system } from '@/warehouses/cart'	

import { append_field } from '@/apps/fields/append'
	
import { retrieve_meal } from '@/fleet/goodest_DB/meals/retrieve'
		
	
	
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
			ingredients: [],
			recipe: {},
			
			/*
				EN
				list
			*/
			show: false
		}
	},
	
	methods: {
		_get,
		async retrieve_meal_ask () {
			var { emblem } = this.$route.params;	
			const { 
				status,
				parsed,
				proceeds
			} = await retrieve_meal ({ emblem })
			if (status !== 200) {
				console.error ("The meal was not found.");
				
				this.found = false;
				this.show = true;
				return;
			}
					
			console.log ({ proceeds })
				
			this.recipe = proceeds.freight.nature;
			this.ingredients = proceeds.freight.nature.ingredients;
			
			this.found = true;
			this.show = true;
		}
	},
	
	async mounted () {		
		await this.retrieve_meal_ask ()
		
		this.show = true;
	},
	
	beforeUnmount () {
		
	}
}