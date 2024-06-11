





/*
	yarn run test:unit src/warehouses/cart/_status/1.status.js
*/


import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'


import assert from 'assert'

import { create_cart_system } from '@/warehouses/cart'	
import { cart_system } from '@/warehouses/cart'	

describe ('cart', () => {
	it ('works', async () => {
		await create_cart_system ()
		assert.equal (cart_system.warehouse ().IDs.length, 0)
		assert.equal (cart_system.warehouse ().treasures.length, 0)
		
		
		await cart_system.moves.change_quantity ({
			treasure: {
				emblem: 10,
				nature: {
					kind: 'food',
					identity: {
						'FDC ID': 1 
					}
				}
			},
			packages: 5
		})
		assert.equal (cart_system.warehouse ().IDs.length, 1)
		assert.equal (cart_system.warehouse ().treasures.length, 1)

		
		await cart_system.moves.change_quantity ({
			treasure: {
				emblem: 11,
				nature: {
					kind: 'supp',
					identity: {
						'DSLD ID': 1 
					}
				}
			},
			packages: 10
		})
		assert.equal (cart_system.warehouse ().IDs.length, 2)
		assert.equal (cart_system.warehouse ().treasures.length, 2)

		
		const found_DSLD_ID = await cart_system.moves.find_DSLD_ID ({
			emblem: 11,
			DSLD_ID: 1
		})
		assert.deepEqual (found_DSLD_ID, { kind: "supp", emblem: 11, DSLD_ID: 1, packages: 10 })



		const found_FDC_ID = await cart_system.moves.find_FDC_ID ({
			emblem: 10,
			FDC_ID: 1
		})
		assert.deepEqual (found_FDC_ID, { kind: "food", emblem: 10, FDC_ID: 1, packages: 5 })



		await cart_system.moves.empty ()
		assert.equal (cart_system.warehouse ().IDs.length, 0)
		assert.equal (cart_system.warehouse ().treasures.length, 0)

		//console.log (cart_system.warehouse ())
	})
})
