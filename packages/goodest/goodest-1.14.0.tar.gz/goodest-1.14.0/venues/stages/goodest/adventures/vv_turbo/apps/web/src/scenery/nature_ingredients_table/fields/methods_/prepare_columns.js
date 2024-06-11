
import cloneDeep from 'lodash/cloneDeep'

import { build_grove } 			from '@/grid/nature/essential_nutrients/grove/sort/cryo/grove-1'
import { sort_grove } 			from '@/grid/nature/essential_nutrients/grove/sort'
import { calc_linear_grove } 	from '@/grid/nature/essential_nutrients/grove/calc_linear_grove'


import { mass_plus_mass_eq } from '@/grid/nature/essential_nutrients/grove/ingredient/mass_plus_mass_eq'
import { name_0 } from '@/grid/nature/essential_nutrients/grove/ingredient/name_0'
import { biological_activity } from '@/grid/nature/essential_nutrients/grove/ingredient/biological_activity'


import { round_quantity } 		from '@/grid/round_quantity'
import { fraction_to_float } 	from '@/grid/Fraction/to_float'
import { has_field } 	from '@/grid/object/has_field'

import { sort_as_floats } from '@%/glamour/table/sorting/as_float.js'

export function prepare_columns () {
	const retrieve_goal = this.goal;
	
	const names = [
		'names',
		'mass + mass equivalents, in grams, per package',
		'',
	]
	
	if (this.table_kind === "EN") {
		names [2] = "percent of essential nutrient composition"
		names [3] = 'Earth days of nutrients per package, based on the picked goal'
	}
	else if (this.table_kind == "CI") {
		names [2] = "percent of cautionary ingredients composition"		
	}
	
	var columns = [{
		'place': '1',
		'name': names [0],
		
		styles: {
			th: {
				width: '300px'
			}
		},
		
		sorting: ({ rows, place, direction }) => {
			const grove = cloneDeep (this.parsedGrove);
			
			console.log ({ grove })
			
			const sorted_grove = grove.sort (function (r1, r2) {
				r1 = name_0 ({ ingredient: r1 })
				r2 = name_0 ({ ingredient: r2 })
				
				function the_string (variable) {
					try {
						if (typeof variable === 'string') {
							return variable.toLowerCase ()
						}
						
						return variable.props.name.toLowerCase ();
					}
					catch (exception) {}
					
					return ''
				}
				
				r1 = the_string (r1)
				r2 = the_string (r2)
				
				const is_backwards = direction === 'backward'
				if (r2 > r1) {
					return is_backwards ? 1 : -1;
				}
				if (r1 > r2) {
					return is_backwards ? -1 : 1;
				}
				return 0;
			})
			
			return this.prepare_rows ({ 
				grove: sorted_grove
			});
		}
	},{
		'place': '2',
		'name': 'mass + mass equivalents, in grams, per package',
		sorting: ({ rows, place, direction }) => {
			const the_grove = cloneDeep (this.parsedGrove);
	
			console.log ({ the_grove })

		
			function the_variable (original_variable) {
				try {
					const the_float = mass_plus_mass_eq ({ 
						ingredient: original_variable
					})
					
					if (typeof the_float === 'number' && isNaN (the_float) === false) {
						return the_float;
					} 
				}
				catch (exception) {}
				
				return ''
			}
			
			const sorted_grove = the_grove.sort (function (r1, r2) {				
				r1 = the_variable (r1)
				r2 = the_variable (r2)
				// console.log ('sort', r1, r2)
				
				if (direction === 'backward') {
					if (r1 === '') {
						return 1
					}
					if (r2 === '') {
						return -1;
					}			
					
					if (r1 > r2) {
						return 1;
					}
					if (r1 < r2) {
						return -1;
					}
					
					return 0
				}
				
			
				if (r1 === '') {
					return 1
				}
				if (r2 === '') {
					return -1;
				}			
				if (r1 > r2) {
					return -1;
				}
				if (r1 < r2) {
					return 1;
				}
				
				return 0		
			})
			
			return this.prepare_rows ({ 
				grove: sorted_grove
			});
		}	
	},{
		'place': '3',
		'name': names [2],
		sorting: ({ rows, place, direction }) => {
			const the_grove = cloneDeep (this.parsedGrove);
			
			function the_variable (original_variable) {
				try {
					const the_float = mass_plus_mass_eq ({ 
						ingredient: original_variable
					})
					
					if (typeof the_float === 'number' && isNaN (the_float) === false) {
						return the_float;
					} 
				}
				catch (exception) {}
				
				return ''
			}
			
			const sorted_grove = the_grove.sort (function (r1, r2) {				
				r1 = the_variable (r1)
				r2 = the_variable (r2)
				// console.log ('sort', r1, r2)
				
				
				if (direction === 'backward') {
					if (r1 === '') {
						return 1
					}
					if (r2 === '') {
						return -1;
					}			
					
					if (r1 > r2) {
						return 1;
					}
					if (r1 < r2) {
						return -1;
					}
					
					return 0
				}
				
			
				if (r1 === '') {
					return 1
				}
				if (r2 === '') {
					return -1;
				}			
				if (r1 > r2) {
					return -1;
				}
				if (r1 < r2) {
					return 1;
				}
				
				return 0;		
			})
			
			return this.prepare_rows ({ 
				grove: sorted_grove
			});
		}
	}]
	
	if (this.table_kind === "EN") {
		columns.push ({
			'place': '4',
			'name': names [3],
			sorting: ({ rows, place, direction }) => {
				const the_grove = cloneDeep (this.parsedGrove);
				
				function the_variable (original_variable) {
					try {
						const the_float = parseFloat (retrieve_goal (original_variable))
						if (typeof the_float === 'number' && isNaN (the_float) === false) {
							return the_float;
						} 
					}
					catch (exception) {}
					
					return ''
				}
				
				const sorted_grove = the_grove.sort (function (r1, r2) {				
					r1 = the_variable (r1)
					r2 = the_variable (r2)
					
					if (direction === 'backward') {
						if (r1 === '') {
							return 1
						}
						if (r2 === '') {
							return -1;
						}			
						if (r1 > r2) {
							return 1;
						}
						if (r1 < r2) {
							return -1;
						}
						
						return 0
					}
					
				
					if (r1 === '') {
						return 1
					}
					if (r2 === '') {
						return -1;
					}			
					if (r1 > r2) {
						return -1;
					}
					else if (r1 < r2) {
						return 1;
					}
					
					return 0		
				})
				
				return this.prepare_rows ({ 
					grove: sorted_grove
				});
			}
		})
	}
	
	return columns;
}