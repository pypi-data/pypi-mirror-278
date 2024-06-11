

/*
 * 	This is "homestead" now?
 * /

/*
	terrain.width <= terrain.mobile_nav_width

*/

import { MAKE_DB } from '@/grid/DB'
import { rhythm_filter } from '@medical-district/rhythm-filter'

export let terrain_DB;

export const create_terrain_system = async function () {	
	const RF = rhythm_filter ({
		every: 200
	});

	terrain_DB = await MAKE_DB ({
		STORAGE: async function () {			
			return {
				/*
					put everything in size,
					because in "lounge",
					
					"terrain" = "terrain.SIZE"
				*/
				SIZE: {
					mobile_nav_width: 900,
					width: window.innerWidth,
					height: window.innerHeight
				}
			}
		},
		
		plays: {
			async RESIZE ({ CHANGE }) {					
				RF.attempt (({ ellipse, is_last }) => {
					CHANGE ('SIZE', {
						mobile_nav_width: 900,
						width: window.innerWidth,
						height: window.innerHeight
					})	
				});				
			}
		},
		
		AT: {
			async START ({ plays }) {				
				function WINDOW_SIZE_CHANGE (EVENT) {					
					plays.RESIZE ()
				}
				
				window.addEventListener ("resize", WINDOW_SIZE_CHANGE);	
			}
		}			
	})	
}

