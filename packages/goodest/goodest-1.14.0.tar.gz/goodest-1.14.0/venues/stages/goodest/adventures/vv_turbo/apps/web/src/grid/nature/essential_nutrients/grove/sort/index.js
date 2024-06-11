



/*
	import { sort_grove } from '@/grid/nature/essential_nutrients/grove/sort'
	sort_grove (
		{ grove }, 
		by = "mass + mass equivalents",
		direction = "forward"
	)
*/

import { fraction_to_float } from '@/grid/Fraction/to_float'

import { mass_plus_mass_eq } from '@/grid/nature/essential_nutrients/grove/ingredient/mass_plus_mass_eq'
import { name_0 } from '@/grid/nature/essential_nutrients/grove/ingredient/name_0'
import { biological_activity } from '@/grid/nature/essential_nutrients/grove/ingredient/biological_activity'

export const sort_grove = function ({ 
	grove,
	by = "mass + mass equivalents",
	direction = "forward"
}) {
	if (!Array.isArray (grove)) {
		console.error ("The 'grove' is not an array.", grove)
		return;
	}
	
	if (direction === "backward") {
		var direction_1 = -1
		var direction_2 = 1
	}
	else {
		var direction_1 = 1
		var direction_2 = -1
	}
	
	/*
		move 1 forward = -1;
		move 2 forward = 1;
	*/
	grove.sort ((i1, i2) => {	
		if (by === "mass + mass equivalents") {
			var comparable_1 = mass_plus_mass_eq ({ ingredient: i1 })
			var comparable_2 = mass_plus_mass_eq ({ ingredient: i2 })
			
			var comparable_1_1 = biological_activity ({ ingredient: i1 })
			var comparable_2_1 = biological_activity ({ ingredient: i2 })
			
			var comparable_3 = name_0 ({ ingredient: i1 }).toLowerCase ()
			var comparable_4 = name_0 ({ ingredient: i2 }).toLowerCase ()
			
			if (comparable_1 === '' && comparable_2 === '') {
				/* console.log (
					comparable_3, 
					comparable_3 > comparable_4, 
					comparable_4
				) */
				
				/*
					next sort by biological activity
				*/
				if (comparable_1_1 === '') {
					return direction_1
				}
				if (comparable_2_1 === '') {
					return direction_2
				}
				if (comparable_1_1 > comparable_2_1) {
					return direction_1
				}
				if (comparable_1_1 < comparable_2_1) {
					return direction_2;
				}
				
				
				/*
					next sort by name
				*/
				if (comparable_3 === '') {
					return direction_1
				}
				if (comparable_4 === '') {
					return direction_2;
				}
				if (comparable_3 > comparable_4) {
					return direction_1
				}
				if (comparable_3 < comparable_4) {
					return direction_2;
				}
			}
			if (comparable_1 === '') {
				return direction_1
			}
			if (comparable_2 === '') {
				return direction_2;
			}			
			if (comparable_1 > comparable_2) {
				return direction_2;
			}
			else if (comparable_1 < comparable_2) {
				return direction_1;
			}
			
			return 0
		}
		else {
			// console.log ({ by })
			throw new Error ("The sorting by string is not accounted for.")
		}
		
		
		return 0
	})

	for (let s = 0; s < grove.length; s++) {
		try {
			const unites = grove [s] ['unites'];
			
			if (Array.isArray (unites) && unites.length >= 1) {
				sort_grove ({
					grove: unites,
					by
				})
			}
		}
		catch (exception) {
			console.error (exception)
		}
	}	
}












