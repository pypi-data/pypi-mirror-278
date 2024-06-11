

/*
	import { status_routes } from '@/apps/Earth/logistics/status'

*/

import { createRouter, createWebHistory } from 'vue-router'

var chassis = "/@status/"
/*
	/@status/DAC
	/@status/scenery/_example/_status/region
*/

export const status_routes = [
	{
		name: 'status_index',
		path: chassis,
		component: () => import ('@/regions/status/index/scenery.vue')
	},
	{
		name: '_example',
		path: chassis + 'scenery/_example/_status/region',
		component: () => import ('@/scenery/_example/_status/region.vue')
	},
	{
		name: 'waterfall',
		path: chassis + 'waterfall',
		component: () => import ('@/regions/status/waterfall/region.vue')
	},
	{
		name: 'DAC',
		path: chassis + 'DAC',
		component: () => import ('@/regions/status/DAC/region.vue')
	},
	{
		name: 'g_table',
		path: chassis + 'glamour/table/_status/status',
		component: () => import ('@%/glamour/table/_status/status.vue')
	}
]