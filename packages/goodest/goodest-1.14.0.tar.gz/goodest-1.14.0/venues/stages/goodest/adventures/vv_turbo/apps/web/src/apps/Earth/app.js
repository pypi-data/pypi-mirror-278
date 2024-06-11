


/*
	import { APP } from '@/main.js'
*/

import '@/assets/main.css'

import { createApp } from 'vue'

/*
	Earth and the earth logistics
*/
import earth from '@/apps/Earth/scenery/planet/field.vue'
import logistics from '@/apps/Earth/logistics'

/*
	mercantile systems
*/
import { create_cart_system } from '@/warehouses/cart'	

import { create_theme_warehouse } from '@/warehouses/theme'
import { palettes } from '@/warehouses/theme/rooms/palettes.js'

import { create_homestead_system } from '@/warehouses/homestead'	
import { create_layout_system } from '@/warehouses/layout'	
import { make_goals_store } from '@/warehouses/goals'
import { make_browser_storage_store } from '@/warehouses/storage'	
	
// import { create_terrain_system } from '@/warehouses/terrain'

	
import { theme_warehouse } from '@/warehouses/theme'

/*
	components
*/
import lounge from '@/scenery/lounge/decor.vue'
//
import s_panel from '@/scenery/panel/decor.vue'
import s_line from '@/scenery/line/decor.vue'
import s_outer_link from '@/scenery/link/outer/decor.vue'
import hw_button from "@/scenery/hw_button/decor.vue" 
import s_button from '@/scenery/button/decor.vue'
import s_paragraph from '@/scenery/paragraph/scenery.vue'

// export let APP = null;



/*
	This course is started in this script.
*/
export async function start () {
	const the_systems = await Promise.all ([
		create_theme_warehouse ({
			palettes
		}),
		make_browser_storage_store ()
	])
	
	try {
		document.body.style.background = theme_warehouse.warehouse ("palette") [1]	
	}
	catch (exception) {
		console.error (exception)
	}
	
	console.log ({ the_systems })
	
	
	console.log ('creating client databases')
	try {
		await Promise.all ([
			create_cart_system ()
		])
	}
	catch (exception) {
		console.error (exception)
	}

	
	const app = createApp (earth)
	app.component ('warehouse_scenery',	lounge);
	app.component ('lounge', lounge);
	app.component ('s_panel', s_panel);
	app.component ('s_line', s_line);
	app.component ('s_outer_link', s_outer_link);
	app.component ('hw_button', hw_button);
	app.component ('s_button', s_button);
	app.component ('s_paragraph', s_paragraph);
	
	app.provide ('homestead_system', await create_homestead_system ())
	app.provide ('layout_system', await create_layout_system ())
	app.provide ('goals_store', await make_goals_store ())
	app.provide ('theme_system', the_systems [1])
	
	app.use (logistics)
	app.mount ('#app')
	
	// APP = app;
}











/*

*/