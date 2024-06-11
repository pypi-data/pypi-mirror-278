

/*
	import { create_homestead_system } from '@/warehouses/homestead'	
*/

/*
	import { homestead_system } from '@/warehouses/homestead'	
*/

/*	
	inject: [ 'homestead_system' ]
 
	created:
		this.homestead_system_monitor = this.homestead_system.monitor (({ inaugural, field }) => {
			const homestead = this.homestead_system.warehouse ()
			this.terrain = homestead.terrain;
		})

	beforeUnmount:
		this.homestead_system_monitor.stop ()
*/

/*	
	inject: [ 'homestead_system' ]
 
	created () {
		this.homestead_system_monitor = this.homestead_system.monitor (({ inaugural, field }) => {
			const homestead = this.homestead_system.warehouse ()
			this.terrain = homestead.terrain;
			 
			
			 
		})
	},
	beforeUnmount () {
		this.homestead_system_monitor.stop ()
	}
*/

/*
	data () {
		return {
			terrain: this.homestead_system.warehouse ()
		}
	}
*/

/*
	homestead_system.moves.empty ()
*/

/*
 * 	agenda:
 * 		https://vuejs.org/guide/components/provide-inject.html
 * 
 * 
 */

import _get from 'lodash/get'

import { make_store } from 'mercantile'
import { rhythm_filter } from '@medical-district/rhythm-filter'

export let homestead_system;
export const create_homestead_system = async function () {
	homestead_system = await make_store ({
		film: 0,
		warehouse: async function () {
			return {
				terrain: {
					mobile_nav_width: 900,
					width: window.innerWidth,
					height: window.innerHeight,
					layout: {
						lines: "3px"
					}
				}				
			}
		},
		moves: {	
			/*
				await homestead_system.moves.resize ()
				 
				terrain.width < terrain.mobile_nav_width 
			*/
			async resize (
				{ change, warehouse }
			) {
				console.log ({ change, warehouse })
				
				let homestead = await warehouse ()
				await change ("terrain", {
					mobile_nav_width: 900,
					width: window.innerWidth,
					height: window.innerHeight,
					layout: {
						lines: "3px"
					}
				})			
			}	
		},
		once_at: {
			async start () {
				const RF = rhythm_filter ({
					every: 200
				});
				
				function window_size_change (EVENT) {	
					RF.attempt (({ ellipse, is_last }) => {
						homestead_system.moves.resize ()
					});	
				}
				
				window.addEventListener ("resize", window_size_change);	
			}
		}			
	})
	
	return homestead_system;
}