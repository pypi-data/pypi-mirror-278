
import cloneDeep from 'lodash/cloneDeep'

import { cart_system } from '@/warehouses/cart'	
import { theme_warehouse } from '@/warehouses/theme'
	

export default {    
	inheritAttrs: false,
	
	inject: [ 
		'homestead_system'
	],
	
	props: {
		style: {
			type: Object,
			default () {}
		}
	},
	
	beforeCreate () {
		// console.log ('lounge beforeCreate', cloneDeep (this.$attrs))
	},
	
    data () {
		//console.log ('homestead_system', this.homestead_system)
		
		const theme = theme_warehouse.warehouse ()
		const homestead = this.homestead_system.warehouse ()
		
        return {
			theme,
            palette: theme.palette,
			palette_name: theme.palette_name,
			
            terrain: homestead.terrain,
			physics: homestead.terrain,
			
			cart: cart_system.warehouse ()
        }
    },
    created () {   
		this.cart_monitor = cart_system.monitor (({ inaugural, field }) => {
			this.cart = cart_system.warehouse ()
		})
		this.homestead_system_monitor = this.homestead_system.monitor (({ inaugural, field }) => {
			const homestead = this.homestead_system.warehouse ()
			this.terrain = homestead.terrain;
		})
		this.theme_warehouse_monitor = theme_warehouse.monitor (({ inaugural, field }) => {
			this.theme = theme_warehouse.warehouse ()
			this.palette = this.theme.palette;
			this.palette_name = this.theme.palette_name;
		})
    },
    beforeUnmount () {
		// console.log ("lounge before unmount")
		
		this.cart_monitor.stop ()
		this.homestead_system_monitor.stop ()
		this.theme_warehouse_monitor.stop ()
    },
	
	mounted () {
		// console.log (this.warehouse_1)
		
	}
}