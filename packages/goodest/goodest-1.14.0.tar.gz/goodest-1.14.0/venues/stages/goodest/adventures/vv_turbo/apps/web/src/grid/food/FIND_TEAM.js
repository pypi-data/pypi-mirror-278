


export function FIND_TEAM (FOOD) {
	try {
		if (typeof FOOD ["TEAM"]["NAME"] === 'string') {
			return FOOD ["TEAM"]["NAME"]
		}
	}
	catch (exception) {
		console.warn ("exception IN @/grid/food/FIND_TEAM")
	}
	
	return ''
}