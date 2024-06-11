
/*
	(source SOURCE.tcsh && cd STORE/CROPS && yarn run test:unit grid)
*/

/*
	CARBOHYDRATE, BY DIFFERENCE
		FIBER, TOTAL DIETARY
*/


import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import { SORT_NUTRIENTS } from '@/grid/nutrients/sort'

import assert from 'assert'

describe ('SORT NUTRIENTS', () => {
	it ('SORTS', () => {
		// assert.deepEqual (round_quantity (91.555), '91.56')
		
		const NUTRIENTS = [
			{
				"QUANTITY": {
					"SYSTEM INTERNATIONAL": {
						"PER PACKAGE": [
							"20.0",
							"IU"
						]
					}
				}
			},
			{
				"QUANTITY": {
					"SYSTEM INTERNATIONAL": {
						"PER PACKAGE": [
							"5.0",
							"IU"
						]
					}
				}
			},
			{
				"QUANTITY": {
					"SYSTEM INTERNATIONAL": {
						"PER PACKAGE": [
							"100.0",
							"mcg"
						]
					}
				}
			},
			{
				"QUANTITY": {
					"SYSTEM INTERNATIONAL": {
						"PER PACKAGE": [
							"10.0",
							"g"
						]
					}
				}
			},
			{
				"QUANTITY": {
					"SYSTEM INTERNATIONAL": {
						"PER PACKAGE": [
							"30.0",
							"mcg"
						]
					}
				}
			},
			{
				"QUANTITY": {
					"SYSTEM INTERNATIONAL": {
						"PER PACKAGE": [
							"10.0",
							"IU"
						]
					}
				}
			},
			{
				"QUANTITY": {
					"SYSTEM INTERNATIONAL": {
						"PER PACKAGE": [
							"20.0",
							"mg"
						]
					}
				}
			} 
		]
		
		SORT_NUTRIENTS ({
			MEASUREMENT_SYSTEM: "SYSTEM INTERNATIONAL",
			NUTRIENTS 
		})


		const RELEVANT = NUTRIENTS.map (NUTRIENT => {
			return NUTRIENT ["QUANTITY"]["SYSTEM INTERNATIONAL"]["PER PACKAGE"]
		})

		console.log (JSON.stringify (RELEVANT, null, 4))
		
		assert.equal (
			JSON.stringify (RELEVANT, null, 4),
			JSON.stringify ([
				[
					"10.0",
					"g"
				],
				[
					"20.0",
					"mg"
				],
				[
					"100.0",
					"mcg"
				],
				[
					"30.0",
					"mcg"
				],
				[
					"20.0",
					"IU"
				],
				[
					"10.0",
					"IU"
				],
				[
					"5.0",
					"IU"
				]
			], null, 4)
		)
	})
	
	it ('SORTS 1', () => {
		// assert.deepEqual (round_quantity (91.555), '91.56')
		
		const NUTRIENTS = [
			{
				"QUANTITY": {
					"SYSTEM INTERNATIONAL": {
						"PER PACKAGE": [
							"10.0",
							"mg"
						]
					}
				}
			},
			{
				"QUANTITY": {
					"SYSTEM INTERNATIONAL": {
						"PER PACKAGE": [
							"30.0",
							"mg"
						]
					}
				}
			},
			{
				"QUANTITY": {
					"SYSTEM INTERNATIONAL": {
						"PER PACKAGE": [
							"20.0",
							"mg"
						]
					}
				}
			} 
		]
		
		SORT_NUTRIENTS ({
			MEASUREMENT_SYSTEM: "SYSTEM INTERNATIONAL",
			NUTRIENTS 
		})
		
		assert.equal (
			JSON.stringify (NUTRIENTS, null, 4),
			JSON.stringify ([
				{
					"QUANTITY": {
						"SYSTEM INTERNATIONAL": {
							"PER PACKAGE": [
								"30.0",
								"mg"
							]
						}
					}
				},
				{
					"QUANTITY": {
						"SYSTEM INTERNATIONAL": {
							"PER PACKAGE": [
								"20.0",
								"mg"
							]
						}
					}
				},
				{
					"QUANTITY": {
						"SYSTEM INTERNATIONAL": {
							"PER PACKAGE": [
								"10.0",
								"mg"
							]
						}
					}
				}
			], null, 4)
		)		
	})
})
