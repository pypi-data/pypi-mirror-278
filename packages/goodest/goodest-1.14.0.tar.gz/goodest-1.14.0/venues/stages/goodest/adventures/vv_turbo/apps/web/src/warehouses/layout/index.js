






/*
	import { create_layout_system } from '@/warehouses/layout'	
	const layout_system = await create_layout_system ()
*/

/*
	this.layout_warehouse_monitor = layout_warehouse.monitor (({ inaugural, field }) => {
		const layout = layout_warehouse.warehouse ()

		console.log ('monitor function', { inaugural, field, warehouse })
	})

	this.layout_warehouse_monitor.stop ()
*/

/*
	layout_warehouse.moves.empty ()
*/

/*
 * 	agenda:
 * 		https://vuejs.org/guide/components/provide-inject.html
 * 
 * 
 */

import _get from 'lodash/get'

import { make_store } from 'mercantile'
import { has_field } from '@/grid/object/has_field'

export const create_layout_system = async function () {
	return await make_store ({
		warehouse: async function () {
			return {
				
			}
		},
		moves: {
			/*
				await layout_warehouse.moves.empty ()
			*/
			async empty ({ change }) {},
		},
		once_at: {
			async start () {}
		}			
	})
}