



export function focus_land_mark ({
	src_element,
	shift_pressed
}) {
	const find_element_index = this.find_element_index;
	
	
	
	const landmarks_selectors = 'nav, [role=navigation], [role=main], [role=region], [role=search]'
	
	const landmarks_unsorted = Array.from (
		document.querySelectorAll (landmarks_selectors)
	)

	const element_indexes = Array.from (document.all);
	const src_element_index = find_element_index (src_element, element_indexes)
	
	
	//
	//	presumably this sorts the landmarks by their order in the document
	//
	const landmarks = landmarks_unsorted.
	map (element => {
		return {
			element,
			index: find_element_index (element, element_indexes)
		}
	}).
	sort ((one, two) => {
		return one.index > two.index
	})
	

	if (shift_pressed === true) {
		const last_index = landmarks.length - 1;
		for (let s = last_index; s >= 0; s--) {
			const landmark = landmarks [s];
			
			if (landmark.index < src_element_index) {
				landmark.element.focus ()
				return;
			}				
		}
		
		//
		// if focus is before every landmarks,
		// then focus the last element.
		//
		landmarks [ last_index ].element.focus ()
	}
	else {
		const last_index = landmarks.length - 1;
		for (let s = 0; s <= last_index; s++) {
			const landmark = landmarks [s];
			
			if (landmark.index > src_element_index) {
				landmark.element.focus ()
				return;
			}				
		}
		
		//
		// if focus is after every landmarks,
		// then focus the first element.
		//
		landmarks [0].element.focus ()
	}
}
