




/*
	yarn run test:unit furnish
*/


import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import assert from 'assert'

import { furnish } from '@/grid/furnish'
	
	

describe ('grid furnish', () => {
	it ('can furnish a number', () => {
		assert.equal (
			furnish ('number') ({ 's': 1 }, [ 's' ], null), 
			1
		)
		

		
	})
	
	it ('is operational', () => {

		
	})
})
