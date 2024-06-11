


export function FIND_STATS_LINK (OPTION) {
	try {
		return '/@/FOOD/STATS/' + OPTION ['CODE']
	}
	catch (exception) {
		console.warn ("exception IN @/grid/food/FIND_STATS_LINK")
	}
	
	return ''
}