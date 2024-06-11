
/*
	import { lap } from '@/fleet/ask/get'
	const { 
		status,
		parsed,
		proceeds
	} = await lap ({
		path: "guets/foods/find_emblem/" + emblem
	});
	if (status !== 200) { 
		
	}
*/



import { assert_equal } from '@/grid/assert/equal'
import { has_field } from '@/grid/object/has_field'


// var address = "https://127.0.0.1"
// var address = "https://0.0.0.0"
/*
	localStorage.setItem ("node address", "https://ruggedgoodest.com")
	localStorage.setItem ("node address", "http://127.0.0.1:48938")
	localStorage.setItem ("node address", "https://0.0.0.0")
*/
function calc_address () {
	const node_address = localStorage.getItem ("node address")
	if (typeof node_address === "string" && node_address.length >= 1) {
		return node_address
	}

	return "/"
}


var address = calc_address ()


export const lap = async function ({
	envelope = {}
} = {}) {
	assert_equal (has_field (envelope, "label"), true)
	assert_equal (has_field (envelope, "freight"), true)

	address += path

	

	const proceeds = await fetch (address, {
		"GET"
	});
	
	try {
		const proceeds_JSON = await proceeds.json ();	
		return {			
			status: proceeds.status,
			parsed: "yes",			
			proceeds: proceeds_JSON
		}
	}
	catch (exception) {
		console.error (exception)		
	}
	
	
	return {
		status: proceeds.status,
		parsed: "no" 
	}
}


