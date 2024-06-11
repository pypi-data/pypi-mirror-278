
/*
	import { append_field } from '@/apps/fields/append'
	await append_field ({
		field_title: "physics",
		field: import ('@/parcels/physics/field.vue')
	})
*/

/*
	plan:
		// title is set within the parcel
	
		import { append_field } from '@/apps/fields/append'
		await append_field ({
			field: import ('@/parcels/physics/field.vue')
		})
*/

import { mapState } from 'pinia'

import select_scenery from '@/scenery/select/decor.vue'
import s_button from '@/scenery/button/decor.vue'

import { theme_warehouse } from '@/warehouses/theme'
import { browser_storage_store } from '@/warehouses/storage'	

export const field = {
	components: {
		select_scenery,
		s_button
	},
	methods: {
		async change_palette ({ value }) {			
			await theme_warehouse.moves ["change palette"] ({ palette_name: value })
		},
		
		async allow_browser_storage () {
			await browser_storage_store.moves.allow ()
		},
		
		async disallow_browser_storage () {
			await browser_storage_store.moves.disallow ()
		}
	},
	
	data () {
		const theme = theme_warehouse.warehouse ()
		
		return {
			browser_storage: browser_storage_store.warehouse (),
			
			palette_name: theme.palette_name,
			options: Object.keys (theme.palettes),
			
		}
	},

	beforeMount () {},

	created () {
		this.browser_storage_store_monitor = browser_storage_store.monitor (({ inaugural, field }) => {
			this.browser_storage = browser_storage_store.warehouse ()
		})
		
		this.theme_warehouse_monitor = theme_warehouse.monitor (({ inaugural, field }) => {
			const theme = theme_warehouse.warehouse ()

			this.palette_name = theme.palette_name;
			this.options = Object.keys (theme.palettes)

			//console.log ('monitor function', { inaugural, field, warehouse })
		})
	},
	
	beforeUnmount () {
		this.theme_warehouse_monitor.stop ()
		this.browser_storage_store_monitor.stop ()
	},
	
	mounted () {}
}