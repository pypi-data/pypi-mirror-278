



/*
	yarn run test:unit scenery/_example/_status/_example.status.js
*/

import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import assert from 'assert'

import s_example from '../example.vue'

describe ('example scenery', () => {
	it ('is operational', () => {
		const wrapper = mount (s_example, {
			props: {}
		})
		
		
	})

})





