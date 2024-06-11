
/*
	import { has_field } from '@/grid/object/has_field'
*/

export function has_field (obj, field) {
	if (Object.prototype.hasOwnProperty.call (obj, field)) {
		return true;
	}
	
	return false;
}