
/*
	const coordinate = await get_next_coordinate () 
*/

let current_coordinate = 0;
export async function get_next_coordinate () {
	current_coordinate = current_coordinate + 1;
	return current_coordinate
}
