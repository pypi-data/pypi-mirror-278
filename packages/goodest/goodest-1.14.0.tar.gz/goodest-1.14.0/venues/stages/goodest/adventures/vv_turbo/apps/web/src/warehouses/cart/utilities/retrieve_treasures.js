

import { has_field } from '@/grid/object/has_field'

export const heal_IDs = function (IDs) {	
	if (!Array.isArray (IDs)) {
		IDs = []
	}
	for (let s = 0; s < IDs.length; s++) {
		const id = IDs [s]
		
		if (!has_field (id, "emblem")) { 
			IDs [s].splice (s, 1)
			continue;
		}
		if (!has_field (id, "DSLD_ID") && !has_field (id, "FDC_ID")) { 
			IDs [s].splice (s, 1)
			continue;
		}
		if (!has_field (id, "packages")) {
			IDs [s].packages = 0
		} 
	}
	
	return IDs
}

export const retrieve_treasures = function () {
	let IDs = []
	try {
		const LS = localStorage.getItem ('IDs')
		IDs = heal_IDs (JSON.parse (LS))
	}
	catch (exception) {
		console.error (exception)
	}
	if (!Array.isArray (IDs)) {
		IDs = []
	}


	let treasures = []
	try {
		treasures = JSON.parse (localStorage.getItem ('treasures'))
		console.log ({ treasures })
	}
	catch (exception) {
		console.error (exception)
	}
	if (!Array.isArray (treasures)) {
		treasures = []
	}


	return { IDs, treasures };
}