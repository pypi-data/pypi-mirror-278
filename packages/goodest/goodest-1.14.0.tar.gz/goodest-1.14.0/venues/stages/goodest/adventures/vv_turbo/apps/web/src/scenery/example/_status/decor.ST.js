

/*
	yarn run test:unit src/scenery/example/_status/decor.ST.js
*/


import { describe, it, expect } from 'vitest'
import assert from 'assert'

import { mount } from '@vue/test-utils'

import example_scenery from '@/scenery/example/decor.vue'
import { palette, change } from '@/scenery/example/_status/palette'

describe ('select_scenery', () => {
	it ('functions', async () => {	
		
		
		/* var palette_proxy = new Proxy (palette, {
			set: function (target, key, value) {
				console.log ("proxy", value)
				target [ key ] = value;
				return true;
			}
		});
		palette_proxy.s = 20
		*/
	
		const wrapper = mount (example_scenery, {
			props: {
				palette,
				palette_change () {
					
				}
			}
		})
		
		console.log ("palette.s:", wrapper.text ())
		
		palette.s = 22
		
		console.log ("palette.s after change:", wrapper.text ())
		
		wrapper.vm.refresh ()
		
		await new Promise (r => {
			setTimeout (() => {
				r ()
			}, 500)
		})
		
		console.log (wrapper.text ())
	})
})
