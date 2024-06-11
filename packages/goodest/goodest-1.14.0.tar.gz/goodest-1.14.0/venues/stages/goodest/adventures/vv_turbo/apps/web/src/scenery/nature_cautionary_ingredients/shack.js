
import { round_quantity } from '@/grid/round_quantity'
import { furnish_string } from '@/grid/furnish/string'
import { fraction_to_float } from '@/grid/Fraction/to_float'
import { has_field } from '@/grid/object/has_field'

import { open_cautionary_ingredients_novel } from '@/parcels/cautionary_ingredients/open.js'
	

import nature_ingredients_table from '@/scenery/nature_ingredients_table/fountains.vue'

import cloneDeep from 'lodash/cloneDeep'
import _get from 'lodash/get'

import book from '@/scenery/icons/book/field.vue'
	

export const shack = {
	props: [ "land" ],
	
	components: {
		nature_ingredients_table,
		book
	},
	
	data () {
		return {
			component_opacity: 0,
			condensed: false,
			scanned_for: []
		}
	},
	watch: {
		land () {
			// this.show_pie ()
		}
	},
	methods: {
		_get,
				
		async show_info () {
			const land = this.land;
			
			await open_cautionary_ingredients_novel ({
				properties: {
					scanned_for: this.scanned_for,
					grove: _get (land, 'grove', '')
				}
			})
		},
		
		
		/*
			trans fat, fatty acids, total trans
		*/
		has_cautionary_ingredients () {
			const land = this.land;
			const grove = _get (land, 'grove', '');
			
			const scanned_for = []
			
			let mass_plus_mass_eq = 0;
			let natures = 0;
			for (let S = 0; S < grove.length; S++) {
				const ingredient = grove [S]
				mass_plus_mass_eq += this.retrieve_mass_plus_mass_eq_parsed ({
					measures: ingredient ["measures"]
				})
				
				natures += ingredient.natures.length;
				
				scanned_for.push (ingredient.info.names)
			}
			
			console.log ({ natures })
			
			this.scanned_for = scanned_for;
			
			if (natures == 0 || mass_plus_mass_eq == 0) {
				return 'no'
			}		
			
			return 'yes'
		},
		
		retrieve_mass_plus_mass_eq_parsed ({
			measures
		}) {
			try {
				return parseFloat (
					measures ['mass + mass equivalents'] ['per recipe'] ['grams'] ['scinote string']
				)
			}
			catch (ex) {}
			
			return 0
		},

		energy_parsed () {
			try {
				return fraction_to_float (
					this.land ["measures"] ['energy'] ['per recipe'] ['food calories'] ['fraction string']
				)
			}
			catch (ex) {}
			
			return ''
		},
		mass_plus_mass_eq_parsed () {
			try {
				return fraction_to_float (
					this.land ["measures"] ['mass + mass equivalents'] ['per recipe'] ['grams'] ['fraction string']
				)
			}
			catch (ex) {}
			
			return ''
		},
		calc_condensed () {
			const layout = this.$refs.layout;
			const { width } = layout.getBoundingClientRect ()
			if (width <= 800) {
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
			this.calc_condensed ()
		});

		this.calc_condensed ()
		this.component_opacity = 1;
		this.RO.observe (layout);
	},
	
	beforeUnmount () {
		const layout = this.$refs.layout;
		this.RO.unobserve (layout)
	}
}