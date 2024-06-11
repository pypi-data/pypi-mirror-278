


/*
	https://www.brailleauthority.org/ueb/symbols_list.pdf
*/

import { has_field } from '@/grid/object/has_field'




export const keydown = function (event) {
	// console.log ('keydown', keydown)
	
	const key_code = event.keyCode;
	
	// modifiers
	const control = event.ctrlKey;
	const meta = event.metaKey;
	const alt = event.altKey;
	const shift_pressed = event.shiftKey;
	
	// ?
	const src_element = event.srcElement;
	const target = event.target;
	
	
	
	
	/*
		https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles#3._landmark_roles
		https://developer.mozilla.org/en-US/docs/Web/API/Element/closest
	*/
	const buttons = {
		// l button
		76: () => {
			this.focus_land_mark ({
				src_element,
				shift_pressed
			})
		},
		
		// tab button
		9: function () {
			if (shift_pressed === true) {
				// console.log ('tab button with shift')
			}
			else {
				// console.log ('tab button without shift')
			}
		}
	}
	
	if (has_field (buttons, key_code)) {
		buttons [ key_code ] ()
	}
}