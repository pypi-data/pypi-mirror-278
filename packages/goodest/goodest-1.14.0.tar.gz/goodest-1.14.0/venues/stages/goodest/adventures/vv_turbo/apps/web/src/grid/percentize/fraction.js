

/*
	
*/


export function PERCENTIZE_FRACTION (FRACTION) {
	if (FRACTION === "?") {
		return ""
	}
	
	return this.round_quantity (parseFloat (FRACTION) * 100) + "%"
}