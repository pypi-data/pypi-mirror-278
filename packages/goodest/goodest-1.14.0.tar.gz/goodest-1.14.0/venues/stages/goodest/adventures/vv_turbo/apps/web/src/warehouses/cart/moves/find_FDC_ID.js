


/*
	const found = await cart_system.moves.find_FDC_ID ({
		emblem,
		FDC_ID,
		
		// if packages are included as a number,
		// then the package quantity is updated
		// if the product is found.
		packages: 11
	})
*/
export async function find_FDC_ID ({ 
	change, 
	warehouse 
}, { 
	emblem, 
	FDC_ID, 
	packages = null
}) {
	let cart = await warehouse ()
	const IDs = cart.IDs;
	
	const ID = parseInt (FDC_ID)
	
	for (let s = 0; s < IDs.length; s++) {
		if (IDs [s].emblem === emblem) {
			if (IDs [s].FDC_ID === ID) {							
				if (typeof packages === 'number') {
					IDs [s].packages = packages;
					await change ("IDs", cart.IDs)
				}
				
				return IDs [s]
			}						
		}					
	}			

	return false;
}