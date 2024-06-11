


/*
	await cart_system.moves.remove ({
		emblem, 
		DSLD_ID = null,
		FDC_ID = null
	})
*/
export async function remove ({ 
	change, 
	warehouse 
}, {
	emblem, 
	DSLD_ID = null,
	FDC_ID = null
}) {
	let cart = await warehouse ()
	let treasures = cart.treasures;
	let IDs = cart.IDs;
	
	let ID = null;
	let ID_field = null;
	let treasure_ID_field = null;
	if (typeof (DSLD_ID) == "number") {
		ID = parseInt (DSLD_ID)
		ID_field = "DSLD_ID"
		treasure_ID_field = "DSLD ID"
	}
	else if (typeof (FDC_ID) == "number") {
		ID = parseInt (FDC_ID)
		ID_field = "FDC_ID"
		treasure_ID_field = "FDC ID"
	}
	else {
		console.error ("Neither ID sent was a number.", { DSLD_ID, FDC_ID })
		return;
	}
	
	for (let s = 0; s < IDs.length; s++) {
		console.log ('ID', IDs [s].emblem, IDs [s] [ID_field])
		
		if (IDs [s].emblem === emblem) {
			if (IDs [s] [ID_field] === ID) {
				console.log ('splicing IDs')
				
				IDs.splice (s, 1)
			}
		}
	}
	
	for (let s = 0; s < treasures.length; s++) {
		console.log (
			'treasures', 
			treasures [s].emblem, 
			treasures [s] ["nature"] ["identity"] [treasure_ID_field]
		)
		
		if (treasures [s].emblem === emblem) {
			if (parseInt (treasures [s] ["nature"] ["identity"] [treasure_ID_field]) === ID) {
				treasures.splice (s, 1)
			}
		}
	}
	
	console.log ('after remove', IDs, treasures)
	
	await change ("IDs",IDs)		
	await change ("treasures", treasures)
}