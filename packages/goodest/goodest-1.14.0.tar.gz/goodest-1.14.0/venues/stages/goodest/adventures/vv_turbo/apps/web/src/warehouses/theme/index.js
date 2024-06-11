

/*
	The same theme system needs to be for the fields and the app,
	therefore fields should use the singleton in the sequence for now....
*/

/*
	import { create_theme_warehouse } from '@/warehouses/theme'	
*/

/*
	import { theme_warehouse } from '@/warehouses/theme'		

	this.theme_warehouse_monitor = theme_warehouse.monitor (({ inaugural, field }) => {
		const theme = this.theme_warehouse.warehouse ()
		this.palette = theme.palette;

		console.log ('monitor function', { inaugural, field, warehouse })
	})

	this.theme_warehouse_monitor.stop ()
*/

/*
	theme_warehouse.moves.empty ()
*/

/*
 * 	agenda:
 * 		https://vuejs.org/guide/components/provide-inject.html
 * 
 * 		inject: [ 'theme_warehouse' ]
 */

import _get from 'lodash/get'
import { make_store } from 'mercantile'
import { has_field } from '@/grid/object/has_field'
import { browser_storage_store } from '@/warehouses/storage'	



export let theme_warehouse;

export const create_theme_warehouse = async function ({ palettes }) {
	theme_warehouse = await make_store ({
		film: 0,
		warehouse: async function () {
			let palette_name = "Moonflower"
			
			try {
				const local_storage_palette_name = localStorage [ "palette_name" ];
				if (Object.keys (palettes).includes (local_storage_palette_name)) {
					palette_name = local_storage_palette_name
				}
			}
			catch (exception) {
				console.error (exception)
			}
						
			const palette = palettes [ palette_name ];
			console.info ("utilizing paletted:", palette_name)
			
			return {
				palette,
				palette_name,
				palettes
			}
		},
		moves: {
			/*
				await theme_warehouse.moves.empty ()
			*/
			async empty ({ change }) {},
			
			
			/*
				await theme_warehouse.moves ["change palette"] ({ palette_name: "" })
			*/
			async "change palette" (
				{ change, warehouse },
				{ palette_name }
			) {
				let theme = await warehouse ()
				
				await change ("palette", theme.palettes [ palette_name ])	
				await change ("palette_name", palette_name)
				
				await theme_warehouse.moves.save_palette ()
			},
			
			
			/*
			 await theme_warehouse.moves.save_palette () 
			*/
			async save_palette () {
				if (browser_storage_store.warehouse ().allowed === 'yes') {
					localStorage.setItem ("palette", JSON.stringify (theme_warehouse.warehouse ().palette));
					localStorage.setItem ("palette_name", theme_warehouse.warehouse ().palette_name);
				}
			}
		},
		once_at: {
			async start () {}
		}			
	})
	
	const monitor = theme_warehouse.monitor (({ inaugural, field }) => {
		const warehouse = theme_warehouse.warehouse ()

		console.log ('monitor function', { inaugural, field, warehouse })
	})
	
	return theme_warehouse;
}