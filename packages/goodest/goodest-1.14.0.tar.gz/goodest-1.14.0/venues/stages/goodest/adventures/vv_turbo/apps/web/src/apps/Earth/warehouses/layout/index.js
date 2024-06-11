
/*
	import { create_layout_system } from '@/apps/Earth/warehouses/layout'

	await Promise.all ([
		create_layout_system ()
	])
*/

/*
	import { layout_system } from '@/apps/Earth/warehouses/layout'
	const layout_system_monitor = layout_system.monitor (({ inaugural, field }) => {
		const warehouse = layout_system.warehouse ()

		console.log ('monitor function', { inaugural, field, warehouse })
	})
	layout_system_monitor.stop ()
*/

/*
	import { layout_system } from '@/apps/Earth/warehouses/layout'
	layout_system.moves.change_current ({ 
		location: [ -1, 0 ] 
	})
*/

import { make_store } from 'mercantile'

export let layout_system;
export const create_layout_system = async function () {
	layout_system = await make_store ({
		warehouse: async function () {				
			return {
				/*
					[ -1,  1 ] [ 0, 1  ] [ 1, 1  ]
					[ -1,  0 ] [ 0, 0  ] [ 1, 0  ]
					[ -1, -1 ] [ 0, -1 ] [ 1, -1 ]	
				*/
				current: [ 0, 0 ]
			}
		},
		
		moves: {
			async change_current (
				{ change, warehouse }, 
				{ location }
			) {
				// let current = (await warehouse ()).current
				await change ("current", location)
				
				return "good";
			}
		},
		
		once_at: {
			async start () {}
		}			
	})
}