


/*
	const found = await cart_system.moves.find_DSLD_ID ({
		emblem: 
		DSLD_ID:
		
		// if packages are included as a number,
		// then the package quantity is updated
		// if the product is found.
		packages: 11
	})
*/
export async function find_DSLD_ID ({ 
	change, 
	warehouse 
}, {
	emblem, 
	DSLD_ID,
	packages = null
}) {
	let cart = await warehouse ()
	const IDs = cart.IDs;
	
	const ID = parseInt (DSLD_ID)

	for (let s = 0; s < IDs.length; s++) {
		if (IDs [s].emblem === emblem) {
			if (IDs [s].DSLD_ID === ID) {
				if (typeof packages === 'number') {								
					IDs [s].packages = packages;
					await change ("IDs", cart.IDs)
				}
				
				return IDs [s]
			}						
		}					
	}
	
	return false
}
