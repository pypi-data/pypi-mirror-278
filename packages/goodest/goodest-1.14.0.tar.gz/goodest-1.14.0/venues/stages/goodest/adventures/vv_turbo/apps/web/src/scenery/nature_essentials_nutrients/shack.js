
/*
	import essential_nutrients from '@/scenery/nature_essentials_nutrients/shack.vue'
*/


import { round_quantity } from '@/grid/round_quantity'
import { furnish_string } from '@/grid/furnish/string'
import { fraction_to_float } from '@/grid/Fraction/to_float'
import { has_field } from '@/grid/object/has_field'

import nature_ingredients_table from '@/scenery/nature_ingredients_table/fountains.vue'

import pie_chart from '@/scenery/charts/pie/veranda.vue'
import s_select from '@/scenery/select/decor.vue'
import cloneDeep from 'lodash/cloneDeep'

import s_outer_link from '@/scenery/link/outer/decor.vue'

import { open_essential_nutrients_novel } from '@/parcels/essential_nutrients/open.js'
	
import book from '@/scenery/icons/book/field.vue'


export const shack = {
	components: {
		book,
		s_outer_link,
		s_select,
		nature_ingredients_table,
		pie_chart
	},
	props: [ "EN" ],
	data () {
		return {
			component_opacity: 0,
			condensed: false
		}
	},
	watch: {
		EN () {
			this.show_pie ()
		}
	},
	methods: {
		show_pie_without_macros () {
			const land = cloneDeep (this.EN);
			
			land.grove = land.grove.filter (ingredient => {
				const filter = [ 
					"protein",
					"carbohydrates",
					"fats"
				].includes (
					ingredient ['info'] ['names'] [0]
				)
				
				// console.log ({ filter })
				
				if (filter) {
					return false;
				}
				
				return true;
			})		
			
			this.$refs.pie_without_macros.show ({
				land
			})
		},
		
		async show_info () {
			await open_essential_nutrients_novel ({})
			
		},
		
		show_pie () {
			console.log ('show_pie', has_field (this.EN, "grove"))
			
			if (has_field (this.EN, "grove")) {				
				this.$refs.pie_every.show ({
					land: cloneDeep (this.EN)
				})
				
				// this.show_pie_without_macros ()
			}
		},
		energy_parsed () {
			try {
				return fraction_to_float (
					this.EN ["measures"] ['energy'] ['per recipe'] ['food calories'] ['fraction string']
				)
			}
			catch (ex) {}
			
			return ''
		},
		mass_plus_mass_eq_parsed () {
			try {
				return fraction_to_float (
					this.EN ["measures"] ['mass + mass equivalents'] ['per recipe'] ['grams'] ['fraction string']
				)
			}
			catch (ex) {}
			
			return ''
		},
		calc_condensed () {
			const layout = this.$refs.layout;
			const { width } = layout.getBoundingClientRect ()
			if (width <= 1200) {
				this.condensed = true
			}
			else {
				this.condensed = false;
			}
			
			
			
			// console.log ('this.condensed:', this.condensed)
		}
	},
	async mounted () {
		const layout = this.$refs.layout;
		this.RO = new ResizeObserver ((entries, observer) => {
			// console.log ('ResizeObserver:', entries)
			
			this.calc_condensed ()
			
			/*
			for (const entry of entries) {
				const {left, top, width, height} = entry.contentRect;

				console.log('Element:', entry.target);
				console.log(`Element's size: ${ width }px x ${ height }px`);
				console.log(`Element's paddings: ${ top }px ; ${ left }px`);
			}
			*/
		});


		this.calc_condensed ()

		this.show_pie ()
		
		this.component_opacity = 1;

		this.RO.observe (layout);
	},
	
	beforeUnmount () {
		const layout = this.$refs.layout;
		this.RO.unobserve (layout)
	}
}