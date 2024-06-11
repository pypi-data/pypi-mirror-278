

/*
	priorities:
		component tests
		
			


*/



var chassis = "/@2/"

export const workshop_routes = [
	{
		name: 'scenery',
		path: chassis + 'scenery',
		component: () => import ('@/regions/workshop/scenery/region.vue')
	}
]