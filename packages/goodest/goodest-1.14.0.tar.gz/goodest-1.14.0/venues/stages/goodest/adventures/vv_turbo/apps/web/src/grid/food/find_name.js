


export function find_name (food) {
	try {
		if (typeof food ["product"] ["name"] === 'string') {
			return food ["product"] ["name"]
		}
	}
	catch (exception) {
		console.warn (exception)
	}
	
	return ''
}