
/*
	import { calc_linear_grove } from '@/grid/nature/essential_nutrients/grove/calc_linear_grove'
	linear_grove = calc_linear_grove ({ grove })
*/

import { sort_grove } from '@/grid/nature/essential_nutrients/grove/sort'
	
import cloneDeep from 'lodash/cloneDeep'
import _get from 'lodash/get'

function loop ({ 
	linear_ingredients, 
	
	grove, 
	indent 
}) {
	for (let s = 0; s <= grove.length - 1; s++) {
		const ingredient = grove [s]
		ingredient.indent = indent
				
		linear_ingredients.push (ingredient)
		const unites = ingredient ["unites"];
		
		if (
			Array.isArray (unites) &&
			unites.length >= 1
		) {
			loop ({ 
				linear_ingredients,
				
				grove: unites, 
				indent: (indent + 1) 
			})
		}
	}
}

export const calc_linear_grove = function ({ grove }) {			
	const linear_ingredients = []
	
	grove = cloneDeep (grove);
	// sort_grove ({ grove })
	
	loop ({ 
		linear_ingredients,
		grove, 
		indent: 0 
	})
	
	const last_index = linear_ingredients.length - 1;
	for (let s = 0; s <= last_index; s++) {
		delete linear_ingredients [s].unites;
	}
	
	return linear_ingredients
}