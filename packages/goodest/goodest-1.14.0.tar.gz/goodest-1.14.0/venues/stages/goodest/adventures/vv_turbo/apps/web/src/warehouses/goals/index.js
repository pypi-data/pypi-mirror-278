



/*
	import { make_goals_store } from '@/warehouses/goals'	
*/

/*
	import { goals_store } from '@/warehouses/goals'
*/

/*	
	inject: [ 'goals_store' ],
	created () {
		this.goals_store_monitor = this.goals_store.monitor (({ inaugural, field }) => {
			const homestead = this.goals_store.warehouse ()
			this.terrain = homestead.terrain;
		})
	},
	beforeUnmount () {
		this.goals_store_monitor.stop ()
	}
*/

/*
	data () {
		return {
			terrain: this.goals_store.warehouse ()
		}
	}
*/

/*
	goals_store.moves.empty ()
*/

/*
 * 	agenda:
 * 		https://vuejs.org/guide/components/provide-inject.html
 * 
 * 
 */

import _get from 'lodash/get'
//
import { make_store } from 'mercantile'
import { rhythm_filter } from '@medical-district/rhythm-filter'
//
import { lap } from '@/fleet/syllabus/lap'

import { browser_storage_store } from '@/warehouses/storage'

function find_goal () {	
	try {
		let goal = JSON.parse (localStorage [ "goal" ]);
		if (Object.keys (goal).length >= 1) {
			return goal;
		}
	}
	catch (exception) {}
	
	return "Please pick a goal"
}

function find_goal_picked () {
	try {
		let goal_picked = localStorage [ "goal_picked" ]
		if (goal_picked === "true") {
			return true;
		}
	}
	catch (exception) {}
	
	return false;
}

export let goals_store;

export const make_goals_store = async function () {
	goals_store = await make_store ({
		film: 0,
		warehouse: async function () {
			const goal = find_goal ()
			const goal_picked = find_goal_picked ()
			
			return {
				goal,
				goal_picked
			}
		},
		moves: {
			/*
				await goals_store.moves.erase_goal ()
			*/
			async erase_goal (
				{ change, warehouse }
			) {
				if (browser_storage_store.warehouse ().allowed === 'yes') {
					localStorage.setItem ("goal", false);
					localStorage.setItem ("goal_picked", false);
				}
				
				await change ("goal", false)
				await change ("goal_picked", false)
			},

			/*
				await goals_store.moves.pick_goal ({ goal })
			*/
			async pick_goal (
				{ change, warehouse },
				{ goal }
			) {				
				await change ("goal", goal)
				await change ("goal_picked", true)
				
				await goals_store.moves.save_goal ()
			},
			
			/*
				await goals_store.moves.save_goal ()
			*/
			async save_goal ({ change, warehouse }) {
				if (browser_storage_store.warehouse ().allowed === 'yes') {
					localStorage.setItem (
						"goal", 
						JSON.stringify (goals_store.warehouse ().goal)
					);
					
					
					localStorage.setItem (
						"goal_picked", 
						goals_store.warehouse ().goal_picked
					);
				}
			},
			
			/*
				
			*/
			async retrieve_goals (
				{ change, warehouse }
			) {
				const { 
					status,
					parsed,
					proceeds
				} = await lap ({
					path: "guests",
					envelope: {
						label: "retrieve goals",
						freight: {}
					}
				});
				if (status !== 200) {
					await change ("goals", [])
					return;
				}
				
				await change ("goals", proceeds.freight)
			}
		},
		once_at: {
			async start () {
				
			}
		}			
	})
	
	return goals_store;
}