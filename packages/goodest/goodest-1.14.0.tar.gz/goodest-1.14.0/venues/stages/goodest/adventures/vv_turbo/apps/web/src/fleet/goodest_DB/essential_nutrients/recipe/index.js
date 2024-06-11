


/*
	import { retrieve_EN_recipe } from '@/fleet/goodest_DB/essential_nutrients/recipe'
	const { 
		status,
		parsed,
		proceeds
	} = await retrieve_EN_recipe ()
*/

import cloneDeep from 'lodash/cloneDeep'

import { cart_system } from '@/warehouses/cart'	
import { lap } from '@/fleet/syllabus/lap'

import { goals_store } from '@/warehouses/goals'

export async function retrieve_EN_recipe () {	
	const IDs = cloneDeep (cart_system.warehouse ().IDs)
	
	var goal = {}
	if (goals_store.warehouse ().goal_picked) {
		goal = goals_store.warehouse ().goal.emblem
	}
	
	/*
		IDs = IDs.map (ID => {})
	*/
	return await lap ({
		path: "guests",
		envelope: {
			"label": "retrieve recipe",
			"freight": {
				"goods": IDs,
				goal
			}
		}
	});
}