
/*
	import { find_nature_name } from '@/grid/nature/identity/name'
	find_nature_name (nature)
*/
export function find_nature_name (nature) {
	try {
		if (typeof nature ["identity"] ["name"] === 'string') {
			return nature ["identity"] ["name"]
		}
	}
	catch (exception) {
		console.warn (exception)
	}
	
	return ''
}