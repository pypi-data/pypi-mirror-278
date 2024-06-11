



/*
	import { open_sink_filter } from '@/parcels/sink-filter/open'
	await open_sink_filter ()
*/

import { append_field } from '@/apps/fields/append'

export async function open_sink_filter () {
	await append_field ({
		label: "sink filter",
		field: import ('@/parcels/sink-filter/field.vue')
	})
}