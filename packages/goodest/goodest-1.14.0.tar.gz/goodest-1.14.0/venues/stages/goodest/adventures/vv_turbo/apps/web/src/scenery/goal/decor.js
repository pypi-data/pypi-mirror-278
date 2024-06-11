
import { furnish_string } from 'procedures/furnish/string'
import { furnish_array } from 'procedures/furnish/array'
import { furnish_dict } from 'procedures/furnish/dict'

import { open_goal } from '@/parcels/goal/open.js'
import s_curtain from '@/scenery/curtain/decor.vue'

import { defineComponent, h, markRaw } from 'vue';
import goal_amount from './components/goal_amount.vue'
import table_row from './components/table_row.vue'


import g_table from '@%/glamour/table/decor.vue'

import pie_chart from '@/scenery/charts/pie/veranda.vue'
	
import { sort_as_strings } from '@%/glamour/table/sorting/as_string.js'

import { round_quantity } from '@/grid/round_quantity'
	

export const decor = {
	components: { s_curtain, g_table, pie_chart },
	props: {
		goal: Object,
		show_goal: {
			type: Boolean,
			default: false
		},
		pick: {
			default () {}
		},
		show_pick: {
			type: Boolean,
			default: false
		}
	},
	
	data () {
		return {
			condensed: false,
			
			rows: [],
			columns: [],
			
			cake_wedges: [],
			
			mass_plus_mass_eq_sum: "? grams",
			// food_calories_sum: "? food calories",
			
		}
	},
	
	mounted () {
		this.build_columns ();
		this.build_rows ();
		this.build_cake_wedges ()
		this.build_mass_plus_mass_eq_sum ()
	},
	
	methods: {	
		calc_condensed () {
			try {
				const layout = this.$refs.layout;
				const { width } = layout.getBoundingClientRect ()
				if (width <= 1200) {
					this.condensed = true
				}
				else {
					this.condensed = false;
				}
			}
			catch (exception) {
				console.warn ("condensed calculation exception:", exception)
			}
		},
		
		find_goal_mass_percent ({ ingredient }) {
			console.log ({ ingredient }, ingredient.goal ["mass + mass equivalents"])
			
			let percent = 0;
			try {
				percent = parseFloat (
					ingredient.goal [
						"mass + mass equivalents"
					] ["per Earth day"] ["portion"] ["percent string"]
				)
			}
			catch (exception) {
				console.warn (exception)
			}
			
			return percent;			
		},
		
		find_goal_mass_percent_rounded ({ ingredient }) {
			const percent = round_quantity (this.find_goal_mass_percent ({ ingredient }))

			return percent
		},
		

		build_mass_plus_mass_eq_sum () {
			let amount = "? grams"
			
			const goal = furnish_dict (this.goal, [ 'nature' ], {})
			
			console.log ({ goal: this.goal })
			
			try {
				amount = goal ["statistics"] ['sum'] [
					"mass + mass equivalents"
				] ["per Earth day"] ["grams"] ["decimal string"] + " grams"
			}
			catch (exception) {
				console.warn (exception)
			}
			
			this.mass_plus_mass_eq_sum = amount;
		},
		
		build_cake_wedges () {
			const goal = this.goal;
			
			const ingredients = furnish_array (goal, [ 'nature', 'ingredients'], [])
			
			const wedges = []
			for (let S = 0; S < ingredients.length; S++) {
				const ingredient = ingredients [S]
				
				const percent = this.find_goal_mass_percent ({ ingredient })
				
				console.log ("percent:", percent)
				
				wedges.push ({
					'label': ingredient ["labels"] [0],
					'data': percent
				})
			}
			
			console.log ({ wedges })
			
			this.$refs.mass_pie_chart.show_v2 ({
				wedges
			})
		},
		
		furnish_string,
		furnish_array,
		
		pick_goal () {
			this.pick ({ goal: this.goal })
		},
		
		find_includes () {
			try {
				return this.goal.nature.label;
			}
			catch (exception) {
				
			}
			
			return {}
		},
		
		build_columns () {
			var columns = [{
				'place': '1',
				'name': 'name',
				styles: {
					th: {
						width: '200px'
					}
				},
				sorting: sort_as_strings
			},{
				'place': '2',
				'name': 'Goal per Earth Day',
				
				sorting: function ({ rows, place, direction }) {
					return rows.sort (function (r1, r2) {
						
						console.log ({ direction })
						
						r1 = r1 [ place ]
						r2 = r2 [ place ]
						
						const r1_grams = r1.props.grams;
						const r1_food_calories = r1.props.food_calories;

						const r2_grams = r2.props.grams;
						const r2_food_calories = r2.props.food_calories;

						if (typeof r2_food_calories === 'string' && r2_food_calories.length >= 1) {
							console.log ('r2_food_calories')
							return direction === 'backward' ? -1 : 1;
						}
						if (typeof r1_food_calories === 'string' && r1_food_calories.length >= 1) {
							console.log ('r1_food_calories')
							return direction === 'backward' ? 1 : -1;
						}
							
						if (typeof r1_grams === 'string' && r1_grams.length >= 1) {
							if (typeof r2_grams === 'string' && r1_grams.length >= 1) {
								const r1_grams_float = parseFloat (r1_grams)
								const r2_grams_float = parseFloat (r2_grams)
								
								if (r2_grams_float > r1_grams_float) {
									return direction === 'backward' ? -1 : 1;
								}
								
								return direction === 'backward' ? 1 : -1;							
							}
						}

						return 0;
					})
				}
			},{
				'place': '3',
				'name': 'Goal per Earth Day, % of mass',
				
				sorting: function ({ rows, place, direction }) {
					return rows.sort (function (r1, r2) {

						try {
							r1 = parseFloat (r1 [ place ].props.amount)
							r2 = parseFloat (r2 [ place ].props.amount)
							
							console.log ({ r1, r2 })
									
							if (r2 > r1) {
								return direction === 'backward' ? -1 : 1;
							}
							
							return direction === 'backward' ? 1 : -1;							

							return 0;
						}
						catch (exception) {
							console.info (exception)
						}
						
						return 0
					})
				}
			}]
			
			this.columns = columns;
		},
		build_rows () {
			const goal = this.goal;
			const ingredients = furnish_array (goal, [ 'nature', 'ingredients'], [])
			
			const rows = []
			for (let S = 0; S < ingredients.length; S++) {
				const ingredient = ingredients [S]
				
				rows.push ({
					'1': ingredient ["labels"] [0],
					'2': {
						component: markRaw (goal_amount),
						props: this.find_goal_amounts ({ ingredient })
					},
					'3': {
						component: markRaw (table_row),
						props: {
							amount: this.find_goal_mass_percent_rounded ({ ingredient })
						}
					},
				})
			}
			
			this.rows = rows;
		},
		
		find_goal_amounts ({ ingredient }) {
			let grams = ""
			let food_calories =""
			
			const exceptions = []
			
			try {
				grams = ingredient.goal [
					"mass + mass equivalents"
				] ["per Earth day"] ["grams"] ["decimal string"]
			}
			catch (exception) {
				exceptions.push (exception)
			}
			
			try {
				food_calories = ingredient.goal [
					"energy"
				] ["per Earth day"] ["food calories"] ["decimal string"]
			}
			catch (exception) {
				exceptions.push (exception)
			}
			
			console.error ({
				ingredient,
				exceptions
			})
			
			return {
				grams,
				food_calories
			}
		},
		
		find_goal_amount ({ ingredient }) {
			const exceptions = []
			
			try {
				const grams = ingredient.goal [
					"mass + mass equivalents"
				] ["per Earth day"] ["grams"] ["decimal string"]
				
				return h (goal_amount, { 
					grams
				})
			}
			catch (exception) {
				exceptions.push (exception)
			}
			
			try {
				return h (goal_amount, { 
					food_calories: ingredient.goal [
						"energy"
					] ["per Earth day"] ["food calories"] ["decimal string"]
				})
			}
			catch (exception) {
				exceptions.push (exception)
			}
			
			console.error ({
				ingredient,
				exceptions
			})
			
			return h (goal_amount, { food_calories: ingredient })
		},
		
		find_goal () {
			
			try {
				return this.goal.nature.label;
			}
			catch (exception) {
				
			}
			
			return {}
		},
		
		find_label () { 
			try {
				return this.goal.nature.label;
			}
			catch (exception) {
				
			}
			
			return ''
		}
	}
}




/**/