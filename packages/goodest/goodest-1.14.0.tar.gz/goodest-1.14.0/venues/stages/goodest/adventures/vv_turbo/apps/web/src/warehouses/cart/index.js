
/*
	maybe this should be interfacing
	exclusively with localStorage.
	
		(or possibly a data node)
*/

/*
	server address
*/

/*
	import { create_cart_system } from '@/warehouses/cart'	
*/

/*
	import { cart_system } from '@/warehouses/cart'	
	
	
	const monitor = cart_system.monitor (({ inaugural, field }) => {
		const warehouse = system.warehouse ()

		console.log ('monitor function', { inaugural, field, warehouse })
	})
*/

/*
	cart_system.moves.empty ()

*/

import { make_store } from 'mercantile'

import { has_field } from '@/grid/object/has_field'
import { browser_storage_store } from '@/warehouses/storage'	

import { retrieve_treasures } from './utilities/retrieve_treasures'

import { remove } from './moves/remove'
import { find_DSLD_ID } from './moves/find_DSLD_ID'
import { find_FDC_ID } from './moves/find_FDC_ID'
import { change_quantity } from './moves/change_quantity'

import _get from 'lodash/get'

export let cart_system;

export const create_cart_system = async function () {
	cart_system = await make_store ({
		warehouse: async function () {
			const { treasures, IDs } = await retrieve_treasures ()
		
			return {
				/*
					[{
						"emblem": 
						DSLD_ID:
					},{
						"emblem": 
						FDC_ID:
					}]
				*/
				IDs,
				treasures
			}
		},
		moves: {
			/*
				await cart_system.moves.empty ()
			*/
			async empty ({ change }) {
				await change ("IDs", [])		
				await change ("treasures", [])
			},
			
			change_quantity,
			find_DSLD_ID,
			find_FDC_ID,
			remove,
			
			sub () {}
		},
		once_at: {
			async start () {}
		}			
	})
	
	const monitor = cart_system.monitor (({ inaugural, field }) => {
		const warehouse = cart_system.warehouse ()

		if (browser_storage_store.warehouse ().allowed === 'yes') {
			if (field === "IDs") {
				localStorage.setItem ('IDs', JSON.stringify (warehouse.IDs))
			}
			if (field === "treasures") {
				localStorage.setItem ('treasures', JSON.stringify (warehouse.treasures))
			}
		}

		console.log ('monitor function', { inaugural, field, warehouse })
	})
}