

/*
	IN PLACE SORT OF NUTRIENTS BY "PER PACKAGE"
*/

import RETURN from 'lodash/get'

function FIND_AMOUNT ({
	NUTRIENT,
	MEASUREMENT_SYSTEM
}) {
	const QUANTITY_PER_PACKAGE = RETURN (NUTRIENT, ["QUANTITY", MEASUREMENT_SYSTEM, "PER PACKAGE" ], []);
	let [ AMOUNT, UNIT ] = QUANTITY_PER_PACKAGE;
	AMOUNT = parseFloat (AMOUNT)
		
	if (UNIT === "IU") {
		return { AMOUNT, UNIT }
	}
	
	if (UNIT === "kg") {
		AMOUNT = AMOUNT * 1000;
	}
	if (UNIT === "mg") {
		AMOUNT = AMOUNT / 1000;
	}
	if (UNIT === "mcg") {
		AMOUNT = AMOUNT / 1000000;
	}
	
	return { AMOUNT, UNIT };
}

export function SORT_NUTRIENTS ({
	NUTRIENTS,
	MEASUREMENT_SYSTEM
}) {
	
	/*
		 1	->	
		-1 	->
	
		 0	-> NO CHANGE?
	*/
	NUTRIENTS.sort ((NUTRIENT_1, NUTRIENT_2) => {
		const { AMOUNT: AMOUNT_1, UNIT: UNIT_1 } = FIND_AMOUNT ({ 
			NUTRIENT: NUTRIENT_1,
			MEASUREMENT_SYSTEM
		})
		
		const { AMOUNT: AMOUNT_2, UNIT: UNIT_2 } = FIND_AMOUNT ({ 
			NUTRIENT: NUTRIENT_2,
			MEASUREMENT_SYSTEM
		})
		
		
		if (UNIT_1 === "IU") {
			if (UNIT_2 === "IU") {
				if (AMOUNT_1 === AMOUNT_2) {
					return 0;
				}	
				if (AMOUNT_1 < AMOUNT_2) {
					return 1;
				}
				
				// THEREFORE: AMOUNT_1 > AMOUNT_2
				return -1;
			}
			
			// THEREFORE: AMOUNT_1 < AMOUNT_2
			return 1;
		}
		if (UNIT_2 === "IU") {
			// THEREFORE: AMOUNT_1 > AMOUNT_2
			
			return -1;
		}
		
		if (AMOUNT_1 === AMOUNT_2) {
			return 0;
		}	
		if (AMOUNT_1 < AMOUNT_2) {
			return 1;
		}

		return -1;
	})
	
	
}