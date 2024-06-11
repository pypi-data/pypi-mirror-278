

/*


*/

//
// This is necessary for highlighting, in style awareness
//
import { theme_warehouse } from '@/warehouses/theme'	
	
import browser_storage_alert from '@/scenery/browser_storage/component.vue'

import { methods } from './methods'

export const structure = {
	components: {
		browser_storage_alert
	},
	methods,

	beforeCreate () {},
	
	data () {
		const theme = theme_warehouse.warehouse ();
		const palette = theme.palette;
		
		return {
			palette,
			opacity: 0
		}
	},	
	created () {
		this.theme_warehouse_monitor = theme_warehouse.monitor (({ inaugural, field }) => {
			const theme = theme_warehouse.warehouse ()
			this.palette = theme.palette;
		})
	},
	beforeUnmount () {
		window.removeEventListener ("keydown", this.keydown);
		this.theme_warehouse_monitor.stop ()
	},
	
	mounted () {
		setTimeout (() => { this.opacity = 1; }, 0)
		window.addEventListener ("keydown", this.keydown);
	}
}