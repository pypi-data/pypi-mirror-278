




/*
	import { make_browser_storage_store } from '@/warehouses/storage'	
*/

/*	
	import { browser_storage_store } from '@/warehouses/storage'	

	inject: [ 'browser_storage_store' ],
	created () {
		const browser_storage_store = this.browser_storage_store;
		this.browser_storage_store_monitor = browser_storage_store.monitor (({ inaugural, field }) => {
			const browser_storage = browser_storage_store.warehouse ()


		})
	},
	beforeUnmount () {
		this.browser_storage_store_monitor.stop ()
	}
*/

/*
	if (browser_storage_store.warehouse ().allowed === 'yes') {
		localStorage.setItem ("goal", JSON.stringify (goal));
		localStorage.setItem ("goal_picked", true);
	}
*/

/*
	data () {
		return {
			browser_storage_allowed: this.browser_storage_store.warehouse ().allowed
		}
	}
*/

/*
	browser_storage_store.moves.empty ()
*/

/*
 * 	itinerary:
 * 		https://vuejs.org/guide/components/provide-inject.html
 * 
 */

import { goals_store } from '@/warehouses/goals'
import { theme_warehouse } from '@/warehouses/theme'	

import _get from 'lodash/get'
import { make_store } from 'mercantile'

export let browser_storage_store;

export const make_browser_storage_store = async function () {
	browser_storage_store = await make_store ({
		film: 0,
		warehouse: async function () {
			let local_storage_allowed = localStorage [ "local_storage_allowed" ];
			if (local_storage_allowed !== 'yes') {
				local_storage_allowed = 'no'
			}
			
			let local_storage_decided = localStorage [ "local_storage_decided" ];
			if (local_storage_decided !== 'yes') {
				local_storage_decided = 'no'
			}
			
			
			return {
				decided: local_storage_decided,
				allowed: local_storage_allowed
			}
		},
		moves: {	
			/*
				await browser_storage_store.moves.allow ()
			*/
			async allow (
				{ change, warehouse }
			) {
				await change ("allowed", 'yes')	
				await change ("decided", 'yes')	

				localStorage.setItem ('local_storage_allowed', 'yes');
				localStorage.setItem ('local_storage_decided', 'yes');
				
				await goals_store.moves.save_goal ()
				await theme_warehouse.moves.save_palette ()
			},

			/*
				await browser_storage_store.moves.disallow ()
			*/
			async disallow (
				{ change, warehouse }
			) {
				await change ("allowed", 'no')	
				await change ("decided", 'yes')
				
				await browser_storage_store.moves.clear ()
			},
			
			/*
				await browser_storage_store.moves.clear ()
			*/
			async clear () {
				localStorage.clear ();
				
			}
		},
		once_at: {
			async start () {
				
			}
		}			
	})
	
	return browser_storage_store;
}