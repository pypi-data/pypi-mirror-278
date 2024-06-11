



/*
	
*/

import { goals_store } from '@/warehouses/goals'

import goal_furniture from '@/scenery/goal/decor.vue'

export const features = {
	components: {
		goal_furniture
	},
	
	data () {
		return {
			goal: {}
		}
	},
	created () {
		this.goals_store_monitor = goals_store.monitor (({ 
			inaugural, 
			field 
		}) => {
			this.goal = goals_store.warehouse ().goal;
			this.goal_picked = goals_store.warehouse ().goal_picked;
		})
	},
	beforeUnmount () {
		this.goals_store_monitor.stop ()
	}
}