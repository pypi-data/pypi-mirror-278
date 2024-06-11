

/*


*/

import { inject, provide } from 'vue'

// import { terrain_DB } from '@/warehouses/terrain'
import { remove_field } from '@/apps/fields/remove'
import boundary from '@/apps/fields/boundary/embellishments.vue'

import { methods } from './methods'

import { theme_warehouse } from '@/warehouses/theme'
import accessibility_enhancer from '@/scenery/accessibility enhancer/structure.vue'


export default {
	components: { boundary, accessibility_enhancer },
	inject: [ 
		'homestead_system',
		
		'field_title'
	],	
	methods,

	data () {
		const homestead = this.homestead_system.warehouse ()
		const theme = theme_warehouse.warehouse ()
		
		return {
			palette: theme.palette,
			
			coordinate: "",
			hacienda_title: "",
			field_element: "",
			
			terrain: homestead.terrain,
			
			outer_attributes: this.find_outer_attributes ()
		}
	},	
	
	created () {
		this.theme_warehouse_monitor = theme_warehouse.monitor (({ inaugural, field }) => {
			const theme = theme_warehouse.warehouse ()
			this.palette = theme.palette;
		})	
		
		this.homestead_system_monitor = this.homestead_system.monitor (({ inaugural, field }) => {
			const homestead = this.homestead_system.warehouse ()
			this.terrain = homestead.terrain;
			
			console.log ('homestead_system_monitor', { field })
			
			try {
				this.change_outer_attributes ()			
			}
			catch (exception) {}
		})
	},
	
	beforeUnmount () {
		this.homestead_system_monitor.stop ()
		this.theme_warehouse_monitor.stop ()
		
		this.$refs.hacienda_platform.removeEventListener ("keydown", this.keypress);
	},
	
	mounted () {
		this.coordinate = inject ('the_coordinate')
		this.hacienda_title = inject ('field_title')
		this.field_element = inject ('field_element')
		
		/*
			this.terrain_DB_unsubscribe = terrain_DB.SUBSCRIBE (({ FIRST }) => {
				this.terrain 			= terrain_DB.STORAGE ("SIZE")
							
				try {
					this.change_outer_attributes ()			
				}
				catch (exception) {}
			})
		*/
		
		// window.addEventListener ("keypress", this.keypress);
		this.$refs.hacienda_platform.addEventListener ("keydown", this.keypress);
		this.$refs.hacienda_platform.focus ()
	}
}