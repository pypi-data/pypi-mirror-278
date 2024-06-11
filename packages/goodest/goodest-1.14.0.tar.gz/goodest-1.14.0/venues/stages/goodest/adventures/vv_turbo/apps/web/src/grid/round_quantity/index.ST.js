

import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import { round_quantity } from '@/grid/round_quantity'

import assert from 'assert'

describe ('grid round_quantity', () => {
	it ('round_quantityS', () => {
		assert.deepEqual (round_quantity (91.555), '91.56')
		assert.deepEqual (round_quantity (91.3123), '91.31')
		assert.deepEqual (round_quantity (1.3123), '1.31')
		assert.deepEqual (round_quantity (1), '1.00')
		assert.deepEqual (round_quantity (0), '0.00')
		
		assert.deepEqual (round_quantity (-1), '-1.00')
		assert.deepEqual (round_quantity (-91.47823), '-91.48')
		assert.deepEqual (round_quantity (-91.555), '-91.55')

		assert.deepEqual (round_quantity ('0'), '0.00')
		assert.deepEqual (round_quantity ('-91.123'), '-91.12')

		assert.deepEqual (round_quantity (''), '')		
		assert.deepEqual (round_quantity ('S'), '')
	})
})
