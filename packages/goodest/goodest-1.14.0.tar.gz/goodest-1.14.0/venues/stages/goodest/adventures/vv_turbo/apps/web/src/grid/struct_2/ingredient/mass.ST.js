

/*
	strategy:

	{
		// name as listed?
		"name": "Protein",
		"mass": {
			//
			// this is the same for any fraction of the package
			//
			"portional": {
				"compositional": {
					"from defined package mass": {},
					"from quantified ingredients": {}
				},
				"effectual": {
					"from quantified ingredients": {
						
					}
				}
			},
			
			"per package": {
				"float grams": 74.392,
				"float string grams": "74.392",
				"fraction string grams": "104697432337295601/1407374883553280"
			},
			"per serving": {
				
				
			}
		},
		"quantified grove": [],
		"struct": {
			
			
		}
	}

*/


const example_1 = {
	"mass": {
		"compositional portion per package": {
			"from defined package mass": {
				"fraction float string": "0.2188",
				"fraction string": "6158672490429153/28147497671065600",
				"percentage string": "21.880%"
			}
		},
		"effectual portion per package": {
			"from quantified ingredients": {
				"fraction float string": "0.22525726995189502",
				"fraction string": "24634689961716612000/109362463493309192069",
				"percentage string": "22.526%"
			}
		},
	
	"per package": {
		"float": {
		  "amount": 74.392,
		  "unit": "g"
		},
		"float grams": 74.392,
		"fraction string": {
		  "amount": "104697432337295601/1407374883553280",
		  "unit": "g"
		},
		"fraction string grams": "104697432337295601/1407374883553280"
	  },
	"per serving": {
		"float": {
		  "amount": 7.0016,
		  "unit": "g"
		},
		"fraction string": {
		  "amount": "6158672490429153/879609302220800",
		  "unit": "g"
		}
	  }
	},
	"name": "Protein",
	"quantified grove": [],
	"struct": {
	  "includes": [],
	  "names": [
		"protein"
	  ],
	  "region": 1
	}
}
  





/*
	yarn run test:unit furnish
*/


import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import assert from 'assert'

import { retrieve_mass } from '@/grid/struct_2/ingredient/mass'

describe ('grid furnish array', () => {
	it ('is operational', () => {
		const mass = retrieve_mass ({ ingredient: example_1 })
			
		assert.equal (mass [0], '74.39')
		assert.equal (mass [1], 'g')		
	})
})
