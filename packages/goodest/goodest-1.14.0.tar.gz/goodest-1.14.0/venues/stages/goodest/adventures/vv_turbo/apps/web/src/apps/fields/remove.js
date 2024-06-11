
/*
	import { remove_field } from '@/apps/fields/remove'	
	remove_field ({ the_coordinate: 1 })
*/

import { fields_element, fields } from '@/apps/fields/moves/variables'


export async function remove_field ({ 
	the_coordinate 
}) {	
	let field = ""
	
	let S = 0;
	while (S < fields.length) {
		if (the_coordinate === fields [S].the_coordinate) {
			field = fields [S]
			break;
		}
			
		S++;
	}
	
	if (typeof field === "string") {
		console.log (fields)
		throw new Error (`field WITH the_coordinate ${ the_coordinate } WAS NOT FOUND`)		
	}
	
	field.the_element.style.opacity = 0;
	
	await new Promise (R => {
		setTimeout (() => {
			R ()
		}, 300)
	})
	
	field.the_element.remove ()
	fields.splice (S, 1);
	
	console.log ({ fields })
}