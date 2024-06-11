

/*
	await cart_system.moves.change_quantity ({
		treasure: {
			emblem: 10,
			nature: {
				identity: {
					'FDC ID': 
				}
			}
		},
		packages: 10
	})
*/	

import { cart_system } from '@/warehouses/cart'	

import _get from 'lodash/get'

export async function change_quantity (
	{ change, warehouse }, 
	{ treasure, packages }
) {
	let cart = await warehouse ()

	const emblem = _get (treasure, [ 'emblem' ], '')
	const identity = _get (treasure, [ 'nature', 'identity' ], '');		
	const kind = _get (treasure, [ 'nature', 'kind' ], '');		
						
	if (kind == "food") {
		const FDC_ID = parseInt (identity [ 'FDC ID' ]);
		
		if (packages == 0) {
			await cart_system.moves.remove ({
				emblem, 
				FDC_ID
			})
			return;
		}
		
		const found = await cart_system.moves.find_FDC_ID ({
			emblem,
			FDC_ID,
			packages
		})
		if (found) {
			return
		}

		cart.treasures.push (treasure)					
		cart.IDs.push ({
			kind: "food",
			
			emblem,
			FDC_ID,
			packages
		})
	}				
	else if (kind == "supp") {
		const DSLD_ID = parseInt (identity [ 'DSLD ID' ]);
	
		if (packages == 0) {
			await cart_system.moves.remove ({
				emblem, 
				DSLD_ID
			})
			return;
		}
	
		const found = await cart_system.moves.find_DSLD_ID ({
			emblem,
			DSLD_ID,
			packages
		})
		if (found) {
			console.log ({ found })
			return
		}
		
		cart.treasures.push (treasure)
		cart.IDs.push ({
			kind: "supp",
			
			emblem,
			DSLD_ID,
			packages
		})
	}
	else {
		console.error ('A "FDC ID" or a "DSLD ID" was not found.')
	}

	await change ("IDs", cart.IDs)		
	await change ("treasures", cart.treasures)						
}

