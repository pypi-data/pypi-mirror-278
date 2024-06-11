
/*
	import { open_goal } from '@/parcels/goal/open.js'
*/

import { append_field } from '@/apps/fields/append'

export async function open_goal () {
	await append_field ({
		field_title: "goal",
		field: import ('@/parcels/goal/features.vue')
	})
}