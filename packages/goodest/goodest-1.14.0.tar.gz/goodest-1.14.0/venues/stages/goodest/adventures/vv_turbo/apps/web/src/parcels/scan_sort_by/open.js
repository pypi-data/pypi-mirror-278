

/*
	import { open_scan_sort_by } from '@/parcels/scan_sort_by/open'
	await open_scan_sort_by ()
*/

import { append_field } from '@/apps/fields/append'

export async function open_scan_sort_by () {
	await append_field ({
		field_title: "scan sort",
		field: import ('@/parcels/scan_sort_by/field.vue')
	})
}