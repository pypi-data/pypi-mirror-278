




/*
	import { open_cautionary_ingredients_novel } from '@/parcels/cautionary_ingredients/open.js'
	await open_cautionary_ingredients_novel ({
		properties: {}
	})
*/

import { append_field } from '@/apps/fields/append'

export async function open_cautionary_ingredients_novel (packet) {
	const properties = packet ["properties"]
	
	await append_field ({
		field_title: "cautionary ingredients",
		field: import ('@/parcels/cautionary_ingredients/feature.vue'),
		properties
	})
}