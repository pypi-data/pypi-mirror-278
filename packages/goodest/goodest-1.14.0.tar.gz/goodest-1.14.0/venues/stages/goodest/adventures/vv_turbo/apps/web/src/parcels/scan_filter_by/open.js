

/*
	import { open_scan_filter_by } from '@/parcels/scan_filter_by/open'
	await open_scan_filter_by ()
*/

import { append_field } from '@/apps/fields/append'

export async function open_scan_filter_by () {
	await append_field ({
		field_title: "scan filter",
		field: import ('@/parcels/scan_filter_by/field.vue')
	})
}