




/*
	import { open_essential_nutrients_novel } from '@/parcels/essential_nutrients/open.js'
	await open_essential_nutrients_novel ({})
*/

import { append_field } from '@/apps/fields/append'

export async function open_essential_nutrients_novel (packet) {
	const properties = packet ["properties"]
	
	await append_field ({
		field_title: "essential nutrients",
		field: import ('@/parcels/essential_nutrients/feature.vue'),
		properties
	})
}