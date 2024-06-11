

/* */

import s_input from '@/scenery/input/decor.vue'
import s_button from '@/scenery/button/decor.vue'
import s_line from '@/scenery/line/decor.vue'
import s_outer_link from '@/scenery/link/outer/decor.vue'

import g_table from '@%/glamour/table/decor.vue'
import { sort_as_strings } from '@%/glamour/table/sorting/as_string.js'

import save_button from './components/save_button.vue'
	
export const decor = {
	components: { 
		s_outer_link, 
		s_input, 
		s_button, 
		s_line,
		g_table
	},
	data () {
		return {
			correspondance: ''
		}
	},
	methods: {
		sort_as_strings,
		send () {
			
		},
		rows () {
			return [{
				'1': 'Ethereum',
				'2': '0x9D5D9559A43080d3F478d7e76dB057b57992b46C',
				'3': {
					component: save_button,
					props: {
						address: '0x9D5D9559A43080d3F478d7e76dB057b57992b46C'
					}
				}
			},{
				'1': 'Polkadot',
				'2': '1wr7RE273GzJDXEQqF28MMWBEsLQSrNvpQCL6B33emuSgNQ',
				'3': {
					component: save_button,
					props: {
						address: '1wr7RE273GzJDXEQqF28MMWBEsLQSrNvpQCL6B33emuSgNQ'
					}
				}
			},{
				'1': 'Cardano',
				'2': 'addr1qy0ula9c8tf5rpu9m3nhnvx8md7vd2eg6snusj8fzycl9uxlaftgt2lccp8crtlzklrkprfp2g3ft77s32gdh6jpgpyqnqhr20',
				'3': {
					component: save_button,
					props: {
						address: 'addr1qy0ula9c8tf5rpu9m3nhnvx8md7vd2eg6snusj8fzycl9uxlaftgt2lccp8crtlzklrkprfp2g3ft77s32gdh6jpgpyqnqhr20'
					}
				}
			}]
		}
	},
	mounted () {
		/*
		let script = document.createElement('script')
		script.setAttribute('src', 'https://js.stripe.com/v3/buy-button.js')
		this.$refs['crate-script'].appendChild(script)
		 */
	}
}