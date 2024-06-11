

import { append_field } from '@/apps/fields/append'

import router_link_scenery from '@/scenery/router_link/decor.vue'
import mural from '@/scenery/name/mural.vue'

import s_button from '@/scenery/button/decor.vue'
	
import mascot from '@/scenery/mascot/craft.vue'
import { open_business } from '@/parcels/business/open.js'

import { theme_warehouse } from '@/warehouses/theme'

// import vanta from 'vanta'
import JParticles from 'jparticles'

import { constants } from '@/constants'

export const field = {
	components: {
		mascot,
		s_button,
		mural,
		router_link_scenery
	},
	
	props: [
		'open_options'
	],

	data () {
		return {	
			focused: false
		}
	},
	created () {},
	
	beforeUnmount () {		
		const element = this.$refs.nav;
		element.removeEventListener ('focus', this.focus)
		element.removeEventListener ('blur', this.blur)
		
		this.theme_warehouse_monitor.stop ()
	},
	mounted () {
		const element = this.$refs.nav;
		element.addEventListener ('focus', this.focus)
		element.addEventListener ('blur', this.blur)
		
		this.theme_warehouse_monitor = theme_warehouse.monitor (({ inaugural, field }) => {
			const theme = theme_warehouse.warehouse ()

			console.log ('theme', { theme })
		})
		
		
		if (constants ["moving_foundations"] == "on") {
			const canvas = this.$refs.canvas;
			new JParticles.Particle (canvas, {
				// color: [ '#fff', '#ff9', '#f9f', '#9ff'],
				
				// color: ['#fff888', '#f9cd76', '#f7b26e', '#d5d02c'],
				range: 0,
				num: 0.1,
				minSpeed: 0.01,
				maxSpeed: 0.05,
				minR: 0.2,
				maxR: 1.2,
				resize: true
			})
		}
	},
	
	methods: {
		open_business,
		
		focus (event) {
			this.focused = true;
		},
		blur (event) {
			this.focused = false;
		}
	}
}