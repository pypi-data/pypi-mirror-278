




/*
	yarn run test:unit src/scenery/select/decor.status.js
*/


import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import assert from 'assert'

import select_scenery from '@/scenery/select/decor.vue'

/*
	https://pinia.vuejs.org/cookbook/testing.html
*/
describe ('select_scenery', () => {
	it ('functions', async () => {
		/*const wrapper = mount (select_scenery, {
			props: {
				name: "palette",
				preselected_option: "chia",
				options: [
					'chia',
					'soy'
				],
				change () {
					console.log ('change')
				}
			}
		})
		*/
	})
})
