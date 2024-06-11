
/*
	priorities:
		add food?


*/


var chassis_staff = "/@1/"

export const staff_routes = [
	{
		name: 'staff',
		path: chassis_staff,
		component: () => import ('@/regions/staff/habitat/decor.vue')
	}
]