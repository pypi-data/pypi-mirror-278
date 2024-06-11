


import { retrieve_food } from '@/fleet/goodest_DB/food/retrieve'


import _get from 'lodash/get'
import { furnish_array } from 'procedures/furnish/array'

export const methods = {
	_get,
	furnish_array,
	
	async find () {
		console.log ('retrieve food', this.$route);
		
		var { emblem } = this.$route.params;
		const { proceeds, status } = await retrieve_food ({ 
			emblem
		})
		if (status !== 200) {
			console.error ("The food was not found.");
			
			this.found = false;
			this.show = true;
			return;
		}
				
		console.log ({ proceeds })
			
		this.treasure = proceeds.freight;
		this.product = proceeds.freight.nature;
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