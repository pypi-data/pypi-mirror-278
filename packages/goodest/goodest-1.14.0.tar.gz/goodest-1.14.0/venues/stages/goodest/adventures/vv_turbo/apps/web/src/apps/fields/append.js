
/*
	import { append_field } from '@/apps/fields/append'
	await append_field ({
		label: "template",
		region: import ('@/parcels/_template/field.vue')
	})
*/

/*
	
	
	objectives:
		import { append_field } from '@/apps/fields/append'
		await append_field ({
			label: "template",
			region: import ('@/parcels/_template/field.vue'),
			provide: {},
			components: {
				"lounge": lounge
			}
		})
*/


/*
	structure:
		#field
			component: area
				component: field
*/


import { defineAsyncComponent } from 'vue'	

import { build } from '@/apps/fields/app'
import { fields_element, fields } from '@/apps/fields/moves/variables'
import { build_field_element } from '@/apps/fields/moves/build_field_element'
import { get_next_coordinate } 	from '@/apps/fields/moves/get_next_coordinate'

import lounge from '@/scenery/lounge/decor.vue'

export async function append_field ({
	//
	//	can use either 'label' or 'field_title'
	//
	label = "",
	field_title = "",

	//
	//	can use either 'region' or 'field'
	//
	region = null,
	field = null,
	
	//
	//	
	//
	properties = {},
	
	//
	before_mount = async function () {},
	
} = {}) {
	//
	//	alias parsing
	//
	if (field) {
		region = field;
	}
	if (label.length >= 1) {
		field_title = label;
	}
	
	//
	
	const field_component = await defineAsyncComponent (() => region)
	const field_element = build_field_element ()
	const the_coordinate = await get_next_coordinate ()
	

	fields.push ({
		the_coordinate,
		the_element: field_element
	})
	fields_element.appendChild (field_element)
	
	const { app } = await build ({
		the_coordinate,
		field: field_component,
		field_title,
		field_element: field_element,
		
		properties
	})
	await before_mount ({ app })
	
	app.mount (field_element)
	
	setTimeout (() => {
		field_element.style.opacity = 1;
	}, 100)
	
	return {
		the_coordinate
	}
}