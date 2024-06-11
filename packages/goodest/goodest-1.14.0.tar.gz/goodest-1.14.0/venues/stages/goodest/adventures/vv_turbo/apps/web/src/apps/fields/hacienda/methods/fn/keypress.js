
import { remove_field } from '@/apps/fields/remove'
import boundary from '@/apps/fields/boundary/embellishments.vue'
import { inject, provide } from 'vue'

export const keypress = function (event) {
	const control = event.ctrlKey;
	const meta = event.metaKey;
	const alt = event.altKey;
	const shift = event.shiftKey;
	
	const code = event.keyCode;
	
	const source_element = event.srcElement;
	const target = event.target;
			
	const forward_tab = shift === false && code === 9;
	const back_tab = shift === true && code === 9;

	// console.log (event)
	console.log ({ 
		event,
		
		source_element,
		target,
		
		control, 
		meta, 
		alt, 
		code, 
		shift 
	})
	
	const hacienda_element = this.$refs.hacienda_platform;
	const field_close_button = this.$refs.boundary.$refs.field_close_button.$refs.button;
	
	// console.log ({ forward_tab, back_tab, target, field_close_button }, target == field_close_button)
	
	/*
		
	*/
	if (forward_tab && target == field_close_button) {				
		event.preventDefault ()
		event.stopPropagation ()
		
		hacienda_element.focus ()
	}
	else if (back_tab && target == hacienda_element) {				
		event.preventDefault ()
		event.stopPropagation ()
		
		field_close_button.focus ()
	}
}