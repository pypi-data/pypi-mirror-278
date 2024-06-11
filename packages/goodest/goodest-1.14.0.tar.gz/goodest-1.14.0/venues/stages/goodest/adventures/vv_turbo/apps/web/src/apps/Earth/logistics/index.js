

/*
	possibilities:
		have a place bar at the top: 
			"navigation"
			"grocery list"
*/


import { createRouter, createWebHistory } from 'vue-router'

import habitat from '@/regions/guests/habitat/decor.vue'

import { staff_routes } from './staff'
import { guests_routes } from './guests'
import { workshop_routes } from './workshop'
import { status_routes } from './status'

const router = createRouter({
	history: createWebHistory (import.meta.env.BASE_URL),
	routes: [
		...guests_routes,
		...staff_routes,
		...workshop_routes,
		
		...status_routes,
		

		/*
			https://router.vuejs.org/guide/migration/#Removed-star-or-catch-all-routes
		*/		
		{ 
			path: '/:pathMatch(.*)*', 
			name: 'not-found', 
			component: () => import ('@/regions/not_found.vue')  
		}
	]
})

export default router
