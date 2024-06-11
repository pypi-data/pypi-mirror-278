


/*
	import { open_ingredient } from '@/parcels/ingredient/open.js'
	await open_ingredient ({
		ingredient
	})
*/

import { append_field } from '@/apps/fields/append'

export async function open_ingredient ({ ingredient = "" } = {}) {
	await append_field ({
		field_title: ingredient,
		field: import ('@/parcels/ingredient/feature.vue'),
		properties: {
			ingredient
		}
	})
}