


/*
	import { sort_quantified_grove } from '@/grid/struct_2/product/quantified_grove/sort'
	sort_quantified_grove ({ quantified_grove })
*/


/*
	sorts by mass
*/
import { retrieve_mass } from '@/grid/struct_2/ingredient/mass'


/*
	not sure if this is true:
		> 0 -> [ 2, 1 ]
		< 0 -> [ 1, 2 ]
		0   -> no change 
*/



export const sort_quantified_grove = ({ quantified_grove }) => {
	// console.log ("sorting quantified grove", quantified_grove.length)
	
	if (!Array.isArray (quantified_grove)) {
		console.error ("The quantified grove is not an array.", quantified_grove)
		return;
	}
	
	quantified_grove.sort ((i1, i2) => {
		const mass_1 = retrieve_mass ({ ingredient: i1 })
		const mass_2 = retrieve_mass ({ ingredient: i2 })
		
		const mass_1_unit = mass_1 [1]
		const mass_2_unit = mass_2 [1]
		
		const mass_1_amount = mass_1 [0]
		const mass_2_amount = mass_2 [0]
		
		const move_1_forward = -1;
		const move_2_forward = 1;
		
		if (mass_1_unit === "g" && mass_2_unit === "g") {
			// console.log ('g & g', parseFloat (mass_1_amount), parseFloat (mass_2_amount))
			
			const mass_1_more = parseFloat (mass_1_amount) > parseFloat (mass_2_amount)
			const equal = parseFloat (mass_1_amount) === parseFloat (mass_2_amount)
		
			if (mass_1_more) {
				// move 1 forward
				return move_1_forward;
			}
			else if (equal) {
				return 0
			}
			else {
				// move 2 forward
				return move_2_forward
			}			
		}
		else if (mass_1_unit === "g" && mass_2_unit !== "g") {
			return move_1_forward;			
		}
		else if (mass_1_unit !== "g" && mass_2_unit === "g") {
			return move_2_forward;			
		}
		
		return 0
	})
	
	
	for (let s = 0; s < quantified_grove.length; s++) {
		try {
			if (Array.isArray (quantified_grove [s]['quantified grove'])) {
				sort_quantified_grove ({
					quantified_grove: quantified_grove [s]['quantified grove']
				})
			}
		}
		catch (exception) {
			console.error (exception)
		}
	}
}