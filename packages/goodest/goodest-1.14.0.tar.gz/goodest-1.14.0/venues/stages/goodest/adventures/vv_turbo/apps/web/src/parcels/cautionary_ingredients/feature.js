

import _get from 'lodash/get'

import nature_ingredients_table from '@/scenery/nature_ingredients_table/fountains.vue'


export const feature = {
	inject: ['properties'],
	
	components: { nature_ingredients_table },
	
	computed: {
		scanned_for () {
			return _get (this, [ 'properties', 'scanned_for' ], [])	
		},
		grove () {
			return _get (this, [ 'properties', 'grove' ], [])	
		}
	},
	
	mounted () {
		const properties = this.properties;
		
		console.log ({ properties })
		
	}	
}