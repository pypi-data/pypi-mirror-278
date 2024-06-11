
/*
	import { open_business } from '@/parcels/business/open.js'
*/

import { append_field } from '@/apps/fields/append'

export async function open_business () {
	await append_field ({
		field_title: "banquet",
		field: import ('@/parcels/business/decor.vue')
	})
}