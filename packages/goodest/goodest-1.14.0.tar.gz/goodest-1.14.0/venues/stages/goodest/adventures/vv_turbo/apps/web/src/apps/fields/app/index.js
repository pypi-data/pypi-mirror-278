

/*
	const UNIT_SYSTEM_field = import ('@/apps/fields/parcels/unit_systems/OPEN.js')
*/

import { createApp, defineAsyncComponent } from 'vue'
import { createPinia } from 'pinia'

import { make_system } from '@medical-district/system' 

import { remove_field } from '@/apps/fields/remove'	
import eco from '@/apps/fields/hacienda/eco.vue'

import lounge from '@/scenery/lounge/decor.vue'
import s_line from '@/scenery/line/decor.vue'

import { create_homestead_system } from '@/warehouses/homestead'
import { create_theme_warehouse } from '@/warehouses/theme'

export async function build ({
	the_coordinate,
	field,
	
	field_title = "",
	field_element,
	
	variables = {},
	properties = {}
}) {	
	const planet = createApp (eco)
	planet.use (createPinia ())


	/*
		https://vuejs.org/guide/components/provide-inject.html#prop-drilling
	*/
	planet.provide ('the_coordinate', the_coordinate)
	planet.provide ('field_title', field_title);
	planet.provide ('field_element', field_element);
	planet.provide ('homestead_system', await create_homestead_system ())
	planet.provide ('properties', properties);
	
	planet.component ('field_component', field);
	planet.component ('lounge', lounge);
	planet.component ('s_line', s_line);

	// planet.config.errorHandler = (err, instance, info) => {}
	// planet.config.warnHandler = (msg, instance, trace) => {}

	return { app: planet }
}

