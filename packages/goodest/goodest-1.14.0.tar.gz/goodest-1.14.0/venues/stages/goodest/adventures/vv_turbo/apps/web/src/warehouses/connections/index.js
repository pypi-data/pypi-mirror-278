


/*
	server address
*/

/*
	import { connections_store } from '@/warehouses/connections'
	connections_store.warehouse ("server") ["address"]
*/


import { make_store } from 'mercantile'
export let physics_system;

export const create_physics_system = async function () {
	physics_system = await make_store ({
		warehouse: async function () {				
			return {
				layout: {
					lines: "3px"
				},
				server: {
					address: "http://127.0.0.1:48938",
				}
			}
		},
		moves: {
			/*
				const harbor_address = await connections_store.moves.retrieve_harbor_address ()
			*/
			async retrieve_harbor_address ({ change, warehouse }) {
				const harbor_address = localStorage.getItem ("harbor_address")
				if (typeof harbor_address === "string" && harbor_address.length >= 1) {
					return harbor_address
				}
				
				return "/"
			},
		},
		once_at: {
			async start () {}
		}			
	})
	
	return physics_system
}