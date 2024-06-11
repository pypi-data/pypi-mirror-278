



/*
	priorities:
		use grid/lap
*/


/*
	import { retrieve_meal } from '@/fleet/goodest_DB/meals/retrieve'
	const { 
		status,
		parsed,
		proceeds
	} = await retrieve_meal ({ emblem })
*/

import { lap } from '@/fleet/syllabus/lap'
import { goals_store } from '@/warehouses/goals'

export async function retrieve_meal ({
	emblem
}) {	
	var goal = {}
	if (goals_store.warehouse ().goal_picked) {
		goal = goals_store.warehouse ().goal.emblem
	}
	
	return await lap ({
		path: "guests",
		envelope: {
			"label": "retrieve meal",
			"freight": {
				"filters": {
					"emblem": emblem
				},
				"goal": goal
			}
		}
	});
}



//