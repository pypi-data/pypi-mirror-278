

import { cart_system } from '@/warehouses/cart'
	
import s_button from '@/scenery/button/decor.vue'
import s_input from '@/scenery/input/decor.vue'

import { has_field } from '@/grid/object/has_field'

import _get from 'lodash/get'

export const decor = {
	components: { 
		s_button, 
		s_input 
	},
	
	props: [ 'kind', 'treasure' ],

	data () {
		return {
			packages: 0,
			
			found: false,
			cart_details: this.empty_details (),
			
			cart: cart_system.warehouse ()
		}
	},
	
	computed: {
		emblem () {
			const treasure = this.treasure
			return _get (treasure, [ 'emblem' ], '')
		},
		identity () {
			const treasure = this.treasure
			return _get (treasure, [ 'nature', 'identity' ], '')	
		}
	},
	
	methods: {
		empty_details () {
			return {
				packages: 0
			}
		},
		
		async change_quantity () {
			const emblem = this.emblem;
			const kind = this.kind;
						
			const packages = parseInt (this.packages);
			const treasure = this.treasure;
			
			await cart_system.moves.change_quantity ({
				treasure,
				packages
			})
		},

		async product_quantity () {
			const emblem = this.emblem;
			const kind = this.kind;
			const identity = this.identity;
			
			
			if (kind === "food") {
				const details = await cart_system.moves.find_FDC_ID ({
					emblem,
					FDC_ID: identity ["FDC ID"]
				})
				if (has_field (details, 'emblem')) {
					this.found = true;
					this.cart_details = details;
				}
				else {
					this.found = false;
					this.cart_details = this.empty_details ();
				}
			}
			else if (kind === "supp") {
				const details = await cart_system.moves.find_DSLD_ID ({
					emblem,
					DSLD_ID: identity ["DSLD ID"]
				})
				if (has_field (details, 'emblem')) {
					this.found = true;
					this.cart_details = details;
				}
				else {
					this.found = false;
					this.cart_details = this.empty_details ()
				}
				
				this.found = false;
				
				//console.log ({ details })
			}
			
			return this.cart_details
		}
	},
	created () {        
		this.cart_monitor = cart_system.monitor (({ inaugural, field }) => {
			this.cart = cart_system.warehouse ()
						
			// console.log ("cart monitor", this.cart)			
						
			this.product_quantity ()
		})
    },
	async mounted () {
		let packages = 0
		try {
			const details = await this.product_quantity ()
			packages = details.packages
		}
		catch (exception) {}
		if (typeof packages !== 'number') {
			packages = 0
		}		
				
		this.packages = packages;
	},	
    beforeUnmount () {
		this.cart_monitor.stop ()
    }
}