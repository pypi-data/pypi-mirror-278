

import _get from 'lodash/get'
import { furnish_array } from 'procedures/furnish/array'

import { retrieve_supp } from '@/fleet/goodest_DB/supp/retrieve'

export const methods = {
	_get,
	furnish_array,
	
	async find () {
		console.log ('find supplement', this.$route);
		
		var { emblem } = this.$route.params;
		const { 
			status,
			parsed,
			proceeds
		} = await retrieve_supp ({ emblem })
		if (status !== 200) {
			console.error ("supplement was not found");
			
			this.found = false;
			this.show = true;
			return;
		}
	
		console.log ({ proceeds })
	
		this.treasure = proceeds.freight;	
		this.nature = proceeds.freight.nature;
		
		this.found = true;
		this.show = true;
	},
	
	change_terrain () {
		console.log ('decor_terrain changed', this.decor_terrain.width)
		
		try {
			if (this.decor_terrain.width >= 1000) {
				this.gt_1000 = true;
				return;
			}
		}
		catch (excepetion) {}
		
		this.gt_1000 = false;
	}
}