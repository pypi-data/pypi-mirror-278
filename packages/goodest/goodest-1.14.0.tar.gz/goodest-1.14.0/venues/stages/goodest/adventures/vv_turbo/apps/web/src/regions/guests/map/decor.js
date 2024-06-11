
/*
	ADDING POINTS:
		https://openlayers.org/en/latest/examples/draw-features-style.html

	OTHER STUFF:
		https://openlayers.org/en/latest/examples/feature-animation.html
		https://openlayers.org/en/latest/examples/heatmap-earthquakes.html
*/



import Map 				from 'ol/Map.js';
import OSM 				from 'ol/source/OSM.js';
import TileLayer 		from 'ol/layer/Tile.js';
import View 			from 'ol/View.js';

import { persist } 		from '@/grid/persist'

const TWO_TONE = false

export default {
	data () {
		return {
			OPACITY: 0
		}
	},

	
	async mounted () {
		const decor = this;
		const mapElement = this.$refs.map;
		const map = new Map ({
			layers: [
				new TileLayer ({
					source: new OSM (),
				})
			],
			target: mapElement,
			view: new View ({
				center: [ 0, 0 ],
				zoom: 2,
			}),
		});
		
		
		await persist ({
			FN: async function () {
				try {
					var CANVASES = mapElement.querySelectorAll ('canvas')
					if (CANVASES.length !== 1) {
						return false;
					}
					if (TWO_TONE) {
						CANVASES [0].style.filter = 'grayscale(100%)'	
					}
					
					decor.OPACITY = 1;
					
					return true;
				}
				catch (exception) {}
				
				return false;
			},
			EVERY: 100,
			END: 10 
		})
	},
	
	beforeUnmount () {},	
	
	
}
