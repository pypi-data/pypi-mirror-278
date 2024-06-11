




/*
	yarn run test:unit src/warehouses/theme/_status/1.status.js
*/

import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import assert from 'assert'

import { create_theme_warehouse } from '@/warehouses/theme'	
import { theme_warehouse } from '@/warehouses/theme'	

describe ('theme warehouse', () => {
	it ('works', async () => {
		await create_theme_warehouse ()
		// assert.equal (cart_system.warehouse ().IDs.length, 0)
		
		await theme_warehouse.moves ["change palette"] ({ 
			palette_name: "olive salad" 
		})
		
		assert.equal (
			theme_warehouse.warehouse ().palette ['1'],
			'#222'
		)
	})
})














//