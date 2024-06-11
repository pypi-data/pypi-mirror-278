





/*
	python3 start.py 'test:unit src/grid/nature/essential_nutrients/grove/calc_linear_grove/index.ST.js'
*/



import { calc_linear_grove } from './index.js'

import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import assert from 'assert'

import { grove } from './grove-1'

describe ('nature, essential nutrients, grove, calc linear nutrients', () => {
	it ('works', () => {
		var linear_grove = calc_linear_grove ({ 
			grove: grove ()
		})
				
		assert.equal (linear_grove.length, 46)
	})
	
	it ('works', () => {
		var linear_grove = calc_linear_grove ({ 
			grove: [
				{
					"unites": [{
						"unites": [{
						
						}]
					}]
				},
				{
					
				}
			]
		})
		
		// console.log ({ linear_grove })
			
		assert.equal (linear_grove [0].indent, 0)
		assert.equal (linear_grove [1].indent, 1)
		assert.equal (linear_grove [2].indent, 2)
		assert.equal (linear_grove [3].indent, 0)
				
		assert.equal (linear_grove.length, 4)
	})
})
