


/*
	import s_curtain from '@/scenery/curtain/decor.vue'
	<s_curtain />
*/


//
// 	necessary for gradient background slide
//
import { theme_warehouse } from '@/warehouses/theme'	
	

export default {
	data () {		
		const theme = theme_warehouse.warehouse ()		
		
		return {
			palette: theme.palette,
			show: 2,	
		
			background_1: '',
			background_2: ''
		}
	},
	
	methods: {
		change_background () {		
			if (this.show === 1) {
				this.background_2 = this.palette [5] ()
				this.show = 2;
			}
			else {
				this.background_1 = this.palette [5] ()
				this.show = 1;
			}
			
			// console.info ("change curtain background", this.show, this.palette [5] ())
		}
	},
	
	created () {	
		this.theme_warehouse_monitor = theme_warehouse.monitor (({ inaugural, field }) => {
			const theme = theme_warehouse.warehouse ()
			this.palette = theme.palette;

			if (inaugural || field === "palette_name") {
				this.change_background ()
			}
				
			// console.log ('curtain theme monitor function', { inaugural, field })
		})	
	},

	
	beforeUnmount () {
		this.theme_warehouse_monitor.stop ()
	},
}

