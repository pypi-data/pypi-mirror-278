

///
//
import { scan_goals } from '@/fleet/nutrition_meadow/goals/scan'
//
import goal_furniture from '@/scenery/goal/decor.vue'
import { open_goal } from '@/parcels/goal/open.js'
//
import s_curtain from '@/scenery/curtain/decor.vue'
//
//\

export const room = {
	inject: [ 'goals_store' ],
	
	components: {
		goal_furniture,
		s_curtain
	},
	
	data () {
		return {
			goals: [],
			goal: {},
			goal_picked: this.goals_store.warehouse ().goal_picked
		}		
	},
	created () {
		this.goals_store_monitor = this.goals_store.monitor (({ 
			inaugural, 
			field 
		}) => {
			this.goals = this.goals_store.warehouse ().goals;
			this.goal = this.goals_store.warehouse ().goal;
			this.goal_picked = this.goals_store.warehouse ().goal_picked;
			
			console.log ('goals_store_monitor', { 
				goals: this.goals, 
				goal: this.goal, 
				goal_picked: this.goal_picked
			})
		})
	},
	beforeUnmount () {
		this.goals_store_monitor.stop ()
	},
	
	methods: {
		async open_goal () {
			await open_goal ()
		},
		
		async erase_goal () {
			await this.goals_store.moves.erase_goal ()
		},
		
		async pick ({ goal }) {
			await this.goals_store.moves.pick_goal ({ goal })
		},
		
		find_label () { 
			try {
				return this.goal.nature.label;
			}
			catch (exception) {
				
			}
			
			return ''
		}
	},
	
	async mounted () {
		await this.goals_store.moves.retrieve_goals ()
	}
	
}












///