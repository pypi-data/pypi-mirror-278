

import { createRouter, createWebHistory } from 'vue-router'

import habitat from '@/regions/guests/habitat/decor.vue'

// var intro_path = "/@/"
var intro_path = "/front/@/"
var intro_path_s1 = "/@@/"

export const guests_routes = [
	{
		name: 'habitat',
		path: '/',
		component: habitat
	},
	{
		name: 'herbs',
		path: intro_path + 'herbs',
		component: () => import ('@/regions/guests/vegan_groceries/decor.vue')
	},
	{
		name: 'controls',
		path: intro_path + 'controls',
		component: () => import ('@/parcels/controls/decor.vue')
	},

	{
		name: 'food',
		path: intro_path + 'food/:emblem',
		component: () => import ('@/regions/guests/food/decor.vue')
	},
	{
		name: 'supp',
		path: intro_path + 'supp/:emblem',
		component: () => import ('@/regions/guests/supp/decor.vue')
	},	
	{
		name: 'meal',
		path: intro_path + 'meal/:emblem',
		component: () => import ('@/regions/guests/meal/decor.vue')
	},	
	
	//--
	//
	//	customs
	//
	{
		name: 'goal',
		path: intro_path + 'goal',
		component: () => import ('@/regions/guests/goal/room.vue'),
		children: []
	},
	{
		name: 'presents',
		path: intro_path + 'presents',
		component: () => import ('@/regions/guests/cart/decor.vue'),
		children: []
	},
	{
		name: 'account',
		path: intro_path + 'account',
		component: () => import ('@/regions/guests/account/decor.vue'),
		children: []
	},
	
	//--
	
	{
		name: 'meals',
		path: intro_path + 'meals',
		component: () => import ('@/regions/guests/meals/decor.vue')
	},	
	{
		name: 'map',
		path: intro_path + 'map',
		component: () => import ('@/regions/guests/map/decor.vue')
	},
	
	//--
	
	{
		name: 'navigation lab',
		path: intro_path_s1 + 'navigation-lab',
		component: () => import ('@/parcels/navigation-lab/field.vue')
	},
	{
		name: 'comparisons',
		path: intro_path_s1 + 'comparisons',
		component: () => import ('@/regions/guests/comparisons/region.vue')
	},
	
	//--
	
	{
		name: 'emblem',
		path: intro_path_s1 + 'emblem',
		component: () => import ('@/regions/guests/emblem/decor.vue')
	},	
]