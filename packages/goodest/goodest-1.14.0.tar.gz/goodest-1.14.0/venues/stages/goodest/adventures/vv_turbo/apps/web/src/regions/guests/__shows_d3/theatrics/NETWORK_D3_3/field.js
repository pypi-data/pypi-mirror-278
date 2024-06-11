
/*
	https://github.com/holtzy/D3-graph-gallery
	https://d3js.org/d3-force
	
	https://gist.github.com/steveharoz/8c3e2524079a8c440df60c1ab72b5d03
*/



import { PHYSICAL } from './methods/PHYSICAL'
import { reinvigorate } from './methods/reinvigorate'
import { FIND_STRUCTURE } from './methods/FIND_STRUCTURE'

/*
	https://fdc.nal.usda.gov/fdc-app.html#/food-details/2262074/nutrients
	https://fdc.nal.usda.gov/portal-data/external/2262074
*/
export const field = {
	data () {
		return {
			OPACITY: 0,
			ZOOM: 1,
			
			/*
				https://fdc.nal.usda.gov/fdc-app.html#/food-details/2262074/nutrients
			*/
			GRAPH: {
				nodes: [{
					id: 0,
					name: "food item",
					mass: {
						full: [ 100, "g" ],
						partial: [ 100 - 53, "g"] 
					}
				},{
					id: 1,
					name: "lipids",
					mass: {
						full: [ 53, "g" ],
						partial: [ 53 - 4.25 - 34.7 - 12.6, "g"] 
					}
				},{
					id: 2,
					name: "saturated fatty acids",
					mass: {
						full: [ 4.25, "g" ]
					}
				},{
					id: 3,
					name: "monounsaturated fatty acids",
					mass: {
						full: [ 34.7, "g" ]
					}
				},{
					id: 4,
					name: "polyunsaturated fatty acids",
					mass: {
						full: [ 12.6, "g" ],
						partial: [ 12.6 - 12.6, "g"] 
					}
				},{
					id: 5,
					name: "pufa 18:2 n-6 c,c",
					mass: {
						full: [ 12.6, "g" ]
					}
				},{
					id: 6,
					name: "protein",
					mass: {
						full: [ 59.6, "g" ],
						partial: [ 59.6 - 8.6, "g"] 
					}
				},{
					id: 7,
					name: "collagen",
					mass: {
						full: [ 8.6, "g" ],
						partial: [ 8.6 - 3.6, "g"] 
					}
				},{
					id: 8,
					name: "glycine",
					mass: {
						full: [ 3.6, "g" ]
					}
				}],
				
				links: [{
					source: 0,
					target: 1
				},{
					source: 1,
					target: 2
				},{
					source: 1,
					target: 3
				},{
					source: 1,
					target: 4
				},{
					source: 4,
					target: 5
				},{
					source: 0,
					target: 6
				},{
					source: 6,
					target: 7
				},{
					source: 7,
					target: 8
				},{
					source: 6,
					target: 8
				}]
			},
			FORCE_PROPERTIES: {
				center: {
					x: 0.5,
					y: 0.5
				},
				charge: {
					enabled: 1,
					strength: -200,
					distanceMin: 200,
					distanceMax: 2000
				},
				collide: {
					enabled: 1,
					strength: .7,
					iterations: 1,
					radius: 100
				},
				forceX: {
					enabled: 1,
					strength: .1,
					x: .5
				},
				forceY: {
					enabled: 1,
					strength: .1,
					y: .5
				},
				link: {
					enabled: 1,
					distance: 30,
					iterations: 1
				}
			}
		}
	},
	
	methods: {
		PHYSICAL,
		reinvigorate,
		FIND_STRUCTURE
	},
	
	async mounted () {
		this.PHYSICAL ()
	}
}