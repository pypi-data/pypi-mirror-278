



export function find_element_index (element, element_indexes) {
	const last_element_index = element_indexes.length - 1;
	
	for (let s = 0; s <= last_element_index; s++) {
		if (element_indexes [s] === element) {
			return s;
		}
	}
}