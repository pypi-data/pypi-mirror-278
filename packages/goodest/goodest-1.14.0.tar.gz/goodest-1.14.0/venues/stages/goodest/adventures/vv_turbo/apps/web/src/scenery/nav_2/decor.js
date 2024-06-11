





import { append_field } from '@/apps/fields/append'

import router_link_scenery from '@/scenery/router_link/decor.vue'

import { layout_system } from '@/apps/Earth/warehouses/layout'

import mascot from '@/scenery/mascot/craft.vue'
import { open_business } from '@/parcels/business/open.js'
import { open_physics } from '@/parcels/physics/open.js'

export const decor = {
	prop: [ 'close_menu' ],
	components: {
		router_link_scenery,
		mascot
	},
	methods: {
		open_business,
		open_physics,
		
		link_clicked () {
			layout_system.moves.change_current ({ 
				location: [ 0, 0 ] 
			})
		}
	}
}

