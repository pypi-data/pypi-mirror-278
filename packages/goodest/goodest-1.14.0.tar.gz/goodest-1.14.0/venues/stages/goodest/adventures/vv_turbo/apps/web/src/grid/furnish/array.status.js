




/*
	yarn run test:unit "src/grid/furnish"
*/


import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import assert from 'assert'

import { furnish_array } from '@/grid/furnish/array'
	
	

describe ('grid furnish array', () => {
	it ('is operational', () => {
		const a1 = furnish_array ({ 's': [ '1' ] }, [ 's' ], null);
		assert.equal (a1[0], '1')
		assert.equal (a1.length, 1)

		const a2 = furnish_array ({}, [ 's' ], null);
		assert.equal (a2.length, 0)
	})
	
	it ('is operational', () => {
		const a1 = furnish_array ([ '1', '2' ]);
		assert.equal (a1.length, 2)
		assert.equal (a1 [0], '1')
		assert.equal (a1 [1], '2')


		
	})
})
