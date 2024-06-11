




/*
	yarn run test:unit furnish
*/


import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import assert from 'assert'

import { furnish_string } from '@/grid/furnish/string'
	
	

describe ('grid furnish string', () => {
	it ('is operational', () => {
		assert.equal (
			furnish_string ({ 's': '1' }, [ 's' ], null), 
			'1'
		)
		
		assert.equal (
			furnish_string ({ 's': '1' }, [ 'w' ], null), 
			''
		)
		
		assert.equal (
			furnish_string ({ 's': '1' }, [ 'w' ], '1234'), 
			'1234'
		)
		
	})
	
	it ('is operational', () => {
		assert.equal (
			furnish_string ('1'), 
			'1'
		)
		
		
		assert.equal (
			furnish_string (null), 
			''
		)
		
		assert.equal (
			furnish_string (1234),
			''
		)
		
	})
})
