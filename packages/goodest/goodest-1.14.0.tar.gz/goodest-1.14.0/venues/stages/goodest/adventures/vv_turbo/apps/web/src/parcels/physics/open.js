
/*
	import { open_physics } from '@/parcels/physics/open.js'
*/

import { append_field } from '@/apps/fields/append'

export async function open_physics () {
	await append_field ({
		field_title: "physics",
		field: import ('@/parcels/physics/field.vue')
	})
}