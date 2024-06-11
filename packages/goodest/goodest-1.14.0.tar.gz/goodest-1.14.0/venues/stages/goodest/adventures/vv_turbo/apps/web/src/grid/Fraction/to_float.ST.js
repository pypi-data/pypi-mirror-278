


/*
	python3 start.py 'test:unit src/grid/Fraction/to_float.ST.js'
*/


import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import assert from 'assert'

import { fraction_to_float } from '@/grid/Fraction/to_float'

describe ('grid Fraction to float', () => {
	it ('works', () => {
		assert.deepStrictEqual (fraction_to_float ("1"), '1.00')
		assert.deepStrictEqual (fraction_to_float ("1/2"), '0.50')
		assert.deepStrictEqual (fraction_to_float ("1/3"), '0.33')
		assert.deepStrictEqual (fraction_to_float ("2/3"), '0.67')
	})
	
	it ('works', () => {
		assert.deepStrictEqual (fraction_to_float ("1", false), 1)
		assert.deepStrictEqual (fraction_to_float ("1/2", false), 0.5)
		assert.deepStrictEqual (fraction_to_float ("1/3", false), 0.3333333333333333)
		assert.deepStrictEqual (fraction_to_float ("2/3", false), 0.6666666666666666)
	})
})
