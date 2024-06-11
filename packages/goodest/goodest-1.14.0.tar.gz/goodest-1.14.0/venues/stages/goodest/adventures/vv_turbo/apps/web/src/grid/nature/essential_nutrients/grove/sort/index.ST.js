








/*
	python3 start.py 'status src/grid/nature/essential_nutrients/grove/sort/index.ST.js'
*/



import { sort_grove } from './index.js'

import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import assert from 'assert'

// import { build_grove } from './cryo/grove-1'
import { build_grove } from '@/grid/nature/essential_nutrients/grove/sort/cryo/grove-1'

describe ('nature, essential nutrients, grove, calc linear nutrients', () => {
	it ('works', () => {
		var grove = build_grove ()
		
		sort_grove ({ 
			grove
		})

		console.log ("1", JSON.stringify (grove [1], null, 4))
	
		assert.equal (grove [0] ["essential"]["names"][0], "fats")
		assert.equal (grove [1] ["essential"]["names"][0], "carbohydrates")
	})
	
})
