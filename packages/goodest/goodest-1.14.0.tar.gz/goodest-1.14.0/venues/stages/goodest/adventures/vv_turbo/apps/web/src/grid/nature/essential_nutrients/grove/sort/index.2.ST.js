








/*
	python3 start.py 'test:unit src/grid/nature/essential_nutrients/grove/calc_linear_grove/index.ST.js'
*/



import { sort_grove } from './index.js'

import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import assert from 'assert'

import { build_grove } from './cryo/grove-1'

describe ('nature, essential nutrients, grove, calc linear nutrients', () => {
	it ('works 2', () => {
		var grove = [
			{
				"measures": {
					"mass + mass equivalents": {
						"per recipe": {
							"grams": {
								"fraction string": "1/1"
							}
						}
					}
				}
			},
			{
				"measures": {
					"mass + mass equivalents": {
						"per recipe": {
							"grams": {
								"fraction string": "3"
							}
						}
					}
				}
			},
			{
				"measures": {
					"mass + mass equivalents": {
						"per recipe": {
							"grams": {
								"fraction string": "2"
							}
						}
					}
				}
			}
		]
		
		sort_grove ({ 
			grove
		})

		console.log (JSON.stringify ({ grove }, null, 4))
	})
})
