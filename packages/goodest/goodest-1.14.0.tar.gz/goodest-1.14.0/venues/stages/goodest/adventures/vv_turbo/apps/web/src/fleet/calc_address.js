
/*
	import { calc_address } from '@/fleet/calc_address'
	address = calc_address ()
*/

export function calc_address () {
	const node_address = localStorage.getItem ("node address")
	if (typeof node_address === "string" && node_address.length >= 1) {
		return node_address
	}

	return "/"
}