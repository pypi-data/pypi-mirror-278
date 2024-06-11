
/*
	https://github.com/simeydotme/sparticles
	https://github.com/LeafWulf/weatherfx?tab=readme-ov-file
*/

// import particles_background_effect from '@%/glamour/background_effects/particles/money.vue'

import Sparticles from "sparticles";

import { rhythm_filter } from '@medical-district/rhythm-filter'

import { homestead_system } from '@/warehouses/homestead'

// import Worker from './worker.js';

// import Worker from 'worker-loader!./worker.js';

import MyWorker from './worker?worker'

export const particles = {
	data () {
		return {
			show: false
		}
	},
	methods: {
		web_worker () {
			const canvas = this.$refs.canvas;
			
			this.worker = new Worker(
				new URL('./worker', import.meta.url),
				{ 
					type: 'module'
				}
			);
			
			// this.worker = new MyWorker();
			
			// Send a message to the worker
			this.worker.postMessage ({
				move: 'start'
			});

			// Receive messages from the worker
			this.worker.onmessage = (event) => {
				this.workerResult = event.data;
			};

		},
		
		build_canvas () {
			console.log ('build_canvas')
			
			const canvas = this.$refs.canvas;
			const bounding_box = canvas.getBoundingClientRect();
			
			if (this.sparticles) {
				this.sparticles.setCanvasSize (bounding_box.width, bounding_box.height)
				this.show = true;
				return;
			}
			
			/*
			try {
				this.sparticles.destroy ()
			}
			catch (exception) {}			
			 */
			
			const properties_3 = {
				"composition":"source-over",
				"count":20,
				"speed":0,
				"parallax":29.5,
				"direction":360,
				"xVariance":6.6,
				"yVariance":10.4,
				"rotate":true,
				"rotation":1.3,
				"alphaSpeed":19.7,
				"alphaVariance":13,
				"minAlpha":2,
				"maxAlpha":2,
				"minSize":8,
				"maxSize":91,
				"bounce":true,
				"drift":18.1,
				"glow":33,
				"twinkle":false,
				"color":["#99c1f1"],
				
				"shape":"circle",
				"style":"stroke",
				
				"imageUrl":""
			}
			
			this.sparticles = new Sparticles (
				canvas, 
				properties_3, 
				bounding_box.width, 
				bounding_box.height
			);
			
			this.show = true;
		}
		
	},
	
	created () {
		const component = this;
		
		const build_canvas = this.build_canvas;
		
		const RF = rhythm_filter ({
			every: 500
		});
		
		function size_change () {	
			component.show = false;
			
			RF.attempt (({ ellipse, is_last }) => {
				build_canvas ()
			});	
		}
		
		this.homestead_system_monitor = homestead_system.monitor (({ inaugural, field }) => {
			// const homestead = this.homestead_system.warehouse ()
			// this.terrain = homestead.terrain;
			
			if (!inaugural) { 
				size_change ()
			}
		})
	},
	beforeUnmount () {
		this.homestead_system_monitor.stop ()
	},
	
	mounted () {
		this.build_canvas ()
		this.web_worker ()
	}	
}