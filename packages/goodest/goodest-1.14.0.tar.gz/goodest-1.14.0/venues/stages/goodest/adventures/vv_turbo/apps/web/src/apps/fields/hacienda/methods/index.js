
import { inject, provide } from 'vue'

import { remove_field } from '@/apps/fields/remove'
import boundary from '@/apps/fields/boundary/embellishments.vue'

import { keypress } from './fn/keypress'

export const methods = {
	close_the_field () {		
		var coordinate = this.coordinate;
		
		remove_field ({
			the_coordinate: coordinate
		})
	},
	
	keypress,
		
	coordinates () {
		try {
			if (this.terrain.width <= 900) {
				const S1 = .05;
				const S2 = .05;
				
				const width = .90;
				const height = .90;
			
				return {
					top: window.innerHeight * S1 + 'px',
					left: window.innerWidth * S2 + 'px',
					
					height: window.innerHeight * height + 'px',
					width: window.innerWidth * width + 'px'
				}
			}
		}
		catch (exception) {
			console.error (exception)
		}
		
		const S1 = .125;
		const S2 = .125;
		
		const width = .75;
		const height = .75;
	
		return {
			top: window.innerHeight * S1 + 'px',
			left: window.innerWidth * S2 + 'px',
			
			height: window.innerHeight * height + 'px',
			width: window.innerWidth * width + 'px'
		}
	},
	
	find_outer_attributes () {
		const palette = this.palette;
		if (palette === undefined) {
			console.log ("palette is undefined")
			return;
		}
		
		const coordinates = this.coordinates ()
		
		return {
			position: 'absolute',
			
			...coordinates,
			
			color: palette [2],
			// borderRadius: '4px',
			
			boxShadow: '0 0 6px -2px ' + palette [4],
			// boxShadow:		'0 0 0px 12px ' + palette [1],
			
			transition: [
				'left .3s',
				'top .3s',
				'width .3s',
				'height .3s',
			
				'background ' + palette.change_duration,
				'color ' + palette.change_duration,
				'border ' + palette.change_duration,
				'box-shadow ' + palette.change_duration,
			].join (', '),

			display: 'flex',
			flexDirection: 'column'
		}
	},
	
	change_outer_attributes () {
		console.log ('change_outer_attributes')
		
		this.outer_attributes = this.find_outer_attributes ();
	}
}
