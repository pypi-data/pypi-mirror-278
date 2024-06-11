



import name_component from './components/name.vue'
import g_table from '@%/glamour/table/decor.vue'
// import { sort_as_floats } from '@%/glamour/table/decor.js'
import { markRaw, reactive, h, defineAsyncComponent } from 'vue';


export const decor = {
	components: {
		name_component,
		g_table
	},
	data () {
		return {
			columns: [{
				'place': '1',
				'name': 'name',
				
				styles: {
					th: {
						width: '200px'
					}
				},
				
				sorting: function ({ rows, place, direction }) {
					return rows.sort (function (r1, r2) {
						r1 = r1 [ place ]
						r2 = r2 [ place ]
						
						console.log ('sorting', r1, r2)
						
						function the_string (variable) {
							if (typeof variable === 'string') {
								return variable
							}
							
							return variable.props.name;
						}
						
						r1 = the_string (r1)
						r2 = the_string (r2)
						
						if (direction === 'backward') {
							return r1 < r2;
						}
						
						return r1 > r2;
					})
				}
			},{
				'place': '2',
				'name': 'mass + mass equivalents, in grams, per package',
				
				sorting: function () {}
			},{
				'place': '3',
				'name': 'percent of essential nutrient composition',
				sorting: function (r1, r2, direction) {
					function the_string (variable) {						
						return parseFloat (variable.split ('%') [0]);
					}
					
					r1 = the_string (r1)
					r2 = the_string (r2)
					
					if (direction === 'backward') {
						return r1 < r2;
					}
					
					return r1 > r2;
				}
			},{
				'place': '4',
				'name': 'Earth days of nutrients per package, based on the picked goal',
				sorting: function (r1, r2, direction) {
					function the_variable (variable) {	
						let the_float = 0
						try {
							the_float = parseFloat (variable);
							if (typeof the_float === 'number' && isNaN (the_float) === false) {
								return the_float;
							}
						}
						catch (exception) {}
						
						return 0						
					}
					
					r1 = the_variable (r1)
					r2 = the_variable (r2)
					
					console.log ({ r1, r2 })
					
					if (direction === 'backward') {
						return r1 < r2;
					}
					
					return r1 > r2;
				}
			}],
			
			rows: [{
				'1': 'protein',
				'2': '56.00280000000001',
				'3': '59.97243881625345%'
			},{
				'1': 'fats',
				'2': '21.9898',
				'3': '23.548499987172963%'
			},{
				'1': {
					component: markRaw (name_component),
					props: {
						name: 'carbohydrates'
					}
				},
				'2': '21.9898',
				'3': '23.548499987172963',
				'4': '10'
			},{
				'1': {
					component: markRaw (name_component),
					props: {
						name: 'dietary fiber',
						indent: 1
					}
				},
				'2': '12',
				'3': '13%'
			},{
				'1': {
					component: markRaw (name_component),
					props: {
						name: 'sugars, total',
						indent: 1
					}
				},
				'2': '124',
				'3': '10%'
			},{
				'1':  {
					component: markRaw (name_component),
					props: {
						name: 'added sugars',
						indent: 2
					}
				},
				'2': '14',
				'3': '10',
				'4': '8'
			}]
		}
	}
}
