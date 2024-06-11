



import { RouterLink, RouterView } from 'vue-router'

import { create_layout_system, layout_system } from '@/apps/Earth/warehouses/layout'
	
import s_alerts from '@/scenery/alerts/decor.vue'
import nav_1 from '@/scenery/nav_1/decor.vue'
import nav_2 from '@/scenery/nav_2/decor.vue'
import accessibility_enhancer from '@/scenery/accessibility enhancer/structure.vue'

import { append_field } from '@/apps/fields/append'

// import { terrain_DB } from '@/warehouses/terrain'

import s_select from '@/scenery/select/decor.vue'

import local_storage_flip from './components/local_storage_flip/decor.vue'


	
export const field = {
	components: {
		local_storage_flip,
	
		s_select,
	
		s_alerts,
		accessibility_enhancer,
		RouterView,
		nav_1,
		nav_2
	},
	
	inject: [ 'homestead_system' ],
	
	methods: {
		toggle_menu () {			
			const current = layout_system.warehouse ().current 
			if (current [0] == 0 && current [1] == 0) {
				layout_system.moves.change_current ({ 
					location: [ -1, 0 ] 
				})
			}
			else {
				layout_system.moves.change_current ({ 
					location: [ 0, 0 ] 
				})
			}
			
			this.menu_showing = !this.menu_showing;
		},
		close_menu () {
			this.menu_showing = false;
			
			layout_system.moves.change_current ({ 
				location: [ 0, 0 ] 
			})
		},
		
		async OPEN_OPTIONS () {
			await append_field ({
				field_title: "options",
				field: import ('@/parcels/physics/field.vue')
			})
		}
	},
		
	data () {
		return {
			terrain: this.homestead_system.warehouse (),
			
			main_margin: 8,
			
			current_x: 0,
			translate: `translateX(0%)`,
			
			GT_1000: true,
			menu_showing: true
		}
	},
	async created () {	
		await Promise.all ([
			create_layout_system ()
		])
		this.layout_system_monitor = layout_system.monitor (({ inaugural, field }) => {
			const warehouse = layout_system.warehouse ()
			this.current_x = layout_system.warehouse ().current [0]

			const percent = (this.current_x * 100 * -1).toString ()
			this.translate = `translateX(${ percent }%)`
			
			console.log ('layout monitor function', warehouse.current)
		})
	
		this.homestead_system_monitor = this.homestead_system.monitor (({ inaugural, field }) => {
			const homestead = this.homestead_system.warehouse ()
		})

		
		/*
		this.terrain_DB_unsubscribe = terrain_DB.SUBSCRIBE (({ FIRST }) => {
			this.terrain = terrain_DB.STORAGE ("SIZE")
		})
		*/
	},
	beforeUnmount () {
		// this.terrain_DB_unsubscribe ()
		
		this.homestead_system_monitor.stop ()
		
		this.layout_system_monitor.stop ()
	},
	mounted () {
		
	}
	
}