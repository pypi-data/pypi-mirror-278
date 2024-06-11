

import { search_treasures } from '@/fleet/goodest_DB/treasures/search'

import { round_quantity } from '@/grid/round_quantity'
import { furnish_string } from '@/grid/furnish/string'
import { is_kind } from '@/grid/struct_2/product/is'

import cloneDeep from 'lodash/cloneDeep'
import _get from 'lodash/get'

import { open_scan_filter_by } from '@/parcels/scan_filter_by/open'
import { open_scan_sort_by } from '@/parcels/scan_sort_by/open'
	

export const methods = {
	_get,
	furnish_string,
	round_quantity,
	is_kind,
	
	async input_changed ({
		search_string 
	}) {
		console.log ('the search string changed:', search_string)
		
		this.search_string = search_string;
		
		if (this.previous_search_string !== this.search_string) {
			this.next = false;
			this.prev = false;
		}
		else {
			this.next = false;
			this.prev = false;
			if (this.amount_after >= 1) {
				this.next = true;
			}
			if (this.amount_before >= 1) {
				this.prev = true;
			}
		}
	},
	
	async search_next () {
		console.log ("next", this.limits)

		this.before = false;
		this.after = this.limits.end;

		this.search ()
	},
	
	async search_prev () {
		this.before = this.limits.start;
		this.after = false;
		
		console.log ("prev")
		
		this.search ()
	},
	
	async search () {
		this.searching = true;
		this.next = false;
		
		let filters = {
			"string": this.search_string,
			"include": {
				"food": true,
				"supp": true,
				"meals": true
			},
			"limit": 25
		}
		if (this.before) {
			filters.before = this.before;
		}
		else if (this.after) {
			filters.after = this.after;
		}
		
		this.previous_search_string = this.search_string;
		
		try {
			const { 
				status,
				parsed,
				
				proceeds
			} = await search_treasures ({
				freight: {
					filters
				}
			});
			if (status === 200) { 
				const freight_proceeds = proceeds.freight;
				const stats = freight_proceeds.stats;
				
				this.treasures = freight_proceeds.treasures;
				
				this.limits = freight_proceeds.limits;
				
				this.amount_after = stats.amounts.after;
				this.amount_before = stats.amounts.before;				
				this.amount_found = stats.amounts.returned;				
				
								
				this.next = false;
				this.prev = false;
				if (this.amount_after >= 1) {
					this.next = true;
				}
				if (this.amount_before >= 1) {
					this.prev = true;
				}
				
				this.searching = false;	
				return;
			}
		}
		catch (exception) {
			console.error (exception)
		}
				
		this.treasures = []
		this.count = 0
		this.searching = false;			
		
		console.error ("The search could not be completed.")
	},
	
	async open_filter_by () {		
		await open_scan_filter_by ()
	},
	async open_sort_by () {		
		await open_scan_sort_by ()	
	},
	
	
	ENERGY_PER_G (FOOD) {
		try {
			let ENERGY_PER_G = this.round_quantity (FOOD ['ENERGY'][0] / _get (FOOD, ['PACKAGE MASS', 'G'], '?')) 
			return ENERGY_PER_G + " " + FOOD['ENERGY'][1] + " PER G"
		}
		catch (exception) {
			// console.warn (exception)
			console.warn ("COULDN'T FIND ENERGY PER GRAM")
		}
		
		return "? KCAL PER G"
	},
	
	FILTERED_NUTRIENTS (NUTRIENTS) {
		return;
		
		return NUTRIENTS.filter (N => {
			if (_get (N, 'UNREPORTED', false)) {
				return false;
			}
			
			return _get (N, ['FRACTION'], 0) > .01
		})
	}
}